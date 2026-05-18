# Data Contracts

## Purpose
Normalizar inputs y outputs de datos del CORE para asegurar interoperabilidad entre workflows de QA, analitica y modelos de riesgo.

## Scope
- Contratos de entrada/salida para procesos de testing orientados a riesgo.
- Estandares minimos de estructura, tipado y trazabilidad.
- Reglas comunes para intercambio entre QA Architect, DS y automatizaciones.

## Core Contract Principles
- Consistencia: mismo significado para el mismo campo en todos los proyectos.
- Trazabilidad: todo registro debe tener origen y contexto de ejecucion.
- Reproducibilidad: inputs identicos deben producir outputs comparables.
- Auditabilidad: cambios de esquema deben quedar versionados.

## Canonical Metadata (Required in all contracts)
| Field | Type | Required | Description |
|---|---|---|---|
| contract_name | string | yes | Nombre del contrato de datos |
| contract_version | string | yes | Version semantica (ej: v1.0) |
| generated_at | datetime (ISO 8601) | yes | Timestamp de generacion |
| source_system | string | yes | Sistema origen del dato |
| environment | string | yes | Entorno (`local`, `ci`, `staging`, `prod`) |
| project_id | string | yes | Identificador del proyecto |
| release_id | string | no | Identificador de release asociado |
| execution_id | string | yes | ID unico de corrida/proceso |
| owner | string | yes | Responsable del contrato |

## Input/Output Normalization Rules
- Fechas y horas en formato ISO 8601 UTC.
- Identificadores en `snake_case` y estables por registro.
- Campos categoricos con valores controlados y documentados.
- Campos numericos con unidad explicita (ms, %, count).
- Campos opcionales deben declarar politica de nullabilidad.

## Common Envelope
```json
{
  "metadata": {
    "contract_name": "string",
    "contract_version": "v1.0",
    "generated_at": "2026-05-12T00:00:00Z",
    "source_system": "string",
    "environment": "ci",
    "project_id": "string",
    "release_id": "string",
    "execution_id": "string",
    "owner": "string"
  },
  "payload": {}
}
```

## Versioning Policy (Base)
- Cambio mayor (`v2.0`): rompe compatibilidad de campos requeridos o semantica.
- Cambio menor (`v1.1`): agrega campos no disruptivos.
- Cambio patch (`v1.0.1`): corrige descripcion, validaciones o metadatos.

## Ownership and Change Control
- Owner primario: DS + QA Architect.
- Toda propuesta de cambio debe incluir impacto en workflows afectados.
- Ningun contrato pasa a uso operativo sin revision cruzada QA/DS.

## `test_prioritization_contract`
### Objective
Definir el schema minimo para priorizacion de tests basado en riesgo y costo.

### Input Schema (`payload.input`)
| Field | Type | Required | Description |
|---|---|---|---|
| test_case_id | string | yes | ID unico del test |
| historical_fail_rate | number (0-1) | yes | Frecuencia historica de falla |
| avg_execution_time_ms | integer | yes | Duracion promedio |
| business_criticality | enum (`low`,`medium`,`high`,`critical`) | yes | Impacto de negocio |
| recent_change_flag | boolean | no | Si el area tuvo cambios recientes |
| module_tag | string | yes | Modulo funcional asociado |
| flaky_score | number (0-1) | no | Indice de inestabilidad del test |

### Output Schema (`payload.output`)
| Field | Type | Required | Description |
|---|---|---|---|
| test_case_id | string | yes | Referencia al test |
| risk_score | number (0-100) | yes | Riesgo calculado |
| priority_rank | integer | yes | Orden de ejecucion sugerido |
| recommended_subset | boolean | yes | Inclusion en subset recomendado |
| reason_codes | string[] | yes | Razones trazables de priorizacion |
| override_allowed | boolean | yes | Debe ser `true` |

### Constraints
- El resultado debe ser explicable (`reason_codes` obligatorio).
- El contrato no ejecuta decisiones autonomas de release.
- QA puede hacer override en cualquier momento.

## `change_impact_contract`
### Objective
Definir el schema minimo para estimar impacto de cambios y alcance de testing.

