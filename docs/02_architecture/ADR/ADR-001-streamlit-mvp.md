# ADR-001: Streamlit for MVP UI

## Context
The MVP needs a simple interface to upload CV PDFs and show extraction results.
The UI must be fast to build, easy to run locally, and suitable for demos.

## Decision
Use Streamlit for the MVP user interface.

## Alternatives Considered
- FastAPI backend + React frontend

## Consequences
- Faster iteration and lower setup cost for the MVP
- Limited UI flexibility and long-term scalability compared to a custom stack
