# ADR-001: Streamlit fuer die MVP-UI

## Kontext
Das MVP benoetigt eine einfache Oberfläche fuer CV-PDF-Uploads und die Anzeige
von Extraktionsergebnissen. Die UI soll schnell implementiert, lokal leicht
ausfuehrbar und demo-tauglich sein.

## Entscheidung
Streamlit wird fuer die MVP-UI verwendet.

## Alternativen
- FastAPI Backend + React Frontend

## Konsequenzen
- schnellere Iteration und geringere Setup-Kosten im MVP
- weniger Flexibilitaet und Skalierbarkeit als ein Custom-Stack