### Input Schema (`payload.input`)
| Field | Type | Required | Description |
|---|---|---|---|
| change_id | string | yes | ID de cambio (commit/PR/release unit) |
| changed_files | string[] | yes | Archivos modificados |
| changed_modules | string[] | yes | Modulos afectados |
| change_type | enum (`feature`,`bugfix`,`refactor`,`infra`) | yes | Tipo de cambio |
| commit_message | string | no | Contexto textual del cambio |
| module_test_map_version | string | yes | Version del mapeo modulo->tests |

### Output Schema (`payload.output`)
| Field | Type | Required | Description |
|---|---|---|---|
| impacted_components | string[] | yes | Componentes impactados |
| suggested_test_scope | string[] | yes | Suites/tests sugeridos |
| impact_risk_level | enum (`low`,`medium`,`high`) | yes | Riesgo estimado |
| impact_reasoning | string[] | yes | Evidencia/razones de impacto |
| conservative_bias_applied | boolean | yes | `true` en sistemas criticos |

### Constraints
- En areas criticas (auth, pagos, seguridad) se aplica sesgo conservador.
- No se permite salida sin `impact_reasoning`.

## `failure_analysis_contract`
### Objective
Definir taxonomia y schema para clasificar fallas de testing con accion sugerida.

### Input Schema (`payload.input`)
| Field | Type | Required | Description |
|---|---|---|---|
| failure_id | string | yes | ID unico de falla |
| test_case_id | string | yes | Test asociado |
| error_message | string | yes | Mensaje de error principal |
| stack_trace | string | no | Stack trace capturado |
| log_excerpt | string | yes | Extracto de logs relevantes |
| screenshot_path | string | no | Ruta a evidencia visual |
| environment_snapshot | object | yes | Versiones/config de entorno |

### Output Schema (`payload.output`)
| Field | Type | Required | Description |
|---|---|---|---|
| root_cause_class | enum (`test_issue`,`environment_issue`,`product_bug`,`unknown`) | yes | Clasificacion principal |
| confidence_score | number (0-1) | yes | Confianza de clasificacion |
| suggested_action | string | yes | Accion recomendada |
| evidence_used | string[] | yes | Evidencia que sustenta la clasificacion |
| uncertainty_flag | boolean | yes | `true` si confianza baja |

### Constraints
- Sin evidencia suficiente, clasificar como `unknown` y activar `uncertainty_flag`.
- Prohibido inferir causa sin `evidence_used`.

## Data Quality Rules
### Validation Gates
- Completitud: minimo 95% de campos requeridos no nulos por lote.
- Unicidad: `execution_id + test_case_id` no puede duplicarse en el mismo ciclo.
- Tipado: validar tipo y rango de campos criticos antes de persistir.
- Temporalidad: timestamps en UTC y monotonia logica por evento.
- Integridad referencial: IDs de tests/modulos deben existir en catalogos vigentes.

### Invalid Data Handling
- Registro invalido => estado `quarantine`.
- Lote con >10% invalidos => bloqueo de consumo para modelos.
- Toda cuarentena debe registrar causa y accion correctiva.

## Leakage + Versioning Policy
### Anti-Leakage Rules
- Separar dataset de entrenamiento/evaluacion por ventana temporal o release.
- Prohibido usar señales futuras en features de prediccion.
- Features derivadas de resultados post-release no pueden usarse para predecir ese mismo release.
- Verificacion obligatoria de leakage antes de entrenar/promover modelos.

### Extended Versioning Rules
- Todo contrato debe mantener `contract_version` semantico.
- Cambios breaking requieren migracion documentada y plan de rollback.
- Changelog obligatorio por version con impacto esperado.
- Compatibilidad hacia atras: mantener lectura de version previa por al menos 1 ciclo de release.

### Control Checklist
- [ ] Split temporal validado.
- [ ] Features sin fuga de informacion futura.
- [ ] Contrato versionado y changelog actualizado.
- [ ] Prueba de compatibilidad hacia atras ejecutada.

## `supply_chain_contract`
### Objective
Define the schema for tracking and validating LLM supply chain dependencies: models, datasets, libraries, and infrastructure.

