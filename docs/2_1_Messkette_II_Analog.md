---
marp: true
theme: beams
author: Julian Huber
size: 16:9
footer: Julian Huber - Bussysteme


---

<!-- paginate: true -->


# 2.1 Messkette II – Analoge Signale & Mapping

<!-- _class: title -->

__Bussysteme__
Julian Huber & Michael Renzler

---

## Orientierung – Einheit 4 von 14

<!-- _class: white -->

### Wo sind wir?

| Abgeschlossen | **Heute** | Als nächstes |
|---|---|---|
| Einheit 3: Messkette I (digital) | **Einheit 4: Messkette II** | Einheit 5: Steuerung I (FSM) |

---

### Was haben wir bisher gelernt?

* EVA-Prinzip und digitale Ein-/Ausgänge am Pico
* Pull-Up/Pull-Down-Beschaltung, GPIO-Grenzen
* LED und Taster anschließen und programmieren

### Wo wollen wir hin?

Digitale Signale kennen nur 0 und 1. Viele Sensoren liefern aber **analoge Größen** (z.B. Helligkeit in Lux). Heute lernen wir, wie der ADC diese Werte erfasst und wie wir Rohwerte mit **Mapping-Funktionen** in physikalische Einheiten umrechnen. PWM ermöglicht dazu stufenlose Ausgangssteuerung – die Grundlage der Konstantlichtregelung.

---

## 🎯 Lernziele – Einheit 4

* ADC-Auflösung und Referenzspannung erklären und berechnen
* PWM-Signal (Duty Cycle, Frequenz) parametrieren
* Analogen Helligkeitssensor anschließen und auslesen
* Lineares Mapping (ADC → Spannung) implementieren
* Komplexeres Mapping (ADC → Lux) implementieren und anpassen

### Aufgaben dieser Einheit

| Aufgabe | Inhalt |
|---------|--------|
| 🤓 ✍️ 2_1_4 | LED mit PWM stufenlos ansteuern |
| ✍️ 2_1_5 | Analogen Helligkeitssensor anschließen und kalibrieren |
| 🤓 ✍️ 2_1_6 | Umgebungsvariablen für das Mapping verwenden |

---

## 🤓 ✍️ Aufgabe 2_1_4: Anschluss einer LED mit PWM an einen Raspberry Pi Pico

> PWM ist die Grundlage für stufenlose Lichtsteuerung – und damit für die **Konstantlichtregelung** (Kapitel 3): Dort muss die Helligkeit nicht nur an/aus, sondern kontinuierlich auf einen Sollwert geregelt werden. Ein binärer Ausgang reicht dafür nicht – PWM macht es möglich.

