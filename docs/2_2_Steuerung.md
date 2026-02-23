---
marp: true
author: Julian Huber
size: 16:9
footer: Julian Huber - Bussysteme

# Strg+[ ] for Options

theme: beams

---

<!-- paginate: true -->


# 2.2 Steuerung

<!-- _class: title -->


---

## Orientierung – Einheit 5 von 14

<!-- _class: white -->

### Wo sind wir?

| Abgeschlossen | **Heute** | Als nächstes |
|---|---|---|
| Einheit 4: Messkette II (analog) | **Einheit 5: Steuerung I** | Einheit 6: Steuerung II (Verknüpfungen + OOP) |

### Was haben wir bisher gelernt?

* EVA-Prinzip, digitale und analoge Ein-/Ausgänge
* PWM und ADC; Mapping von Rohwerten in physikalische Einheiten
* Raspberry Pi Pico in CircuitPython programmieren

### Wo wollen wir hin?

Sensoren liefern Werte – doch wie entscheidet das System, **was** es tun soll? Heute lernen wir **Ablaufsteuerungen** mit endlichen Automaten (FSM). Die Treppenlichtschaltung aus dem RA-Schema wird Schritt für Schritt zu einem lauffähigen Programm. Dazu strukturieren wir Code mit **Funktionen**, um ihn wiederverwendbar zu machen.

---

## Lernziele – Einheit 5

* Ablaufsteuerung vs. Verknüpfungssteuerung abgrenzen
* Endlichen Automaten (FSM) mit Zuständen, Übergangsbedingungen und Ausgaben beschreiben
* Zeitbedingte Übergänge (Hold-Timer) in CircuitPython implementieren
* Treppenlichtschaltung als FSM entwerfen und implementieren
* Code in Funktionen kapseln (Eingaben, Parameter, Ausgaben)
* Lokale vs. globale Variablen erklären

### Aufgaben dieser Einheit

| Aufgabe | Inhalt |
|---------|--------|
| ✍️ 2_2_1 | Treppenhauslicht als FSM implementieren |
| ✍️ 2_2_2 | Treppenlicht mit zwei Tastern entwerfen (FSM auf Papier) |
| 🤓 ✍️ 2_2_3 | Treppenlicht mit zwei Tastern implementieren |
| 🤓 ✍️ 2_3_1 | Tageslichtschaltung mit Funktionen implementieren |
| ✍️ 2_3_2 | Code in Funktionen auslagern (Refactoring) |

---


## Ursprünge der Steuerungstechnik und Automatisierung


* **20–62** - Heron von Alexandria Automaten einer Wein und Milch spendenden Bacchus-Figur
* **1784** Webmaschinen von hölzernen Lochkarten 
* **1835** erfindet Joseph Henry das elektromechanische Relais
* **1969**  Odo J. Struger beim US-Unternehmen Allen-Bradley eine SPS (zeitgleich mit  Richard E. Morley)

![bg right:33%](images/Hero_of_Alexandria,_Automata,_Venice,_Gr._516.jpg)

---

### 🧠 Evolution zu Industrie 4.0

* **Industrie 1.0** (1784): Einsatz von mechanischen Webstühlen, die insbesondere durch **Lochkarten-Steuerungen** und später durch umlaufenden Bänder zu Webmaschinen weiterentwickelt wurden.
 
* **Industrie 2.0** (1870): erster Einsatz von Fließbändern in den USA (Schlachthöfe) unter Nutzung elektrischer Antriebe, die durch entsprechende **Schütz- und Relais-Steuerungen** geschaltet wurden.
 
* **Industrie 3.0** (1969) **Speicherprogrammierbaren Steuerungen**, Durchbruch bei der Industrieelektronik und Informationstechnik zur massenweisen Steuerung und Automatisierung der Produktion

* **Industrie 4.0** (2012) Cyber-Physikalischer Systeme mit globaler Vernetzung zur global optimierten Steuerung der international organisierten Produktion (**Internet der Dinge**). 

---

## Ablaufsteuerung

* steuert den Ablauf *ereignisdiskreter Prozesse* (Schrittkette). Beim Erreichen eines Schwellwertes einer Steuergröße (Ereignis) wir ein weiterer Prozess angestoßen.
    * z.B. Ablauf in einer Waschmaschine
    * z.B. Human Centric Lighting
    * z.B. Treppenhauslicht

