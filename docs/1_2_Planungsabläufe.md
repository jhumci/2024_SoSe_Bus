---
marp: true
theme: beams
author: Julian Huber
size: 16:9
footer: Julian Huber - Bussysteme


---

<!-- paginate: true -->



# 1.2 Planungsabläufe



__Bussysteme__
Julian Huber & Michael Renzler

<!-- _class: title -->

---

## Orientierung – Einheit 2 von 14


### Wo sind wir?

| Abgeschlossen | **Heute** | Als nächstes |
|---|---|---|
| Einheit 1: Einführung GA | **Einheit 2: Planung & Funktionen** | Einheit 3: Messkette I (digital) |

### Was haben wir bisher gelernt?

* Ziele der GA; Ebenen- und Schalenmodell nach VDI 3813/3814
* EN 15232: Energieeffizienzklassen durch GA-Automatisierungsgrad

---

## Orientierung – Einheit 2 von 14

### Wo wollen wir hin?

Wie entsteht ein automatisiertes Gebäude aus der Idee bis zur Umsetzung? Wir erarbeiten Planungsphasen, erstellen ein **Raumautomations-Schema** und identifizieren Sensor-, Aktor- und Anwendungsfunktionen – die Bausteine aller späteren Kapitel.

---

## 🎯 Lernziele – Einheit 2

* Planungsphasen der GA (Lastenheft, Pflichtenheft) erklären
* Raumautomations-Schema (RA-Schema) lesen und erstellen
* Sensor-, Aktor- und Anwendungsfunktionen abgrenzen
* Funktionen Treppenlicht, Konstantlicht, Automatiklicht beschreiben
* RA-Schema für einen Beispielraum (Treppenlicht + Konstantlicht) erstellen

### Aufgaben dieser Einheit

| Aufgabe | Inhalt |
|---------|--------|
| ✍️ 1_2_1 | RA-Schema für Treppenlicht und Konstantlichtregelung erstellen |
| ✍️ 1_2_2 | Pflichtenheft für eine Raumautomation formulieren |

---


## Planungsabläufe für die Gebäudeautomation



![w:850](images/PlanungGebäudeautimatisierung.png)




[Hochschule Biberach - Nachhaltiges Planen, Bauen und Betreiben durch Einsatz von Gebäudeautomation]



---

## Grundlagenermittlung und Bedarfsplanung

