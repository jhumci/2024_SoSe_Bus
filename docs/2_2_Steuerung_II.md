---
marp: true
theme: beams
author: Julian Huber
size: 16:9
footer: Julian Huber - Bussysteme
math: mathjax


---

<!-- paginate: true -->


# 2.2 Steuerung II – Funktionen & Objektorientierung

<!-- _class: title -->

---

## Orientierung – Einheit 6 von 14

<!-- _class: white -->

### Wo sind wir?

| Abgeschlossen | **Heute** | Als nächstes |
|---|---|---|
| Einheit 5: Steuerung I (FSM) | **Einheit 6: Steuerung II** | Einheit 7: Regelungstechnik I |

### Was haben wir bisher gelernt?

* Analoge Sensoren auslesen und Messwerte in Lux umrechnen (ADC, Mapping)
* Ablaufsteuerungen mit FSM: Zustände, Übergänge, zeitbedingte Ausgaben
* Treppenlichtschaltung implementiert

---

### Wo wollen wir hin?

Nicht jede Steuerung folgt einem zeitlichen Ablauf – manchmal hängt der Ausgang einfach von mehreren Eingängen **gleichzeitig** ab. Heute bauen wir eine **Tageslichtschaltung** als Funktion und verbessern sie anschließend mit **Objektorientierung**.

---

## 🎯 Lernziele – Einheit 6

* Verknüpfungssteuerung durch eine Boolesche Funktion beschreiben und implementieren
* Tageslichtschaltung mit Hysterese (`PAR_OND`, `PAR_OFFD`) als Python-Funktion umsetzen
* Messrauschen als Problem erkennen und durch Mittelwertbildung lösen
* Eine Klasse mit Attributen und Methoden beschreiben und verwenden
* Sensor mit gleitendem Mittelwert als Klasse implementieren

---

### Aufgaben dieser Einheit

| Aufgabe | Inhalt |
|---------|--------|
| ✍️ 2_3_1 | Tageslichtschaltung mit `PAR_OND` / `PAR_OFFD` implementieren |
| ✍️ 2_3_2 | Sensor-Klasse mit gleitendem Mittelwert implementieren |


---

## Verknüpfungssteuerungen

* Während **Ablaufsteuerungen** einen zeitlichen Prozess steuern (FSM), verknüpfen **Verknüpfungssteuerungen** Eingangssignale direkt mit einem Ausgang
* Der Ausgang hängt ausschließlich von den **aktuellen Eingangswerten** ab

```
Eingang 1 ──┐
Eingang 2 ──┤─── [Boolesche Funktion] ──► Ausgang
Eingang 3 ──┘
```

Diese Trennung ist akademisch – die meisten Systeme enthalten beide Typen.

---

```
Taster Segment 1 ──┐
Taster Segment 2 ──┤─── [Treppenlichtschaltung] ──► Lichtaktor
GLT              ──┘
```

---

### Beispiel: Wechselschalter

<!-- _class: white -->

![h:280](images/Wechselschaltung.svg)

| Schalter 1 | Schalter 2 | Lampe |
|------------|------------|-------|
| 0 | 0 | 1 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

**Boolsche Funktion**
$$L = (S_1 \land S_2) \lor (\lnot S_1 \land \lnot S_2)$$

__Hinweis: Man könnte es auch als FSM betrachten, aber die Verknüpfungssteuerung ist hier natürlicher__

---

## Tageslichtschaltung

<!-- _class: white -->

![bg right:33% h:720](images/Tageslichtschaltung.png)

Die Tageslichtschaltung steuert die Beleuchtung in Abhängigkeit von:

| Variable | Bedeutung |
|----------|-----------|
| `P_ACT` | Anwesenheit einer Person |
| `H_ROOM` | Raumhelligkeit in Lux |
| `PAR_OND` | Einschaltschwellwert in Lux |
| `PAR_OFFD` | Ausschaltschwellwert in Lux |
| `L_MAN` | Manuelle Einschaltung |
| `L_SET` | Ausgang: Lampe ein/aus |