---

### Beispiel Treppenlichtschaltung

> Über die Funktion Treppenlichtschaltung können Beleuchtungseinrichtungen temporär eingeschaltet werden. Nach Ablauf der Treppenlichthaltezeit kann eine Abschaltvorwarnzeit aktiv werden, die den Nutzer z. B. durch kurzzeitige Unterbrechung(„Flackern“) über die bevorstehende Abschaltung informiert. Ein erneuter Empfang einer Eingabeinformation zum Einschalten startet die Verzögerungszeit neu. Die Funktion benötigt als Eingabeinformation das Ergebnis der Bedienfunktion Licht stellen und liefert ihrerseits die Ausgabeinformation für eine oder mehrere Aktorfunktionen Lichtaktor.

![bg right:35% h:600](images/Treppenlichtschaltung.pdf.png)


---

#### Naive Lösung

```Python
import time
import board
import digitalio

PAR_HOLD = 3
PAR_WARN = 1

button_pin = board.GP0  # Replace with the GPIO pin connected to your button

button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Use pull-up resistor; change if using pull-down

led_pin = board.GP1      # Replace with the GPIO pin connected to your LED
led = digitalio.DigitalInOut(led_pin)
led.direction = digitalio.Direction.OUTPUT


while True:
    if not(button.value):  # Button is pressed (LOW)
        print("Button Pressed!")  
        led.value = True
        time.sleep(PAR_HOLD)  
        for i in range(1,5):
            led.value = False
            time.sleep(0.1)
            led.value = True
            time.sleep(0.1)
        time.sleep(PAR_WARN)
        led.value = False
```

---

#### Probleme mit der naiven Lösung

<!-- _class: white -->

![bg right:35% h:520](images/mermaid-diagram-2024-03-12-163310.svg)

* Erneutes betätigen des Taster setzt die Wartezeit nicht zurück
* Unser System hat kein Gedächtnis (über den Zustand)
* Der Ablauf sollte besser nicht nur durch einen Zeitlichen Rahmen, sondern auch durch Zustände gesteuert werden

---

```Mermaid
stateDiagram
    A : LED ein 1
    B : LED flackert
    C : LED ein 2
    E : LED aus
    [*] --> E : Systemstart
    E --> A : L_MAN
    A --> B : PAR_HOLD
    C --> E : PAR_WARN
    B --> C
```

---


### Finite State Machine (Endlicher Automat)

* In Abhängigkeit vom Systemzustand erwarten wir unterschiedliches Verhalten z.B.
    * Nach Tastendruck soll die Lampe angeschaltet werden
    * Nach Ablauf einer Wartezeit soll die Lampe ausgeschaltet werden
    * Davor gibt es ein Flackern als Warnung
    * Nach einem weiteren Tastendruck wird die Wartezeit zurückgesetzt
* Einfache Systeme lassen sich meist durch Ihre Zustände und deren Übergänge beschreiben
* Durch die Beschreibung als State-Machine können wir das Verhalten des Systems sauber trennen und die Implementierung vereinfachen

---


#### Implementierung eines Cola-Automaten

<!-- _class: white -->


* Der Automat startet im Zustand `Auswahl anfordern`
* Der Automat kann in den Zustand `Bezahlung anfordern` wechseln
* Wird die geforderte Summe erreicht, wechselt der Automat in den Zustand `Ware ausgeben`
* Ist die Ausgabe abgeschlossen, wechselt der Automat wieder in den Zustand `Auswahl anfordern`
* Wird die Bezahlung abgebrochen, wechselt der Automat in den Zustand `Rückgeld herausgeben` und dann wieder in den Zustand `Auswahl anfordern`

![bg right:35% w:450](images/state_machice_cola.svg)

---

#### 🤓 (Deterministic) Finite State Machine (Endlicher Automat)