* Zunächst wird z.B. während der Ausschreibungsphase ein **Lastenheft** erstellt, welches beschreibt **was** erreicht werden soll
* Häufig enthält dieses eine textuelle Beschreibung des gewünschten Endzustandes
* meist formuliert durch die Kund:in / Bauherr:in ggf. unterstützt durch einen Planungsbüro
* Je nach Projekt kann hier auch auf bestehende Normen verwiesen werden bzw. diese müssen berücksichtigt werden
  * z.B. Energieeffizienzklasse A nach [EN15232](https://assets.new.siemens.com/siemens/assets/api/uuid:ada002be-3fe1-4d03-8f8c-cafbd4ed6e96/auswahlhilfe-fur-energieeffizienz-funktionen-de.pdf)
  * d.h. Heizsystem mit Einzelraumre­gelung mit Kom­munikation und Bedarfsanforde­rung 

---

## Ansätze zur Dokumentation der Bedarfsplanung

### 🤓 Österreich

- Leistungsgruppen der standardisierten Bauausschreibung
- Komponenten-basiert. D.h. es werden Komponenten(typen) beschrieben, die in der Ausschreibung verwendet werden sollen und weniger auf die Erfüllung von Funktionen eingegangen

- Leistungsgruppen
  - [LG 84 - GA-System Raumautomation](http://docplayer.org/141267828-Leistungsgruppe-lg-84-ga-system-raumautomation-ra-kennung-ht-version-012-leistungsbeschreibung-haustechnik.html)
  - [LG 85 GA-System Anlagenautomation (AA)](https://www.bmaw.gv.at/dam/jcr:082b2d59-2a63-4aff-b6fa-53d9872ea4d7/LG85%20-%20GA-System%20Anlagenautomation%20(AA).pdf)
  - [LG 86 GA-Management (GA-M)](https://www.bmaw.gv.at/dam/jcr:b480f287-0f66-40c9-9f3e-1fe925deaa39/LG86%20-%20GA-Management%20(GA-M).pdf)

---

## Ansätze zur Dokumentation der Bedarfsplanung

### 🤓 Schweiz

* Stärkerer Fokus auf die Funktionen (z.B. durch Funktionstests)
*  KBOB [Empfehlung Gebäudetechnik](https://www.kbob.admin.ch/dam/kbob/de/dokumente/Publikationen/gebaeudetechnik/KBOB_Empfehlung_Geb%C3%A4udetechnik_Endfassung_2020_d.pdf.download.pdf/KBOB_Empfehlung_Geb%C3%A4udetechnik_Endfassung_2020_d.pdf) dient als Definition der Anforderung an die gebäude-technischen Installationen und Anlagen
---

## Vor- bis Genehmigungsplanung 

* Fachplaner nehmen eine formale Beschreibung der Funktionen vor
* Die konzipieren **wie** die Funktionen umgesetzt werden sollen (Pflichtenheft)
* Typisch für diese Phase ist die Erstellung von **Fließbildern** und **Schemata**
    * z.B. Stromlaufpläne, Pneumatikpläne, Hydraulikpläne, etc.
    * Raumautomations-Schema und Raumautomations-Funktionschema (VDI 3813)
    * Anlagenautomations-Schema und Anlagenautomations-Funktionschema (VDI 3814)


---



## Komponenten-Sicht durch Preplanning


![h:350](images/light-building-eplan-preplanning-02.jpg)




[Beispiel Preplanning mit Software von EPLAN](https://www.eplan.de/unternehmen/news/automatisiertes-engineering-in-der-gebaudeautomation/): Bereiche, Räume, Segmente, Funktionen, Sensoren und Aktoren werden in einem Fließbild dargestellt und miteinander verknüpft


---

## Funktions-Sicht durch Raumautomations-Schema (VDI 3813)


![h:320](images/RA-Schema.png)

Auch hier werden Segemente und Räume bereits am Anfang festgelegt (siehe Y-Achse). Zwar werden auch Komponenten zugeordnet (obere Hälfte), aber die Funktionen (untere Hälfte) stehen im Vordergrund. Es wird beschrieben, welche Funktionen in einem Raum/Segment benötigt werden und wie diese miteinander verknüpft sind. Die konkrete Umsetzung erfolgt erst später.

---

* Zuordnung von Sensoren, Aktoren und **Funktionen** zueinander (sie Verbindung von physisikalischem Präsenzmelder (Auge) zu einer Funktion "Präsenzerkennung" (Kasten links unten) 
* und zu Raum vs. Segment (keine genaue Räumliche Positionierung,aber Entscheidung: Müssen wir die Präsenzerkennung pro Segment oder pro Raum vornehmen?)
* Blockbausteine für Funktionen: Nutzen Attribute der Sensoren, um Attribute der Aktoren zu verändern

---



## Wiederholung Funktionen

Wiederverwendbare Bausteine:

```Python
def f(x):
    """this function's name is f. It takes a value x and returns a value y"""
    [...]
    y = 2*x
    return y

f(2) # Funktionsaufruf, führt die Funktion mit Argument aus und gibt Rückgabe aus
```

- __Eingaben__: z.B. `x` – Werte, die in die Funktion eingehen und sich abhängig vom Systemzustand ändern können
- __Parameter__: z.B. `2` – unveränderliche Werte, die einmalig konfiguriert werden (z.B. in Abhängigkeit der Raumgröße)
- __Ausgaben__: z.B. `y` – Werte welche von der Funktion abhängig von Parametern und Eingaben zurückgegeben werden


---

## Wiederholung Funktionen



* **Eingaben**: Werte, die in die Funktion eingehen und sich abhängig vom Systemzustand ändern können
* **Parameter**: unveränderliche Werte, die einmalig konfiguriert werden (z.B. in Abhängigkeit der Raumgröße)
* **Ausgaben**: Werte, welche von der Funktion abhängig von Parametern und Eingaben zurückgegeben werden
* Viele Funktionen stehen für viele Systeme standardisiert zur Verfügung (z.B. [Loxone](https://www.loxone.com/dede/produkte/loxone-config/), [Beckhoff](https://infosys.beckhoff.com/index.php?content=../content/1031/tf8040_tc3_buildingautomation/9281637003.html&id=1985937068038063516), etc.)
* oder können selbst implementiert werden

![bg right:20% h:400](images/Raumautomationschema_siemens.png)

Vorsicht, das stimmt nicht ganz mit der üblichen Benennung bei Programmiersprachen überein


---

## Raumautomatisierungs-Funktionen im Sinne der VDI 3813

![h:350](images/Raumautomationschema_siemens.png)

- Wiederverwendbare Bausteine, die in verschiedenen Räumen und Segmenten eingesetzt werden können
- Sie nutzen Attribute der Sensoren, um Attribute der Aktoren zu verändern
- Sie können auch andere Funktionen als Eingabe oder Ausgabe haben (z.B. Treppenlichtschaltung, siehe weiter unten)



---

##### Sensorfunktionen

![bg right:40% h:720](images/Helligektismessung.pdf.png)

> Ziel: **Erfassen** von Zuständen

- Präsenzerkennung,
- Fensterüberwachung, 
- Taupunktüberwachung,
- Lufttemperaturmessung,
- Helligkeitsmessung,
- Luftqualitätsmessung, 
- Windgeschwindigkeit,
- Niederschlag

[Quelle](VDI 3813)

---

##### Sensorfunktion am Beispiel der Helligkeitsmessung

![bg right:40% h:720](images/Helligektismessung.pdf.png)

- Eingang: meist Signal eines physischen Sensors, z.B. Helligkeitssensor (`H`)
- Ausgabe: z.B. `H_OUT` – ein Wert, der von der Funktion abhängig von der Sensorinformation zurückgegeben wird in definierter Form (z.B. Beleuchtungsstärke in Lux)
- Parameter: z.B. `PAR_CAL` – ein konfigurierter Parameter, z.B. Kalibrierungswert


---

##### Sensorfuktionen != Sensoren / Datenpunkte

* *"künstliche"* Trennung
* erhöht Flexibilität
* Ein Datenpunkt / Sensor
  * Lufttemperaturmessung
  * Luftqualitätsmessung
  * ggf. Taupunktüberwachung

![bg right](images/rfft_frontal_display.jpg)

[Quelle](https://www.sensorshop24.de/raumkombifuehler-fuer-temperatur-und-feuchte-0-10v-4-20ma)

---


##### Beispiel Verschattungkorrektur



![](images/11659900299__de__Web.jpg)




[Quelle](https://infosys.beckhoff.com/index.php?content=../content/1031/tcplclibhvac/11659363083.html&id=)

---

#### Aktorfunktionen

> Ziel: **Steuerung** von Komponenten

* binärer Schaltaktor
* Lichtaktor,
* Sonnenschutzaktor,
* Stellantriebsaktor 
  (z.B: Heizkörper)


![bg right:40% h:720](images/Lichtaktor.pdf.png)

---

#### Bedien-, Anzeige und Managementfunktionen

- Bedien- und Anzeigefunktionen (**lokal**)
  - Stellantriebsaktor, Sonnenschutzstellen, Antriebstellen, Temperatursollwertstellen, Raumnutzungsart wählen, Präsenzmelden
- **Managementfunktionen**
  - Aufzeichnung, Archivierung und statistische Analyse


![bg right:40% h:720](images/LichtStellen.pdf.png)

---

#### Anwendungsfunktionen 

> sind Programmabläufe die meist mehrere Aktoren und Sensoren miteinbeziehen

- **Raumklima**
    - Energieniveauwahl, Energieniveauwahl mit Startoptimierung,Sollwertermittlung, Funktionswahl, Temperaturregelung, Raum‐Zulufttemperatur‐Kaskade, Ventilatorsteuerung, Sequenzsteuerung, Stellwertbegrenzung, Luftqualitätsregelung, Nachtkühlung, Volumenstromregelung

---

#### Anwendungsfunktionen 


- **Beleuchtung**
  - Lichtschaltung, **Treppenlichtschaltung**, Automatiklicht, Tageslichtschaltung, Kostantlichtregelung, Dämmerungsschaltung 

- **Sonnenschutz**
  - Prioritätssteuerung, Dämmerungsautomatik, Sonnenautomatik, Lamellennachführung, Verschattungskorrektur, Thermoautomatik, Witterungsschutz

- **Übergreifend**
  - Belegungsauswertung, Steuerung über Raumnutzung, Zeitprogramm, Trennwandsteuerung, Thermoautomatik

---

#### Beispiel Treppenlichtschaltung

> Über die Funktion Treppenlichtschaltung können Beleuchtungseinrichtungen temporär eingeschaltet werden. Nach [...] Treppenlichthaltezeit kann eine Abschaltvorwarnzeit aktiv werden, die [...] z.B. durch [...] „Flackern“ über die [...] Abschaltung informiert. Ein erneutes [...] Einschalten startet die Verzögerungszeit neu. Die Funktion benötigt als Eingabeinformation das Ergebnis der Bedienfunktion Licht stellen und liefert ihrerseits die Ausgabeinformation für eine oder mehrere Aktorfunktionen Lichtaktor.

![bg right:40% h:720](images/Treppenlichtschaltung.pdf.png)





---

#### Ableitungen aus Vorplanung und Raumautomations-Schema

* Raumautomations-Schema zielt insbesondere auf die Implementierung, der gezielten Funktionalität (Funktionsbausteine werden auch in der Programmierung eingesetzt)
* Grafisches Werkzeug: Intuitive Prüfung auf Vollständigkeit möglich
* Entscheidung für Raum und Segment
  * z.b. ein vs. mehrere Bewegungsmelder pro Segment
* Für die Mengenplanung und Installationsplanung ist eine andere Darstellung hilfreicher


---

## ✍️ Aufgabe 1_2_1: Raumautomationsschema für ein Treppenhaus

- Befüllen Sie das vorliegende Raumautomations-Schema mit den entsprechenden Funktionen für die Beleuchtung eines Treppenhauses für eine Treppenlichtschaltung. Sie können das gesamte Treppenhaus über alle Stockwerke hinweg als einen Raum betrachten, oder aber die einzelnen Stockwerke als Segmente.
- Alle Leuchten werden über einen Aktor für das gesamte Treppenhaus zusammengefasst
- Das Treppenhaus verbindet zwei Stockwerke, auf jedem soll ein Bedienelement für die Beleuchtung angebracht werden
- Die Anwendungsfunktion Treppenlichtschaltung soll hierüber gesteuert werden können
- zusätzlich soll die Beleuchtung auch direkt aus der Gebäudeleittechnik für das Gesamte Treppenhaus gesteuert werden können

---



![h:600](images/RA_schemaCut.png)




---

### ✔️ Lösung

<!-- _color: black -->

??? optional-class "💡 anzeigen"
  ![h:580](images/RA_Loesung.png)


---



#### Weiteres Raumautomations-Schema (nicht Normgerecht)




![](images/Funktionsschema.svg)


---

## Planungsabläufe für die Gebäudeautomation



![w:850](images/PlanungGebäudeautimatisierung.png)

---

## Ausführung

* Entscheidung für Hardware und Software, um die Funktionen umzusetzen
* Erstellung von **Detailplänen** und **Dokumentationen**
* Installation der Hardware und Verkabelung
* Implementierung von Software
* Funktionstests


---

### Beispiel: Parametrisierung eines DALI-Systems

![h:600](images/DaliMasterConfig2.png)

---

### Beispiel: Programmierung eine SPS 

![height:600](images/tcRun.png)


---


### Auswahl der Komponenten und Bussysteme

* i.d.R. gibt es eine Vielzahl von möglichen Bussystemen, die für die Umsetzung der Funktionen in Frage kommen
* häufig werden mehrere Bussysteme kombiniert und müssen orchestriert werden
* neben den Kosten müssen auch Anforderungen an Erweiterbarkeit und Wartbarkeit berücksichtigt werden
* Erweiterbarkeit:
    * Wie einfach ist es, neue Komponenten hinzuzufügen?
    * Wie offen  ist das System für Veränderungen?
Wartbarkeit:
      * Sind Dienstleister oder Personal verfügbar, die das System warten können?    
      * Ist davon auszugehen, dass das System in 10 Jahren noch verfügbar ist?

---

## Betriebsphase

* Softwareupdates:
    * Wie können Softwareupdates eingespielt werden?
    * Over-the-Air vs manuell?
    * Wie werden die Updates getestet?
* Funktionstests:
    * Wie kann die Funktionalität überprüft werden?
    * Wie können Fehler identifiziert werden?

---


## Automatisierungspyramide vs. Cloud

![bg w:600 right:46%](images/HierarchischeGliederungderFunktionenderGebäudeautomation.png)

* Zunehmende Bedeutung von Cloud-Systemen
* Insbesondere die höheren Ebenen der Automatisierungspyramide werden zunehmend in die Cloud verlagert
* Einzelne Komponenten auf Prozess-Ebene (z.B. Präsenzmelder) können auch direkt mit der Cloud (Gebäudeleittechnik) kommunizieren, ohne über die Automationsebene zu gehen.


---

## Fazit

* Planungsphasen verlaufen von einer Zielbeschreibung (was? / Lastenheft) über die Konzeption (wie? /Pflichtenheft) bis zur Umsetzung (Detailplanung, Installation, Inbetriebnahme)
* Raumautomations-Schemata sind ein Werkzeug, um das Wie? zu beschreiben, insbesondere die Funktionen und deren Verknüpfung zueinander
* Funktionen sind wiederverwendbare Bausteine, die in verschiedenen Räumen und Segmenten eingesetzt werden können. Sie nutzen Attribute der Sensoren, um Attribute der Aktoren zu verändern

---

## Appendix: Ausgewählte Anwendungsfunktionen


### Funktionen für die Raumklimaregelung II

- **Startoptimierung**
Wird dem Raumtemperaturregler über ein Zeitprogramm zusätzlich zum gegenwärtigen **Energieniveau** auch das **nächste** und der zugehörige **Zeitpunkt** mitgeteilt, ist der Regler in der Lage, den optimalen Aufheizzeitpunkt des Raums anhand zusätzlicher Informationen, wie der Raum- und der Außentemperatur, so zu bestimmen, dass die gewünschte Raumtemperatur genau zu dem gewählten Zeitpunkt zur Verfügung steht (Erweiterung der Energieniveauwahl).

- **Fensterüberwachung**
Bei geöffneten Fenstern sorgt die Fensterüberwachung für eine automatische Umschaltung auf das **Energieniveau Gebäudeschutz** um Energieverschwendung zu vermeiden. Der Zustand der Fenster wird über entsprechende Kontakte eingelesen.

---

### Funktionen für die Raumklimaregelung III

- **Sollwertermittlung**
Abhängig vom Energieniveau muss ein **Raumtemperaturregler** in der Lage sein, die korrekte Sollwertvorgabe zu ermitteln. Zusätzlich kann der Sollwert bei hohen Außentemperaturen gleitend angehoben werden (**Sommerkompensation**), um zu große Unterschiede zur Raumtemperatur zu vermeiden.

- **Temperaturregelung**
Die **eigentliche Regelung der Raumtemperatur** durch Ermittlung der korrekten Stellantriebsstellung für Heizen oder Kühlen erfolgt durch die Funktion Temperaturregelung. In den meisten Fällen kommen **PI-Regler** zum Einsatz, die in der Lage sind, statische Regelabweichungen zu eliminieren.

---

### Funktionen für die Raumklimaregelung IV

- **Ventilatorsteuerung**
Luftgestützte Anlagen, z. B. Gebläsekonvektoren, verfügen über Ventilatoren zum Lufttransport. Die Luftmenge kann dabei meist mehrstufig an die erforderliche Heiz- oder Kühlleistung angepasst werden. Die **Wahl der geeigneten Ventilatorstufe** erfolgt anhand der Differenz der Ist- zur Soll-Raumlufttemperatur oder analog zu den Stellantrieben der Heiz- oder Kühlregister.

- **Luftqualitätsregelung**
Wird die Versorgung der Räume mit Frischluft über mechanische Systeme, wie Zentral- oder Fassadenlüftungsanlagen gewährleistet, wird die **Zuluftmenge** zur Einsparung elektrischer Energie für die Ventilatoren **an die Raumluftqualität angepasst**.

---

### Funktionen für die Raumklimaregelung IV



- **Nachtkühlung**
Kühle Nachtluft lässt sich zum Herunterkühlen der Raumluft nutzen, falls **Fenster oder Fassadenklappen motorisch geöffnet** werden können oder **Gebläsekonvektoren** mit Zuluftklappen vorhanden sind. Diese Funktion sollte mit Hilfe der gemessenen lokalen Raumtemperatur und der Außentemperatur raumindividuell ausgeführt werden, um eine optimale Absenkung zu erreichen.

- **Thermoautomatik**
Durch die Fenster eintretendes Sonnenlicht sorgt für einen Wärmeeintrag in den Raum, der je nach Raumtemperatur willkommen oder unwillkommen ist. Die Thermoautomatik übernimmt **in unbelegten Räumen** nun die Kontrolle über den **Sonnenschutz** zur Unterstützung von Heiz- oder Kühlvorgängen. So kann im Sommer eine Überhitzung vermieden und im Winter die Heizung durch solare Gewinne entlastet werden.


---

### Funktionen für Beleuchtung, Blendschutz und Tageslichtnutzung

- **Konstantlichtregelung**
Ein Sensor zur Erfassung der Raumhelligkeit, z. B. innerhalb eines Multisensors, sorgt für die exakte Anpassung des **Beleuchtungsniveaus** an die Arbeitsaufgabe. Hierfür erforderlich sind **dimmfähige** Aktoren (analoger Ausgang).

- **Tageslichtschaltung**
Der "kleine Bruder" der Konstantlichtregelung ist überall dort einsetzbar, wo die Beleuchtung **nur schaltbar** ausgeführt werden kann. Zur Erfassung der Helligkeit ist ebenfalls ein Sensor im Raum erforderlich. Unterschreitet das Tageslicht die erforderliche Raumhelligkeit, wird Kunstlicht automatisch in ein oder mehreren Stufen zugeschaltet und bei Zunahme des Tageslichtanteils wieder abgeschaltet (digitaler Ausgang).


---

### Funktionen für Beleuchtung etc. II


- **Automatiklicht**
In Räumen ohne ausreichende Tageslichtversorgung, z. B. in Fluren oder Sanitärräumen, lässt sich Energie sparen, indem die Beleuchtung nur temporär eingeschaltet wird. Die **Präsenzerkennung** liefert die hierfür erforderlichen Sensordaten. Eine einstellbare **Abschaltverzögerung** sorgt für Beleuchtungskomfort.


- **Sonnenautomatik**
**Außenliegende** Jalousien und bedingt auch Markisen sorgen vor allem für einen **Wärmeschutz** des Gebäudes. **Innenliegende** Jalousien, Vertikallamellen u. ä. sorgen vor allem für **Blendfreiheit** an Arbeitsplätzen. Die Sonnenautomatik sorgt nutzt Wetterdaten, damit der außenliegende Sonnenschutz eine einstellbare Position immer dann einnimmt, wenn eine bestimmte Strahlungsintensität überschritten wird. Der innen liegende Blendschutz ist i. d. R. nicht automatisiert, da das Blendungsempfinden individuell zu bewerten ist.

---

### Funktionen für Beleuchtung etc. III


- **Lamellennachführung**
Die Lamellennachführung ist eine **Weiterentwicklung der Sonnenautomatik**. Bei hoher Strahlungsintensität fährt der Sonnenschutz dazu in eine Stellung, die **zyklisch dem Sonnenstand** angepasst wird. So wird unter Aufrechterhaltung des Blendschutzes die Tageslichtversorgung maximiert. 


- **Verschattungskorrektur**
Umliegende Gebäude oder eigene Gebäudeteile sorgen auf den Fassaden für Schattenwurf, der die Blendschutzfunktion für die **im Schatten liegenden Jalousien zeitweise unnötig** macht. Die Jalousien sollten für eine bessere Tageslichtversorgung in dieser Zeit geöffnet sein. Die Verschattungskorrektur korrigiert dies in Verbindung mit der Sonnenautomatik oder der Lamellennachführung arbeitet. Die Funktion wird gelegentlich auch Jahresverschattungsdiagramm genannt.

---

### Funktionen für Beleuchtung etc. IV


- **Dämmerungsschaltung**
Außenbeleuchtung ist nur dann erforderlich, wenn es dunkel wird. Da der Zeitpunkt jahreszeitlich variiert, sorgt die Dämmerungsschaltung selbstständig für den optimalen Einschaltmoment. 

- **Witterungsschutz**
Witterungsschutzfunktionen vermeiden Schäden an der Sonnenschutzanlage. Sensoren für Temperatur, Niederschlag, Windgeschwindigkeit und -richtung stellen die erforderlichen Wetterdaten zur Verfügung, damit der Sonnenschutz rechtzeitig vor Beschädigungen eingezogen wird (ggf. auch für Fenster).
