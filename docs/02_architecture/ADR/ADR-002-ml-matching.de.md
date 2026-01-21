# ADR-002: ML-Matching Roadmap (Plan)

## Status
Akzeptiert (optional Hybrid-ML)

## Kontext
Die aktuelle Basis ist regelbasiertes Matching fuer Transparenz und Determinismus.
Ein ML-Ansatz folgt erst nach stabiler Baseline und Evaluationsdaten.

Recruiter-relevante Kriterien:
- Rolle/Senioritaet, Standort/Remote, Arbeitserlaubnis
- Jahre Erfahrung und relevante Domaenen
- Pflicht-Skills und Tools
- Zertifikate und Sprachen
- Ausbildungsanforderungen
- klare Gaps vs. Must-have Anforderungen

## Entscheidung
Ein optionales Hybrid-ML-Matching wird implementiert (Bi-Encoder Similarity + Feature-Fusion),
die deterministische Baseline bleibt Default.

## Implementierung (Aktuell)
- ML-Module unter `src/core/ml/` (Embedding, Semantic Matcher, Feature Fusion).
- Strategieauswahl in `src/core/matcher.py` mit Env-Flag `MATCHING_STRATEGY=hybrid_ml`.
- Erklaerbarkeit: Semantic Similarity, Skill-Overlap, Section-Coverage, Top-Chunks.
- Optionaler Calibrator via `ML_CALIBRATOR_PATH` (Logistic Regression), Baseline bleibt unberuehrt.

## ML-Plan (High Level)
1) Datenerhebung
   - CV/JD Paare mit Labels (match / kein match / teilweise) kuratieren.
   - Bevorzugt synthetische oder consented Daten; keine Persistenz von PII.
2) Feature-Strategie
   - Strukturierte Felder aus dem regelbasierten Extractor.
   - Text-Embeddings pro CV/JD Abschnitt (Skills, Experience, Summary).
   - Hybrid-Scoring: Regeln als Constraints + ML-Similarity.
3) Modellfamilien
   - Baseline: Cosine Similarity auf Sentence Embeddings.
   - Kandidaten: Bi-Encoder Embeddings; optional Cross-Encoder Re-Ranker.
4) Evaluation
   - Precision/Recall, Ranking-Metriken (MRR, nDCG).
   - Human Review der Erklaerungen (Top Matches, False Positives).
5) Privacy und Bias
   - Keine externen APIs fuer sensible Daten.
   - Bias-Risiken dokumentieren (Name, Gender) und mitigieren.
6) Rollout
   - Baseline bleibt Default.
   - ML im Shadow Mode, Vergleich zur Baseline, dann optionaler Gate.

## Konsequenzen
- Baseline bleibt Default und deterministisch.
- ML ist optional und erklaerbar; Evaluation bleibt Voraussetzung fuer Abschluss.
