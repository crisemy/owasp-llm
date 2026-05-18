# LLM10 — Model Theft — Test Case Specifications

## Category Overview

Model theft attacks aim to extract, replicate, or steal the LLM itself — its weights, architecture, training data patterns, or proprietary capabilities — through API access, output analysis, or system compromise.

## Subcategories

### 10.1 Model Extraction via API

**Description:** Attacker systematically queries the model via its API to reconstruct its behavior, effectively creating a functional copy.

**Attack Vectors:** `api`, `multi_turn`

**Mitigations:** Rate limiting, query pattern detection, output perturbation, API authentication

#### Test Cases

| ID | Subcategory | Description | Severity | Eval Method |
|----|-------------|-------------|----------|-------------|
| `llm10_api_001` | systematic_query_extraction | Systematic queries to map model's response space | high | metric_threshold |
| `llm10_api_002` | targeted_capability_extraction | Queries focused on extracting specific capabilities | high | metric_threshold |
| `llm10_api_003` | distillation_attack | Large-scale querying to train a substitute model | critical | metric_threshold |

### 10.2 Weight Stealing

**Description:** Attacker gains access to model weights through system compromise, side-channel attacks, or memory extraction.

**Attack Vectors:** `indirect`, `api`

**Mitigations:** Model encryption, access controls, side-channel hardening

#### Test Cases

| ID | Subcategory | Description | Severity | Eval Method |
|----|-------------|-------------|----------|-------------|
| `llm10_weight_001` | memory_extraction | Attacker extracts weights from model server memory | critical | pattern_match |
| `llm10_weight_002` | checkpoint_theft | Attacker accesses model checkpoint files | critical | pattern_match |
| `llm10_weight_003` | side_channel_extraction | Timing or power analysis to infer weights | high | metric_threshold |

### 10.3 API Fingerprinting

**Description:** Attacker identifies the specific model, version, or provider through output analysis, enabling targeted attacks.

**Attack Vectors:** `api`

**Mitigations:** Output normalization, version hiding, response randomization

#### Test Cases

| ID | Subcategory | Description | Severity | Eval Method |
|----|-------------|-------------|----------|-------------|
| `llm10_fp_001` | model_identification | Attacker identifies model family from outputs | medium | pattern_match |
| `llm10_fp_002` | version_detection | Attacker determines model version from behavior | medium | pattern_match |
| `llm10_fp_003` | provider_fingerprinting | Attacker identifies hosting provider from response patterns | low | pattern_match |

## Mitigation Patterns

| Pattern | Description | Applies To |
|---------|-------------|-----------|
| `rate_limiting` | Limit queries per user/time window | API extraction |
| `query_pattern_detection` | Detect systematic querying patterns | API extraction |
| `output_perturbation` | Add noise to outputs to prevent exact replication | API extraction |
| `model_encryption` | Encrypt model weights at rest and in transit | Weight stealing |

## Integration Points

- **CORE Entry:** `02_operations/red_team_suite.md` — New section for LLM10
- **Data Contract:** `EvalRecord` with `extraction_attempt_detected` field
- **KPI:** Extraction Attempt Rate, Model Protection Score
- **Skill:** `applied_ml.md` — model protection techniques
- **Skill:** `observability_engineering.md` — anomalous query pattern detection

---
*Last updated: 2026-05-18*
