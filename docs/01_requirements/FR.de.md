# Funktionale Anforderungen (FR)

## FR-001 PDF-Upload und Validierung
Prioritaet: MUST
Status: UMGESETZT
Akzeptanz:
- PDF bis 10MB
- Dateityp validieren
- klare Fehlermeldungen anzeigen

## FR-002 Textextraktion (Phase 1)
Prioritaet: MUST
Status: UMGESETZT
Abhaengigkeit: FR-001
Akzeptanz:
- pdfplumber als Primaer-Extraktor
- deterministisches Verhalten fuer gleiche Eingabe
- Metadaten: Methode, Seitenzahl, Wortanzahl, Qualitaet
- Fehlerbehandlung ohne Crash (leerer Text + Fehler)
- OCR-Fallback ist in Phase 1 explizit ausser Scope

## FR-003 CV-Strukturanalyse
Prioritaet: MUST
Status: UMGESETZT
Akzeptanz:
- Sektionen erkennen: Kontakt, Erfahrung, Ausbildung, Skills, Projekte
- DE/EN-Header unterstuetzen
- Graceful Degradation

## FR-004 Skill-Extraktion und Kategorisierung
Prioritaet: MUST
Status: UMGESETZT
Akzeptanz:
- Skill-Datenbank
- Synonyme (z. B. JS -> JavaScript)
- Kategorien: Technical, Soft, Languages, Certifications

## FR-005 ATS-Recruiter-Kriterien aus CV extrahieren
Prioritaet: MUST
Status: UMGESETZT
Akzeptanz:
- Kontakt: Name, Email, Telefon, Standort, Links (LinkedIn/GitHub/Portfolio)
- Summary/Profil erkannt, falls vorhanden
- Erfahrung: Rolle, Unternehmen, Zeitraum, Kerntaetigkeiten
- Ausbildung: Abschluss, Institution, Zeitraum
- Skills: Hard/Soft/Tools/Methoden
- Zertifikate und Sprachen erkennen
- Verfuegbarkeit/Notice Period erkennen, falls vorhanden
- Fehlende Felder werden als "nicht gefunden" markiert (kein Crash)

## FR-006 Stellenbeschreibung-Upload und Parsing
Prioritaet: MUST
Status: UMGESETZT
Akzeptanz:
- JD Upload (PDF)
- Extrahierte Felder: Rolle, Senioritaet, Standort/Remote, Anforderungen, Nice-to-have, Verantwortlichkeiten
- Anforderungen als strukturierte Skill- und Keyword-Listen
- DE/EN-Header unterstuetzen
- Graceful Degradation

## FR-007 CV <-> JD Matching (Baseline, regelbasiert)
Prioritaet: MUST
Status: UMGESETZT
Abhaengigkeit: FR-005, FR-006
Akzeptanz:
- Score mit nachvollziehbarer Begruendung (Match/Gap pro Kriterium)
- Gewichtung konfigurierbar (z. B. Skills, Erfahrung, Ausbildung, Sprache)
- Fehlende Informationen transparent anzeigen
- Deterministisches Verhalten fuer gleiche Eingabe

## FR-008 ML-Ansatz fuer Matching planen
Prioritaet: SHOULD
Status: GEPLANT
Akzeptanz:
- Dokumentierter ML-Plan (Datenbedarf, Features, Modellfamilien)
- Evaluationsmetriken (Precision/Recall, Ranking, Human Review)
- Bias- und Privacy-Risiken dokumentiert
- Rollout-Plan (Baseline -> ML-Experiment)
