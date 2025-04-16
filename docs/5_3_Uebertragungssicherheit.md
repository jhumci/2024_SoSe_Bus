---
marp: true
author: Julian Huber
size: 16:9
footer: Julian Huber - Bussysteme

# Strg+[ ] for Options

theme: beams

---

<!-- paginate: true -->

# 5.3 Übertragungssicherheit

<!-- _class: title -->

---

## 🎯 Lernziele

Nach dieser Einheit können Sie:

- Verschiedene Fehlertypen bei der Datenübertragung unterscheiden.
- Maßnahmen zur Erkennung und Korrektur von Übertragungsfehlern erklären.
- Den Hamming-Abstand von Codes berechnen und dessen Bedeutung verstehen.

---

## 🧠 Aufbau von Datenpaketen

![center](images/2022-05-10-13_47_26-Window.webp)

Datenpakete (auch „Telegramme“) enthalten Informationen, die über ein Bussystem übertragen werden. Der Aufbau variiert je nach System, umfasst jedoch typischerweise:

- **Steuerfeld**: Definiert die Priorität der Nachricht.
- **Quelladresse**: Identifiziert den Absender (ähnlich einer MAC-Adresse).
- **Zieladresse**: Gibt den Empfänger an.
- **Routing-Zähler**: Zählt, wie oft die Nachricht über Koppler weitergeleitet wurde.
- **Nutzinformation**: Die eigentlichen Daten, z. B. Messwerte eines Sensors.
- **Sicherungsfeld**: Prüft, ob die Daten korrekt übertragen wurden (z. B. Prüfsumme).



---

## 🛡️ Datensicherung

Daten können durch Störungen verloren gehen oder verfälscht werden. Beispiel:

```
Gesendet:    010000010000001110000000
Empfangen 1: 010000110000001110000000  (1 Bitfehler)
Empfangen 2: 01000010000001110000000   (2 Bitfehler)
```

---

## 🛡️ Datensicherung

### Ursachen für Fehler:
- Elektromagnetische Störungen.
- Probleme mit der Taktung.
- Defekte Hardware.

### Maßnahmen zur Datensicherung
- **OSI-Schicht 1 (Physikalische Schicht)**: Abgeschirmte Kabel, Glasfaserkabel oder potentialfreie Übertragung reduzieren Störungen.
- **OSI-Schicht 2 (Sicherungsschicht)**: Überwachung der Daten auf Fehler und Korrekturmaßnahmen.

---

## 🧠 Fehlerarten

Wir betrachten **bitorientierte Codes**, bei denen jede Bitkombination gültig ist. Fehler sind nicht direkt erkennbar, da keine Bitfolge „verboten“ ist. Es gibt drei Haupttypen von Fehlern:

- **Offensichtlicher Fehler**
- **Nicht erkennbarer Fehler**
- **Erkennbarer Fehler**

![bg right:33% height:300](images/Fehlertypen.svg)

---

## 📏 Fehlermaße

Die **Bitfehlerrate** ($p$) gibt an, wie häufig Fehler auftreten:

$$p = \frac{\text{Anzahl fehlerhafter Bits}}{\text{Gesamtzahl gesendeter Bits}}$$

- **Ungünstigster Fall**: $p = 0.5$ (jedes zweite Bit ist fehlerhaft, Nachricht unbrauchbar).
- **Extremfall**: $p = 1$ (alle Bits invertiert, z. B. `001` → `110`).
- **Realistischer Wert**: $p = 10^{-4}$ (1 von 10.000 Bits ist fehlerhaft).

---

## 🔍 Fehlererkennung durch Codierung

Die Art der Codierung beeinflusst, ob Fehler erkannt werden können. Beispiel mit einem nicht-bitorientierten Code (Deutsche Sprache):

- **Offensichtlicher Fehler**: `Gxbäude` → erkennbar, korrigierbar zu `Gebäude`.
- **Nicht erkennbarer Fehler**: `Mein` → `Dein` (beides gültige Wörter).
- **Erkennbarer Fehler**: `Tein` → ungültiges Wort.

---

**Beispiel für einen einfachen binären Code**:
- `00`: Schalter **ein**
- `11`: Schalter **aus**
- `01`, `10`: Ungültig

Ein Ein-Bit-Fehler (z. B. `00` → `01`) führt zu einem ungültigen Codewort und ist erkennbar.

![bg right:40% height:300](images/Fehlertypen.svg)

---

## 📏 Hamming-Abstand

Der **Hamming-Abstand** misst, wie viele Positionen sich zwischen zwei gleich langen Codewörtern unterscheiden. Der Hamming-Abstand eines Codes ist der **kleinste** Abstand zwischen zwei gültigen Codewörtern.

**Beispiele**:
- Code `{00, 11}`: Hamming-Abstand = 2.
- Code `{00, 01, 10, 11}`: Hamming-Abstand = 1.
- Code `{'Haus', 'Baum', 'Tier'}`: Hamming-Abstand = 2.

**Regel**: Ein Code mit Hamming-Abstand $h$ kann bis zu $h-1$ Bitfehler erkennen.

