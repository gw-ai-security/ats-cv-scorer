# Funktionale Anforderungen (FR)

## FR-001 PDF-Upload und Validierung
Prioritaet: MUST
Status: GEPLANT
Akzeptanz:
- PDF bis 10MB
- Dateityp validieren
- klare Fehlermeldungen anzeigen

## FR-002 Textextraktion (Phase 1)
Prioritaet: MUST
Status: IN ARBEIT
Abhaengigkeit: FR-001
Akzeptanz:
- pdfplumber als Primaer-Extraktor
- deterministisches Verhalten fuer gleiche Eingabe
- Metadaten: Methode, Seitenzahl, Wortanzahl, Qualitaet
- Fehlerbehandlung ohne Crash (leerer Text + Fehler)
- OCR-Fallback ist in Phase 1 explizit ausser Scope

## FR-003 CV-Strukturanalyse
Prioritaet: MUST
Status: GEPLANT
Akzeptanz:
- Sektionen erkennen: Kontakt, Erfahrung, Ausbildung, Skills, Projekte
- DE/EN-Header unterstuetzen
- Graceful Degradation

## FR-004 Skill-Extraktion und Kategorisierung
Prioritaet: MUST
Status: GEPLANT
Akzeptanz:
- Skill-Datenbank
- Synonyme (z. B. JS -> JavaScript)
- Kategorien: Technical, Soft, Languages, Certifications
