# OWASP Top 10 for LLM — Implementation Plan

Plan de trabajo para extender el CORE con cobertura completa de OWASP Top 10 for LLM, integrando la taxonomía de seguridad en `red_team_suite.md`, los data contracts, skills y flujos existentes.

---

## Current Coverage (Gap Analysis)

| OWASP LLM | Category | Actual Coverage | Action |
|-----------|----------|-----------------|--------|
| LLM01 | Prompt Injection | ✅ red_team_suite.md (Direct Override, Contextual Embedding, Recursive Injection) | Refinar |
| LLM02 | Insecure Output Handling | ❌ No cubierto | Agregar |
| LLM03 | Training Data Poisoning | ❌ No cubierto | Agregar |
| LLM04 | Model Denial of Service | ❌ No cubierto | Agregar |
| LLM05 | Supply Chain Vulnerabilities | ❌ No cubierto | Agregar |
| LLM06 | Sensitive Information Disclosure | ✅ red_team_suite.md (Membership Inference, Model Inversion) | Refinar |
| LLM07 | Insecure Plugin Design | ❌ No cubierto | Agregar |
| LLM08 | Excessive Agency | ❌ No cubierto | Agregar |
| LLM09 | Overreliance | ⚠️ Parcial (cobertura implícita en testing general) | Agregar |
| LLM10 | Model Theft | ❌ No cubierto | Agregar |

---

## Work Plan — 6 Weeks

---

### Week 1 — Research & Foundation

**Objetivo:** Entender a fondo cada categoría faltante y diseñar el esquema de integración al CORE.

| Tarea | Descripción | Artefacto |
|-------|-------------|-----------|
| 1.1 | Estudiar OWASP LLM Top 10 oficial (leer cada categoría, vectores de ataque, mitigaciones) | Research notes |
| 1.2 | Mapear cada categoría contra los componentes del CORE (qué skills, qué contracts, qué templates aplican) | Mapping matrix |
| 1.3 | Diseñar el esquema de test case extendido para incluir campos específicos LLM (model_version, plugin_id, tool_def, etc.) | Extended test case schema |
| 1.4 | Identificar qué skills de 04_personal_tooling/skills/ necesitan actualización | Skills audit |

**Deliverable:** Mapping matrix + extended schema draft

---

### Week 2 — LLM02 (Insecure Output Handling) + LLM04 (Model DoS)

**Objetivo:** Agregar cobertura para Output Handling y Denial of Service.

| Tarea | Descripción | Artefacto |
|-------|-------------|-----------|
| 2.1 | Diseñar test cases para LLM02: output que ejecuta código no sanitizado, XSS via LLM output, markdown injection | Test cases JSON |
| 2.2 | Diseñar test cases para LLM04: input recursivo, consumo excesivo de tokens, concurrent requests | Test cases JSON |
| 2.3 | Definir métricas específicas: output toxicity score, token exhaustion threshold, latency degradation | Metrics definitions |
| 2.4 | Actualizar `red_team_suite.md` sección AI/LLM Domain con las 2 nuevas categorías | Updated red_team_suite.md |

**Deliverable:** red_team_suite.md actualizado con LLM02 + LLM04

---

### Week 3 — LLM05 (Supply Chain) + LLM07 (Insecure Plugin Design) + LLM10 (Model Theft)

**Objetivo:** Agregar cobertura para la cadena de suministro, plugins y robo de modelo.

| Tarea | Descripción | Artefacto |
|-------|-------------|-----------|
| 3.1 | Diseñar test cases para LLM05: dependencias vulnerables, modelos pre-entrenados comprometidos, poisoned datasets de terceros | Test cases JSON |
| 3.2 | Diseñar test cases para LLM07: plugin con permisos excesivos, tool injection, plugin sin validación de inputs | Test cases JSON |
| 3.3 | Diseñar test cases para LLM10: model extraction via API, weight stealing, model inversion attacks | Test cases JSON |
| 3.4 | Actualizar `data_contracts.md` para incluir registro de dependencias y plugins (supply chain contract) | Updated data_contracts.md |

**Deliverable:** red_team_suite.md actualizado con LLM05 + LLM07 + LLM10 + nuevo supply chain contract

---

### Week 4 — LLM03 (Training Data Poisoning) + LLM08 (Excessive Agency)

**Objetivo:** Agregar cobertura para envenenamiento de datos y agencia excesiva del modelo.

| Tarea | Descripción | Artefacto |
|-------|-------------|-----------|
| 4.1 | Diseñar test cases para LLM03: backdoor triggers, data poisoning via fine-tuning, split-view poisoning | Test cases JSON |
| 4.2 | Diseñar test cases para LLM08: action execution sin confirmación, credential exposure via tool calls, privilege escalation | Test cases JSON |
| 4.3 | Actualizar `kpi_governance.md` con ejemplos específicos de seguridad LLM (poisoning detection rate, agency misuse count) | Updated kpi_governance.md |
| 4.4 | Actualizar skill `applied_ml.md` y `ai_system_design.md` con referencias a poisoning y agency | Updated skills |

**Deliverable:** red_team_suite.md actualizado con LLM03 + LLM08 + KPIs actualizados

---

### Week 5 — LLM09 (Overreliance) + Integration

**Objetivo:** Agregar cobertura para overreliance y consolidar todo en el CORE.

