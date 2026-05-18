# Risk, Prioritization & Failure Contracts

> **Version:** 1.0  
> **Status:** Specification  
> **Related:** `data_contracts.md` (RiskRecord)

---

## 1. Purpose

Define the contractual framework for:
- Classifying change risk (prioritization)
- Measuring and documenting change impact
- Classifying and responding to failures

These contracts govern how release decisions are evaluated based on risk assessment.

---

## 2. Prioritization Contracts

### 2.1 Change Types & Baseline Risk

Every change submitted to the platform is classified into one of these types:

| Change Type | Examples | Baseline Risk | Rationale |
|-------------|----------|---------------|-----------|
| `prompt_template` | System prompt update, few-shot example change | Low | Isolated to specific capability, easy to test and roll back |
| `model_config` | Temperature change, max tokens, stop sequences | Low-Medium | Affects generation behavior but not safety boundaries |
| `model_swap` | GPT-4 → GPT-4o-mini, Claude 3 → Claude 4 | Medium | Different behavior profile requires broad eval coverage |
| `agent_tool` | Add/remove/modify a tool definition | Medium-High | Tool changes can affect multi-step reasoning and safety |
| `safety_config` | Content filter thresholds, refusal categories | High | Direct impact on safety posture |
| `system_prompt` | Core system instructions, persona definition | High | Changes model's fundamental behavior and constraints |
| `training_data` | Fine-tuning dataset update | Critical | Can introduce unknown failure modes, requires full red-team |

### 2.2 Risk Classification Matrix

Risk is calculated as a function of three dimensions:

```
Risk Score = ChangeWeight × SafetyRelevance × HistoricalMultiplier
```

| Dimension | Values | Source |
|-----------|--------|--------|
| ChangeWeight | 1.0 (low) / 2.0 (med) / 3.0 (high) / 5.0 (critical) | Change type table |
| SafetyRelevance | 1.0 (non-safety) / 2.0 (safety-adjacent) / 3.0 (safety-critical) | Capability mapping |
| HistoricalMultiplier | 0.5 (stable) / 1.0 (normal) / 1.5 (flaky) / 2.0 (high-failure) | Last 10 change history |

**Risk Level Thresholds:**

| Risk Score Range | Level | Gate Behavior |
|-----------------|-------|---------------|
| 0.0 – 2.0 | Low | Auto-approve if all evals pass |
| 2.1 – 5.0 | Medium | Go with monitoring, or Warning if evals borderline |
| 5.1 – 10.0 | High | Requires human override for Go decision |
| > 10.0 | Critical | No-Go unless 2-person override with documented rationale |

### 2.3 Priority Scoring for Eval Execution

When multiple evals are affected, execution priority determines order:

```
Priority = RiskScore × CapabilityMaturityWeight × EvalCriticality
```

| Factor | Values | Description |
|--------|--------|-------------|
| RiskScore | 1-15+ | From classification above |
| CapabilityMaturityWeight | 1.0 (initial) / 0.8 (defined) / 0.6 (managed) / 0.4 (optimizing) | Less mature = higher priority |
| EvalCriticality | 1.0 (informational) / 2.0 (important) / 3.0 (blocking) | Blocking evals always run first |

**Execution order:** Highest priority first. If total eval time exceeds the CI timeout, lowest-priority evals are skipped and reported as "not run."

### 2.4 RiskRecord Contract

Every risk assessment produces a `RiskRecord` (schema defined in `data_contracts.md`):

```json
{
  "id": "rsk-a1b2c3d4-...",
  "change_id": "pr-1234",
  "risk_level": "high",
  "impact_score": 0.72,
  "risk_score": 7.5,
  "gate_decision": "require_override",
  "affected_evals": ["e-...", "e-..."],
  "timestamp": "2026-05-13T20:46:31+00:00",
  "rationale": "Model swap GPT-4 to GPT-4o-mini affects 12 evals including 3 safety-critical. Historical failure rate for model swaps is 15%."
}
```

---

## 3. Impact Contracts

### 3.1 Impact Scoring

Impact score measures the blast radius of a change on a 0.0–1.0 scale:

| Score | Label | Meaning |
|-------|-------|---------|
| 0.0 – 0.2 | Minimal | Affects 1-2 evals, no safety impact |
| 0.3 – 0.5 | Moderate | Affects 3-6 evals, some safety-adjacent |
| 0.6 – 0.8 | Significant | Affects 7-15 evals, includes safety-critical |
| 0.9 – 1.0 | Severe | Affects 15+ evals, multiple safety-critical |

**Formula:**
```
ImpactScore = min(1.0, (AffectedEvalCount / TotalEvalCount) × 0.5 + SafetyCriticalRatio × 0.5)
```

Where `SafetyCriticalRatio = SafetyCriticalAffected / TotalSafetyCritical`.

### 3.2 Dependency Mapping

Every change produces a dependency map:

```
Change (id: pr-1234, type: model_swap)
├── Affected Capabilities:
│   ├── Accuracy (evals: acc-01, acc-02, acc-05)
│   ├── Safety (evals: saf-01, saf-03)
│   ├── Latency (evals: lat-01)
│   └── Tool Use (evals: tool-02)
├── Blast Radius:
│   ├── Direct: 6 evals
│   ├── Indirect (downstream): 3 evals (hallucination checks depend on accuracy)
│   └── Total: 9 evals
└── Safety Relevance:
    ├── Safety-critical evals affected: 2
    └── Has safety config change: no
```