### Input Schema (`payload.input`)
| Field | Type | Required | Description |
|---|---|---|---|
| dependency_id | string | yes | Unique identifier for the dependency |
| dependency_type | enum (`model`,`dataset`,`library`,`plugin`,`infrastructure`) | yes | Type of dependency |
| name | string | yes | Dependency name |
| version | string | yes | Version or commit hash |
| source | string | yes | Origin (pypi, huggingface, github, internal, etc.) |
| expected_hash | string | no | Expected SHA-256 hash for integrity verification |
| license | string | no | License type |
| last_verified_at | datetime (ISO 8601) | no | Last integrity verification timestamp |
| known_vulnerabilities | string[] | no | List of known CVEs or security advisories |

### Output Schema (`payload.output`)
| Field | Type | Required | Description |
|---|---|---|---|
| dependency_id | string | yes | Reference to the dependency |
| integrity_status | enum (`verified`,`failed`,`unverified`,`outdated`) | yes | Current integrity status |
| risk_level | enum (`low`,`medium`,`high`,`critical`) | yes | Risk assessment |
| vulnerability_count | integer | yes | Number of known vulnerabilities |
| last_scan_at | datetime (ISO 8601) | yes | Last vulnerability scan timestamp |
| remediation_required | boolean | yes | Whether remediation is required |
| sbom_entry_id | string | yes | Reference to SBOM entry |

### Constraints
- All model and dataset dependencies MUST have `expected_hash` for integrity verification.
- Dependencies with `critical` risk level block release until remediated.
- SBOM (Software Bill of Materials) must be maintained and versioned.
- Integrity verification required before any model update or dataset ingestion.

## `plugin_security_contract`
### Objective
Define the schema for registering, validating, and monitoring LLM plugins/tools with security controls.

### Input Schema (`payload.input`)
| Field | Type | Required | Description |
|---|---|---|---|
| plugin_id | string | yes | Unique plugin identifier |
| plugin_name | string | yes | Human-readable name |
| version | string | yes | Plugin version |
| permissions | string[] | yes | List of granted permissions |
| action_boundaries | string[] | yes | Actions the plugin is NOT allowed to perform |
| input_schema | object | yes | Expected input schema for validation |
| output_schema | object | yes | Expected output schema for validation |
| requires_human_approval | boolean | yes | Whether actions require human confirmation |
| max_calls_per_session | integer | no | Rate limit per session |
| owner | string | yes | Plugin owner/maintainer |

### Output Schema (`payload.output`)
| Field | Type | Required | Description |
|---|---|---|---|
| plugin_id | string | yes | Reference to the plugin |
| registration_status | enum (`active`,`suspended`,`deprecated`) | yes | Current registration status |
| permission_violations | integer | yes | Count of permission violations detected |
| last_violation_at | datetime (ISO 8601) | no | Timestamp of last violation |
| validation_passed | boolean | yes | Whether input/output validation is passing |
| risk_score | number (0-1) | yes | Calculated risk score |
| audit_trail_id | string | yes | Reference to audit trail |

### Constraints
- Plugins with `critical` permission violations are automatically suspended.
- Input and output schemas must be validated before plugin activation.
- All plugin calls must be logged for audit purposes.
- `requires_human_approval` must be `true` for any plugin with destructive permissions.

## `EvalRecord`
### Objective
Define the canonical schema for evaluation results. Used by all test execution, KPI calculation, and security assessment pipelines.

### Input Schema (`payload.input`)
| Field | Type | Required | Description |
|---|---|---|---|
| eval_id | string | yes | Unique evaluation identifier |
| test_case_id | string | yes | Reference to the test case being evaluated |
| prompt_id | string | yes | Reference to the prompt used |
| response_id | string | yes | Reference to the model response |
| eval_type | enum (`accuracy`,`safety`,`latency`,`tool_use`,`hallucination`,`injection`,`toxicity`,`agency`,`extraction`) | yes | Type of evaluation |
| expected_behavior | string | yes | What the system should have done |
| actual_behavior | string | yes | What the system actually did |

