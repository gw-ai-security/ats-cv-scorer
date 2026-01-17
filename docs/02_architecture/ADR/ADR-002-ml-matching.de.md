# ADR-002: ML-Matching Roadmap (Plan)

## Status
Vorgeschlagen

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
Ein ML-Plan baut auf der Baseline auf und verbessert Recall, ohne Erklaerbarkeit,
Privacy-by-Design oder Reproduzierbarkeit zu verlieren.

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
Deterministisches Matching bleibt primaer, bis ML nachweislich sicher,
reproduzierbar und messbar besser ist.
