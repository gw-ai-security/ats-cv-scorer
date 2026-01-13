# Funktionale Anforderungen (FR)

## FR-001 PDF-Upload & Validierung
Priorität: MUST
Status: GEPLANT
Akzeptanz:
- PDF bis 10MB
- Dateityp validieren
- verständliche Fehlermeldungen

## FR-002 Multi-Strategie Textextraktion
Priorität: MUST
Status: GEPLANT
Abhängigkeit: FR-001
Akzeptanz:
- pdfplumber als Primary
- OCR Fallback bei < 50 Wörtern
- Metadaten: Methode, Seitenzahl, Qualität

## FR-003 CV-Strukturanalyse
Priorität: MUST
Status: GEPLANT
Akzeptanz:
- Sektionen: Kontakt, Erfahrung, Ausbildung, Skills, Projekte
- DE/EN Header
- Graceful Degradation

## FR-004 Skill-Extraktion & Kategorisierung
Priorität: MUST
Status: GEPLANT
Akzeptanz:
- Skill-Datenbank
- Synonyme (z. B. JS → JavaScript)
- Kategorien: Technical, Soft, Languages, Certifications
