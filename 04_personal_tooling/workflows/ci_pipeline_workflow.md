# Workflow: CI Pipeline (GitHub Actions)

## Steps

1. Trigger pipeline
2. Collect context (PR, changes)
3. Run impact analysis
4. Run prioritization
5. Execute tests (parallel)
6. Collect artifacts:
   - logs
   - screenshots
7. Run failure analysis
8. Generate report

## Constraints
- Must be fast
- Must be reproducible