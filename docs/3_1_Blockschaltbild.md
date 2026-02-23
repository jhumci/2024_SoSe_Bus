---
marp: true
author: Julian Huber
size: 16:9
footer: Julian Huber - Bussysteme

# Strg+[ ] for Options

theme: beams

---

<!-- paginate: true -->


# 3.1 Blockschaltbild

<!-- _class: title -->




---

## Orientierung – Einheit 7 von 14

<!-- _class: white -->

### Wo sind wir?

| Abgeschlossen | **Heute** | Als nächstes |
|---|---|---|
| Einheit 6: Steuerung II | **Einheit 7: Regelungstechnik I** | Einheit 8: Regelungstechnik II |

### Was haben wir bisher gelernt?

* Ablauf- und Verknüpfungssteuerungen (FSM, Boolesche Logik)
* OOP: Sensor- und Aktorklassen, JSON-Serialisierung
* Tageslichtschaltung implementiert – aber: was tun bei Störungen?

### Wo wollen wir hin?

Eine Steuerung reagiert nicht auf Störungen – dafür brauchen wir Regelung. Heute lernen wir, Signalflüsse mit **Blockschaltbildern** darzustellen. Wir modellieren den offenen Regelkreis und implementieren eine erste **Zweipunktregelung** für die Konstantlichtregelung.

---

## Lernziele – Einheit 7

* Blockschaltbild-Elemente (P-, I-, D-Glied, Totzeitglied) erklären
* Tageslichtschaltung als Blockschaltbild darstellen
* Offenen Regelkreis (Steuerkette) von geschlossenem Regelkreis abgrenzen
* Zweipunktregelung mit Hysterese beschreiben und implementieren
* Simulationsparameter (Verstärkung, Zeitkonstante) identifizieren

### Aufgaben dieser Einheit

| Aufgabe | Inhalt |
|---------|--------|
| ✍️ 3_0 | Tageslichtschaltung in Blockschaltbild übersetzen (Papier) |
| ✍️ 3_1_1 | Zweipunktregelung: Blöcke und Parameter identifizieren |
| ✍️ 3_1_2 | Zweipunktregelung simulieren |
| ✍️ 3_1_3 | Zweipunktregelung für Tageslichtschaltung |

---


## Blockschaltbild



![h:300](images/Blockschaltbild1.png)



* Grafische Beschreibung von Systemen in der Regelungs- und Steuerungstechnik
* Systeme werden durch Blöcke dargestellt, die durch Pfeile verbunden sind
  * z.B. Steuerungsfunktion (z.B. in Python)
  * z.B. thermodynamisches Modell eines Raums

---

* I.d.R. beschäftigen wir uns mit **dynamischen Systemen**
    * Die Ausgangsgröße hängt nicht nur  von den Eingangsgrößen ab (vgl. _Funktion_) 
    * sondern auch vom Systemzustand und damit inneren Zustandsgrößen (vgl. _Objekt_)


[Quelle](Lunze )

---

### 🤓 Dynamische Systeme

* lineare Systeme: Systemfunktion ist eine lineare Funktion
* nichtlineare Systeme: Systemfunktion ist eine nichtlineare Funktion
* zeitinvariante Systeme: Systemfunktion ist unabhängig von der Zeit
* zeitvariante Systeme: Systemfunktion ist abhängig von der Zeit

---


## Elemente eines Blockschaltbildes


![bg left:45% w:600](images/Blockschaltbild2.png)

* Übertragungsglieder beschreiben Systeme mit deren Eigenschaften / Funktionen
* Pfeile die Ein- und Ausgangsgrößen
* Komplexe Systeme können durch mehrere Systeme zusammengesetzt werden
* Systeme werden im Zeitbereich durch ihre Funktionsbeziehung zwischen Ausgang $y$ und Eingang $u$ unterschieden $f(u)=y$


---

### Proportionalglied (P-Glied)

* Linear und zeitinvariant
* Beschreibt Systeme mit direktem proportionaler Systemfunktion $f$ für den Zusammenhang zwischen Eingang ($u$) und Ausgang ($y$)
  * $y = f(u)=K_p \cdot u$
  * $K_p$ ... Proportionalitätsfaktor

![bg right:33% w:400](images/P-controller-symbol-1.svg)

---

#### Wirkweise eines P-Glieds

* $y = f(u)=K_p \cdot u$
* Beispiel: 
  * je höher die $\text{CO}_2$ Konzentration in einem Raum, desto schneller dreht sich ein Ventilator in einer Lüftungsanlage
  * $y$ ... Drehfrequenz der Ventilators in $\text{Hz}$
  * $u$ ... $\text{CO}_2$ Konzentration in $\text{ppm}$
  * $K_p$ ... Proportionalitätsfaktor in $\frac{\text{Hz}}{\text{ppm}}$