| Tarea | Descripción | Artefacto |
|-------|-------------|-----------|
| 5.1 | Diseñar test cases para LLM09: auto-generated content sin validación humana, hallucination acceptance, feedback loops peligrosos | Test cases JSON |
| 5.2 | Refinar LLM01 y LLM06 existentes para alinearlos completamente con OWASP | Updated test cases |
| 5.3 | Actualizar `00_project_methodology.md` — sección AI Engineering con referencias a cada OWASP categoría | Updated methodology |
| 5.4 | Actualizar `human_override_protocol.md` para incluir casos de uso específicos de LLM security overrides | Updated override protocol |

**Deliverable:** Cobertura OWASP LLM completa + methodology actualizada

---

### Week 6 — Architecture, Testing & Documentation

**Objetivo:** Documentar la arquitectura de seguridad LLM, validar cobertura y generar reporte final.

| Tarea | Descripción | Artefacto |
|-------|-------------|-----------|
| 6.1 | Documentar la arquitectura de seguridad LLM (ver sección abajo) | Architecture diagram + doc |
| 6.2 | Validar cobertura: cada OWASP categoría debe tener al menos 3 test cases | Coverage matrix |
| 6.3 | Cross-check: verificar que cada skill/template/workflow del CORE referencie correctamente la seguridad LLM donde aplique | Audit report |
| 6.4 | Generar release del módulo de seguridad LLM dentro del CORE | Changelog + version bump |

**Deliverable:** Arquitectura documentada + cobertura validada + release

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    CORE — LLM Security Module                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  02_operations/red_team_suite.md                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Security Testing Framework                               │   │
│  │  ├── Generic Structure (test case format, metrics, proc) │   │
│  │  └── Domain Example: AI/LLM Systems                     │   │
│  │       ├── LLM01 Prompt Injection    (original + refined) │   │
│  │       ├── LLM02 Insecure Output     (NEW)                │   │
│  │       ├── LLM03 Training Poisoning  (NEW)                │   │
│  │       ├── LLM04 Model DoS           (NEW)                │   │
│  │       ├── LLM05 Supply Chain        (NEW)                │   │
│  │       ├── LLM06 Info Disclosure     (original + refined) │   │
│  │       ├── LLM07 Insecure Plugin     (NEW)                │   │
│  │       ├── LLM08 Excessive Agency    (NEW)                │   │
│  │       ├── LLM09 Overreliance        (NEW)                │   │
│  │       └── LLM10 Model Theft         (NEW)                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  01_fundamentals/data_contracts.md                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Contracts                                                 │   │
│  │  ├── supply_chain_contract  (NEW) — dependencies, models  │   │
│  │  └── plugin_security_contract (NEW) — plugins, tools, api │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  01_fundamentals/kpi_governance.md                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Updated LLM KPIs:                                        │   │
│  │  ├── Poisoning Detection Rate                            │   │
│  │  ├── Plugin Misuse Count                                 │   │
│  │  ├── Agency Violation Rate                               │   │
│  │  ├── Token Exhaustion Incidents                          │   │
│  │  └── Supply Chain Vulnerability Score                    │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  02_operations/human_override_protocol.md                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Updated Override Types:                                  │   │
│  │  ├── security_override — new target_type for LLM issues  │   │
│  │  └── agency_override — override automated decisions      │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  04_personal_tooling/skills/                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Updated Skills:                                          │   │
│  │  ├── ai_system_design.md  + poisoning + agency           │   │
│  │  ├── applied_ml.md        + supply chain + model theft   │   │
│  │  └── observability_eng    + security metrics monitoring  │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  00_project_methodology.md                                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Updated AI Engineering path:                             │   │
│  │  ├── Phase 1: contracts incl. supply_chain + plugin      │   │
│  │  ├── Phase 2: execution with security test automation    │   │
│  │  └── Phase 3: monitoring with LLM security KPIs         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow (Security Evaluation)

```
Test Case Repository (JSONL)
       │
       ▼
Test Executor ──► Target LLM System
       │               │
       │               ▼
       │          Response
       │               │
       ▼               ▼
  Evaluation Engine ──► Pass/Fail + Score
       │
       ├──► red_team_results/
       │
       └──► KPI Dashboard (ASR, MTTD, Remediation Rate)
               │
               ▼
          Release Gate (Go/No-Go based on security thresholds)
```

### Integration Points

| OWASP Category | CORE Entry Point | Depends On |
|----------------|-----------------|------------|
| LLM01, LLM06 | red_team_suite.md (existing) | data_contracts.md (EvalRecord) |
| LLM02, LLM04 | red_team_suite.md (new section) | kpi_governance.md (new KPIs) |
| LLM03, LLM05 | red_team_suite.md + data_contracts.md | skills/data_engineering.md |
| LLM07, LLM08 | red_team_suite.md + human_override_protocol.md | skills/ai_system_design.md |
| LLM09 | red_team_suite.md + templates/release_quality_report.md | skills/quality_economics.md |
| LLM10 | red_team_suite.md | skills/applied_ml.md |

---

## Quick Start

Para empezar inmediatamente:

```
Week 1 → Research & mapping
Week 2 → LLM02 + LLM04 (output handling, DoS)
Week 3 → LLM05 + LLM07 + LLM10 (supply chain, plugins, model theft)
Week 4 → LLM03 + LLM08 (poisoning, agency)
Week 5 → LLM09 + integration
Week 6 → Architecture & validation
```

Cada semana produce un avance concreto en `red_team_suite.md` y sus archivos relacionados. Al final de la semana 6, el CORE cubre el 100% de OWASP Top 10 for LLM.