* Sorgen Sie nun dafür, dass die LED mit PWM angesteuert wird, so dass diese nach Betätigung des Tasters für $1\,\text{s}$ leuchtet und dann langsam über $5\,\text{s}$ ausgeht
+ Sie können auf die Verkabelung und den Aufbau der vorherigen [Aufgabe](https://wokwi.com/projects/457487523147649025) aufbauen

---

### Beispielcode für PWM

```Python
import pwmio
import board

pwm = pwmio.PWMOut(board.GP1)  # output on LED pin with default of 500Hz

while True:
    for cycle in range(0, 65535):  # Cycles through the full PWM range from 0 to 65535
        pwm.duty_cycle = cycle  # Cycles the LED pin duty cycle through the range of values
    for cycle in range(65534, 0, -1):  # Cycles through the PWM range backwards from 65534 to 0
        pwm.duty_cycle = cycle  # Cycles the LED pin duty cycle through the range of values
```

* Die Länge des Duty-Cycles wird durch $2^{16}=65536$ Werte abgestuft
* bei `duty_cycle = 0` der Duty-Cycle bei $0 \%$ und die LED aus
* bei `duty_cycle = 65535` der Duty-Cycle  genau so lang wie die Periodendauer

[Quelle](https://docs.circuitpython.org/en/latest/shared-bindings/pwmio/index.html)

---

### [✔️ Lösung](https://wokwi.com/projects/458180124100438017)


---

### Analoge Eingänge

<!-- _class: white -->


![](images/Messkette.svg)



* Sensoren liefern meist analoge Signale (z.B. Spannung, Strom, Widerstand)
* z.B. basieren viele Temperatursensoren auf dem Widerstand von Metallen
* Damit ändert sich bei gleichbleibender Spannung der Strom, welcher am Eingang gemessen werden kann

---

#### Analog-Digital-Wandler

* Der Analog-Digital-Wandler (ADC) wandelt ein analoges Signal in eine digitale Zahl um
* Dabei gibt es zwei relevante Parameter
    * Auflösung: Anzahl der möglichen Werte
    * Referenzspannung: Spannungsbereich, der in die Auflösung abgebildet wird
    * z.B. 16 Bit Auflösung und $3.3 \,\text{V}$ Referenzspannung 
    $\Rightarrow$ $2^{16} = 65536$ Werte zwischen $0$ und $3.3 \,\text{V}$
* Zudem können sich Systeme in ihrer Abtastrate unterscheiden, d.h. wie oft Werte gelesen werden können (z.B. durch den Sleep-Timer im `while`-loop)

---

## ✍️ Aufgabe 2_1_5: Anschluss eines analogen Helligkeitssensors

* Verbinden Sie die `+` und `-` Leiste des Breadboards mit $3.3 \,\text{V}$ und `GND` des Raspberry Pi Pico
* Verbinden Sie den analogen Eingang `A0` (`G26`) mit einem Kabel
* Fügen Sie den folgenden Code ein


---

## ✍️ Aufgabe 2_1_5: Anschluss eines analogen Helligkeitssensors


```Python
import board
import analogio
import time

# Initialisierung des ADC (Analog-Digital Converter)
ldr = analogio.AnalogIn(board.A0)

# Wiederholung
while True:
    # ADC als Dezimalzahl lesen
    read = ldr.value
    # Ausgabe in der Kommandozeile/Shell
    print("ADC:", read)
    # Warten
    time.sleep(1)
```

- Um den Wertebereich des ADC zu testen, können Sie den Eingang direkt mit `+` und `-` verbinden

---

## ✍️ Aufgabe 2_1_5: Anschluss eines analogen Helligkeitssensors

* Verbinden Sie den Eingang zunächst mit `+`, dann mit `-` 
* Welche Werte erhalten Sie?



---

## ✍️ Aufgabe 2_1_5: Anschluss eines analogen Helligkeitssensors


* Schließen Sie einen Fotowiderstand als [analogen Helligkeitssensor](https://www.elektronik-kompendium.de/sites/praxis/bauteil_ky018-ldr.htm) an den Raspberry Pi Pico an: [Beispiel](https://wokwi.com/projects/424662007489899521) 
    * _meist_ Links (I): +VCC z.B. 3,3 oder 5 Volt
    * Mitte: GND / Masse / 0 Volt
    * _meist_ Rechts (S): Verbindungspunkt des Spannungsteilers
* Sie können den Sensor entweder auf dem Breadboard montieren oder ihn mit Male-Female-Kabeln direkt verbinden
* Verdunkeln Sie und beleuchten Sie den Sensor und beobachten Sie die Änderung des Eingangswertes
* Je mehr Licht auf den Fotowiderstand fällt, desto kleiner wird sein Widerstand. 
* Optional können Sie auch die Beleuchtungsstärke mit einem Luxmeter messen und die Werte vergleichen

---

## ✍️ Aufgabe 2_1_5: Anschluss eines analogen Helligkeitssensors


![h:500](images/aufbau_pico_ky018.png)



---

## ✍️ Führen Sie ein Messprotokoll

* Zum Testen können Sie den Analog-Eingang mit $3.3 \text{ Volt}$ und $0 \text{ Volt}$ verbinden
* Lesen Sie den Wert des Sensors aus und geben Sie diesen auf der Konsole aus
* Notieren Sie sich einige Werte (`ADC`) für verschiedene Hell-Dunkel-Verhältnisse (z.B. Zuhalten, Raumlicht, Taschenlampe) und notieren Sie die Werte (oder Erstellen Sie eine Tabelle mit der [Simulation](https://wokwi.com/projects/424662007489899521))



| Umgebung    | ADC | E in Lux | U in V |
|-------------|-----|----------|--------|
| Abgedunkelt |     |          | |
| Raumlicht   |     |          | |
| Taschenlampe|     |          | |




[Quelle](https://www.elektronik-kompendium.de/sites/raspberry-pi/2612221.htm)


---


| Umgebung    | ADC | E in Lux | U in V |
|-------------|-----|----------|--------|
||65007| 0.1| |
||63007|1| |
||54301|10| |
||49484|20| |
||40489|50| |
||32727|100| |
||24950|200| |
||15987|501| |
||10866|1000| |
||3952|5000| |
||2496|10000| |
||512|100000| |

---

## ✍️ Berechnen Sie eine Mapping-Funktion zwischen ADC-Wert und Spannung

#### Mapping von Eingangswert zu Spannung

* Die Spannung und der `ADC`- Wert sind linear zueinander
* Entsprechend kann jeder Wert des `ADC` über einer lineare Funktion in eine Spannung umgerechnet werden

---

## ✍️ Berechnen Sie eine Mapping-Funktion zwischen ADC-Wert und Spannung


| Symbol | Description |
|--------|-------------|
| $U_{max}$ | maximale Spannung |
| $U_{min}$ | minimale Spannung |
| $z_{max}$ | maximaler Messwert des ADC |
| $z_{min}$ | minimaler Messwert des ADC |

* Annahme: Linearer Zusammenhang
    $U = f(z) = \beta_0 + \beta_1 z$

---
## ✍️ Berechnen Sie eine Mapping-Funktion zwischen ADC-Wert und Spannung


* 1: Wie groß ist der Y-Achsenabschnitt $\beta_0$?
    * Bei welchen Wert hat $U$, wenn $z=0$?
* 2: Wie groß ist die Steigung $\beta_1$?
    * Wie groß ist die Änderung von $U$ pro Änderung von $z$?
    * $\beta_1 = \frac{{U_{max}} - U_{min}}{z_{max} - z_{min}}$



---

## ✍️ Berechnen Sie eine Mapping-Funktion zwischen ADC-Wert und Spannung

* Der folgende Code übernimmt dein Eingangswert und gibt einen Spannungs-Wert zwischen 3.3 und 0 zurück
* Fügen Sie die Funktion `map_lin` in den Code ein und geben Sie die Spannung auf der Konsole aus


```Python
def map_lin(z):
    U_max = 3.3
    U_min = 0
    z_max = 65535
    z_min = 0
    beta_0 = U_min
    beta_1 = (U_max - U_min) / (z_max - z_min)
    return beta_0 + beta_1 * z
```

---

## ✍️ Berechnen Sie eine Mapping-Funktion zwischen ADC-Wert und Spannung

* Wenn Sie Ihren Code schön aufgeräumt haben wollen können eine Datei `mappings.py` im gleiche Ordner wie `code.py` erstellen und die Funktion dort speichern
* Sie können diese dann mittels `from mappings import map_lin` ins `main.py` importieren und nutzen

### [✔️ Lösung](https://wokwi.com/projects/457492267340534785)

---

## ✍️ Berechnen Mapping von Eingangswert zu physikalischer Größe


* Um sinnvoller mit den Werten arbeiten zu können, ist es sinnvoller die gelesen `ADC`-Werte `read` in eine Variable mit einer sinnvollen physikalischen Einheit  zu überführen
* In Unserem Fall wollen wir die Beleuchtungsstärke $E$ in Lux erhalten
* Zeichnen Sie zunächst die Werte von `ADC` gegen die gemessenen Beleuchtungsstärken in Lux auf (z.B. in Excel) und versuchen Sie eine Funktion zu finden, die die Werte gut beschreibt
* Im Fall dieses Sensors und Aufbaus lassen sich die Werte gut mit einer Parabel anpassen

---

* Der Zusammenhang zwischen `ADC`-Wert und Beleuchtungsstärke $E$ in Lux sieht aus, wie eine Hyperbel.
* Im nächten Semester werden wir lernen, dass der Fotoresistor dem Potenzgesetz folgt, d.h.  es folgt etwa $R​=C⋅E−γ$, wobei $R$ der Widerstand, $E$ die Beleuchtungsstärke, $C$ eine Konstante und $\gamma$ der sogenannte Dunkelstrom-Exponent ist. In unserem Fall lesen wir nicht direkt $R$ sondern eine Spannung, die über einem Spannungsteiler gemessen wird. Entsprechend wird die Sache noch etwas komplizierter.


![bg right:43% w:550](../Aufgaben/2_1_4/messkurve/messwerte.png)

---

* Durche eine Log-Log-Plot der Werte können wir die Potenzfunktion in eine lineare Funktion überführen, welche sich dann [leichter anpassen](https://colab.research.google.com/drive/11aHwiEgmw3qW6GzxGUjvuVZJLqs4XCbK?usp=sharing) lässt und zumindest einen gewissen Bereich gut beschreibt. In diesem Fall erhalten wir die folgende Funktion, welche die Werte gut beschreibt:


```
Gefittete Parameter im Log-Log-Raum:
beta_1 (Steigung): -2.3332
beta_0 (Achsenabschnitt): 11.9614
Bestimmtheitsmaß R²: 0.8260
```

---

Die folgende Funktion implementiert die gefittete Funktion, welche die Werte gut beschreibt. Sie können diese Funktion in `mappings.py` speichern und dann in `code.py` importieren und nutzen, um die Beleuchtungsstärke in Lux auszugeben.

```Python
def map_log_log_lin(z):
    if z < 1:
        z = 1
    log10_z = math.log(z) / LN10
    log10_E = BETA_1 * log10_z + BETA_0
    return math.exp(log10_E * LN10)
```


![bg right:43% w:550](../Aufgaben/2_1_4/messkurve/loglog.png)


---

## ✍️ Berechnen Sie eine Mapping-Funktion zwischen ADC-Wert und Spannung

![bg right:43% w:550](../Aufgaben/2_1_4/messkurve/fit.png)


* Ergänzen Sie in eine Datei `mappings.py` (im gleichen Ordner, wie die `code.py`) eine Funktion `map_log_log_lin()`, die stattdessen das oben angegeben Modell implementiert. Und passen Sie `code.py` so an, dass die Beleuchtungsstärke in Lux ausgegeben wird und validieren Sie die Werte mit einem Luxmeter oder den Werten aus der Simulation. 

---


##### Übliche Beleuchtungsstärken $E$

| Umfeld | $E \text{ in lux}$ |
|--------|-------------------|
| Mondlose, klare Nacht | 0,0003 |
| Nachts bei Vollmond | 0,2 |
| Beleuchtete Strassen, Plätze | 10..20 |
| Abstellräume, Lagerräume | 50 |
| Lagerräume, Toiletten, Treppen | 100 |
| Speiseräume, Werkhallen, | 200 |
| Läden, Sitzungszimmer | 300 |
| Arbeitsplätze, Schulzimmer | 500 |
| erhöhte Ansprüche | 750 |
| Elektronikmontage, Uhrenmacher | 1.000 |
| Bedeckter Himmel im Winter | 1.000.. 2.000 |
| Bedeckter Himmel im Sommer | 5.000..20.000 |
| Sonnenlicht im Winter | 10.000 |
| Sonnenlicht im Sommer | 100.000 |




---

##### Nachverarbeitung nach ADC

* Viele (teurere) Peripheriegeräte kommen als Transmitter (Kombination aus dem Sensor selbst und einem Messumformer)
* Diese linearisieren sie Spannungs-(oder Strom-)Ausgabe
* Eine Umrechnung der Spannungswerte an Eingang in die physikalische Größen muss jedoch weiterhin stattfinden
* Informationen hierzu finden sich meist im [Datenblatt](https://shop.bb-sensors.com/out/media/Bedienungsanleitung_Helligkeitssensor_Messumformer_0555%20300x.pdf)

![bg right:43% w:550](images/BB-Helligkeit_Datenblatt.png)


[Quelle](https://shop.bb-sensors.com/Messtechnik-je-Branche/Gebaeudetechnik/Helligkeitssensor-mit-Messumformer-0-10-V.html)


---

## 🤓 Verwendung von Globalen Variablen

- einige Variablen sind so grundlegend, dass wir Sie nicht im Code sondern zentral verändern wollen
- Hierzu können wird Umgebungsvariablen in der `settings.toml` verändern im Verzeichnis `CIRCUITPY` ändern

```
MY_NAME = "Julian"
```
- Im Code können diese mittels `os` aufgerufen werden

```Python
#  connect to your SSID
import os

print(os.getenv('MY_NAME'))
```

* Passen Sie den Code so an, dass die zur Umwandlung benötigten Werte als Umgebungsvariablen gesetzt werden können. Funktioniert __nicht in Wokwi__.

---

## 🤓 ✍️ Aufgabe 2_1_6: Umgebungsvariablen für das Mapping verwenden

* Passen Sie die Funktion `map_log_log_lin()` so an, dass die Parameter $BETA_0$ und $BETA_1$ als Umgebungsvariablen gesetzt werden können
* Überlegen Sie sich, was noch alles sinnvoll in einer `settings.toml` gespeichert werden könnte?
* Erinnern Sie sich an die Raumautomatisierungsfunktion mit Eingaben, Ausgaben und Parametern? Was davon passt am sinnvollerweise in die `settings.toml`?


![bg right:40% h:720](images/Helligektismessung.pdf.png)


---

### Analoge Ausgänge

<!-- _class: white -->


![](images/Messkette.svg)



* Entsprechend gibt es auch analoge Ausgänge
* Diese können z.B. zur Ansteuerung von Motoren genutzt werden
* Dabei wird einer meist der Wert einer Integer-Variable im Speicher in einen Spannungswert umgewandelt

---

## Fazit

- Analoge Signale können mit einem ADC in digitale Werte umgewandelt werden
- Die Pulsweitenmodulation (PWM) ermöglicht die stufenlose Ansteuerung von Aktoren, z.B. LEDs über digitale Ausgänge (die schnell zwischen an und aus wechseln können)
- Das Mapping von ADC-Werten zu physikalischen Größen kann über verschiedene Funktionen erfolgen (z.B. linear, quadratisch, logarithmisch), die aus der Kalibrierung der Sensoren abgeleitet werden können
- Umgebungsvariablen können genutzt werden, um wichtige Parameter zentral zu speichern und zu verändern, ohne den Code selbst anpassen zu müssen