---

### Wahrheitstabelle

| `P_ACT` | `H_ROOM < PAR_OND` | `L_MAN` | `L_SET` |
|---------|---------------------|---------|---------|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 1 |
| * | * | 1 | 1 |

**Boolsche Funktion**

$$L_\text{SET} = L_\text{MAN} \lor \bigl(P_\text{ACT} \land (H_\text{ROOM} < \text{PAR\_OND})\bigr)$$

---

### Hysterese: Zwei Schwellwerte gegen Flackern

Liegt `H_ROOM` genau nahe `PAR_OND`, kann die Lampe schnell hin- und herschalten.

**Lösung: zwei Schwellwerte**

* `PAR_OND` – **Ein**schaltschwellwert (z. B. 100 Lux): unterschritten → einschalten
* `PAR_OFFD` – **Aus**schaltschwellwert (z. B. 300 Lux): überschritten → ausschalten
* Zwischen beiden Werten: **letzter Zustand beibehalten** (`L_LAST`)

```
H_ROOM:  ───────────────────────────────────────►
              PAR_OND      PAR_OFFD
                 │             │
                 ▼             ▼
  EIN ◄──────────┤             ├──────────► AUS
         (Hysterese-Zone: L_LAST)
```

---

### Implementierung als Python-Funktion

```python
def l_set(p_act, h_room, PAR_OND, PAR_OFFD, l_man, l_last):
    if l_man:
        return True          # manuelle Einschaltung hat Vorrang
    if not p_act:
        return False         # niemand anwesend → aus
    if h_room < PAR_OND:
        return True          # zu dunkel → einschalten
    if h_room > PAR_OFFD:
        return False         # hell genug → ausschalten
    return l_last            # Hysterese: letzten Zustand beibehalten
```

* Reine Funktion: gleiche Eingaben → gleicher Ausgang
* `l_last` muss vom Hauptprogramm übergeben werden

---

### Hauptprogramm

```python
from tageslichtschaltung import l_set
from mappings import map_log_log_lin

PAR_OND  = 100   # Lux: einschalten, wenn dunkler
PAR_OFFD = 300   # Lux: ausschalten, wenn heller
L_MAN    = False

l_last = False   # Startzustand

while True:
    h_room = map_log_log_lin(ldr.value)
    p_act  = not button.value

    l_last = l_set(p_act, h_room, PAR_OND, PAR_OFFD, L_MAN, l_last)
    led.value = l_last

    print(f"H_ROOM: {h_room:.1f} Lux | P_ACT: {p_act} | L_SET: {l_last}")
    time.sleep(0.5)
```

---

## ✍️ Aufgabe 2_3_1: Tageslichtschaltung implementieren

![bg right:33% h:720](images/Tageslichtschaltung.png)

