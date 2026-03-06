---
marp: true
theme: beams
author: Julian Huber
size: 16:9
footer: Julian Huber - Bussysteme


---

<!-- paginate: true -->


# 2.2 Steuerung II – Funktionen & Verknüpfungssteuerung

<!-- _class: title -->

---

## Orientierung – Einheit 6 von 14

<!-- _class: white -->

### Wo sind wir?

| Abgeschlossen | **Heute** | Als nächstes |
|---|---|---|
| Einheit 5: Steuerung I (FSM) | **Einheit 6: Steuerung II** | Einheit 7: Regelungstechnik I |

### Was haben wir bisher gelernt?

* Ablaufsteuerungen mit FSM (Zustände, Übergänge, Ausgaben)
* Treppenlichtschaltung implementiert
* Code mit Funktionen strukturieren (Kapselung, Parameter, Rückgabewerte)

### Wo wollen wir hin?

Nicht jede Steuerung folgt einem zeitlichen Ablauf – manchmal hängt der Ausgang einfach von mehreren Eingängen **gleichzeitig** ab. Heute lernen wir **Verknüpfungssteuerungen** mit Boolescher Algebra. Danach strukturieren wir komplexere Systeme objektorientiert: Sensoren und Aktoren als Klassen mit Attributen und Methoden.

---

## Lernziele – Einheit 6

* Verknüpfungssteuerung mit Wahrheitstabelle und Boolescher Funktion beschreiben
* Tageslichtschaltung als Boolesche Funktion implementieren


---

### Aufgaben dieser Einheit

| Aufgabe | Inhalt |
|---------|--------|
| ✍️ 2_2_4 | Tageslichtschaltung als Verknüpfungssteuerung |


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



---

## Verknüpfungssteuerungen

* Während Ablaufsteuerungen den Ablauf eines Prozesses steuern, verknüpfen Verknüpfungssteuerungen die Eingangssignale mit den Ausgangssignalen
* Diese Trennung ist jedoch eher akademisch, da die meisten Systeme sowohl Ablauf- als auch Verknüpfungssteuerungen enthalten

---

### Beispiel: Wechselschalter

<!-- _class: white -->

* Verknüpfungssteuerungen können z.B. durch Wahreheitstabellen und Boolsche Funktionen beschrieben werden
* Später werden wir hierzu noch grafische Beschreibungen kennenlernen (Funktionsplan, Kontaktplan, ...)


![h:300](images/Wechselschaltung.svg)

---

**Wahrheitstabelle**

| Schalter 1 | Schalter 2 | Lampe |
|------------|------------|-------|
|     0      |     0      |   1   |
|     0      |     1      |   0   |
|     1      |     0      |   0   |
|     1      |     1      |   1   |

**Boolsche Funktion**
$L = (S_1 \land S_2) \lor (\lnot S_1 \land \lnot  S_2)$


---


## ✍️ Aufgabe 2_2_4: Implementierung einer vereinfachten Tageslichtschaltung

![bg right:33% h:720](images/Tageslichtschaltung.png)

* Wir vereinfachen die Tageslichtschaltung, indem wir die Parameter für Zeit und Mindest-Beleuchtungsstärke (`PAR_SETPT`) weglassen
* Zeichen Sie zunächst eine Wahrheitstabelle für die Tageslichtschaltung
* Setzen Sie `L_MAN` zunächst im Code auf `False` 

--- 

* 🤓 schließen Sie dafür nur einen zusätzlichen Button dafür an, wenn Sie mit der restlichen Schaltung fertig sind
* Nutzen Sie einen Button, um den Anwesenheitszustand `P_ACT` zu simulieren
*H_ROOM* können Sie entweder als Beleuchtungsstärke, Spannung oder  `ADC-Wert` setzen
* `L_SET` soll das Ausgangssignal sein, das die Lampe steuert und kann zunächst auf `True` gesetzt werden. 🤓 Später können Sie diesen auch durch eine Pulsweitenmodulation setzen.

---

| `P_ACT` | `H_ROOM` `<` `PAR_SETPT` | `L_MAN` | `L_SET` |
|-------|----------------|-------|-------|
|   0   |        0       |   0   |   0   |
|   1   |        0       |   0   |   0   |
|   0   |        1       |   0   |   0   |
|   1   |        1       |   0   |   1   |
|   0   |        0       |   1   |   1   |
|   1   |        0       |   1   |   1   |
|   0   |        1       |   1   |   1   |
|   1   |        1       |   1   |   1   |

$$L_{\text{SET}} = (P_{\text{ACT}} \land (H_{\text{ROOM}} < \text{PAR}_{\text{SETPT}})) \lor  L_{\text{MAN}})$$

---

### Hinweise 

- Bauen Sie auf Aufgaben 2_1_3 und 2_1_5 auf, um die Tageslichtschaltung zu implementieren


??? optional-class "💡 anzeigen"
    ```python
    --8<-- "Aufgaben\2_1_3\code.py"
    ```
??? optional-class "💡 anzeigen"
    ```python
    --8<-- "Aufgaben\2_1_5\code.py"
    ```
??? optional-class "💡 anzeigen"
    ```python
    --8<-- "Aufgaben\2_1_5\mappings.py"
    ```

---

### [✔️ Lösung](Aufgaben\2_2_4)

<!-- _color: black -->

??? optional-class "💡 anzeigen"
    ```python
    --8<-- "Aufgaben\2_2_4\code.py"
    ```
---