* Dieser Ansatz basiert auf der Theorie der formalen Sprachen
* Eine DFSM beschreibt ein System mit endlich vielen Zuständen beschreibt
* Eine DFSM ist ein 5-Tupel $M = (Q, \Sigma, q_0, F, \delta)$ mit
    * Endlicher Zustandsmenge $Q$
    * Endliche Eingabealphabet $\Sigma$
    * Endlicher Startzustand $q_0 \in Q$
    * Endlicher Endzustandsmenge $F \subseteq Q$
    * Übergangsfunktion $\delta: Q \times \Sigma \rightarrow Q$

---

#### 🤓 In der Theorie der formalen Sprachen

<!-- _class: white -->


![bg right:33% h:250](images/DFAexample.svg)

* $Q = \{S_1, S_2\}$
* $\Sigma = \{0,1\}$
* $q_0 = S_1$
* $F = \{S_1\}$
* $\delta(S_1, 0) = S_2$,  $\delta(S_1, 1) = S_1$
* $\delta(S_2, 0) = S_1$,  $\delta(S_2, 1) = S_2$
* Akzeptiert (endet in $F$)
    * `1`, `11`, `01101`, `11001` 
* Akzeptiert nicht (endet nicht in $F$)
    * `0`, `10`, `10100`, `01001`
