# Skill: Change Impact Analysis

## Goal
Estimate risk and affected areas from code or feature changes.

## Inputs
- Changed files / modules
- Commit messages
- Historical defect mapping
- Test coverage map (if available)

## Output
- Affected components
- Risk level (low / medium / high)
- Suggested test scope

## Strategy

### Rule-Based Layer
- Map modules → test suites
- Detect critical areas (auth, payments, etc.)

### Data Layer
- Correlate past changes → failures
- Identify patterns

## Constraints
- Conservative bias on critical systems
- Must provide reasoning

## Anti-Patterns
- Ignoring indirect dependencies
- Overconfidence in low-data scenarios