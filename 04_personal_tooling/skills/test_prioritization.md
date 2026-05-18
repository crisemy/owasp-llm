# Skill: Test Prioritization

## Goal
Select and order test cases based on predicted risk and business impact.

## Mode
AI-assisted (suggestion only, human approval required)

## Inputs
- Historical test results
- Failure frequency
- Test execution time
- Code changes (optional)
- Business criticality tags

## Output
- Prioritized test list
- Suggested execution subset
- Risk score per test

## Strategy

### Phase 1: Heuristic Scoring (QA-driven)
- High failure frequency → increase priority
- High business impact → increase priority
- Long execution time → penalize (for optimization)

### Phase 2: ML Enhancement (DS-driven)
- Classification model (fail / pass likelihood)
- Optional: ranking model

## Constraints
- Must be explainable
- No black-box decisions
- Must allow QA override

## Anti-Patterns
- Random selection
- Full regression by default