# Evaluationsplan

## Metriken
- PDF-Erfolgsrate (Extraktion ohne Fehler)
- Response Time (End-to-End Verarbeitungszeit)
- Usability (SUS nach Demo)
- Privacy Checks (keine Dateien nach Session)
- ML-Matching (optional): nDCG / MRR, F1 / ROC-AUC (falls Calibrator genutzt)
- Explainability-Review (Top-Chunks und Skill-Overlap)

## Messung
- Erfolg vs. Fehler je Upload protokollieren
- Response Time je Request messen; P95 berechnen
- SUS-Scores von Pilot-Usern erheben
- Tempfiles geloescht, keine persistierten CV-Daten
- Ranking-Metriken auf gelabelten CV/JD Paaren evaluieren (synthetisch oder public)
- Erklaerungsartefakte auf Konsistenz pruefen

## Akzeptanzschwellen
- PDF-Erfolgsrate >= 95% auf Sample-Set
- Response Time P95 < 30 Sekunden
- SUS Score >= 70
- Privacy Checks: 100% pass
- ML-Metriken dokumentiert in `docs/04_evaluation/EVALUATION_RESULTS.md`