![bg right:37% h:400](images/p-glied-verhalten.svg)

---

![bg left h:500](images/p-zusammenhang.svg)

* Unabhängig vom Verlauf der Eingangsgröße $u(t)$ ist der Wert der Ausgangsgröße $y(t)$ immer proportional

---

#### 🧠 Einheits-Sprungfunktion

* Eine Funktion, die am Zeitpunkt $t=0$ von $u=0$ auf $u=1$ springt und sonst konstant bleibt
* beliebtes Werkzeug in die Regelungstechnik: Wie reagiert ein System, wenn wir eine Sprungfunktion an den Eingang legen (auch in der E-Technik!)

![bg right h:300](images/Sprungfunktion.svg)

---

#### 🧠 Sprungantwort (Reaktion) eines P-Glieds auf eine Sprungfunktion

![h:500](images/P-Glied-Reaktion_Sprungfunktion.svg)


---

<!-- _class: white-->



![](images/P-controller-symbol-1.svg)



* Das Symbol repräsentiert die Sprungantwort
* weitere Beispiele:
  * Entwicklung Spannungsabfall am Ohmschen Widerstand 
  beim Anlegen einer Quellenspannung
  * Antwort eines Helligkeitssensors auf Lichteinfall

[Quelle](Lunze )


---

### Totzeitglied (T-Glied)

* beschreibt die zeitliche Verzögerung, bis ein System auf das Eingangssignal (z.B. der Sprungfunktion) reagiert. 
* Nicht die Trägheit des Systems sondern eine Leerlaufzeit $T_t$. 

![bg right w:400](images/Totzeit-controller-symbol-1.svg.png)

---

![](images/VerzoegerterSprung.svg)

---

#### 🧠 Sprungantwort eines T-Glieds auf eine Sprungfunktion

![h:500](images/totzeitglied.svg)


---

## Simulation von Blockschaltbildern

Blockschaltbilder lassen sich mit grafischen Simulationswerkzeugen direkt simulieren (z.B. Scilab xcos, Matlab Simulink, Python/scipy). In den folgenden Aufgaben wird beschrieben, **welche Bausteine** verbunden werden sollen – das konkrete Werkzeug wählen Sie oder wird in der Vorlesung festgelegt.

---

## ✍️ Aufgabe 3_0: Tageslichtschaltung als Blockschaltbild (Papier)

> Bevor wir simulieren: Übersetzen Sie den Code, den Sie in Kapitel 2 geschrieben haben, in die Sprache der Blockschaltbilder.

**Aufgabe (kein Werkzeug nötig):**

Skizzieren Sie auf Papier das Blockschaltbild der Tageslichtschaltung aus Aufgabe 2_3_1. Beantworten Sie dabei:

1. Welche Python-Variable entspricht der **Führungsgröße** (gewünschter Sollwert)?
2. Welche Variable ist die **Messgröße** (tatsächlich gemessener Wert)?
3. Was ist das **Stellglied** – und welches Python-Objekt setzt es um?
4. Was ist die **Steuerstrecke** – also das System, das durch die Stellgröße beeinflusst wird?
5. Gibt es **Störgrößen**? Wenn ja: Welche?

---

### ✔️ Lösung

<!-- _color: black -->

??? optional-class "💡 anzeigen"
    - Führungsgröße: `PAR_SETPT` (Helligkeitssollwert in Lux)
    - Messgröße: `h_room` (gemessene Raumhelligkeit über LDR + ADC)
    - Stellglied: LED-Aktor (Python: `led.value`), gesteuert durch `l_set()`
    - Steuerstrecke: die Raumhelligkeit als physikalisches System (Licht verteilt sich im Raum)
    - Störgrößen: Tageslichteinfall von außen, andere Lichtquellen im Raum

---

## ✍️ Aufgabe 3_1_0: Proportional mit Totzeitglied

**Zu modellieren:**

- Eingangsquelle: Sprungfunktion (Amplitude 1, Sprungzeitpunkt $t=1\,\text{s}$)
- Glied 1: Proportionalglied (Verstärkung $K_P = 2$)
- Glied 2: Totzeitglied (Totzeit $T_t = 3\,\text{s}$)
- Ausgang: Zeitverlauf-Plot (Eingang und Ausgang überlagert)

**Aufgaben:**
- Beobachten Sie den Zeitverlauf am Ausgang
- Variieren Sie $K_P$ (z.B. 0,5 / 2 / 5) und $T_t$ (z.B. 1 s / 3 s / 8 s) – was verändert sich am Ausgangssignal?

![h:300](images/xcos_start.webp)


---

