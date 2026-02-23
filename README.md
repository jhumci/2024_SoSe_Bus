# Readme

## to run

`python -m mkdocs serve -a 127.0.0.1:7000`
`python -m mkdocs gh-deploy`

## Plugins

- Password https://pypi.org/project/mkdocs-encryptcontent-plugin/
- latex pymdownx.arithmatex, settings in docs\javascripts\mathjax.js
- pymdownx.superfences for identend code boxes

## Helpers

- Some [PS-Skripts](https://github.com/jhumci/image_mgmt) to copy pictures between lectures and remove pictures not used in any slide:

## Einleitung

Diese Lehrveranstaltung vermittelt die technischen Grundlagen moderner Gebäudeautomation – von der Idee der Automatisierung über das konkrete Messen, Steuern und Regeln bis hin zu den Bussystemen, die alle Komponenten im Gebäude miteinander verbinden.

Der Kurs richtet sich an Studierende der Ingenieurwissenschaften. Theoretische Konzepte werden konsequent am Praxisbeispiel erarbeitet: Als durchgängiger Anwendungsfall dienen reale Automatisierungsaufgaben wie **Treppenlichtschaltung** und **Konstantlichtregelung**, die schrittweise von der Handskizze bis zur lauffähigen Implementierung (Raspberry Pi Pico / SPS) entwickelt werden.

## Roter Faden

Die Vorlesung beantwortet sechs aufeinander aufbauende Leitfragen:

**1. Warum automatisieren wir Gebäude?**
Gebäudeautomation dient Komfort, Energieeffizienz und Betriebskostensenkung. Normen (VDI 3813/3814) strukturieren die Aufgaben in Feld-, Automations- und Managementebene. Bevor eine Zeile Code geschrieben wird, entsteht ein Raumautomations-Schema: Es zeigt, welche Sensoren, Aktoren und Funktionen ein Raum braucht – unabhängig von der späteren Hardware.

**2. Welche Funktionen stecken in einem automatisierten Gebäude?**
Sensorfunktionen erfassen Zustände (Helligkeit, Präsenz, Temperatur). Aktorfunktionen steuern Komponenten (Licht, Jalousie, Heizventil). Anwendungsfunktionen verknüpfen beides zu Verhalten (Treppenlicht, Automatiklicht, Konstantlichtregelung). Diese Trennung ist der Schlüssel zum Verständnis aller späteren Kapitel.

**3. Wie messen wir zuverlässig?**
Die Messkette – von der physikalischen Größe über Sensor, ADC bis zum Verarbeitungswert – bestimmt, was ein System überhaupt „weiß". Digitale und analoge Ein-/Ausgänge, Pull-Up/Pull-Down-Beschaltung, PWM und ADC-Auflösung sind die Bausteine. Lineare und nichtlineare Mapping-Funktionen übersetzen Rohwerte in physikalische Einheiten.

**4. Wie steuern wir – und wo stößt die Steuerung an Grenzen?**
Ablaufsteuerungen (endliche Automaten / FSM) bilden zeitliches Verhalten ab. Verknüpfungssteuerungen (Boolsche Logik) kombinieren Bedingungen. Objektorientierung strukturiert komplexe Systeme mit Sensor- und Aktor-Klassen. Sobald eine Steuerung auf Störungen nicht reagieren kann, brauchen wir Regelung.

**5. Wie regeln wir – und wie legen wir Regler aus?**
Das Blockschaltbild macht Signalflüsse sichtbar. Der geschlossene Regelkreis kompensiert Störungen automatisch. P-, PI- und PID-Regler haben unterschiedliche Stärken bei Schnelligkeit, Überschwingen und bleibender Regelabweichung. Methoden wie Ziegler-Nichols geben eine erste Parametrierung. Eine SPS bringt diese Konzepte in die industrielle Praxis – Aufbau und Hardware werden in der Vorlesung behandelt, die Programmierung im Labor vertieft.

**6. Wie kommunizieren Geräte – und welches Bussystem wähle ich?**
Bussysteme ersetzen aufwändige Punkt-zu-Punkt-Verkabelung. Auf Bitebene entscheiden Leitungscodes und Symbolrate, was über das Kabel gesendet wird. Buszugriffsverfahren (Master/Slave, CSMA) regeln, wer wann sendet. Übertragungssicherung (Parität, Hamming-Abstand, CRC) macht Kommunikation fehlertolerant. Mit diesem Fundament erarbeiten die Studierenden selbst reale GA-Systeme (KNX, BACnet, DALI, Modbus, EnOcean u. a.) und präsentieren Anwendungsfälle, Topologien und Auswahlkriterien im Plenum.

## Anwendungsfälle

- Treppenlicht
- Konstantlichtregelung

## Einheiten

| Einheit | Thema | Slide-Decks | Lernziele |
|---------|-------|-------------|-----------|
| 1 | **Einführung Gebäudeautomation** | 1_1_Gebäudeautomation | Ziele der GA; Raum-, Anlagen- und Management-Automation abgrenzen; Ebenenmodell (Feld/Automation/Management) nach VDI 3814; Schalenmodell (Segment/Raum/Bereich) nach VDI 3813 |
| 2 | **Planung & Funktionen der GA** | 1_2_Planungsabläufe | Planungsphasen (HOAI); Lastenheft vs. Pflichtenheft; Raumautomations-Schema lesen und erstellen; Sensor-, Aktor- und Anwendungsfunktionen (Treppenlicht, Konstantlicht, Automatiklicht) |
| 3 | **Messkette I – Digitale Signale & Hardware** | 2_1_Messkette (Teil 1) | EVA-Prinzip; digitale Ein-/Ausgänge; Pull-Up/Pull-Down; Raspberry Pi Pico in Betrieb nehmen; LED und Taster anschließen und ansteuern |
| 4 | **Messkette II – Analoge Signale & Mapping** | 2_1_Messkette (Teil 2) | ADC-Auflösung und Referenzspannung; PWM; analogen Helligkeitssensor anschließen; lineares und quadratisches Mapping von Rohwerten in physikalische Einheiten |
| 5 | **Steuerung I – Ablaufsteuerungen & FSM** | 2_2_Steuerung, 2_3_Funktionen | Geschichte der Automatisierung; endliche Automaten (Zustände, Übergänge, Ausgaben); zeitbedingte Übergänge; Treppenlichtschaltung als FSM implementieren; Funktionsgedanke (Eingaben/Parameter/Ausgaben) |
| 6 | **Steuerung II – Verknüpfungen & OOP** | 2_2_Steuerung (Verknüpfungen), 2_4_Objektorientierung | Boolsche Verknüpfungssteuerungen; OOP-Grundkonzepte (Klassen, Objekte, Attribute, Methoden); Sensor- und Aktor-Klassen; Komposition; JSON-Darstellung von Objekten |
| 7 | **Regelungstechnik I – Blockschaltbild & Zweipunktregelung** | 3_1_Blockschaltbild | Blockschaltbild-Elemente (P-, I-, D-Glied, Totzeitglied); Simulation mit Scilab xcos; offener Regelkreis (Steuerung); Zweipunktregelung mit Hysterese; Konstantlicht-Regelung als Einstieg |
| 8 | **Regelungstechnik II – Regelkreis & PID** | 3_2_Regelkreis | Geschlossener Regelkreis; Regelkreisbegriffe (Führungsgröße, Regelgröße, Stellgröße, Störgröße); P-, PI-, PID-Regler; Wirkung von Trägheit und Totzeit auf den Regelkreis |
| 9 | **Regelungstechnik III – Regelverhalten & Auslegung** | 3_3_Regelverhalten | Regelverlauf im Zeitbereich; Gütekriterien (Überschwingen, Ausregelzeit, bleibende Abweichung); Methode nach Ziegler-Nichols; Reglerauswahl für typische GA-Aufgaben (Temperatur, CO₂, Licht) |
| 10 | **SPS – Grundlagen & Hardware** | 4_1_Speicherprogrammierbare_Steuerung | Aufbau und Funktionsprinzip einer SPS (am Beispiel Beckhoff); Unterschied Mikrocontroller vs. SPS; EVA-Prinzip in der SPS; digitale und analoge I/Os; Zykluszeit und Programmstruktur; IEC 61131-3 Überblick (Programmierung im Labor) |
| 11 | **Bussysteme I – Signalisierung** | 5_1_Signalisierung | Unterschied SPS-Verdrahtung vs. Bussystem; Leitungscodes; Symbolrate vs. Bitrate; serielle/parallele Übertragung; differentiale Busse; Beispiel USB |
| 12 | **Bussysteme II – Zugriffsverfahren** | 5_2_Buszugriffsverfahren | Master/Slave-Verfahren (Polling), Worst-Case-Latenz; zufällige Zugriffsverfahren (CSMA); Anforderungen an Brandmelde- und GA-Systeme; Systemvergleich |
| 13 | **Bussysteme III – Übertragungssicherheit** | 5_3_Uebertragungssicherheit | Aufbau von Datenpaketen; Fehlerarten; Parität; Hamming-Abstand; Blocksicherung (CRC); Gütekriterien für Übertragungssicherheit |
| 14 | **Bussysteme IV – GA-Systeme: Rechercheaufgabe & Präsentationen** | 5_4_Bussysteme_in_der_Gebudeautomation | Studierende erarbeiten selbst je ein GA-Bussystem (DALI, KNX, BACnet, Modbus, EnOcean, LON, …) und präsentieren: Topologie, Übertragungsmedium, Zugriffsverfahren, typische Anwendungsfälle, Auswahlkriterien (Kosten, Offenheit, Erweiterbarkeit, Herstellerbindung) |
