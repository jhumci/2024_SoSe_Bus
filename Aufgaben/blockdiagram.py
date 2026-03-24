"""
blockdiagram.py – Diskrete Blockschaltbild-Simulation
======================================================

Bereitgestellt für die Vorlesung *Bussysteme* (MCI).

Kurzanleitung
-------------
Blöcke werden durch Übergabe anderer Blöcke als ``source``-Argument verknüpft.
Die Simulation und Darstellung übernimmt ``Scope``.

Einfaches Beispiel (offene Kette)::

    from blockdiagram import Step, Gain, TransportDelay, Scope

    u = Step(t_step=1, final=1)
    y = TransportDelay(Tt=3, source=Gain(K=2, source=u))
    Scope(t_end=15).run(Eingang=u, Ausgang=y)

Regelkreis-Beispiel::

    from blockdiagram import Step, Sum, Gain, PT1, Scope

    w = Step(final=100)
    e = Sum()                          # Summationsstelle – Eingänge später verbinden
    regler = Gain(K=1, source=e)
    strecke = PT1(tau=2, source=regler)
    e.connect(w, +1)                   # w addieren
    e.connect(strecke, -1)             # Istwert subtrahieren (Rückführung)
    Scope(t_end=30).run(Sollwert=w, Istwert=strecke, Regelabweichung=e)

Verfügbare Blöcke
-----------------
Quellen:
    Constant, Step, Sine

Lineare Glieder:
    Gain, TransportDelay, PT1, Integrator

Verknüpfung:
    Sum, SinglePointController, TwoPointController

Regler:
    PID

Ausgabe:
    Scope
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import deque


# ─────────────────────────────────────────────────────────────────────────────
# Internes Schrittzähler-System (verhindert Mehrfachberechnung je Zeitschritt)
# ─────────────────────────────────────────────────────────────────────────────

_current_step: int = -1


def _next_step() -> None:
    """Erhöht den globalen Schrittzähler (wird von Scope aufgerufen)."""
    global _current_step
    _current_step += 1


# ─────────────────────────────────────────────────────────────────────────────
# Basisklasse
# ─────────────────────────────────────────────────────────────────────────────

class Block:
    """
    Basisklasse für alle Blöcke.

    Jeder Block berechnet seinen Ausgangswert genau **einmal pro Zeitschritt**.
    Bei erneuter Abfrage im selben Schritt wird der gecachte Wert zurückgegeben.
    Das bricht algebraische Schleifen auf und ermöglicht Rückführungen.
    """

    def __init__(self):
        self._last_output: float = 0.0
        self._computed_step: int = -2  # verschieden von _current_step beim Start

    def output(self, t: float, dt: float) -> float:
        """Gibt den Ausgangswert zum Zeitpunkt *t* zurück."""
        if self._computed_step == _current_step:
            return self._last_output          # Schleife → gecachten Wert liefern
        self._computed_step = _current_step
        self._last_output = self._compute(t, dt)
        return self._last_output

    def _compute(self, t: float, dt: float) -> float:
        raise NotImplementedError(f"{type(self).__name__} muss _compute() implementieren")


# ─────────────────────────────────────────────────────────────────────────────
# Quellen (Generatoren) – haben keinen Eingang
# ─────────────────────────────────────────────────────────────────────────────

class Constant(Block):
    """Konstantblock: gibt immer denselben Wert aus.

    Parameters
    ----------
    value : float
        Ausgabewert (Standard: 1.0)

    Example
    -------
    >>> w = Constant(100)   # Sollwert 100 Lux
    """

    def __init__(self, value: float = 1.0):
        super().__init__()
        self.value = value

    def _compute(self, t, dt):
        return self.value


class Step(Block):
    """Sprungfunktion: springt bei *t_step* von *initial* auf *final*.

    Parameters
    ----------
    t_step   : Zeitpunkt des Sprungs (Standard: 0)
    initial  : Wert vor dem Sprung   (Standard: 0)
    final    : Wert nach dem Sprung  (Standard: 1)

    Example
    -------
    >>> u = Step(t_step=1, final=1)        # springt bei t=1 s von 0 auf 1
    >>> T = Step(t_step=1000, initial=10, final=-5)  # Temperatursprung
    """

    def __init__(self, t_step: float = 0.0, initial: float = 0.0, final: float = 1.0):
        super().__init__()
        self.t_step = t_step
        self.initial = initial
        self.final = final

    def _compute(self, t, dt):
        return self.final if t >= self.t_step else self.initial


class Sine(Block):
    """Sinusgenerator: *amplitude* · sin(2π·t/period + phase) + *offset*.

    Parameters
    ----------
    amplitude : Amplitude des Sinus
    period    : Periodendauer in Simulationssekunden
    offset    : Gleichanteil (Standard: 0)
    phase     : Phasenverschiebung in Radiant (Standard: 0)

    Example
    -------
    >>> # Außenhelligkeit: 0–500 Lux, Periode 24 h
    >>> h = Sine(amplitude=250, period=24, offset=250)
    """

    def __init__(self, amplitude: float = 1.0, period: float = 1.0,
                 offset: float = 0.0, phase: float = 0.0):
        super().__init__()
        self.amplitude = amplitude
        self.period = period
        self.offset = offset
        self.phase = phase

    def _compute(self, t, dt):
        return self.amplitude * np.sin(2 * np.pi * t / self.period + self.phase) + self.offset


# ─────────────────────────────────────────────────────────────────────────────
# Lineare zeitinvariante Glieder
# ─────────────────────────────────────────────────────────────────────────────

class Gain(Block):
    """Proportionalglied: y = K · u

    Parameters
    ----------
    K      : Verstärkungsfaktor
    source : Eingangsblock

    Example
    -------
    >>> y = Gain(K=2, source=u)
    """

    def __init__(self, K: float, source: Block):
        super().__init__()
        self.K = K
        self.source = source

    def _compute(self, t, dt):
        return self.K * self.source.output(t, dt)


class TransportDelay(Block):
    """Totzeitglied: verzögert das Eingangssignal um *Tt* Sekunden.

    Parameters
    ----------
    Tt     : Totzeit in Sekunden
    source : Eingangsblock

    Example
    -------
    >>> y = TransportDelay(Tt=3, source=gain)
    """

    def __init__(self, Tt: float, source: Block):
        super().__init__()
        self.Tt = Tt
        self.source = source
        self._buffer: deque | None = None
        self._buffer_dt: float | None = None

    def _compute(self, t, dt):
        # Buffer bei erstem Aufruf oder bei geändertem dt initialisieren
        if self._buffer is None or self._buffer_dt != dt:
            n = max(1, round(self.Tt / dt))
            self._buffer = deque([0.0] * n, maxlen=n)
            self._buffer_dt = dt
        u = self.source.output(t, dt)
        delayed = self._buffer[0]
        self._buffer.append(u)
        return delayed


class PT1(Block):
    """PT1-Glied (Verzögerung 1. Ordnung): G(s) = K / (τs + 1)

    Das Ausgangssignal nähert sich exponentiell dem stationären Endwert an.
    Nach einer Zeitkonstante τ sind 63 % des Endwerts erreicht.

    Parameters
    ----------
    tau     : Zeitkonstante τ in Sekunden
    K       : Statische Verstärkung (Standard: 1.0)
    source  : Eingangsblock
    initial : Anfangswert des Ausgangs (Standard: 0.0)

    Example
    -------
    >>> raum = PT1(tau=120, K=0.35, source=regler)   # träger Raum
    """

    def __init__(self, tau: float, K: float = 1.0, source: Block = None,
                 initial: float = 0.0):
        super().__init__()
        self.tau = tau
        self.K = K
        self.source = source
        self._y = initial

    def _compute(self, t, dt):
        u = self.source.output(t, dt)
        # Euler-Vorwärts: dy/dt = (K·u − y) / τ
        self._y += dt * (self.K * u - self._y) / self.tau
        return self._y


class Integrator(Block):
    """Integrationsglied: y(t) = initial + K · ∫₀ᵗ u(τ) dτ

    Parameters
    ----------
    K       : Verstärkung (Standard: 1.0)
    source  : Eingangsblock
    initial : Anfangswert (Standard: 0.0)

    Example
    -------
    >>> fuellstand = Integrator(K=1, initial=10, source=zufluss)
    """

    def __init__(self, K: float = 1.0, source: Block = None, initial: float = 0.0):
        super().__init__()
        self.K = K
        self.source = source
        self._y = initial

    def _compute(self, t, dt):
        u = self.source.output(t, dt)
        self._y += dt * self.K * u
        return self._y


# ─────────────────────────────────────────────────────────────────────────────
# Verknüpfungsglieder
# ─────────────────────────────────────────────────────────────────────────────

class Sum(Block):
    """Summationsstelle: addiert oder subtrahiert mehrere Eingänge.

    Eingänge können im Konstruktor **oder** nachträglich per ``connect()``
    hinzugefügt werden. Das ermöglicht Rückführungen (erst Block bauen,
    dann Verbindung herstellen).

    Parameters
    ----------
    *sources : Eingangsblöcke (optional)
    signs    : Liste mit Vorzeichen (+1 oder -1) für jeden Eingang.
               Standard: alle +1.

    Example – direkter Aufbau::

        e = Sum(w, y_mess, signs=[+1, -1])   # e = w − y_mess

    Example – späte Verbindung (für Regelkreise)::

        e = Sum()
        # ... weitere Blöcke definieren ...
        e.connect(w,      sign=+1)   # Sollwert addieren
        e.connect(strecke, sign=-1)  # Istwert subtrahieren
    """

    def __init__(self, *sources, signs=None):
        super().__init__()
        self._sources: list[Block] = list(sources)
        self._signs: list[float] = list(signs) if signs else [+1.0] * len(sources)

    def connect(self, source: Block, sign: float = +1.0) -> None:
        """Fügt einen weiteren Eingang hinzu."""
        self._sources.append(source)
        self._signs.append(sign)

    def _compute(self, t, dt):
        return sum(s * src.output(t, dt)
                   for s, src in zip(self._signs, self._sources))


class SinglePointController(Block):
    """Einfacher Schwellwertschalter (Einpunktregler).

    Schaltet den Ausgang basierend auf einem einzigen Schwellwert:

    * Ausgang → 1 (an), wenn Eingang **<** *threshold*
    * Ausgang → 0 (aus), wenn Eingang **≥** *threshold*

    Kein Gedächtnis: Der Ausgang hängt ausschließlich vom aktuellen Eingang ab.
    Bei Eingangswerten nahe am Schwellwert führt das zu schnellem Flattern.

    Parameters
    ----------
    threshold : Schaltschwelle
    source    : Eingangsblock

    Example
    -------
    >>> led = SinglePointController(threshold=220, source=h_aussen)
    """

    def __init__(self, threshold: float, source: Block):
        super().__init__()
        self.threshold = threshold
        self.source = source

    def _compute(self, t, dt):
        u = self.source.output(t, dt)
        return 1.0 if u < self.threshold else 0.0


class TwoPointController(Block):
    """Zweipunktregler mit Hysterese.

    Schaltet den Ausgang basierend auf dem Eingangssignal:

    * Ausgang → 1 (an), wenn Eingang **<** *on_level*
    * Ausgang → 0 (aus), wenn Eingang **>** *off_level*
    * Sonst: letzter Zustand bleibt (Hysterese-Bereich)

    Parameters
    ----------
    on_level      : Einschaltschwelle (Eingang fällt darunter → an)
    off_level     : Ausschaltschwelle (Eingang steigt darüber → aus)
    source        : Eingangsblock
    initial_state : Anfangszustand (Standard: False = aus)

    Example
    -------
    >>> led = TwoPointController(on_level=200, off_level=250, source=h_raum)
    """

    def __init__(self, on_level: float, off_level: float, source: Block,
                 initial_state: bool = False):
        super().__init__()
        self.on_level = on_level
        self.off_level = off_level
        self.source = source
        self._state = initial_state

    def _compute(self, t, dt):
        u = self.source.output(t, dt)
        if u < self.on_level:
            self._state = True
        elif u > self.off_level:
            self._state = False
        return float(self._state)


# ─────────────────────────────────────────────────────────────────────────────
# Regler
# ─────────────────────────────────────────────────────────────────────────────

class PID(Block):
    """Diskreter PID-Regler.

    u(t) = Kp·e + Ki·∫e dt + Kd·de/dt

    Parameters
    ----------
    Kp     : Proportionalanteil
    Ki     : Integralanteil   (Standard: 0 → reiner P-Regler)
    Kd     : Differentialanteil (Standard: 0)
    source : Eingangsblock (Regelabweichung e)

    Example
    -------
    >>> regler = PID(Kp=1.0, Ki=0.5, source=e)
    """

    def __init__(self, Kp: float, Ki: float = 0.0, Kd: float = 0.0,
                 source: Block = None):
        super().__init__()
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.source = source
        self._integral = 0.0
        self._last_error = 0.0

    def _compute(self, t, dt):
        e = self.source.output(t, dt)
        self._integral += e * dt
        derivative = (e - self._last_error) / dt if dt > 0 else 0.0
        self._last_error = e
        return self.Kp * e + self.Ki * self._integral + self.Kd * derivative


# ─────────────────────────────────────────────────────────────────────────────
# Simulation und Visualisierung
# ─────────────────────────────────────────────────────────────────────────────

class Scope:
    """Führt die Simulation durch und stellt Signale als Zeitverlauf dar.

    Parameters
    ----------
    t_end  : Simulationsende in Sekunden (Standard: 10)
    dt     : Abtastzeit in Sekunden (Standard: 0.01)
    title  : Diagrammtitel (optional)
    ylabel : Beschriftung der y-Achse (optional)
    xlabel : Beschriftung der x-Achse (Standard: "Zeit t [s]")

    Verwendung
    ----------
    Übergabe der Signale als Schlüsselwort-Argumente an ``run()``:
    der Schlüsselname wird als Legende verwendet::

        Scope(t_end=15).run(Eingang=u, Ausgang=y)

    Der Rückgabewert ist ein Dict ``{label: [werte]}`` für weitere Auswertung.

    Example
    -------
    >>> scope = Scope(t_end=30, dt=0.1, ylabel="Temperatur [°C]")
    >>> data = scope.run(Sollwert=w, Istwert=strecke, Abweichung=e)
    """

    def __init__(self, t_end: float = 10.0, dt: float = 0.01,
                 title: str = "", ylabel: str = "", xlabel: str = "Zeit t [s]"):
        self.t_end = t_end
        self.dt = dt
        self.title = title
        self.ylabel = ylabel
        self.xlabel = xlabel

    def run(self, **signals: Block) -> dict[str, list[float]]:
        """Simuliert und plottet die übergebenen Blöcke.

        Parameters
        ----------
        **signals : Label=Block-Paare

        Returns
        -------
        dict mit den simulierten Zeitreihen (für eigene Auswertung)
        """
        t_values = np.arange(0, self.t_end, self.dt)
        results: dict[str, list[float]] = {label: [] for label in signals}

        for t in t_values:
            _next_step()          # neuer Zeitschritt → Cache ungültig machen
            for label, block in signals.items():
                results[label].append(block.output(t, self.dt))

        # Darstellung
        n = len(signals)
        if n == 1:
            fig, axes = plt.subplots(1, 1, figsize=(10, 4))
            axes = [axes]
        else:
            fig, axes = plt.subplots(n, 1, figsize=(10, 3 * n), sharex=True)

        for ax, (label, values) in zip(axes, results.items()):
            ax.plot(t_values, values, label=label, linewidth=1.5)
            ax.set_ylabel(label)
            ax.legend()
            ax.grid(True, alpha=0.3)

        axes[-1].set_xlabel(self.xlabel)
        if self.ylabel and n == 1:
            axes[0].set_ylabel(self.ylabel)
        if self.title:
            axes[0].set_title(self.title)
        plt.tight_layout()
        plt.show()

        return results
