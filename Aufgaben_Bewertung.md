# Kritische Bewertung der Aufgaben

## Roter Faden der Aufgaben – Ist-Stand

Der **ideale Bogen** für die Aufgaben wäre:
*Treppenlicht / Konstantlichtregelung planen → messen → steuern → regeln → kommunizieren*

Dieser Bogen ist im Kern vorhanden, wird aber an mehreren Stellen durch Seitenäste oder Inkonsistenzen gestört. Die folgende Karte zeigt, wo der rote Faden hält und wo er reißt:

```
1_2_1 (RA-Schema)
  → 2_1_1-3 (LED + Taster)
    → 2_1_5 (LDR + Mapping)
      → 2_2_1 (FSM Treppenlicht lesen)
        → 2_2_4 (Tageslichtschaltung implementieren)  ← ✅ starke Verbindung
          → 2_3_1 (Tageslicht modular)
            → 2_4_1/2 (Sensor als Klasse)
              → 2_4_3 (Daten für Bus vorbereiten)  ← Brücke zu Kap. 5!
                → 3_1_2 (Tageslicht in xcos)
                  → 3_2_1 (Konstantlicht mit P-Regler)  ← ✅ zweiter Anwendungsfall
                    → 3_3_1 (Reglerauswahl für GA)
                      → 4_1_1/2 (SPS: ADC + Sensor)
                        → 5_2_1 (Polling-Berechnung)
                          → 5_2_2 (Brandmeldung: Verfahrenswahl)
                            → 5_3_1 (Drehschalter Hamming)
                              → Rechercheaufgabe (5_4)  ← ✅ Krönung
```

---

## Bewertung je Aufgabe

### Kapitel 1.2 – Planungsabläufe

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **1_2_1** Raumautomations-Schema Treppenhaus | ✅ Behalten | Direkter Einstieg ins laufende Beispiel (Treppenlicht). Grafisch-konkret, kein Code nötig, fördert planerisches Denken vor der Technik. |

---

### Kapitel 2.1 – Messkette

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **2_1_1** Pico Setup + LED blink | ✅ Behalten | Essenzieller Einstieg. Keine Vereinfachung möglich ohne Verständnisverlust. |
| **2_1_2** Taster anschließen (Pull-Up) | ✅ Behalten | Baut direkt auf 2_1_1 auf, EVA-Prinzip wird greifbar. |
| **2_1_3** LED + Taster (Zustandswechsel) | ✅ Behalten | Erste echte Interaktion, verbindet Eingang + Ausgang. |
| **2_1_4** 🤓 LED mit PWM | ⚠️ Anpassen | Inhaltlich gut (PWM ist relevant für Dimmen), aber zeitlich ein Exkurs. Als explizites 🤓 behalten, aber **nicht** in der Hauptpräsentation hervorheben. Außerdem: der Bezug zur Konstantlichtregelung (stetige Ansteuerung) sollte explizit hergestellt werden. |
| **2_1_5** Helligkeitssensor + lineares Mapping | ✅ Behalten | Zentraler Baustein für alle späteren Aufgaben. Gut motiviert. |
| **2_1_5** (zweite Aufgabe, gleiche Nummer!) Quadratisches Mapping | ⚠️ Umbenennen → **2_1_6** | Inhaltlich gut. **Problem: doppelte Nummerierung.** Umbenennen in `2_1_6`. Außerdem sollte explizit erwähnt werden, warum ein nichtlineares Mapping nötig ist (physikalische Motivation). |
| **2_1_6 (alt)** 🤓 settings.toml / Umgebungsvariablen | ❌ Entfernen | Bricht den Fluss, ist Konfigurationsmanagement-Detailwissen. Kein Bezug zum roten Faden. Falls behalten, dann als 🤓🤓 im Appendix. |

---

