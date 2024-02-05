---
marp: true
author: Julian Huber
size: 16:9
footer: Julian Huber - Bussysteme

# Strg+[ ] for Options

class: invert

theme: lemon

---

<!-- paginate: true -->


# 3.2 Regelkreise


---

## Beispiel Konstantlicht-Regelung

> regelt die Raumbeleuchtung oder Teile davon bei Belegung automatisch so, dass eine eingestellte Mindestbeleuchtungsstärke nicht unterschritten wird

* Im Gegensatz zur Tageslichtschaltung, soll es aber auch nicht unnötig hell sein, wenn es draußen schon hell ist

![bg right:35% h:720](images/RA_Konstantlicht.pdf.png)

---

### Konstantlichtregelung

* Lichtstärke kann (quasi) stetig gesteuert werden (z.B. über Dimmer oder Pulsweitenmodulation)

![](images/Helligkeitsregelung.svg)


---

## ✍️ Aufgabe 3_2_1: Konstantlicht-Regelung

* Laden Sie die Datei [Konstantlicht_nur_p.zcos]() und passen Sie den P-Parameter in `PID`-Baustein an und beobachten Sie die Reaktion des Systems
* Welche Komponenten werden durch welche Bausteine dargestellt?

![](images/Konstantlichtregelung_nur_p.png)

---

## Proportional-Regler

* Reaktion der Stellgröße bzw. Steuerungsgröße 
$u(t)=K_P \cdot e(t)$
* multipliziert die Regelabweichung $e_t$ mit dem Verstärkungsfaktor $K_P$ und gibt das Ergebnis aus
* je dunkler $y_m$ im Verhältnis zur Führungsgröße ($w$), desto heller die Beleuchtung ($u$)


![bg right w:600](images/Helligkeitsregelung.svg)

---

* Reaktion der Stellgröße:
* $
  u(t)=K_P \cdot e(t)$

```Python
def p-regler(e, k_p):
  ausgang = e * k_p
  return ausgang
```


![bg right:60% height:600](images/P-Regler-Funktionen.svg)



---

## ✍️ Aufgabe 3_2_2: Regelung der CO2-Konzentration

- Ziel ist der Entwurf eines Reglers zur Steuerung einer Belüftungsanlage auf Basis der Schadstoffkonzentration im Raum in ppm 
- Zeichnen Sie den Verlauf der Stellgrößen (Drehzahl der Anlage) für folgende zwei Regler:
  - stetiger Proportionalregler: $u(t) = \frac{2}{min \cdot ppm} e(t)$ 
  - Regelung nach Logik nächste Seite.

---

### Lösung

![bg right:66% height:600](images/AufgabeRegler.svg)

---

### Lösung



```Python
def regler (e, letzte_drehzahl):
  if e ==1000:
    drehzahl = letzte_drehzahl
  else:
    if e > 1000:
      drehzahl = e
    else:
      drehzahl = 0
  return drehzahl
    
```


---

### Zusammenfassung P-Regler

![bg right w:500](images/Idealer_P_Sprungantwort.svg)

* P-Glied, welches als Regler eingesetzt wird
* Zeitverhalten: reagiert **unverzögert** 
* bleibende Regelabweichung bei Systemen mit Ausgleich (Regelstrecken die bei konstantem Eingang einen konstanten Wert anstreben)

---

## ✍️ Aufgabe 3_2_3: Wassertank mit PID-Regler

Entfernen Sie den I und D-Anteil des PID-Reglers und beobachten Sie die Reaktion des Systems

![](images/PID_internal.zcos.png)

[](https://help.scilab.org/PID)

---

## 🧠 Integral-Regler

![bg right w:500](images/Idealer_I_Sprungantwort.svg)

* Antwort $u(t)$ auf Sprung unmittelbar, jedoch nicht sofort mit voller Stärke
* Je länger ($t$) die Regelabweichung besteht und umso größer sie ist, desto stärker die Antwort
* $u(t)=\frac{1}{T_n}\int_0^te(\tau)d\tau$

###### Abbildung rechts ist Reaktion auf Sprungfunktion 

---

![bg right w:500](images/Idealer_I_Sprungantwort.svg)

* $u(t)=\frac{1}{T_n}\int_0^te(\tau)d\tau$
* $u(t)=K_I \cdot \int_0^te(\tau)d\tau$
* $T_n$ ... Nachstellzeit bestimmt den Gradienten des Anstieges von $u$ 
* *summiert* die Regelabweichung über die Zeit auf
* **Regelabweichungen** werden auch bei Strecken mit Ausgleich vollständig **eliminiert**, dafür **langsamer**

---


![height:600](images/i-Regler.svg)

---

## Proportional-Integral-Regler


![](images/Idealer_PI_Sprungantwort.svg)

* Sprungantwort: $u(t)=K_Pe(t) + K_I \cdot \int_0^te(\tau)d\tau$
* PI-Regler **Kombination** aus P- und I-Regler
* schnelle Reaktion (wie P-Regler)
* exakte Ausregelung ohne eine bleibende Regelabweichung (wie I-Regler) 

---

## 🧠 Proportional-Differenzial-Regler

![](images/Idealer_PD_Sprungantwort.svg)

* Sprungantwort: $u(t)=K_Pe(t)+K_d \frac{de(t)}{dt}=K_Pe(t)+T_v \frac{de(t)}{dt}$
* kombiniert P-Regler mit Differenzial-Anteil
* der D-Anteil bewertet die Änderung einer Regelabweichung (differenziert) und berechnet so deren **Änderungsgeschwindigkeit**
* reagiert schon auf "Ankündigungen" von Veränderungen 
* **sehr schnell**, doch bleibende **Regelabweichung**
* Unruhe im Regelkreis wird verstärkt, wenn Sensorsignal verrauscht 


---


![height:600](images/d-regler.svg)


---

## ✍️ Aufgabe 3_2_4: Reaktion D-Regler

✍️ Wie sieht die Reaktion aus?

![height:600](images/d-regler-Aufgabe.svg)