* Bauen Sie auf Aufgabe 2_1_5 auf – Helligkeitssensor, LED und Taster sind bereits angeschlossen
* Erstellen Sie `tageslichtschaltung.py` mit der Funktion `l_set()`
* Verwenden Sie `map_log_log_lin` aus Ihrer `mappings.py`
* [Wokwi-Projekt](https://wokwi.com/projects/457735322111636481) als Starter

--- 

* Steuern Sie die LED anhand der Tageslichtschaltung:
  * Taster simuliert Anwesenheit (`P_ACT`)
  * Starten Sie mit `PAR_OND = 100` und `PAR_OFFD = 300`
  * Setzen Sie `L_MAN = False`
* Beobachten Sie das Verhalten, wenn Sie den Sensor abdecken oder beleuchten

---

### 🤓 Sichtbarkeit von Variablen

* Variablen innerhalb einer Funktion sind **lokal** – außerhalb nicht sichtbar

```python
def l_set(p_act, h_room, PAR_OND, PAR_OFFD, l_man, l_last):
    dunkel = h_room < PAR_OND   # lokale Variable
    ...

print(dunkel)  # NameError: name 'dunkel' is not defined
```

* Variablen außerhalb aller Funktionen sind **global** – in Python per Konvention in Großbuchstaben

```python
PAR_OND = 100   # global, überall sichtbar

def l_set(...):
    ...         # PAR_OND kann hier gelesen werden
```

---

### [✔️ Lösung 2_3_1](https://wokwi.com/projects/457736998769423361)

---

## Objektorientierung


### Probleme, die wir bisher noch nicht gelöst haben

* Lichtsensoren liefern **keine stabilen Werte** – der ADC-Rohwert schwankt von Messung zu Messung
* Bei Helligkeitswerten nahe den Schwellwerten kann die Lampe dadurch **flackern**
* Jeder Fotoresistor hat eine andere Kennlinie – die Umrechnung von ADC-Wert zu Lux ist nicht immer gleich


---

### Beispiel: aufeinanderfolgende Messungen nahe PAR_OFFD = 300 Lux

* z.B. durch Sonnenlichtreflexion, Bewegung, Sensorrauschen
* Licht ist an, Raum ist bei ca. 280 Lux

| t | Lux | L_SET | Grund |
|---|-----|-------|-------|
| 0 | 280 | 1 | Hysterese → bleibt an |
| 1 | 285 | 1 | Hysterese → bleibt an |
| 2 | 310 | **0** | > PAR_OFFD → **aus** |
| 3 | 275 | 0 | Hysterese → bleibt aus |
| 4 | 280 | 0 | Hysterese → bleibt aus |

→ Ein einzelner Ausreißer schaltet das Licht **dauerhaft** aus, obwohl der Raum eigentlich zu dunkel ist.

---

## Lösung: Gleitender Mittelwert

Anstatt den Einzelmesswert zu verwenden, berechnen wir den **Durchschnitt der letzten $n$ Messungen**:

$$\bar{x}_t = \frac{1}{n} \sum_{i=0}^{n-1} x_{t-i}$$

---
**Beispiel mit n = 4**

| t | Messwert | Puffer | Mittelwert |
|---|---------|--------|-----------|
| 0 | 280 | [280] | 280.0 |
| 1 | 285 | [280, 285] | 282.5 |
| 2 | 310 | [280, 285, 310] | 291.7 |
| 3 | 275 | [280, 285, 310, 275] | 287.5 |
| 4 | 280 | [285, 310, 275, 280] | 287.5 |

→ Der geglättete Wert bleibt unter 300 – das Licht bleibt **an**.

---

## Erinnerung: Messkette

![bg right:40% h:720](images/Helligektismessung.pdf.png)

- Solche Verarbeitungsschritte (Mittelwertbildung) gehören zur **Messkette** – sie beeinflussen die Qualität der Messung und damit die Steuerung
- Sie Sind meist in der Sensorfunktion oder -klasse implementiert, damit der Hauptcode sich nicht darum kümmern muss
- Reine Funktionen reagieren immer mit dem gleichen Ausgang auf die gleichen Eingaben – sie haben kein Gedächtnis. Um einen gleitenden Mittelwert zu berechnen, benötigen wir jedoch einen **Puffer**, der die letzten Messwerte speichert → **Objektorientierung**.

---

## Objektorientierung (OOP) – Das kennen Sie schon!

Sie haben in jeder Einheit bereits mit Objekten gearbeitet, ohne es zu wissen:

```python
# ldr ist ein Objekt der Klasse AnalogIn
ldr = analogio.AnalogIn(board.A0)
print(ldr.value)              # Attribut lesen

# led ist ein Objekt der Klasse DigitalInOut
led = digitalio.DigitalInOut(board.GP15)
led.direction = digitalio.Direction.OUTPUT  # Attribut setzen
led.value = True                            # Attribut schreiben
```

* Jede Variable mit einem Punkt-Zugriff (`.`) ist ein **Objekt**
* `ldr` und `led` sind zwei verschiedene Objekte – jedes hat seinen eigenen Zustand (es kann also, wie eine variable, Werte speichern)

---

## Klasse vs. Objekt

<!-- _class: white -->

| Begriff | Bedeutung | Beispiel |
|---------|-----------|---------|
| **Klasse** | Bauplan / Schablone | `DigitalInOut` |
| **Objekt** | konkretes Exemplar | `led`, `button` |
| **Attribut** | gespeicherter Wert | `led.value`, `ldr.value` |
| **Methode** | Funktion des Objekts | – |

```python
# Zwei Objekte der gleichen Klasse – unabhängige Zustände für die jeweilige LED:
led1 = digitalio.DigitalInOut(board.GP15)
led2 = digitalio.DigitalInOut(board.GP14)

led1.value = True   # nur led1 leuchtet
led2.value = False  # led2 bleibt aus
# Hilft uns z.B. bei der unabhängigen Steuerung von mehreren Aktoren
```

---

## Warum brauchen wir eigene Klassen?

Unser Problem: Die Funktion `map_log_log_lin` hat kein Gedächtnis – sie kann keine vergangenen Messwerte speichern.

```python
# Reine Funktion: kein Gedächtnis
def map_log_log_lin(z):
    ...             # immer nur ein Messwert, nie ein Puffer

# Was wir bräuchten:
letzten_10_werte = ???   # wo speichern wir die?
```

### Lösung
Eine Klasse, die den Puffer als **Attribut** speichert und das Lesen + Mitteln als **Methoden** anbietet.
__Methoden__ sind Funktionen, die Zugriff auf die Attribute des Objekts haben – sie können also den Puffer aktualisieren und den geglätteten Wert zurückgeben.

---

## Eine eigene Klasse schreiben

```python
class LDRSensor:           # Klassendefinition: Bauplan

    def __init__(self, pin, n=10):   # Konstruktor
        # Attribute anlegen – jedes Objekt bekommt seine eigene Kopie
        self.adc    = analogio.AnalogIn(pin)
        self.n      = n
        self.buffer = [self.adc.value]

    def update(self):                # Methode 1
        ...

    def get_lux(self):               # Methode 2
        ...
```

```python
# Objekt aus der Klasse erstellen:
sensor = LDRSensor(board.A0, n=10)
#                  ^^^^^^^^^  ^^^^
#                  Argumente für __init__
```

---

## `__init__` – Der Konstruktor

`__init__` wird **einmalig** aufgerufen, wenn das Objekt erstellt wird.
Hier werden alle Attribute initialisiert.

```python
def __init__(self, pin, n=10):
    self.adc    = analogio.AnalogIn(pin)  # ADC-Objekt speichern
    self.n      = n                       # Puffergröße speichern
    self.buffer = [self.adc.value]        # Puffer mit aktuellem Wert füllen
```

```python
sensor_raum = LDRSensor(board.A0, n=10)
# → __init__ läuft: self.adc = AnalogIn(A0), self.n = 10, self.buffer = [...]

sensor_gang = LDRSensor(board.A1, n=5)
# → __init__ läuft erneut für ein zweites, unabhängiges Objekt
```

Beide Objekte haben **eigene** `adc`-, `n`- und `buffer`-Attribute.

---

## `self` – Das Objekt kennt sich selbst

`self` ist der Name für das Objekt, auf dem die Methode gerade aufgerufen wird.

```python
sensor = LDRSensor(board.A0, n=10)
sensor.update()
# Python ruft intern auf: LDRSensor.update(sensor)
#                                            ^^^^^^ das ist self
```

Innerhalb der Methode:

```python
def update(self):
    self.buffer.pop(0)          # greift auf den Puffer DIESES Objekts zu
    self.buffer.append(...)     # nicht auf den Puffer eines anderen Objekts
```

**Faustegel**: Jede Variable, die das Objekt über mehrere Methodenaufrufe hinweg erinnern soll, wird als `self.xyz` gespeichert.

---

## Methoden – Funktionen des Objekts

Methoden sehen aus wie Funktionen, haben aber immer `self` als ersten Parameter und Zugriff auf alle Attribute.

```python
def update(self):
    """Liest einen neuen ADC-Wert und fügt ihn dem Puffer hinzu."""
    self.buffer.pop(0)                  # ältesten Wert entfernen
    self.buffer.append(self.adc.value)  # neuen Wert hinzufügen

def get_lux(self):
    """Gibt den geglätteten Helligkeitswert in Lux zurück."""
    avg = sum(self.buffer) / self.n
    return map_log_log_lin(avg)
```

Aufruf – `self` wird **nicht** explizit übergeben:

```python
sensor.update()            # Python ergänzt self automatisch
h = sensor.get_lux()
```

---

## Die vollständige Sensor-Klasse

```python
import analogio, math
from mappings import map_log_log_lin

class LDRSensor:
    """Helligkeitssensor (LDR) mit gleitendem Mittelwert."""

    def __init__(self, pin, n=10):
        self.adc    = analogio.AnalogIn(pin)
        self.n      = n
        self.buffer = [self.adc.value] * n   # Puffer vorbelegen

    def update(self):
        self.buffer.pop(0)
        self.buffer.append(self.adc.value)

    def get_lux(self):
        avg = sum(self.buffer) / self.n
        return map_log_log_lin(avg)
```

---

### Verwendung im Hauptprogramm wenn in der `sensor.py` definiert

```python
from sensor import LDRSensor

sensor = LDRSensor(board.A0, n=10)   # Objekt erstellen

while True:
    sensor.update()             # neuen Messwert einlesen
    h_room = sensor.get_lux()  # geglätteten Wert abrufen

    l_last = l_set(p_act, h_room, PAR_OND, PAR_OFFD, L_MAN, l_last)
    led.value = l_last

    time.sleep(0.1)
```

**Mehrere Sensoren** – einfach mehrere Objekte erstellen:

```python
sensor_raum = LDRSensor(board.A0, n=10)
sensor_gang = LDRSensor(board.A1, n=5)
```

Jedes Objekt verwaltet seinen eigenen Puffer – der Hauptcode muss sich nicht darum kümmern.

---

## ✍️ Aufgabe 2_3_2: Sensor-Klasse mit gleitendem Mittelwert

* Erstellen Sie eine Datei `sensor.py` mit der Klasse `LDRSensor`
* Die Klasse soll:
  * Im Konstruktor `__init__` den ADC initialisieren und den Puffer anlegen
  * Mit `update()` einen neuen Messwert in den Puffer aufnehmen
  * Mit `get_lux()` den geglätteten Helligkeitswert in Lux zurückgeben
* Passen Sie das Hauptprogramm aus Aufgabe 2_3_1 so an, dass es die Klasse verwendet
* Beobachten Sie, wie sich das Verhalten durch die Glättung verändert
* 🤓 Experimentieren Sie mit verschiedenen Puffergrößen (`n`): Was passiert bei sehr großem `n`?

--- 

### [✔️ Lösung 2_3_2](https://wokwi.com/projects/457742519220103169)

---

## Fazit

* Verknüpfungssteuerungen hängen von den aktuellen Eingangswerten ab – keine zeitlichen Abläufe (streng genommen)
* Wir müssen trotzem auch zeitliche Aspekte berücksichtigen, wenn wir sinnvoll Steuerungen implementieren wollen. Hierzu haben zwei zwei Ansätze kennengelernt:
  * Hysterese mit zwei Schwellwerten (`PAR_OND`, `PAR_OFFD`)
  * Gleitender Mittelwert zur Glättung von Sensorwerten
* Objektorientierung ermöglicht es uns, **Zustand** (z.B. den Puffer der letzten Messwerte) in **Objekten** zu speichern und durch **Methoden** zu
* In der Aufgabe 2_3_1 haben wir das Problem zwar mit einer reinen Funktion gelöst, aber wenn man genau hinsieht etwas getrickst: Mit `l_last` haben wir den Zustand der Hysterese von außerhalb der Funktion verwaltet. Das hätte man auch in einer Klasse mit einem `self.l_last`-Attribut lösen können.