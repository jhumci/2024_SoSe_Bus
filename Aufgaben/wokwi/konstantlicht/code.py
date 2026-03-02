"""
Konstantlichtregelung nach VDI 3813 – mit geschlossenem Regelkreis
===================================================================

Problem in Wokwi:
  Der Fotoresistor wird über einen manuellen Slider gesteuert –
  es gibt KEINE physikalische Kopplung zwischen LED und LDR.

Lösung:
  MockUmgebung – ein Software-Streckenmodell, das den Regelkreis
  schließt. Das Modell simuliert:
    • Tageslicht (Störgröße, konfigurierbar)
    • LED-Beitrag = f(Stellwert)
    • Sensor-Messwert = Tageslicht + LED-Beitrag

  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │   Störgröße          ┌────────────────┐                     │
  │   (Tageslicht) ─────►│  MockUmgebung  │                     │
  │                      │  (Strecke)     │                     │
  │   Stellwert ────────►│                ├──► simulierter      │
  │                      └────────────────┘    Sensorwert (Lux) │
  │      ▲                                         │            │
  │      │                                         ▼            │
  │ ┌────────────┐    ┌───────────┐    ┌────────────────┐       │
  │ │ Aktorfkt:  │◄───│ PIDRegler │◄───│ Sensorfkt:     │       │
  │ │ Licht-     │    │           │    │ Helligkeits-   │       │
  │ │ stellen    │    └───────────┘    │ messung        │       │
  │ └────────────┘                     └────────────────┘       │
  │   GP15 (PWM)                         GP26 oder Mock         │
  └─────────────────────────────────────────────────────────────┘

Modus:
  MOCK_MODUS = True  → geschlossener Regelkreis (Software-Strecke)
  MOCK_MODUS = False → echten LDR am GP26 verwenden (manueller Slider)

CSV-Logging:
  Regelgrößen werden als CSV über die serielle Schnittstelle ausgegeben.
  → Im Wokwi Serial Monitor kopieren und als .csv speichern.

Logic Analyzer:
  PWM-Signal an GP15 wird vom Logic Analyzer aufgezeichnet.
  → Nach Simulation-Stopp wird eine VCD-Datei heruntergeladen.
  → Öffnen mit PulseView (kostenlos): https://sigrok.org/wiki/PulseView
"""

import board
import analogio
import pwmio
import time
import math

# ╔═══════════════════════════════════════════════════════════════╗
# ║  KONFIGURATION                                               ║
# ╚═══════════════════════════════════════════════════════════════╝

MOCK_MODUS = True       # True = Software-Strecke, False = echter LDR
SOLLWERT_LUX = 500.0    # Ziel-Beleuchtungsstärke [Lux]
ABTASTZEIT = 0.1        # Zykluszeit [s]
CSV_INTERVALL = 0.5     # CSV-Ausgabe alle N Sekunden