---

## 🛠️ Fehlererkennung mit Hamming-Abstand

**Beispiel-Code**: `{0001, 0110, 1000}`

- Kleinster Hamming-Abstand: 2 (z. B. `1000` und `0001` unterscheiden sich an 2 Positionen).
- **Fazit**: Der Code kann **1-Bit-Fehler** erkennen, da ein Fehler kein anderes gültiges Codewort erzeugt (z. B. `0001` → `0011` ist ungültig).
- **Problem**: Ein **2-Bit-Fehler** kann unbemerkt bleiben (z. B. `0001` → `1000`).

**Regel für Fehlerkorrektur**:
- Um $t$ Fehler zu korrigieren, muss der Hamming-Abstand mindestens $h=2 t + 1$ betragen.

---

## ✍️ Aufgabe 5_3_1: Drehschalter

Ein Drehschalter hat vier Einstellungen, die als binäre Codes übertragen werden: `00`, `01`, `10`, `11`. Der Hamming-Abstand beträgt 1, sodass ein Ein-Bit-Fehler ein anderes gültiges Codewort erzeugt (z. B. `00` → `01`).

**Aufgabe**: Entwickeln Sie einen binären Code mit Hamming-Abstand ≥ 3, der:
- Fehler erkennt **und** korrigiert.
- Nur Einfachfehler (max. 1 Bitfehler) berücksichtigt.

![bg right](images/Drehschalter.png)

[Quelle](https://at.rs-online.com/web/p/nockenschalter/2212822)

---

## ✔️ Lösung: Drehschalter

Ein Code mit Hamming-Abstand ≥ 3 ermöglicht die Korrektur von Einfachfehlern. Beispielcode für vier Einstellungen:

- `11000000`: Stellung 1
- `00110000`: Stellung 2
- `00001100`: Stellung 3
- `00000011`: Stellung 4

**Hamming-Abstand**: Mindestens 3 (z. B. `11000000` und `00110000` unterscheiden sich an 3 Positionen).

**Fehlerkorrektur**:
- Empfangen: `10000000` → am nächsten zu `11000000` (1 Bit Unterschied) → korrigiert.
- Empfangen: `11100000` → am nächsten zu `11000000` (2 Bits Unterschied) → nicht korrigierbar.

---

## 🔢 Paritätsbit (Even-Bit) zur Fehlererkennung

Ein **Paritätsbit** wird hinzugefügt, um die Anzahl der `1`-Bits in einer Nachricht gerade (oder ungerade) zu machen. Beispiel:

- Gesendet: `0010` (2 in Binär, 1 `1`-Bit → ungerade).
- Paritätsbit (gerade Parität): `1` (macht die Gesamtzahl der `1`-Bits gerade).
- Übertragen: `00101`.

**Fehlererkennung**:
- Empfangen: `00111` → 3 `1`-Bits (ungerade) → Fehler erkannt.
- Empfangen: `10101` → 4 `1`-Bits (gerade) → kein Fehler erkannt (2-Bit-Fehler bleibt unbemerkt).

**Einschränkung**: Nur ungerade Anzahlen an Fehlern werden erkannt.

![bg right:25% width:300](images/800px-Code_Even_dualergaenzt.svg.png)

---

## 🧱 Blocksicherung

- Die Blocksicherung erweitert das Paritätsbit-Konzept auf eine Matrix aus Datenbits. Für jede Zeile und Spalte wird ein Paritätsbit berechnet.
- Anstelle nur nach allen X-Bits eine Paritätsbit einzufügen wird auch ein spaltenweises Paritätsbit (im Beispielsweise P als Even-Bit) eingefügt.

<center>

![height:250](images/Blocksicherung.png)

</center>


[Quelle](Gerhard Schnell & Bernhard Wiedemann )

---


![height:700](images/BeispielBlocksicherung/Folie1.JPG)

* Ein Ein-Bit-Fehler in der Matrix wird erkannt und kann korrigiert werden.

---

![height:700](images/BeispielBlocksicherung/Folie2.JPG)

* Ein Ein-Bit-Fehler im Kontrollfeld wird erkannt und kann korrigiert werden.

---

![height:700](images/BeispielBlocksicherung/Folie3.JPG)

* Ein Zwei-Bit-Fehler im Kontrollfeld wird erkannt, aber nicht korrigiert.


---

## 📚 Glossar

- **Bitfehlerrate**: Anteil fehlerhafter Bits an allen gesendeten Bits.
- **Hamming-Abstand**: Anzahl der Positionen, an denen sich zwei Codewörter unterscheiden.
- **Paritätsbit bzw. Even-Bit**: Zusätzliches Bit, das die Anzahl der `1`-Bits in einer Nachricht gerade oder ungerade macht.
- **Blocksicherung**: Methode zur Fehlererkennung und -korrektur durch Hinzufügen von Paritätsbits für Zeilen und Spalten eines Datenblocks.

---

## 📽️ Weiterführende Ressource

[▶️ 3Blue1Brown: A discovery-oriented introduction to error correction code](https://www.youtube.com/watch?v=X8jsijhllIA)