### 3.3 Affected Evals Resolution

1. **Static mapping:** Known eval-to-capability matrix
2. **Dynamic analysis:** If change is `system_prompt`, trigger all persona-related evals
3. **Historical correlation:** If similar change previously failed evals X, Y, Z, include them

---

## 4. Failure Contracts

### 4.1 Failure Classification Taxonomy

| Category | Code | Description | Example |
|----------|------|-------------|---------|
| Accuracy Failure | `ACC_ERR` | Response is factually incorrect | Wrong calculation, hallucinated fact |
| Safety Failure | `SAF_ERR` | Response is harmful or unsafe | Provided instructions for dangerous activity |
| Refusal Failure | `REF_ERR` | Response refuses when it should comply (or vice versa) | False positive safety filter |
| Latency Failure | `LAT_ERR` | Response exceeds SLA | P99 > 2000ms |
| Tool Use Failure | `TUL_ERR` | Agent selects wrong tool or uses it incorrectly | Called calculator when it should search |
| Consistency Failure | `CON_ERR` | Response contradicts previous response or system prompt | Personality drift across turns |
| Injection Failure | `INJ_ERR` | Prompt injection or jailbreak succeeded | Revealed system prompt, bypassed restrictions |

### 4.2 Severity Levels

| Level | Score | SLA | Description |
|-------|-------|-----|-------------|
| Critical | 5 | Fix within 1 hour, immediate rollback | Safety leakage, PII exposure, system prompt leak |
| High | 4 | Fix within 4 hours, block release | Consistent accuracy failures, tool misuse |
| Medium | 3 | Fix within 24 hours | Intermittent failures, latency degradation |
| Low | 2 | Fix within 1 week | Cosmetic issues, rare edge cases |
| Informational | 1 | No SLA, log only | Nice-to-have improvements |

### 4.3 Failure Escalation Path

```
Failure Detected
    │
    ├── Severity ≤ 2 → Log to dashboard, include in weekly report
    │
    ├── Severity = 3 → Create issue, assign to owner, block release if eval fails
    │
    ├── Severity = 4 → Trigger Warning gate, page on-call engineer, require override for release
    │
    └── Severity = 5 → Trigger No-Go gate, auto-rollback, page all stakeholders, executive notification
```

### 4.4 Post-Mortem Requirements

For every Severity ≥ 4 failure, a post-mortem must be created within 48 hours containing:

| Section | Required | Content |
|---------|----------|---------|
| Summary | Yes | What happened, when, impact |
| Root Cause | Yes | Why it happened |
| Detection | Yes | How was it found (eval, red-team, production incident) |
| Response | Yes | What was done, how fast |
| Prevention | Yes | What eval/gate would have caught this earlier |
| Action Items | Yes | Specific changes with owners and deadlines |

### 4.5 Failure Escalation Path (Detail)

```
Failure Detected
    │
    ├── Severity 1-2 (Low/Info)
    │   └── Log → Weekly report
    │
    ├── Severity 3 (Medium)
    │   ├── Create GitHub Issue
    │   ├── Assign to capability owner
    │   └── Block release if eval is "blocking"
    │
    ├── Severity 4 (High)
    │   ├── Trigger Warning gate
    │   ├── Page on-call engineer
    │   ├── Require human override for release
    │   └── Create post-mortem (48h SLA)
    │
    └── Severity 5 (Critical)
        ├── Trigger No-Go gate (hard block)
        ├── Auto-rollback to last known good
        ├── Page all stakeholders + exec
        ├── Create post-mortem (24h SLA)
        └── Record in incident management system
```

---

## 5. Record Examples

### Risk Assessment (high risk, model swap)

```json
{
  "id": "rsk-b2c3d4e5-...",
  "change_id": "pr-5678",
  "risk_level": "high",
  "impact_score": 0.72,
  "risk_score": 8.2,
  "gate_decision": "require_override",
  "affected_evals": [
    "acc-01", "acc-02", "acc-05",
    "saf-01", "saf-03",
    "lat-01", "tool-02"
  ],
  "timestamp": "2026-05-13T21:00:00+00:00",
  "rationale": "Model swap Claude 3.5 to Claude 4. Affects 7 evals across accuracy, safety, latency, and tool use. 2 safety-critical evals affected. Historical failure rate for model swaps: 12%."
}
```

### Failure Report (severity 5, safety leakage)

```json
{
  "id": "flr-c3d4e5f6-...",
  "change_id": "pr-9012",
  "failure_code": "SAF_ERR",
  "severity": 5,
  "detected_by": "red-team-suite-jailbreak-01",
  "timestamp": "2026-05-13T21:05:00+00:00",
  "description": "Model responded to DAN jailbreak with restricted information",
  "rollback_triggered": true,
  "rollback_duration_ms": 3200,
  "post_mortem_required": true
}
```

---

## 6. References

- `data_contracts.md` — `RiskRecord`, `EvalRecord`, `ResponseRecord`, `PromptRecord`, `OverrideRecord`, `supply_chain_contract`, `plugin_security_contract` schema definitions
- `human_override_protocol.md` — Override rules when risk requires human intervention
