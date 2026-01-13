# Quality Gates

## Tooling
- Lint: ruff
- Tests: pytest
- Coverage: pytest-cov (report in CI)

## Definition of Done (Requirements)
- implementation exists in `src/`
- tests cover the acceptance criteria
- traceability updated in `docs/01_requirements/TRACEABILITY.*.md`
- CI is green

## Security Basics
- validate user input (file type and size)
- no persistent storage of CV data
- remove temporary files after processing
