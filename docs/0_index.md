---

marp: true
theme: beams
author: Julian Huber
size: 16:9
footer: Julian Huber - Bussysteme


---

<!-- paginate: true -->



# Bussysteme in der Gebäudeautomation

<!-- _class: title -->

Julian Huber & Michael Renzler

---

## Warum Gebäudeautomation?



> Ein modernes Gebäude ist kein passives Objekt – es misst, entscheidet, regelt, kommuniziert.

* ca. **40 %** des Energieverbrauchs in Europa entfallen auf Gebäude
* GA-Systeme senken diesen Anteil [beispielsweise](https://www.dabonline.de/bautechnik/energieeffizienz-foerderung-gebaeudeautomation-pflicht-beg-smart-home/) um **bis zu 30 %** (EN 15232)
* Gleichzeitig steigen Komfort und Betriebssicherheit

---

## Was steckt dahinter?

> Ein Gebäude ist ist auch ein System aus Systemem (Leuchten, Wärmepumpe, Jalousien, Lüftungsanlagen, Menschen die es nutzen und betreiben). Wir werden und auch mit der Automatisierung dieser Systeme beschäftigen.

- Die hier vermittelten Konzepte und Methoden sind nicht auf die Gebäudeautomation beschränkt, sondern gelten für die Automatisierung von Systemen allgemein.
- Die Messprinzipien und Auswertung der Daten werden Sie im kommenden Semester in der Vorlesung  __Intelligente Messtechnik und Sensorik__ vertiefen.
- In den Vertiefungen zu __Heizungs-, Lüftungs- und Klimatechnik (HLK)__ werden Sie die Automatisierung von Gebäuden aus der Perspektive der Anlagentechnik betrachten und auf die hier vermittelten Konzepte zurückgreifen.





---

## Was Sie in dieser Vorlesung erwartet

<!-- _class: white -->

* **14 Einheiten** – von der Idee der Automatisierung einzelner Komponenten bis zur Kommunikation zwischen Geräten
* **Durchgängiges Beispiel:** _Treppenlichtschaltung_ und _Konstantlichtregelung_ – von der Handskizze bis zur lauffähigen Implementierung
* **Praxis von Anfang an:** Ab Einheit 3 programmieren Sie einen echten Mikrocontroller (Raspberry Pi Pico)
* **Eigenverantwortliches Arbeiten:** Sie sind aufgefordert den Raspberry Pi Pico in und nach der Vorlesung weiter zu erforschen, zu programmieren und zu verstehen. In Einheit 14 recherchieren und präsentieren Sie selbst ein reales GA-Bussystem

---

## Der Rote Faden

<!-- _class: white -->

Die Vorlesung beantwortet sechs aufeinander aufbauende Fragen:

| # | Leitfrage | Einheiten |
|---|-----------|:-----------:|
| 1 | **Warum** automatisieren wir Gebäude? | 1–2 |
| 2 | **Welche Funktionen** stecken in einem automatisierten Gebäude? | 2 |
| 3 | **Wie messen** wir zuverlässig? | 3–4 |
| 4 | **Wie steuern** wir – und wo stoßen wir an Grenzen? | 5–6 |
| 5 | **Wie regeln** wir – und wie legen wir Regler aus? | 7–9 |
| 6 | **Wie kommunizieren** Geräte – und welches Bussystem wähle ich? | 10–14 |

---

## Übersicht: 14 Einheiten

| Einheit | Thema |
|:-------:|-------|
| 1 | Einführung Gebäudeautomation |
| 2 | Planung & Funktionen der GA |
| 3 | Messkette I – Digitale Signale & Hardware |
| 4 | Messkette II – Analoge Signale & Mapping |
| 5 | Steuerung I – Ablaufsteuerungen & FSM |
| 6 | Steuerung II – Verknüpfungen & OOP |

--- 

## Übersicht: 14 Einheiten

| Einheit | Thema |
|:------:|-------|
| 7 | Regelungstechnik I – Blockschaltbild & Zweipunktregelung |
| 8 | Regelungstechnik II – Regelkreis & PID |
| 9 | Regelungstechnik III – Regelverhalten & Auslegung |
| 10 | SPS – Grundlagen & Hardware |
| 11–13 | Bussysteme I–III: Signalisierung, Zugriffsverfahren, Sicherheit |
| 14 | Bussysteme IV – GA-Systeme (Recherche & Präsentationen) |
| 15 | Klausurvorbereitung |

---

## Unsere Anwendungsfälle: Treppenlicht & Konstantlichtregelung

<!-- _class: white -->

Wir arbeiten die gesamte Vorlesung an **zwei konkreten Automatisierungsaufgaben**:

### Treppenlichtschaltung
Taster gedrückt → Licht an → nach 60 s aus. Mit zwei Tastern. Als endlicher Automat.

### Konstantlichtregelung
Sensor misst Helligkeit → Regler stellt LED-Helligkeit nach → Sollwert wird gehalten trotz Sonnenlicht.

---

## Was wir von Ihnen erwarten

* **Mitarbeit:** Die Übungsaufgaben sind kein Bonus – sie sind der Kern der Vorlesung. Wer die Aufgaben löst, versteht den Stoff.
* **Neugier:** Sie werden auf Probleme stoßen, die nicht im Skript stehen. Das ist gewollt. Recherchieren, ausprobieren, fragen.
* **Eigenverantwortung in Einheit 14:** Sie wählen ein GA-Bussystem, recherchieren es selbst und erklären es Ihren Kommilitonen.
* **Keine Pflichtabgaben** – aber die Klausur zeigt, ob Sie dabei waren.

---

## Leistungsbewertung & Organisation

### Klausur (100 %)
* Schriftlich am Ende des Semesters
* Fokus auf Anwendung: Berechnungen, Entwurf, Begründung von Entscheidungen
* Bei geringer Teilnehmer:innenzahl ist im Falle einer Nachklausur auch ein mündlicher Prüfungsmodus möglich

### Labor (unabhängig, Laborbericht)
* Baut auf den Inhalten der Vorlesung auf
* Bewertet nach den Vorgaben des *Academic Walkthrough*
* Vollständige Anwesenheitspflicht

---

## Unterlagen
* Alle Folien und Skripte auf Sakai (werden laufend aktualisiert)
* PDF-Versionen: Fehler werden während des Semesters nicht nachkorrigiert

---

## Hardware

<!-- _class: white -->

* Für jede Zweier-Gruppe wird die notwendige Hardware gestellt und für die Dauer des Semesters ausgeliehen
* Wer sich eigene Hardware zulegen möchte:

| Bauteil | Wozu |
|---------|------|
| Raspberry Pi Pico (WH) | Mikrocontroller für Einheiten 3–6 |
| Micro-USB-Kabel | für Mikrocontroller |
| Breadboard | Steckplatine für Prototyping |
| KY-018 Fotowiderstand | Analoger Helligkeitssensor |
| Widerstand $10\,\text{k}\Omega$, $470\,\Omega$ | Pull-Up/Pull-Down, LED-Schutz |
| LEDs, Taster, Jumperkabel | Digitale Ein-/Ausgänge |

---

## Ausblick: Das Labor

<!-- _class: white -->

Das Labor ergänzt die Vorlesung mit **industrienaher Hardware** (Beckhoff-SPS, DALI-Bus):

| Labor | Themen |
|-------|--------|
| **Bussysteme** | SPS-Programmierung (Strukturierter Text, Funktionsbausteine), MQTT-Datenübertragung in die Cloud, Lichtsteuerung mit DALI |
| **Elektrotechnik** | Gleichstrom, Kondensator & Spule, Wechselstrom |

> Was Sie in der Vorlesung als Konzept kennenlernen – FSM, PID-Regler, Buszugriff – implementieren Sie im Labor auf echter SPS-Hardware.

* Labor findet im SBT-Labor *4C-313* (Bussysteme) bzw. *MCI VI* (Elektrotechnik) statt
* Labor-Unterlagen und *Academic Walkthrough* **vor** dem ersten Termin lesen

---

## Los geht's

### Einheit 1: Einführung Gebäudeautomation

* Was automatisieren wir eigentlich?
* Wie strukturieren Normen (VDI 3813/3814) die Aufgaben?
* Was kostet uns fehlende Automation – und was bringt sie?
