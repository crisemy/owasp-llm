# Human Override Protocol

This document defines the protocol for human operators to override automatic decisions in any automated QA or AI system.

## 1. Purpose

To provide a controlled mechanism for human experts to intervene when:
- Automatic evaluations produce false positives/negatives
- Novel attack vectors are detected that require human judgment
- Business context requires exception to automated policies
- System uncertainty exceeds acceptable thresholds

## 2. Scope

This protocol applies to:
- Override of evaluation results (accuracy, safety, etc.)
- Override of risk assessments
- Override of release gates (Go/No-Go decisions)
- Override of KPI-based alerts
- **LLM Security Overrides** (`security_override`): Override automated security evaluation results for injection detection, toxicity scoring, and other LLM-specific security metrics
- **LLM Agency Overrides** (`agency_override`): Approve or override autonomous agent decisions that exceeded defined boundaries (plugin actions, tool use, data access)

## 3. Override Request Structure

Each override request MUST contain:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `override_id` | `uuid` | yes | Unique identifier for this override |
| `target_id` | `uuid` | yes | ID of the record being overridden (EvalRecord, RiskRecord, etc.) |
| `target_type` | `enum` | yes | Type of target: `eval`, `risk`, `gate`, `kpi_alert`, `security_override`, `agency_override` |
| `original_decision` | `string` | yes | The automatic decision being overridden |
| `override_decision` | `string` | yes | The human decision to apply instead |
| `justification` | `string` | yes | Detailed explanation (min 20 chars) |
| `operator_id` | `string` | yes | Identifier of the human operator |
| `operator_role` | `string` | yes | Role of operator (e.g., `safety_engineer`, `prod_owner`) |
| `timestamp` | `datetime` | yes | When override was requested (ISO 8601) |
| `expires_at` | `datetime` | no | Optional expiration for temporary overrides |
| `tags` | `array[string]` | no | Classification tags (e.g., `false_positive`, `novel_threat`) |
| `evidence_links` | `array[string]` | no | Links to supporting evidence, docs, etc. |

#### Target Type Extensions for LLM Security

| Target Type | Description | Applies To |
|-------------|-------------|-----------|
| `security_override` | Override automated security evaluation results (false positive/negative) | LLM01-LLM10 eval results, injection detection, toxicity scoring |
| `agency_override` | Override or approve autonomous agent decisions that exceeded boundaries | LLM07 (plugin actions), LLM08 (agent decisions) |

## 4. Override Workflow

### 4.1 Request Submission
1. Human operator identifies need for override via UI or API
2. Operator submits override request with all required fields
3. System validates request format and business rules
4. Request enters `pending` state

### 4.2 Review Process
1. Depending on `target_type`, request may route to specific reviewers
2. Reviewers can:
   - Approve override
   - Reject with feedback
   - Request additional information
3. All review actions are logged

### 4.3 Decision Application
1. Upon approval, override decision is applied immediately
2. Original decision is preserved in audit trail
3. System continues processing with overridden value
4. Override becomes immutable after application

### 4.4 Expiration and Review
1. Temporary overrides automatically revert at `expires_at`
2. All overrides subject to periodic review (e.g., weekly)
3. Expired overrides generate review tasks

## 5. Audit Trail Requirements

Every override action MUST generate an audit log entry containing:

- `audit_id` (uuid)
- `override_id` (reference)
- `action` (requested, approved, rejected, applied, expired)
- `actor` (operator_id or system)
- `timestamp` (ISO 8601)
- `changes` (diff of what changed)
- `ip_address` (if applicable)
- `user_agent` (if applicable)

Audit logs are append-only and tamper-evident.

## 6. Security Considerations

### 6.1 Authentication
- All override requests MUST be authenticated
- Supported methods: API keys, OAuth2, SSO (SAML/JWT)
- Anonymous overrides are prohibited

### 6.2 Authorization
- Operators can only override within their permitted domains
- Role-based access control (RBAC) determines:
  - Which target types can be overridden
  - Which justification reasons are permitted
  - Whether expiration can be set

### 6.3 Integrity
- Override requests are signed by the operator
- Audit logs are hashed and chained
- Regular integrity verification jobs

### 6.4 Confidentiality
- Justification and evidence may contain sensitive info
- Access to override details restricted to need-to-know basis
- Encryption at rest and in transit for override data

## 7. Rate Limiting and Abuse Prevention

- Maximum overrides per operator per hour: configurable
- Maximum overrides per target per day: configurable
- Automated detection of override patterns that suggest evasion
- Override spikes trigger security alerts

## 8. Integration Points

### 8.1 API Endpoints
- `POST /overrides` - Submit new override request
- `GET /overrides/{override_id}` - Get override status
- `POST /overrides/{override_id}/approve` - Approve request
- `POST /overrides/{override_id}/reject` - Reject request
- `GET /overrides` - List overrides with filtering
- `GET /audit/log` - Query audit trail

### 8.2 Events
- `override.requested`
- `override.approved`
- `override.rejected`
- `override.applied`
- `override.expired`
Each event emits structured data for monitoring and dashboards.

## 9. UI Requirements

The human review interface SHALL provide:

1. **Override Submission Form**
   - Fields matching override request structure
   - Validation and helpful tooltips
   - Attachment upload for evidence

2. **Pending Review Queue**
   - List of overrides awaiting action
   - Filtering by target_type, operator, date
   - Priority highlighting (e.g., safety-related)

3. **Override Details View**
   - Full context of the original automatic decision
   - Side-by-side comparison of original vs proposed
   - Justification and evidence display
   - Approve/reject buttons with comment required

4. **Audit Trail Browser**
   - Searchable, filterable log of all override actions
   - Export capabilities (CSV, JSON)
   - Timeline view of override activity

## 10. Compliance and Reporting

### 10.1 Metrics Tracked
- Override rate (overrides per 1000 decisions)
- Override acceptance rate (% approved)
- Mean time to review (MTTR)
- Override effectiveness (post-hoc validation)
- Common override reasons (tags analysis)

### 10.2 Reporting
- Daily override summary to platform owners
- Weekly trends report
- Monthly compliance review
- Incident report for security-relevant override patterns

## 11. Implementation Notes

### 11.1 Data Storage
- Override requests stored as `OverrideRecord` (see contracts)
- Audit logs stored separately for immutability
- Both follow CORE canonical metadata standards

### 11.2 Error Handling
- Invalid override requests return 400 with details
- Authentication failures return 401
- Authorization failures return 403
- System errors return 500 with incident ID

### 11.3 Backwards Compatibility
- Systems should gracefully handle missing override data
- Default behavior is to follow automatic decision when override unavailable
- Versioning of override schema to allow evolution

---
*Last updated: 2026-05-14*