### Output Schema (`payload.output`)
| Field | Type | Required | Description |
|---|---|---|---|
| eval_id | string | yes | Reference to the evaluation |
| pass | boolean | yes | Whether the evaluation passed |
| score | number (0-1) | no | Numeric score (0=fail, 1=pass) |
| confidence | number (0-1) | no | Confidence in the evaluation result |
| injection_detected | boolean | no | Whether prompt injection was detected (LLM01, LLM07) |
| toxicity_score | number (0-1) | no | Toxicity/harmfulness score of response (LLM02, LLM06, LLM09) |
| token_count | integer | no | Number of tokens consumed (LLM04) |
| latency_ms | integer | no | Response latency in milliseconds (LLM04) |
| compute_cost | number | no | Compute cost for this evaluation (LLM04) |
| agency_violation | boolean | no | Whether agent exceeded boundaries (LLM08) |
| hallucination | boolean | no | Whether response contains hallucinated content (LLM09) |
| human_validated | boolean | no | Whether a human validated the result (LLM09) |
| extraction_attempt_detected | boolean | no | Whether model extraction attempt was detected (LLM10) |
| privacy_violation_type | string | no | Type of privacy violation (LLM06) |
| data_leaked | string | no | Description of data that was leaked (LLM06) |
| sanitization_applied | boolean | no | Whether output sanitization was applied (LLM02) |
| eval_method | enum (`pattern_match`,`llm_judge`,`metric_threshold`,`human_review`,`schema_validation`) | yes | Method used to evaluate |
| failure_reason | string | no | Reason for failure if `pass = false` |
| timestamp | datetime (ISO 8601) | yes | When evaluation was performed |

### Constraints
- `eval_method` must match the test case's specified evaluation method.
- LLM-specific fields are optional and populated only when relevant to the eval type.
- Evaluations with `confidence < 0.5` must set `human_validated = true` or flag for review.

## `ResponseRecord`
### Objective
Define the canonical schema for LLM system responses. Used for latency tracking, token accounting, and response analysis.

### Input Schema (`payload.input`)
| Field | Type | Required | Description |
|---|---|---|---|
| prompt_id | string | yes | Reference to the originating prompt |
| model_version | string | yes | Model version that generated the response |
| temperature | number | no | Temperature setting used |
| max_tokens | integer | no | Max tokens configured |
| plugins_enabled | string[] | no | List of plugins/tools available during generation |

### Output Schema (`payload.output`)
| Field | Type | Required | Description |
|---|---|---|---|
| response_id | string | yes | Unique response identifier |
| prompt_id | string | yes | Reference to the prompt |
| response_text | string | yes | Full text of the model's response |
| latency_ms | integer | yes | Time from request to first token + completion |
| token_count | integer | yes | Total tokens in response |
| finish_reason | enum (`stop`,`length`,`content_filter`,`error`) | yes | Why generation ended |
| tool_calls | object[] | no | List of tool calls made by the model |
| error_message | string | no | Error message if generation failed |
| timestamp | datetime (ISO 8601) | yes | When response was generated |

### Constraints
- `latency_ms` must include both time-to-first-token and full completion time.
- `token_count` must match the tokenizer used by the model.
- `tool_calls` must follow the plugin security contract schema.

## `PromptRecord`
### Objective
Define the canonical schema for prompts sent to the LLM system. Used for evaluation coverage tracking and prompt management.

### Input Schema (`payload.input`)
| Field | Type | Required | Description |
|---|---|---|---|
| prompt_text | string | yes | The prompt text sent to the model |
| category | string | yes | Prompt category (e.g., `security_test`, `functional`, `benchmark`) |
| source | string | yes | Origin of the prompt (test suite, user, automated) |
| system_prompt | string | no | System prompt context if applicable |
| conversation_history | object[] | no | Previous turns if multi-turn conversation |
| metadata | object | no | Additional metadata (tags, labels, etc.) |

