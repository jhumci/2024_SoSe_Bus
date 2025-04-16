---
marp: true
author: Julian Huber
size: 16:9
footer: Julian Huber - Bussysteme

# Strg+[ ] for Options

theme: beams

---

<!-- paginate: true -->


# 3.3 Regelverhalten

<!-- _class: title -->





---

## 🧠 PID-Regler


![](images/Idealer_PID_Sprungantwort.svg)

- **universellste** der klassischen Regler
-  Der PID-geregelte Kreis ist genau und sehr schnell, deshalb wird er bevorzugt in den **meisten Anwendungen** eingesetzt
* $u(t)=K_P \cdot e(t) + \frac{1}{T_N}\int_0^te(\tau)d\tau + T_v \frac{de(t)}{dt}$

---

### Umformung mit Vorhalt- und Nachstellzeit für PID-Regler:
- Neben der Darstellung mit Vorhalte- und  Nachhaltezeit findet sich auch häufig eine Darstellung mit Faktoren ($K$):
- $u(t)=K_P \cdot e(t) + \frac{1}{T_N}\int_0^te(\tau)d\tau + T_v \frac{de(t)}{dt}$

- $u(t)=K_P \cdot e(t) + K_I\int_0^te(\tau)d\tau + K_d \frac{de(t)}{dt}$

- $u(t)=K_P \cdot [e(t) + \frac{K_I}{K_P}\int_0^te(\tau)d\tau + \frac{K_D}{K_P} \frac{de(t)}{dt}]$


---

### Diskrete Implementierung als [Python-Klasse](https://colab.research.google.com/drive/1O8G7-Fn4ul-Wgq0B6-iOtqbzagVuC1Vz?usp=sharing)

```Python
class PIDRegler:
    def __init__(self, kp, ki, kd, dt):
        """
        Diskreter PID-Regler ohne Begrenzung
        :param kp: Proportionalbeiwert
        :param ki: Integralbeiwert
        :param kd: Differentialbeiwert
        :param dt: Abtastzeit
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt

        self.integral = 0
        self.last_error = 0

    def reset(self):
        """Setzt internen Zustand zurück."""
        self.integral = 0
        self.last_error = 0

    def update(self, setpoint, measurement):
        """
        Berechnet den PID-Reglerausgang
        :param setpoint: Sollwert
        :param measurement: Istwert
        :return: Steuersignal
        """
        error = setpoint - measurement

        # Integralanteil
        self.integral += error * self.dt

        # Differentialanteil
        derivative = (error - self.last_error) / self.dt

        # PID-Ausgabe
        output = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Fehler für nächsten Schritt speichern
        self.last_error = error

        return output
```

---

## Systeme ohne zeitliche Verzögerung

<center>

![h:400](images/ohneTrägheit.svg)

</center>

* alle Systeme reagieren unmittelbar auf Veränderungen der Eingänge
* z.B. wird die Lichtstärke der Lampe ($u_r$) erhöht, erhöht sich die Helligkeit im Raum ($y$)



---

## Systeme mit zeitlicher Verzögerung

<center>

![h:400](images/TraegeSysteme.svg)

</center>

* z.B. mit Erhöhung des Durchfluss durch die Heizung ($u_r$) erwärmt sich der Raum nur langsam ($y$). Das Thermometer gibt die gemessene Temperatur ($y_m$) nur mit Verzögerung weiter

---

### Bestimmung des dynamischen Verhaltens

<center>

![h:350](images/ReglerDynamisch.png)

</center>