### Proportionalglied mit Verzögerung 1. Ordnung (PT1-Glied)

* beschreibt Trägheit im System oder eine Dämpfung 
* nähert sich über die Zeit einer waagrechten Linie an
  * z.B. Spannung am Kondensator
  * z.B. Temperatur im Raum nach dem Einschalten einer Fußbodenheizung
  * Beschränktes Wachstum


![bg right:40% w:400](images/Pt1-controller-symbol-1.svg.png)


---

- Es gibt noch viele weitere typische Glieder 
- Mehr dazu beim Thema stetige Regler
- aus diesen lassen sich komplexe Modelle zusammenstellen lassen 
(z.B. als Blockschaltbild)

---

## Blockschaltbild einer Steuerung

![](images/SteuerungBlock.png)


* Die **Führungsgröße** ist die Größe, welche das Verhalten der Stellglieds bestimmt ($\rightarrow$ z.B. die aktuelle Beleuchtungsstärke gemessen am Lichtsensor  im Freien)
* Durch das Stellen eines **Stellglieds** (oder Stelleinrichtung bzw. Aktor) wird die Steuerstrecke beeinflusst ($\rightarrow$ Mikrocotroller steuert Spannung an LED an oder aus basierend auf einen Schwellenwert)



[Quelle](https://upload.wikimedia.org/wikipedia/commons/6/64/R_S_Block.svg)

---

## 🧠 Steuerung

![](images/SteuerungBlock.png)

* **Stellgröße** ist die Ausgangsgröße des Stellglieds ($\rightarrow$ Spannung an der LED)
* **Steuerstrecke** ist das System, das durch die Stellgröße und Störgrößen beeinflusst wird ($\rightarrow$ Helligkeit im Raum)
* Auf die Steuerstrecke wirken neben der Stellgröße aus **Störgrößen** 
($\rightarrow$ Lichteinfall von Außen, weitere nicht gesteuerte Lichtquellen im Raum)



[Quelle](https://upload.wikimedia.org/wikipedia/commons/6/64/R_S_Block.svg)


---

### Stellglied

* ist nun kein standardisiertes Glied,
 sondern hat eine spezielle Funktion die sich aus Hard- und Software ergibt
* diese beinhaltet Steuerungslogik
* und physikalische Umsetzung
* zeitliche Reaktion meist nicht unmittelbar, sondern verzögert 
(z.B. Rechenzeit als Totzeit)

```Python
def l_set(p_act, h_room, PAR_SETPT, l_man):
    return (p_act and h_room<PAR_SETPT) or l_man
```

---

### Steuerstrecke

* beschreibt die echte Welt
* häufig in vereinfachten Modellen
* zeitliche Reaktion meist nicht unmittelbar (z.B. PT1-Glied)

```Python
def beleuchtungsstraerke_raum_lux(lichtabgabe_led, lichteinfall_aussen, wand_farbe):
  # Größe des Raumes
  # Größe der Fenster
  # Reflexion der Wände
  <...>
  return beleuchtungsstraerke_raum_lux
```

```Python
def raumtemperatur(heizleistung_in_w, aussen_temp_in_c):
  # Temperatur im Zeitpunkt zuvor
  # Trägheit der Temperaturänderung
  # Größe des Raumes
  # Isolation der Raumes
  <...>
  return raum_temp_in_c
```



---

## ✍️ Aufgabe 3_1_1: Wassertank ohne Steuerung

**Szenario:** Ein 100 l fassender Wassertank ist zu Beginn mit 10 l gefüllt. Es fließen konstant 5 l/min hinein.

**Zu modellieren:**

- Konstante Quelle: Zufluss $5\,\text{l/min}$ (konstanter Block)
- Integrationsglied: integriert den Zufluss über die Zeit → ergibt den Füllstand in Liter (Anfangswert = 10 l)
- Ausgang: Zeitverlauf-Plot des Füllstands

![h:300](images/xcos_simple.png)

**Fragen:**
- Nach wie vielen Minuten ist der Tank voll?
- Was passiert, wenn der Zufluss auf 2 l/min sinkt?

---

### ✔️ Lösung

<!-- _color: black -->

??? optional-class "💡 anzeigen"
    Der Füllstand wächst linear: $V(t) = 10 + 5t$. Nach $t = 18\,\text{min}$ ist der Tank voll.

---

## ✍️ Aufgabe 3_1_2: Einfache Tageslichtschaltung

> Hier übersetzen wir die Tageslichtschaltung aus Aufgabe 2_3_1 erstmals in ein Blockschaltbild.

**Zu modellieren:**

- Eingangsquelle: Zeitverlauf der Außenhelligkeit (z.B. Sinuskurve: tagsüber 500 Lux, nachts 0 Lux, Periode 24 h)
- Schwellwertglied (Schalter): gibt `1` aus wenn Helligkeit < 220 Lux, sonst `0`
- Ausgang: Zeitverlauf-Plot (Helligkeit und LED-Zustand überlagert)

![h:300](images/Tageslichtschaltung_xcos_.png)

**Fragen:**
- Überprüfen Sie: Geht die LED bei Unterschreitung von 220 Lux an oder aus?
- Welchen Wert müsste der Schwellwert haben, damit die LED bei Raumlicht (300 Lux) gerade noch brennt?

---

### ✔️ Lösung

<!-- _color: black -->

??? optional-class "💡 anzeigen"
    Der Schalter muss so konfiguriert sein, dass er bei Werten **unterhalb** des Schwellwerts `1` ausgibt (LED an). Der Schwellwert ist auf 220 Lux einzustellen.

---




## Zwei-Punkt Regelung

- Vorteile
  - einfach zu verstehen
  - und zu implementieren

```Python
regelabweichung = soll_lux - ist_lux 

zweipunkt_regler(regelabweichung):
  if regelabweichung > 0:
    licht = True
  else:
    licht = False
  return licht
```

[Quelle](Vorsicht: Wir greifen hier zum Thema Regelung vor, setzen den Regler aber in einer Steuerung ohne Regelkreis ein!)

---


### Probleme Zwei-Punkt Regelung

* Nachteile bei zeitlich wenig trägen Systemen
  * Regler schaltet ständig zwischen den Ausgangswerten
  * kritisch insbesondere bei mechanische Belastung
  * z.B. Motor wird ständig an und aus geschaltet

---


## Hysterese

- bewirkt eine Schalttoleranz ober- und unterhalb des Sollwerts

![h:500](images/zweipunkt_hysterese.svg)


---

```Python
def zweipunkt_hysterese(ist_lux, on_level, off_level, letzter_zustand):
    if ist_lux > off_level:
      licht = False
    elif ist_lux < on_level:
      licht = True
    else:
      licht = letzter_zustand

    return licht
```

```Python
class zweipunkt_hysterese():

    def __init__(self, on_level, off_level):
        self.on_level = on_level
        self.off_level = off_level
        self.letzter_zustand = False

    def calc_output(self, ist_lux):
        if ist_lux > self.off_level:
            self.letzter_zustand = False
        elif ist_lux < self.on_level:
            self.letzter_zustand = True
        return self.letzter_zustand

```


![bg right w:500](images/Zweipunktkennlinie_mit_hysterese.png)

[Quelle](https://www.wikiwand.com/de/Methode_der_harmonischen_Balance#Media/Datei:Zweipunktkennlinie.png)


---

![](images/ohne_hysterese.gif)

[Quelle](https://www.youtube.com/watch?v=nC5ZPEPtH9w)

---

### Drei-Punkt Regelung

* vermeidet ständiges Umschalten
* sinnvoll bei Neutralstellung z.B. Motoren

  ```Python
  drei_punk_regler(abstand):
    if abstand > 6:
      fahre = "vorwärts"
    elif abstand < 4:
      fahre = "rückwärts"
    else:
      fahre = "nicht"
    return fahre

  bewegung = drei_punk_regler(abstand)
  ```

![bg right:33% w:400](images/Dreipunktkennlinie.png)



---

## ✍️ Aufgabe 3_1_3: Zweipunktregelung für Tageslichtschaltung

> Erweitern Sie das Modell aus 3_1_2 um eine Hysterese, um das ständige Schalten bei Helligkeitswerten nahe am Schwellwert zu vermeiden.

**Zu modellieren:**

- Eingangsquelle: gleicher Helligkeitsverlauf wie in 3_1_2
- Schwellwertglied **mit Hysterese**: LED geht bei Helligkeit < **200 Lux** an, geht bei Helligkeit > **250 Lux** aus (Schaltband = 50 Lux)
- Ausgang: Zeitverlauf-Plot (Helligkeit + LED-Zustand)

![h:250](images/TagesLichtHystere.png)

**Fragen:**
- Vergleichen Sie den Schaltverlauf mit 3_1_2: Wie oft schaltet die LED?
- Was passiert, wenn das Schaltband (Hysterese) sehr groß (z.B. 300 Lux) oder sehr klein (z.B. 5 Lux) gewählt wird?

---

### ✔️ Lösung

<!-- _color: black -->

??? optional-class "💡 anzeigen"
    Mit Hysterese schaltet die LED deutlich seltener. Ein zu großes Schaltband führt zu langen Phasen mit falscher Beleuchtung; ein zu kleines Schaltband verhält sich fast wie ohne Hysterese (häufiges Flattern).