# =================================================================
# 1. PID-Regler (universell, wiederverwendbar)
# =================================================================
class PIDRegler:
    """
    Diskreter PID-Regler mit Anti-Windup (Clamping).

    Parameter:
        kp, ki, kd   : float – Reglerparameter
        output_min    : float – minimaler Stellwert (default 0.0)
        output_max    : float – maximaler Stellwert (default 1.0)
    """

    def __init__(self, kp=1.0, ki=0.0, kd=0.0,
                 output_min=0.0, output_max=1.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.output_min = output_min
        self.output_max = output_max

        self._integral = 0.0
        self._letzter_fehler = None

    def reset(self):
        """Internen Zustand zurücksetzen."""
        self._integral = 0.0
        self._letzter_fehler = None

    def berechne(self, fehler, dt):
        """
        Berechnet den Stellwert für den aktuellen Zeitschritt.

        Parameter:
            fehler : float – Regeldifferenz (Sollwert - Istwert)
            dt     : float – Zeitschritt in Sekunden

        Rückgabe:
            float – begrenzter Stellwert [output_min, output_max]
        """
        if dt <= 0:
            return 0.0

        # P-Anteil
        p_anteil = self.kp * fehler

        # I-Anteil
        self._integral += fehler * dt
        i_anteil = self.ki * self._integral

        # D-Anteil
        if self._letzter_fehler is None:
            d_anteil = 0.0
        else:
            d_anteil = self.kd * (fehler - self._letzter_fehler) / dt
        self._letzter_fehler = fehler

        # Summe + Begrenzung
        stellwert = p_anteil + i_anteil + d_anteil
        stellwert_begrenzt = max(self.output_min,
                                min(self.output_max, stellwert))

        # Anti-Windup: Integral zurücknehmen bei Sättigung
        if stellwert_begrenzt != stellwert:
            self._integral -= fehler * dt

        return stellwert_begrenzt


# =================================================================
# 2. Sensorfunktion: Helligkeitsmessung (VDI 3813-2)
# =================================================================
class Helligkeitsmessung:
    """
    VDI 3813 Sensorfunktion – Erfassung der Beleuchtungsstärke.

    Parameter:
        pin         : board.Pin   – analoger Eingangspin (z.B. board.GP26)
                                    None wenn nur Mock verwendet wird
        kennlinie   : callable    – f(adc_wert) -> lux
        glaettung   : float       – Tiefpassfaktor [0..1], 1.0 = kein Filter
    """

    def __init__(self, pin=None, kennlinie=None, glaettung=0.3):
        self._adc = None
        if pin is not None:
            self._adc = analogio.AnalogIn(pin)

        self._glaettung = glaettung
        self._gefilterter_wert = None
        self._mock_wert = None  # für Mock-Modus

        if kennlinie is not None:
            self._kennlinie = kennlinie
        else:
            self._kennlinie = self._default_kennlinie

    @staticmethod
    def _default_kennlinie(adc_wert):
        """Lineare Standardkennlinie: ADC (0–65535) → Lux (0–1000)."""
        return (adc_wert / 65535) * 1000.0

    def set_mock_lux(self, lux):
        """
        Setzt einen simulierten Lux-Wert (für Mock-Modus).
        Wird von MockUmgebung aufgerufen.
        """
        self._mock_wert = lux

    @property
    def adc_rohwert(self):
        """Aktueller ADC-Rohwert (0–65535), oder None im Mock-Modus."""
        if self._adc is not None:
            return self._adc.value
        return None

    def messen(self):
        """
        Führt eine Messung durch.

        Rückgabe:
            float – Beleuchtungsstärke in Lux (geglättet)
        """
        if self._mock_wert is not None:
            # Mock-Modus: direkt den simulierten Wert verwenden
            lux = self._mock_wert
        elif self._adc is not None:
            # Echter Sensor: ADC → Kennlinie
            lux = self._kennlinie(self._adc.value)
        else:
            lux = 0.0

        # Exponentielle Glättung
        if self._gefilterter_wert is None:
            self._gefilterter_wert = lux
        else:
            a = self._glaettung
            self._gefilterter_wert = (a * lux
                                      + (1 - a) * self._gefilterter_wert)

        return self._gefilterter_wert


# =================================================================
# 3. Aktorfunktion: Lichtstellen (VDI 3813-2)
# =================================================================
class Lichtstellen:
    """
    VDI 3813 Aktorfunktion – Ansteuerung der Beleuchtung.

    Parameter:
        pin       : board.Pin  – PWM-Ausgangspin
        frequenz  : int        – PWM-Frequenz in Hz
    """

    def __init__(self, pin, frequenz=1000):
        self._pwm = pwmio.PWMOut(pin, frequency=frequenz, duty_cycle=0)
        self._stellwert = 0.0

    @property
    def stellwert(self):
        """Aktueller Stellwert (0.0–1.0)."""
        return self._stellwert

    def stellen(self, wert):
        """Setzt den Beleuchtungs-Stellwert [0.0 .. 1.0]."""
        self._stellwert = max(0.0, min(1.0, wert))
        self._pwm.duty_cycle = int(self._stellwert * 65535)

    def ausschalten(self):
        """Beleuchtung ausschalten."""
        self.stellen(0.0)


# =================================================================
# 4. MockUmgebung – Software-Streckenmodell (schließt Regelkreis)
# =================================================================
class MockUmgebung:
    """
    Simuliert die physikalische Umgebung (Strecke/Plant):
      Gesamthelligkeit = Tageslicht + LED-Beitrag

    Parameter:
        led_max_lux    : float – max. Beleuchtungsstärke der LED bei 100%
        tageslicht_lux : float – konstante Störgröße (Tageslicht)
        traegheit      : float – Zeitkonstante der Strecke [0..1]
                                 (1.0 = sofort, 0.1 = sehr träge)

    Methoden:
        aktualisiere(stellwert) → float  – gibt aktuelle Lux zurück
        set_tageslicht(lux)              – Störgröße ändern (Sprung)
    """

    def __init__(self, led_max_lux=800.0, tageslicht_lux=200.0,
                 traegheit=0.3):
        self.led_max_lux = led_max_lux
        self.tageslicht_lux = tageslicht_lux
        self.traegheit = traegheit
        self._aktuelle_helligkeit = tageslicht_lux

    def set_tageslicht(self, lux):
        """Störgröße (Tageslicht) ändern – simuliert z.B. Wolke."""
        self.tageslicht_lux = lux

    def aktualisiere(self, stellwert):
        """
        Berechnet die aktuelle Beleuchtungsstärke.

        Parameter:
            stellwert : float – aktueller LED-Stellwert [0..1]

        Rückgabe:
            float – gemessene Beleuchtungsstärke [Lux]
        """
        # Ziel-Helligkeit = Tageslicht + LED-Anteil
        ziel = self.tageslicht_lux + stellwert * self.led_max_lux

        # PT1-Verhalten (Trägheit des Raums / Sensors)
        a = self.traegheit
        self._aktuelle_helligkeit = (
            a * ziel + (1 - a) * self._aktuelle_helligkeit
        )

        return self._aktuelle_helligkeit


# =================================================================
# 5. CSV-Logger – Datenaufzeichnung über Serial
# =================================================================
class CSVLogger:
    """
    Gibt Regelgrößen als CSV über die serielle Schnittstelle aus.

    Verwendung:
        logger = CSVLogger()
        logger.kopfzeile()        # einmalig am Anfang
        logger.zeile(t, soll, ist, stell, fehler)
    """

    SPALTEN = ("zeit_s", "sollwert_lux", "istwert_lux",
               "stellwert", "fehler_lux", "tageslicht_lux")

    def __init__(self, trennzeichen=","):
        self._trz = trennzeichen

    def kopfzeile(self):
        """Gibt die CSV-Kopfzeile aus."""
        print(self._trz.join(self.SPALTEN))

    def zeile(self, zeit, sollwert, istwert, stellwert,
              fehler, tageslicht=0.0):
        """Gibt eine CSV-Datenzeile aus."""
        print(self._trz.join([
            f"{zeit:.2f}",
            f"{sollwert:.1f}",
            f"{istwert:.1f}",
            f"{stellwert:.4f}",
            f"{fehler:.1f}",
            f"{tageslicht:.1f}",
        ]))


# =================================================================
# 6. Anwendungsfunktion: Konstantlichtregelung (VDI 3813-2)
# =================================================================
class Konstantlichtregelung:
    """
    VDI 3813 Anwendungsfunktion – Konstantlichtregelung.

    Parameter:
        sensor   : Helligkeitsmessung
        aktor    : Lichtstellen
        regler   : PIDRegler
        sollwert : float – Soll-Beleuchtungsstärke [Lux]
        umgebung : MockUmgebung oder None (für echten Sensor)
    """

    def __init__(self, sensor, aktor, regler, sollwert=500.0,
                 umgebung=None):
        self.sensor = sensor
        self.aktor = aktor
        self.regler = regler
        self.sollwert = sollwert
        self.umgebung = umgebung

        self._aktiv = True
        self._letzte_zeit = None

    @property
    def aktiv(self):
        return self._aktiv

    @aktiv.setter
    def aktiv(self, wert):
        self._aktiv = wert
        if not wert:
            self.aktor.ausschalten()
            self.regler.reset()
            self._letzte_zeit = None

    def schritt(self):
        """
        Führt einen Regelschritt durch.

        Rückgabe:
            tuple(istwert, stellwert, fehler)
        """
        if not self._aktiv:
            return 0.0, 0.0, 0.0

        # Zeitschritt bestimmen
        jetzt = time.monotonic()
        if self._letzte_zeit is None:
            dt = 0.1
        else:
            dt = jetzt - self._letzte_zeit
        self._letzte_zeit = jetzt

        # Mock-Umgebung: Strecke aktualisieren → Sensorwert setzen
        if self.umgebung is not None:
            sim_lux = self.umgebung.aktualisiere(self.aktor.stellwert)
            self.sensor.set_mock_lux(sim_lux)

        # Istwert messen
        istwert = self.sensor.messen()

        # Regeldifferenz + Stellwert berechnen
        fehler = self.sollwert - istwert
        stellwert = self.regler.berechne(fehler, dt)

        # Aktor ansteuern
        self.aktor.stellen(stellwert)

        return istwert, stellwert, fehler


# =================================================================
# 7. Hauptprogramm – Zusammenbau und Regelschleife
# =================================================================

def main():
    print()
    print("=" * 55)
    print("  Konstantlichtregelung nach VDI 3813")
    print(f"  Modus: {'MOCK (Software-Strecke)' if MOCK_MODUS else 'ECHT (LDR an GP26)'}")
    print("=" * 55)

    # --- Kennlinie (Studierende können anpassen) ---
    def meine_kennlinie(adc_wert):
        """Beispiel: linear 0–65535 → 0–1000 Lux."""
        return (adc_wert / 65535) * 1000.0

    # --- Komponenten instanziieren ---

    if MOCK_MODUS:
        # Mock: Sensor ohne Hardware-Pin
        sensor = Helligkeitsmessung(
            pin=None,
            kennlinie=meine_kennlinie,
            glaettung=0.4,
        )
        # Streckenmodell
        umgebung = MockUmgebung(
            led_max_lux=800.0,      # LED schafft max. 800 Lux
            tageslicht_lux=200.0,   # Start: 200 Lux Tageslicht
            traegheit=0.3,          # PT1-Trägheit
        )
    else:
        # Echt: LDR an GP26
        sensor = Helligkeitsmessung(
            pin=board.GP26,
            kennlinie=meine_kennlinie,
            glaettung=0.2,
        )
        umgebung = None

    # Aktorfunktion: LED an GP15
    aktor = Lichtstellen(pin=board.GP15, frequenz=1000)

    # PID-Regler
    regler = PIDRegler(
        kp=0.008,
        ki=0.003,
        kd=0.001,
        output_min=0.0,
        output_max=1.0,
    )

    # Anwendungsfunktion
    regelung = Konstantlichtregelung(
        sensor=sensor,
        aktor=aktor,
        regler=regler,
        sollwert=SOLLWERT_LUX,
        umgebung=umgebung,
    )

    # --- Info ausgeben ---
    print(f"  Sollwert:   {regelung.sollwert} Lux")
    print(f"  PID:        Kp={regler.kp}, Ki={regler.ki}, Kd={regler.kd}")
    if umgebung:
        print(f"  Tageslicht: {umgebung.tageslicht_lux} Lux (Start)")
        print(f"  LED max:    {umgebung.led_max_lux} Lux")
    print("=" * 55)
    print()

    # --- CSV-Logger ---
    logger = CSVLogger(trennzeichen=",")
    logger.kopfzeile()

    # --- Regelschleife ---
    start = time.monotonic()
    letzter_csv = start

    while True:
        istwert, stellwert, fehler = regelung.schritt()

        jetzt = time.monotonic()
        vergangen = jetzt - start

        # === Störgrößen-Sprung simulieren (nur Mock) ===
        # Nach 10s: Wolke → Tageslicht sinkt auf 50 Lux
        # Nach 20s: Sonne → Tageslicht steigt auf 600 Lux
        # Nach 30s: Normal → zurück auf 200 Lux
        if umgebung is not None:
            if 10.0 <= vergangen < 10.1:
                umgebung.set_tageslicht(50.0)
                print("# STOERUNG: Wolke -> Tageslicht = 50 Lux")
            elif 20.0 <= vergangen < 20.1:
                umgebung.set_tageslicht(600.0)
                print("# STOERUNG: Sonne -> Tageslicht = 600 Lux")
            elif 30.0 <= vergangen < 30.1:
                umgebung.set_tageslicht(200.0)
                print("# STOERUNG: Normal -> Tageslicht = 200 Lux")

        # CSV-Zeile ausgeben
        if (jetzt - letzter_csv) >= CSV_INTERVALL:
            tageslicht = umgebung.tageslicht_lux if umgebung else 0.0
            logger.zeile(
                zeit=vergangen,
                sollwert=regelung.sollwert,
                istwert=istwert,
                stellwert=stellwert,
                fehler=fehler,
                tageslicht=tageslicht,
            )
            letzter_csv = jetzt

        time.sleep(ABTASTZEIT)


# Start
main()