### Output Schema (`payload.output`)
| Field | Type | Required | Description |
|---|---|---|---|
| prompt_id | string | yes | Unique prompt identifier |
| prompt_text | string | yes | The prompt text |
| category | string | yes | Prompt category |
| source | string | yes | Origin of the prompt |
| token_count | integer | yes | Number of tokens in the prompt |
| created_at | datetime (ISO 8601) | yes | When prompt was created |
| eval_count | integer | yes | Number of evaluations performed against this prompt |

### Constraints
- `eval_count` tracks how many times this prompt has been evaluated.
- Prompts used in security tests must have `category = security_test`.

## `RiskRecord`
### Objective
Define the canonical schema for risk assessments. Used for change risk classification, release gating, and override targeting.

### Input Schema (`payload.input`)
| Field | Type | Required | Description |
|---|---|---|---|
| change_id | string | yes | ID of the change being assessed (PR, commit, release) |
| change_type | enum (`prompt_template`,`model_config`,`model_swap`,`agent_tool`,`safety_config`,`system_prompt`,`training_data`) | yes | Type of change |
| affected_evals | string[] | yes | List of evaluation IDs affected by the change |
| safety_critical | boolean | yes | Whether change affects safety-critical components |

### Output Schema (`payload.output`)
| Field | Type | Required | Description |
|---|---|---|---|
| id | string | yes | Unique risk assessment identifier |
| change_id | string | yes | Reference to the change |
| risk_level | enum (`low`,`medium`,`high`,`critical`) | yes | Calculated risk level |
| impact_score | number (0-1) | yes | Blast radius score |
| risk_score | number (0-15+) | yes | Calculated risk score |
| affected_evals | string[] | yes | Evaluations impacted |
| rationale | string | yes | Explanation of risk assessment |
| gate_decision | enum (`auto_approve`,`monitor`,`warning`,`require_override`,`no_go`) | yes | Release gate decision |
| timestamp | datetime (ISO 8601) | yes | When assessment was performed |

### Constraints
- `risk_level = critical` always results in `gate_decision = no_go`.
- `risk_level = high` requires `gate_decision = require_override` or `no_go`.
- Risk assessments are immutable once published; overrides create new records.

## `OverrideRecord`
### Objective
Define the canonical schema for human override requests. Used for audit trails, compliance reporting, and security decision review.

### Input Schema (`payload.input`)
| Field | Type | Required | Description |
|---|---|---|---|
| target_id | string | yes | ID of the record being overridden |
| target_type | enum (`eval`,`risk`,`gate`,`kpi_alert`,`security_override`,`agency_override`) | yes | Type of target record |
| original_decision | string | yes | The automatic decision being overridden |
| override_decision | string | yes | The human decision to apply |
| justification | string | yes | Detailed explanation (min 20 chars) |
| operator_id | string | yes | Human operator identifier |
| operator_role | string | yes | Operator role (e.g., `safety_engineer`) |
| expires_at | datetime (ISO 8601) | no | Expiration for temporary overrides |
| tags | string[] | no | Classification tags |
| evidence_links | string[] | no | Links to supporting evidence |

### Output Schema (`payload.output`)
| Field | Type | Required | Description |
|---|---|---|---|
| override_id | string | yes | Unique override identifier |
| target_id | string | yes | Reference to overridden record |
| target_type | enum | yes | Type of target |
| status | enum (`pending`,`approved`,`rejected`,`applied`,`expired`) | yes | Current override status |
| original_decision | string | yes | Original automatic decision |
| override_decision | string | yes | Human decision applied |
| justification | string | yes | Operator's explanation |
| operator_id | string | yes | Operator identifier |
| operator_role | string | yes | Operator role |
| reviewed_by | string | no | Reviewer identifier (if different from operator) |
| review_comment | string | no | Reviewer feedback |
| created_at | datetime (ISO 8601) | yes | When override was requested |
| applied_at | datetime (ISO 8601) | no | When override was applied |
| expires_at | datetime (ISO 8601) | no | Expiration timestamp |
| audit_trail_id | string | yes | Reference to immutable audit log |

### Constraints
- Overrides cannot be modified after `status = applied`.
- `security_override` and `agency_override` require `operator_role` with security clearance.
- All override actions generate append-only audit log entries.
- Temporary overrides automatically revert to original decision at `expires_at`.