* Anwendung
    * Parser
    * [Regular Expressions](https://en.wikipedia.org/wiki/Regular_expression)

---

##### 🤓 Regular Expressions

* Eine reguläre Sprache ist eine Menge von Zeichenketten, die durch einen regulären Ausdruck beschrieben werden können
* z.B. Beider Suche nach einer Zeichenkette in einem Text
    * Alles, was `mapping` im Namen hat:
        * `.*mapping.*`
    * Alles was mit mapping beginnt und mit einer Zahl endet
        * `mapping\d+`

---

#### In der Programmierpraxis

<!-- _class: white -->


![bg right:35% w:450](images/mermaid-diagram-2024-03-12-163310.svg)

* Die Knoten stellen Systemzustände dar. Innerhalb dieser Zustände muss das Systemen nicht statisch sein (z.B. Zeit muss z.B. mitgezählt werden)
* Die gerichteten Kanten stellen Übergänge zwischen den Zuständen dar, die durch Events und Bedingungen ausgelöst werden
* Die Systemzustände können nur in festgelegten Reihenfolgen durchlaufen werden
* Ein Endzustand ist optional

---

## ✍️ Aufgabe 2_2_1: Implementierung eines Treppenhauslichts

<!-- _class: white -->


* In `code_state_machine.py` (folgende Folie) ist das auf der rechten Seite dargestellte Programm implementiert
* Beschreiben Sie verbal, was in jedem der Zustände passiert
* Berücksichtigen Sie dabei im Besonderen, warum es die beiden Zustände `LED leuchtet` und `LED flackert` gibt und diese nicht in einem zusammengefasst wurden

![bg right h:720](images/mermaid-diagram-2024-01-25-114138.svg)



---

<!-- _class : white -->

```Python
import time
import board
import digitalio

PAR_HOLD = 5
PAR_WARN = 2
state = "start"

if state == "start":
    button_pin = board.GP0  # Replace with the GPIO pin connected to your button
        
    button = digitalio.DigitalInOut(button_pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP  # Use pull-up resistor; change if using pull-down
        
    led_pin = board.GP1      # Replace with the GPIO pin connected to your LED
    led = digitalio.DigitalInOut(led_pin)
    led.direction = digitalio.Direction.OUTPUT

    state = "LED aus"
    print("Erfolgreich gestartet")

while True:
    time.sleep(0.5)
    if state == "LED aus":
        print("State: LED aus \n  Warte auf Aktion")
        if not(button.value):  # Button is pressed (LOW)
            print("Button Pressed!")
            state = "LED an"
            led.value = True

    
    if state == "LED an":
        print("State: LED an")
        time_start = time.time()
        print("  um: ", time.time())
        state = "LED leuchtet"

    if state == "LED leuchtet":
        if not(button.value):  # Button is pressed (LOW)
            print("Button Pressed!")
            state = "LED an"

        print("LED leuchtet") 
        print(" seit: ", time.time() - time_start)
        if time.time() - time_start > PAR_HOLD:
            state = "LED flackert" 

    if state == "LED leuchtet2":
        if not(button.value):  # Button is pressed (LOW)
            print("Button Pressed!")
            state = "LED an"

        print(" seit Warnung: ", time.time() - time_warning)
        if time.time() - time_warning > PAR_WARN:
            state = "LED aus" 
            led.value = False
        
    if state == "LED flackert":
        for i in range(1,5):
            led.value = False
            time.sleep(0.1)
            led.value = True
            time.sleep(0.1)
        time_warning = time.time()
        state = "LED leuchtet2" 
        led.value = True
```

![bg right h:720](images/mermaid-diagram-2024-01-25-114138.svg)

---


```Mermaid
stateDiagram
    A : Start
    C:  LED an
    D:  LED leuchtet
    E:  LED leuchtet2
    F:  LED flackert
    G : LED aus
    [*] --> A : Systemstart
    A --> C : Taster wird gedrückt
    C --> D : 
    D --> F : PAR_HOLD vergeht
    E --> G : PAR_WARN vergeht
    F --> E: 
    D --> C: Taster wird gedrückt
    E --> C: Taster wird gedrückt   
    G --> C: Taster wird gedrückt   
```

---

### [✔️ Lösung](Aufgaben\2_2_1)

<!-- _color: black -->

??? optional-class "Lösung anzeigen"
    ```python
    --8<-- "Aufgaben\2_2_1\code_state_machine.py"
    ```

---

## ✍️ Aufgabe 2_2_2: Treppenlicht mit zwei Tastern (State Machine entwerfen)

> Erweitern Sie das Treppenlicht aus Aufgabe 2_2_1: Ein echtes Treppenhaus hat auf **jedem Stockwerk** einen eigenen Taster. Beide sollen das Licht einschalten und die Haltezeit neu starten können.

* Das Treppenhaus verbindet zwei Stockwerke mit je einem Taster (`BUTTON_A`, `BUTTON_B`)
* Drückt man einen beliebigen Taster, geht das Licht für `PAR_HOLD` Sekunden an
* Nach Ablauf der Haltezeit flackert das Licht für `PAR_WARN` Sekunden als Vorwarnung
* Ein erneuter Druck auf irgendeinen der beiden Taster (auch während der Vorwarnung) startet die Haltezeit neu
* **Zeichnen Sie** die State Machine (Zustände, Übergänge, Ausgaben) – zunächst ohne Code

**Fragen:**
- Welche Zustände brauchen Sie?
- Wie ändern sich die Übergänge im Vergleich zu 2_2_1, wenn zwei Taster möglich sind?
- Was ändert sich am Code (Bedingungen in den `if`-Zweigen)?

---

### ✔️ Lösung

<!-- _color: black -->

??? optional-class "💡 anzeigen"
    Die Zustände sind identisch mit 2_2_1. Der einzige Unterschied: jede Taster-Bedingung lautet nun `not(button_a.value) or not(button_b.value)` statt nur `not(button.value)`. Die State Machine selbst ändert sich strukturell nicht.

---

## 🤓✍️ Aufgabe 2_2_3: Treppenlicht mit zwei Tastern implementieren

* Implementieren Sie die erweiterte Treppenlichtschaltung aus Aufgabe 2_2_2 auf dem Raspberry Pi Pico
* Schließen Sie einen zweiten Taster an `GP2` an
* Passen Sie den Code aus Aufgabe 2_2_1 so an, dass beide Taster die Haltezeit starten und neu starten können


---


---


<!-- paginate: true -->


# 2.3 Funktionen

<!-- _class: title -->



---

## Funktionale Programmierung

* Berechnung von Output aus Input wird in wieder aufrufbaren Funktionen gekapselt
* Funktion hat nur Input und Output aber keinen Speicher / Zustand 

```Python
def add(a, b):
    return a + b

add(1, 2) # 3
add(3, 4) # 7
```

---

## Steuerfunktion

$$L_{\text{SET}} = (P_{\text{ACT}} \land (H_{\text{ROOM}} < \text{PAR}_{\text{SETPT}})) \lor  L_{\text{MAN}}$$

```Python
def l_set(p_act, h_room, PAR_SETPT, l_man):
    return (p_act and (h_room<PAR_SETPT)) or l_man
```

```Python
from tageslichtschaltung import l_set
from mapping import map_quat

while True:
    l_set_value = l_set(p_act, h_room, PAR_SETPT, l_man)
```

---


## 🤓✍️ Aufgabe 2_3_1: Implementierung einer Tageslichtschaltung

* Implementieren Sie die Tageslichtschaltung in Python
* Stellen Sie zunächst sicher, dass LED, Button und Analog-Digital-Wandler korrekt angeschlossen sind
* Setzen Sie die manuelle Einstellung `l_man` dauerhaft auf `False` 
* Setzen Sie den Sollwert `PAR_SETPT` auf einen geigneten Wert
* Legen Sie die beiden Module `tageslichtschaltung.py` und `mappings.py` in den gleichen Ordner wie Ihre Hauptdatei
* 🤓 Recherchieren Sie einen geeigneten Sensor, den Sie für die Anwesenheitserkennung verwenden können

---

### Möglicher Startpunkt

```Python
import board
import analogio
import time
from mappings import map_quat
from tageslichtschaltung import l_set
import digitalio

# Initialisierung des ADC (Analog-Digital Converter)
ldr = analogio.AnalogIn(board.A2)

# Initialisierung der LED
led_pin = board.GP1      # Replace with the GPIO pin connected to your LED
led = digitalio.DigitalInOut(led_pin)
led.direction = digitalio.Direction.OUTPUT

# Initialisierung Button
button_pin = board.GP0  # Replace with the GPIO pin connected to your button
button = digitalio.DigitalInOut(button_pin)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP  # Use pull-up resistor; change if using pull-down


# Parameter setzen
PAR_SETPT = 100
l_man = False


# Wiederholung
while True:
    # ADC als Dezimalzahl lesen
    read = ldr.value
    # Ausgabe in der Kommandozeile/Shell
    print("ADC:", read)
    print("E in Lux", map_quat(read))

```

---

### `tageslichtschaltung.py`

```Python
def l_set(p_act, h_room, PAR_SETPT, l_man):
    return (p_act and h_room<PAR_SETPT) or l_man
```

---

### `mappings.py`

```Python
def map_lin(z):
    E_max = 1
    E_min = 0
    z_max = 65535
    z_min = 0
    beta_0 = E_min
    beta_1 = (E_max - E_min) / (z_max - z_min)
    return beta_0 + beta_1 * z

def map_quat(x):
    s = 44000
    a = 0.0015
    return ((x-s)*a) **2

```

### [✔️ Lösung](Aufgaben\2_3_1)

<!-- _color: black -->

??? optional-class "💡 anzeigen"
    ```python
    --8<-- "Aufgaben\2_3_1\code.py"
    ```

---

## ✍️ Aufgabe 2_3_2:

* Welche Teile des Codes könnte man ebenfalls in Funktionen auslagern?
* Wie schätzen Sie den Aufwand ein, wenn man nun weitere Tageslicht-Schaltungen mit anderen LEDs und Sensoren auf der gleichen Platine realisieren möchte?

### ✔️ Lösung

* Initialisierung, da die Code immer gleich ist und sich nur je nach Aufbau die Pins ändert
* Umrechnungen
* Einfacher, wenn mehr (z.B. auch die Zuweisung der Ein- und Ausgänge) in Funktionen ausgelagert wird

---

## Sichtbarkeit von Variablen

### Lokale Variablen

* Variablen, die innerhalb einer Funktion definiert werden (z.B. `s`) sind außerhalb der Funktion nicht sichtbar (*Kapselung*)
* Dies gilt für die meisten Programmiersprachen und z.B. auch für Schleifen

``` Python
def map_quat(x):
    s = 44000
    a = 0.0015
    return ((x-s)*a) **2

print(s)
# NameError Traceback (most recent call last)
# <ipython-input-11-76c4dd40fb41> in <module>
# ----> 1 print(s)

# NameError: name 's' is not defined
```

---

### Globale Variablen

- Variablen, die (bewusst) überall im Programmcode aufrufbar sind (z.B. `PAR_SETPT`) sind **globale Variablen**
- in Python werden globale Variablen in Großbuchstaben geschrieben

```Python
A_GLOBAL_VAR = 1

def my_function():
  a_local_variable = 2
  return a_local_variable

another_variable = my_function()

print(A_GLOBAL_VAR) # 1
print(a_local_variable) # Error
print(another_variable) # 2
```