### Kapitel 2.2 – Steuerung

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **2_2_1** FSM-Code Treppenlicht lesen & analysieren | ✅ Behalten | Excellent scaffolded: Code ist gegeben, Studierende analysieren ihn. Unmittelbarer Bezug zur Aufgabe 1_2_1 (RA-Schema). Dieser Moment – das Erkennen des Plans im Code – ist ein pädagogischer Höhepunkt. |
| **2_2_2** State Machine für Dimmschalter (entwerfen) | ⚠️ Anpassen | **Roter Faden unterbrochen.** Ein Dimmschalter ist kein Treppenlicht. Entweder: umformulieren als Erweiterung des Treppenlichts (z.B. „Treppenlicht mit Dimm-Vorwarnung statt Flackern") oder ersetzen durch eine Erweiterung von 2_2_1. |
| **2_2_3** 🤓 Dimmschalter implementieren | ⚠️ Anpassen | Gleiches Problem. Als 🤓 ist es vertretbar, wenn 2_2_2 angepasst wird. |
| **2_2_4** Tageslichtschaltung (Verknüpfungssteuerung) | ✅ Behalten | Sehr gut. Verweist explizit auf 2_1_3 und 2_1_5. Zweiter laufender Anwendungsfall. |

---

### Kapitel 2.3 – Funktionen

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **2_3_1** 🤓 Tageslichtschaltung modular implementieren | ✅ Behalten | Baut sauber auf 2_2_4 auf. Modularisierung fühlt sich motiviert an. |
| **2_3_2** Reflexion: Was als Funktion auslagern? | ✅ Behalten | Selten: eine rein konzeptuelle Aufgabe ohne Code. Sehr gut für Diskussion und Metareflexion. Bricht nicht den Fluss, sondern festigt ihn. |

---

### Kapitel 2.4 – Objektorientierung

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **2_4_1** Sensor-Klasse: Mittelwertmethode | ✅ Behalten | OOP-Einstieg fühlt sich motiviert an: der Sensor aus 2_1_5 bekommt eine Klasse. Gute Kontinuität. |
| **2_4_2** 🤓 Sensor-Klasse: Sliding Window + Mapping | ✅ Behalten | Sinnvolle Erweiterung. Die Integration von `mappings.py` in die Klasse macht den Vorteil von OOP erlebbar. |
| **2_4_3** `prepare_data()` für Busübertragung | ✅ Behalten – **Potenzial heben** | Aktuell unterschätzt. Diese Aufgabe fragt „was überträgst du eigentlich über den Bus?" und ist eine perfekte konzeptuelle Brücke zu Kapitel 5. **Empfehlung:** explizit als Vorgriff auf Bussysteme kennzeichnen und die Frage schärfen: „Warum macht Datenmenge auf einem Bus mit 1200 Baud (DALI) einen Unterschied?" |

---

### Kapitel 3.1 – Blockschaltbild

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **3_1_0** P-Glied + Totzeitglied (xcos/Matlab) | ✅ Behalten | Guter Einstieg in das Simulationstool. Kurz, explorativer Charakter. |
| **3_1_1** Wassertank ohne Steuerung (xcos) | ✅ Behalten | Der Wassertank ist ein klassisches, intuitiv verständliches Modell. Baut später als Regelkreis weiter (3_2_3). Gute Kontinuität. |
| **3_1_2** Einfache Tageslichtschaltung (xcos) | ✅ Behalten | Bringt das laufende Beispiel ins Blockschaltbild. Wichtige Verbindung zwischen Python-Code und formalem Modell. |
| **3_1_3** Einfache Tageslichtschaltung (**Zweipunktregelung**) | ⚠️ Umbenennen | **Doppelter Name mit 3_1_2!** Inhalt ist gut (Zweipunktregelung mit Hysterese), aber Namensgleichheit verursacht Verwirrung. Umbenennen in **„3_1_3: Zweipunktregelung für Tageslichtschaltung"**. |
| **Fehlendes Bindeglied** zwischen Kap. 2 und 3 | ❌ Fehlt | Es gibt keine Aufgabe, die explizit erklärt: *„Hier ist der Python-Code von 2_3_1 – und hier ist dasselbe als Blockschaltbild."* Dieser Übergang von der Implementierungswelt in die Simulationswelt ist der größte konzeptuelle Sprung im Kurs. **Empfehlung:** Eine kurze Aufgabe hinzufügen: Skizzieren Sie das Blockschaltbild der Tageslichtschaltung aus Kap. 2 (ohne Simulation, nur Papier). |

---

### Kapitel 3.2 – Regelkreis

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **3_2_1** Konstantlicht-Regelung P-Regler (xcos) | ✅ Behalten – **Highlight** | Exzellent: der zweite laufende Anwendungsfall (Konstantlichtregelung) bekommt seinen Regelkreis. Bleibende Regelabweichung wird erlebbar. Motiviert I-Anteil. |
| **3_2_2** CO₂-Regelung (zeichnen) | ⚠️ Anpassen | Neues Szenario (CO₂), das bisher nie vorkam. Der Inhalt – Vergleich logischer Regler vs. P-Regler – ist wertvoll. **Empfehlung:** Entweder auf die Konstantlichtregelung umstellen, oder explizit als bewusste Erweiterung des Blickwinkels einleiten: „Hier sehen wir ein weiteres GA-System, das ganz anders reagiert." |
| **3_2_3** Wassertank mit PID-Regler (xcos) | ✅ Behalten | Gute Kontinuität: gleicher Wassertank wie 3_1_1, jetzt mit Regelkreis. Macht den Unterschied P vs. PI vs. PID erlebbar. |
| **3_2_4** Reaktion D-Regler (konzeptuell) | ✅ Behalten | Schnelle Verständnisaufgabe ohne Simulation. Gute Abwechslung. |

---

### Kapitel 3.3 – Regelverhalten

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **🌡️ Aufgabe 1** PID + PT1 Einheitssprung (Simulink) | ⚠️ Anpassen | Inhaltlich gut. **Problem:** Werkzeugwechsel zu Simulink/Matlab mitten im Kurs (vorher xcos/Scilab). Außerdem bricht die Namenskonvention (🌡️ statt ✍️, „Aufgabe 1" statt „3_3_1"). **Empfehlung:** Einheitlich umbenennen, Werkzeug vereinheitlichen oder den Wechsel explizit begründen. |
| **🌡️ Aufgabe 2** Heizkurve (Simulink) | ⚠️ Anpassen | Sehr gute Aufgabe (realer GA-Anwendungsfall, Steuerung ohne Rückkopplung). Heizung ist ein neues Szenario, das aber gut motiviert ist. **Problem:** Die Komplexität (PT1→PT1-Kaskade) ist deutlich höher als alle bisherigen Simulationsaufgaben. Besser scaffolden (Blockschaltbild zuerst auf Papier zeichnen, dann simulieren). |
| **🔁 Aufgabe 3** Temperaturregelung P-Regler (Simulink) | ✅ Behalten | Schließt die Heizung zum geregelten System. Gute Progression. |
| **3_3_1** Reglerauswahl für GA-Anwendungen | ✅ Behalten – **Highlight** | Selten gut: keine Simulation, keine Hardware, nur Nachdenken. Verbindet die Regelungstheorie direkt mit GA-Anwendungsfällen aus dem Kurs (Startoptimierung, Konstantlicht). |
| **3_3_2** Ziegler-Nichols (Google Colab) | ⚠️ Anpassen | Weiterer Werkzeugwechsel (Google Colab)! Der Inhalt ist wichtig, aber das Bild `ReglerEinstellen.png` ohne Beschriftung und die fehlende Beschreibung des Szenarios machen die Aufgabe unklar. **Empfehlung:** Szenario explizit benennen (z.B. Konstantlichtregelung oder Raumtemperatur), Werkzeug vereinheitlichen. |
| **🤓 3_3_2** (identische Überschrift!) Ziegler-Nichols xcos | ❌ Umbenennen → **3_3_3** | **Zwei Aufgaben haben exakt denselben Namen.** Das ist ein Fehler. Umbenennen in `3_3_3`. |

---

### Kapitel 4.1 – SPS Grundlagen

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **4_1_1** ADC-Auflösung berechnen (12-Bit Sensor) | ✅ Behalten | Kurze Rechenaufgabe, die den Unterschied Pico (16-Bit) vs. SPS (12-Bit) spürbar macht. Gut als Anknüpfung an Kap. 2. |
| **4_1_2** Drucksensor 4–20 mA (Drahtbrucherkennung) | ✅ Behalten – **Potenzial heben** | Inhaltlich ausgezeichnet: Drahtbrucherkennung über 4-20 mA ist ein typisches Praxisthema, das zeigt warum 0–10 V oft nicht verwendet wird. Aber: das Szenario (Lüftungsanlage, Drucksensor) ist neu und hat keinen expliziten Bezug zum laufenden Beispiel. **Empfehlung:** Den GA-Kontext der Lüftungsanlage kurz einbetten: „In Ihrer Konstantlicht-Anlage kommt nun auch ein Drucksensor für die Lüftung hinzu..." |

---

### Kapitel 5.1 – Signalisierung

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **5_1_1** Symbolrate + Bitrate ablesen | ✅ Behalten | Konkrete Rechenaufgabe direkt nach dem Konzept. Kurz und präzise. |
| **5_1_2** Leitungscodes (erkennen/skizzieren) | ✅ Behalten | Standard-Konsolidierungsaufgabe, visuell. Gut. |

---

### Kapitel 5.2 – Buszugriffsverfahren

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **5_2_1** Worst-Case Polling (Berechnung + JS-Demo) | ✅ Behalten – **Highlight** | Hervorragend. Die Berechnung macht die Latenz greifbar, das JS-Demo lässt Studierende die Verzögerung selbst spüren. Direkte Verbindung zur GA-Praxis (Türöffner!). |
| **5_2_2** Buszugriffsverfahren für Brandmeldesystem | ✅ Behalten – **Highlight** | Szenario-basiert, offen, sicherheitskritisch. Erzwingt das Abwägen von Deterministik vs. CSMA. Perfekte Vorbereitung auf die Rechercheaufgabe. |

---

### Kapitel 5.3 – Übertragungssicherheit

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **5_3_1** Drehschalter: Code mit Hamming-Abstand ≥ 3 entwerfen | ✅ Behalten | Konkretes Design-Problem, wenige Parameter, gut lösbar in der Vorlesung. Zeigt den Trade-off: mehr Sicherheit = mehr Redundanz = mehr Bandbreite. |

---

### Kapitel 5.4 – GA-Bussysteme (Rechercheaufgabe)

| Aufgabe | Bewertung | Kommentar |
|---------|-----------|-----------|
| **Rechercheaufgabe Gebäudebussysteme** | ✅ Behalten – **Bester Abschluss** | Die Aufgabe ist sehr gut strukturiert. Die geforderten Kriterien (Übertragungsmedium, Buszugriffverfahren, Telegrammaufbau, Anwendungsfall) sind direkt aus den Einheiten 11–13 abgeleitet. Präsentation: 3 Folien / 5 Minuten ist realistisch. **Verbesserung:** Explizit fordern, dass die GA-spezifischen Auswahlkriterien aus dem Kurs (Energieeffizienz, Norm-Kompatibilität EN 15232, Wartbarkeit) einbezogen werden – damit schließt sich der Bogen zu Einheit 1 (Planungsphasen). |

---

## Übergreifende Probleme

### 1. Werkzeuginkonsistenz
Der Kurs verwendet **vier verschiedene Werkzeuge** für Simulationsaufgaben:
- CircuitPython (Kap. 2)
- Scilab xcos (Kap. 3.1, 3.2)
- Matlab/Simulink (Kap. 3.3)
- Google Colab (Kap. 3.3)

Jeder Werkzeugwechsel kostet Einstiegszeit und lenkt von Inhalten ab. **Empfehlung:** Entweder Scilab oder Matlab konsequent durchhalten. Google Colab könnte Python-basierte Simulationen ermöglichen, die an den Code aus Kap. 2 anknüpfen.

### 2. Namens- und Nummerierungsfehler
- **2_1_5**: doppelt vergeben (zweite Aufgabe = quadratisches Mapping)
- **3_1_2 + 3_1_3**: beide heißen „Einfache Tageslichtschaltung"
- **3_3_2**: zweimal als Überschrift für zwei verschiedene Aufgaben
- **4_2_6** (in der Präsentation benannt als `2_4_6`): Nummerierungsfehler

### 3. Fehlende konzeptuelle Brücke (Kap. 2 → 3)
Es gibt keine Aufgabe, die den Übergang von der Python-Implementierung zum Blockschaltbild explizit vollzieht. Der Sprung von „ich schreibe CircuitPython" zu „ich baue ein xcos-Modell" ist der größte Bruch im Kurs.

**Vorschlag für eine neue Brückenaufgabe (vor 3_1_0):**

> *Zeichnen Sie auf Papier ein Blockschaltbild der Tageslichtschaltung aus Aufgabe 2_3_1. Welches Python-Objekt entspricht welchem Block? Identifizieren Sie Eingangs-, Ausgangs-, Stell- und Störgrößen.*

### 4. Kein abschließender Rückbezug auf Planung
Einheit 1 startet mit dem Raumautomations-Schema (1_2_1). Die Rechercheaufgabe in Einheit 14 ist ein guter Abschluss. Aber **der Kreis zum RA-Schema schließt sich nie explizit**.

**Vorschlag für eine Abschlussaufgabe (im Rahmen der Präsentationen):**

> *Ergänzen Sie das Raumautomations-Schema aus Aufgabe 1_2_1 um die Angabe des Bussystems. Welches der präsentierten Systeme würden Sie für die Treppenlicht-Anlage wählen – und warum?*

---

## Zusammenfassung

| Kategorie | Anzahl |
|-----------|--------|
| ✅ Behalten (inkl. Highlights) | ~22 |
| ⚠️ Anpassen / Umbenennen | ~10 |
| ❌ Entfernen | 1 (2_1_6 alt) |
| Fehlend (neu erstellen) | 2 (Brückenaufgabe 2→3, Abschlussaufgabe 14) |

Die Aufgaben folgen im Kern bereits einem kohärenten roten Faden rund um Treppenlicht und Konstantlichtregelung. Die größten Optimierungspotenziale liegen in der **Werkzeugkonsistenz**, der **Nummerierungsbereinigung** und dem Schließen der **konzeptuellen Lücke zwischen Implementierung und Simulation**.