* Ziel der Regelungstechnik ist es ein erwünschtes Verhalten 
der Regelgröße $y$ zu erhalten
* Mathematische Beschreibung und Analyse
* Simulationsprogramme: z.B. [Matlab Simulink](https://de.mathworks.com/solutions/control-systems.html) oder [Scilab Xcos](https://www.scilab.org/scilab/features)

[Quelle](https://www.samsongroup.com/document/l102de.pdf)


---


### Fazit

* Zeitverhalten von Regelkreisen wird durch alle Komponenten (Zeitverhalten) und die Einstellung des Reglers (gewählte Parameter) beeinflusst
* komplexere Regelkreise müssen als Gesamtheit betrachtet werden
  * Beobachtung am echten System
  * Modellierung durch Vereinfachung (Regelungstechnik)
  * Kalibrierung am realen System

---

## 🌡️ Aufgabe 1: Reaktion von PID und PT1 auf Einheitssprung

Ziehen Sie die Elemente `Step` und `PID`, `Trasfer Fcn` und `Scope` in den Arbeitsbereich und verbinden Sie diese sinnvoll.

- `Step`: Einheitssprung mit Amplitude 1 und Zeit 1
- `PID`: PID-Regler mit `P=1`, `I=0`, `D=0`
- `Transfer Fcn`: PT1-Glied mit Nummerator `[1]` und Denominator `[5, 1]`
- `Scope` mit zwei Eingängen

Passen die Parameter an und beobachten Sie die Reaktion des Systems.

---

### 🤓 Die Transferfunktion des PT1-Gliedes ist:

  $$
  G(s) = \frac{1}{5s + 1}.
  $$

Eine Transferfunktion ist eine mathematische Beschreibung eines Systems im Frequenzbereich. Für uns ist jetzt die Form wichtig, die wir in Simulink verwenden können. Die Übertragungsfunktion eines PT1-Gliedes ist:
$$
G(s) = \frac{1}{\tau s + 1} = \frac{\text{Ausgangsgröße im Frequenzbereich}}{\text{Eingangsgröße im Frequenzbereich}}
$$

wobei wir $\tau$ als Zeitkonstante bezeichnen. Diese Zeitkonstante beschreibt, wie schnell das System auf eine Änderung reagiert. In unserem Fall ist $\tau = 5$ Sekunden. Zu diesem Zeitpunkt hat das System 63% der Endantwort erreicht. Nach 5 Zeitkonstanten ($t=5\tau$) hat das System 99% der Endantwort erreicht.


---

## 🌡️ Aufgabe 2: Heizkurve einer Heizung (ohne Regelung)

<center>

![h:500](https://www.energiesparhaus.at/bilderupload2023/20231127846784.jpg)

</center>

---

### Situation

In einem ausgekühlten Gebäude wird die Raumtemperatur durch eine einfache **Heizkurve** gesteuert. Es gibt **keine Rückkopplung**, sondern nur eine fest definierte Beziehung zwischen der **Außentemperatur** und der **Vorlauftemperatur** der Heizung. Wir nehmen an dies passiert im Stellglied verzögert mittels PT1-Glied ($\tau=60 \text{ min}$). Die Vorlauftemperatur beeinflusst wiederum die **Raumtemperatur** in der Steuerstrecke, ebenfalls mit trägem Verhalten verzögert mittels PT1-Glied ($\tau=120 \text{ min}$ und eine proportionale Verstärkung von $0.35$).

---

### Die Zusammenhänge sind wie folgt:

Die [Heizkurve](https://de.wikipedia.org/wiki/Heizkurve) berechnet die Vorlauftemperatur $T_{\text{VL}}$ aus der Außentemperatur $T_{\text{außen}}$:

$$
T_{\text{VL}} = a \cdot (T_{\text{außen}}) + b
$$

mit:

- $a = -1{,}5$ (Steigung der Heizkurve)  
- $b = 60$ (Basisaufschlag)

Die **Raumtemperatur** $T_{\text{Raum}}$ reagiert auf die Vorlauftemperatur mit einem **PT1-Verhalten**: Für die Simulation im Matlab verwenden wir die Übertragungsfunktion:

$$
G(s) = \frac{1}{\tau s + 1}, \quad \tau = 120\ \text{min}
$$

---

### 🧩 Aufgabe 2a: Blockschaltbild zeichnen

Zeichnen Sie ein Blockschaltbild der Steuerkette mit folgenden Blöcken:

- Außentemperatur (Eingangsgröße)  
- Heizkurve (Stellglied)  
- Vorlauftemperatur (Stellgröße)  
- Raum (Steuerstrecke)  
- Raumtemperatur (zu steuernde Größe)  

> **Hinweis:** Es handelt sich um eine *Steuerung*, d. h. **keine Rückführung** der Raumtemperatur!

---

### 🛠️ Aufgabe 2b: Umsetzung in Simulink

Erstellen Sie in MATLAB Simulink ein Modell der oben beschriebenen Steuerstrecke:

- Außentemperatur als **Step-Block** mit einem Sprunghaften Abfall nach 1000 Minuten von 10 auf -5°C.  
- Heizkurve als **einfache Rechenvorschrift** (Gain- und Summierblöcke).  
- Die Stellglied und Raumdynamik als **Transfer Fcn** mit:  
  $$
  G(s) = \frac{1}{\tau s + 1}
  $$
- Der Raum mit einem zusätzlichen Gain-Glied von $0.35$ (Verstärkung).


---

### 🔍 Beobachtung

- Visualisieren Sie die Raumtemperatur, Vorlauftemperatur und Außentemperatur im **Scope**.
- Wie entwickelt sich die Raumtemperatur über der Zeit?  
- Was passiert, wenn die Außentemperatur plötzlich sinkt?  
- Wie gut funktioniert die Steuerung?


---

## 🔁 Aufgabe 3: Temperaturregelung eines Raumes mit P-Regler

### Situation

Der Raum soll nun auf eine gewünschte Temperatur geregelt werden. Die **Regelgröße** ist die **Raumtemperatur** $T(t)$, die durch das Heizsystem geregelt wird.
Das gesamte Heizsystem wird nun als $PID$-Regler abgebildet. An dessen Eingang wird der Unterschied zwischen **Soll- und Ist-Temperatur** erfasst. Die Raum verhält sich, wie bisher (PT1 + Gain). Wir können die Raumtemperatur exakt und unmittelbar messen. 


---

## 🧩 Aufgabe 2a: Blockschaltbild

Zeichnen Sie ein **Blockschaltbild** des Regelkreises. Die folgenden Elemente sollen enthalten sein:

- Soll-Temperatur (Führungsgröße)
- Temperatur-Differenz (Regelabweichung $e(t)$)
- Heizsystem (Regler)  
- Regelstrecke (Raum als PT1-Glied)
- Ist-Temperatur (Regelgröße)


---

## 🛠️ Aufgabe 2b: Umsetzung in Simulink

Erstellen Sie in **MATLAB Simulink** ein Modell des beschriebenen Regelkreises:

- Verwenden Sie einen **Step-Block** für die Solltemperatur (z. B. Sprung  von $15$ auf $20^\circ \text{C}$ bei $t = 300$ min).  
- Implementieren Sie den **PID-Regler** zunächt mit einem $K_p = 3$ und ohne I und D-Anteil.  
- Simulationsdauer: **1000 Sekunden**  
- Beobachten Sie die Entwicklung der Führungsgröße, Regelabweichung und Ist-Temperatur im **Scope**.

---

## 🔍 Beobachtungen

- Wird die Soll-Temperatur erreicht?
- Wie verändert sich die Regelung, wenn Sie $K_p$ erhöhen oder verkleinern?
- Passen Sie auch die Größen $T_n$ ($1/$ `I`) und $T_v$ (`D`) an.
- Was müsste man ändern, um die Regelabweichung vollständig zu eliminieren?
- Testen Sie die `Tune`-Funktion von Simulink. Was passiert?



---

## Regelverlauf der verschiedenen Reglertypen im Zeitverlauf

<center>

![](images/Reglervergleich.gif)

</center>

* Reaktion auf Sprungfunktion im einfachen Regelkreis
* Deutlich wird die bleibende Regelabweichung des P-Reglers
* Das schnelle Verhalten der Regler mit D-Anteil


[Quelle](https://rn-wissen.de/wiki/index.php/Regelungstechnik)


---

## Kriterien zur Beurteilung eines Regelkreises


* Führungsverhalten bei Anregung mit Sprungfunktion:
* **Ausregelzeit** $t_\epsilon$: gibt den Zeitpunkt an, ab dem die Regelabweichung kleiner als eine vorgegebene Schranke $±\epsilon$ ist.
* Maximale **Überschwingweite** $e_{max}$: gibt den Betrag der maximalen Regelabweichung an, die nach dem erstmaligen Erreichen des Sollwertes  auftritt

![bg height:350 right:33%](images/KriterienRegelkreis.png)

[Quelle](https://srv.ifr.ing.tu-bs.de/static/files/lehre/vorlesungen/gdr/Skript_GdR.pdf)




---

### Regelfläche

- **Regelfläche**: Die Fläche zwischen Führungsgröße und Ist-Wert kann als Maß definiert werden. 
* Besonders sinnvoll ist die Beurteilung mittels der Regelfläche allerdings nur, wenn kein Überschwingen auftritt
* Alternativ z.B. Absolutwert des Integrals der Regelfläche


![bg height:350 right:33%](images/Regelflache.png)

[Quelle](https://srv.ifr.ing.tu-bs.de/static/files/lehre/vorlesungen/gdr/Skript_GdR.pdf)

---

### Praktische Überlegungen

- Um eine gewünschtes Regelverhalten zu erreichen, muss ein geeigneter Regler mit den passenden Faktoren (z.B. Verstärkungsfaktor $K_P$) ausgewählt werden. 
- Hier lässt sich entweder ein **Modell der Regelstrecke** bilden. In der Praxis werden Regelkreise häufig durch **Ausprobieren** von Regler-Einstellungen eines PID-Regler kalibriert.

---


### 🤓 Praktische Überlegungen PID-Regler


![height:400 ](images/Xqt_Regler.png)

[Quelle](https://de.wikipedia.org/wiki/Faustformelverfahren_(Automatisierungstechnik))

---


## ✍️ Aufgabe 3_3_1: Auswahl Reglerverhalten

- Welchen Reglerverlauf wünschen Sie sich für folgende Anwendungen
  - **Startoptimierung** der Raumtemperatur 
(unter Energieffizienzgesichtspunkten)
  - **Konstantlichtregelung** 
(Beleuchtung aus Komfortgesichtspunkten)
  - **Bewegungssteuerung** eines Laufroboters

![bg height:200 right:30%](images/Xqt_Regler.png)

[Quelle](https://de.wikipedia.org/wiki/Faustformelverfahren_(Automatisierungstechnik))

---

### Lösung

- Welchen Reglerverlauf wünschen Sie sich für folgende Anwendungen
- **Startoptimierung** der Raumtemperatur 
(unter Energieffizinzgesichtspunkten)
  * Langsam kein Überschwingen
- **Konstantlichtregelung** 
(Beleuchtung aus Komfortgesichtspunkten)
  * Langsam kein Überschwingen
- **Bewegungssteuerung** eines Laufroboters
  * Schnell, minimales Überschwingen

![bg height:200 right:30%](images/Xqt_Regler.png)

[Quelle](https://de.wikipedia.org/wiki/Faustformelverfahren_(Automatisierungstechnik))


---

## Beispiele

### Hardware PID-Regler

![h:400](images/pid_regler_hardware.png)

[Quelle](https://www.reichelt.at/at/de/pid-regler-quantrol-lc100-5--55-c-quan-lc100-d-24-p147710.html?PROVID=2807)


---

### Software Baustein PID-Regler


![bg right h:600](images/5119077259__Web.gif)


* Eingänge
  * `rW`: Sollwert
  * `rX`: Istwert
* Eingangsparameter
  * `rKp`: Proportionalfaktor Verstärkung
  * `tTi`: Integrierzeit [s]
  * `tTv`: Vorhaltezeit [s]
* Ausgänge
  * `rY`: Stellgröße
  * `rXW`: Regelabweichung


[Quelle](https://infosys.beckhoff.com/index.php?content=../content/1031/tf8000_tc3_hvac/4685059723.html&id=)

---

## Methode von Ziegler und Nichols

- **heuristisches** Verfahren zur Bestimmung von Reglerparametern
- nur für existierenden **stabile Anlagen** geeignet
- oder bei denen instabiles Verhalten keine Schäden verursachen kann

---

  ![h:200](images/znschwing.gif)

* Eigenschaft Regelstrecke und P-Regler
* dynamischen Eigenschaften hängen stark vom Verstärkungsfaktor ($K_P$ - im Bild $K_R$) des Gesamtsystems ab.
* Ab bestimmtem $K_P^{krit}$ beginnt die Regelgröße zu schwingen (Stabilitätsgrenze)


[Quelle](http://www.chemgapedia.de/vsengine/vlu/vsc/de/ch/7/tc/regelung/grundlagen/regelung_grundlagen.vlu/Page/vsc/de/ch/7/tc/regelung/grundlagen/regparam/regparam.vscml.html)

---

### Umformung mit Vorhalt- und Nachstellzeit für PID-Regler:
- Neben der Darstellung mit Vorhalte- und  Nachhaltezeit findet sich auch häufig eine Darstellung mit Faktoren ($K$):
- $u(t)=K_P \cdot e(t) + \frac{1}{T_N}\int_0^te(\tau)d\tau + T_v \frac{de(t)}{dt}$

- $u(t)=K_P \cdot e(t) + K_I\int_0^te(\tau)d\tau + K_d \frac{de(t)}{dt}$

- $u(t)=K_P \cdot [e(t) + \frac{K_I}{K_P}\int_0^te(\tau)d\tau + \frac{K_D}{K_P} \frac{de(t)}{dt}]$





---


### Vorgehen Methode von Ziegler und Nichols (I)

- **Voreinstellung** des Reglers als reiner P-Regler: 
  - $K_I=0$, $K_D=0$ 
  - bzw. $T_v=0$, $T_n=∞$

- $u(t)=K_P \cdot e(t) + K_I\int_0^te(\tau)d\tau + K_D \frac{de(t)}{dt}$
- $u(t)=K_P \cdot [e(t) + \frac{1}{T_N}\int_0^te(\tau)d\tau + T_v \frac{de(t)}{dt}]$

![h:200](images/znschwing.gif)

---

### Methode von Ziegler und Nichols (II)

![h:150](images/znschwing.gif)
* **Erhöhung von $K_P$** (beginnend mit kleinen Werten von $K_P$ ) bis zur **Stabilitätsgrenze** (die Regelgröße $x$ beginnt gleichmaßig mit konstanter Amplitude zu schwingen)
* **Ablesen von $K_P^{krit}$**
Messung der beobachtbaren Periodendauer $T^{krit}$
* **Berechnung der Reglerparameter** ($K_P$, $T_n$, $T_v$) entsprechend den folgenden Regeln:


[Quelle](Ziegler, John G., and Nathaniel B. Nichols. "Optimum settings for automatic controllers." trans. ASME 64.11 (1942))

---

### Einstellregeln nach Ziegler und Nichols (III)

 | | $K_P$         | $T_n$                | $T_v$              |                
|------------|-------------------|-----------------|-----------------|
| P-Regler   | $K_P = K_P^{krit} \cdot 0,5$  |              |             |
| PI-Regler  | $K_P$=$K_P^{krit} \cdot 0,45$ | $T_n=0,85 \cdot T^{krit}$ |              |
| PID-Regler | $K_P$=$K_P^{krit} \cdot 0,6$  | $T_n=0,5 \cdot T^{krit}$  | $T_v=0,12 \cdot T^{krit}$ |





---

## ✍️ Aufgabe 3_3_2:

![](images/ReglerEinstellen.png)

- Finden Sie gtue Werte für den Regler für die folgenden Anwendungen nach der Methode von Ziegler und Nichols: [Colab](https://colab.research.google.com/drive/1NHJB1KzMxQen6Ehki6Cs0nEQDZiuFb8t?usp=sharing)

---

## 🤓 ✍️ Aufgabe 3_3_2:

- Finden Sie gtue Werte für den Regler für das folgende [System](https://github.com/jhumci/scilab_xcos_solutions/blob/main/Bussysteme/3_3_3/PT1-Glied.zcos) nach der Methode von Ziegler und Nichols

---

### ✔️ Lösung

<!-- _color: black -->

??? optional-class "💡 anzeigen"
    [Link](https://github.com/jhumci/scilab_xcos_solutions/blob/main/Bussysteme/3_3_3/PT1-Glied_Loesung.zcos)