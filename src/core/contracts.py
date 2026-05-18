"""
CORE Data Contracts — Pydantic Models

Programmatic enforcement of all data contracts defined in:
  01_fundamentals/data_contracts.md

Every record type from the OWASP LLM security module is represented here.
Models are split into Input (what goes into a process) and Output (what comes out).

Version: v1.0
Last updated: 2026-05-18
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ─────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────

class EvalType(str, Enum):
    ACCURACY = "accuracy"
    SAFETY = "safety"
    LATENCY = "latency"
    TOOL_USE = "tool_use"
    HALLUCINATION = "hallucination"
    INJECTION = "injection"
    TOXICITY = "toxicity"
    AGENCY = "agency"
    EXTRACTION = "extraction"


class EvalMethod(str, Enum):
    PATTERN_MATCH = "pattern_match"
    LLM_JUDGE = "llm_judge"
    METRIC_THRESHOLD = "metric_threshold"
    HUMAN_REVIEW = "human_review"
    SCHEMA_VALIDATION = "schema_validation"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class GateDecision(str, Enum):
    AUTO_APPROVE = "auto_approve"
    MONITOR = "monitor"
    WARNING = "warning"
    REQUIRE_OVERRIDE = "require_override"
    NO_GO = "no_go"


class ChangeType(str, Enum):
    PROMPT_TEMPLATE = "prompt_template"
    MODEL_CONFIG = "model_config"
    MODEL_SWAP = "model_swap"
    AGENT_TOOL = "agent_tool"
    SAFETY_CONFIG = "safety_config"
    SYSTEM_PROMPT = "system_prompt"
    TRAINING_DATA = "training_data"


class OverrideTargetType(str, Enum):
    EVAL = "eval"
    RISK = "risk"
    GATE = "gate"
    KPI_ALERT = "kpi_alert"
    SECURITY_OVERRIDE = "security_override"
    AGENCY_OVERRIDE = "agency_override"


class OverrideStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    APPLIED = "applied"
    EXPIRED = "expired"


class DependencyType(str, Enum):
    MODEL = "model"
    DATASET = "dataset"
    LIBRARY = "library"
    PLUGIN = "plugin"
    INFRASTRUCTURE = "infrastructure"


class IntegrityStatus(str, Enum):
    VERIFIED = "verified"
    FAILED = "failed"
    UNVERIFIED = "unverified"
    OUTDATED = "outdated"


class FinishReason(str, Enum):
    STOP = "stop"
    LENGTH = "length"
    CONTENT_FILTER = "content_filter"
    ERROR = "error"


class PluginRegistrationStatus(str, Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DEPRECATED = "deprecated"


# ─────────────────────────────────────────────
# Canonical Metadata (required in all contracts)
# ─────────────────────────────────────────────

class CoreModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class CanonicalMetadata(CoreModel):
    contract_name: str
    contract_version: str = Field(..., pattern=r"^v\d+\.\d+(\.\d+)?$")
    generated_at: datetime
    source_system: str
    environment: str  # local, ci, staging, prod
    project_id: str
    release_id: Optional[str] = None
    execution_id: str
    owner: str


class CommonEnvelope(CoreModel):
    metadata: CanonicalMetadata
    payload: Dict[str, Any]


# ─────────────────────────────────────────────
# EvalRecord
# ─────────────────────────────────────────────

class EvalRecordInput(CoreModel):
    eval_id: str
    test_case_id: str
    prompt_id: str
    response_id: str
    eval_type: EvalType
    expected_behavior: str
    actual_behavior: str


class EvalRecordOutput(CoreModel):
    eval_id: str
    pass_status: bool = Field(..., alias="pass")
    score: Optional[float] = Field(None, ge=0.0, le=1.0)
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    injection_detected: Optional[bool] = None
    toxicity_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    token_count: Optional[int] = None
    latency_ms: Optional[int] = None
    compute_cost: Optional[float] = None
    agency_violation: Optional[bool] = None
    hallucination: Optional[bool] = None
    human_validated: Optional[bool] = None
    extraction_attempt_detected: Optional[bool] = None
    privacy_violation_type: Optional[str] = None
    data_leaked: Optional[str] = None
    sanitization_applied: Optional[bool] = None
    eval_method: EvalMethod
    failure_reason: Optional[str] = None
    timestamp: datetime

    @field_validator("failure_reason")
    @classmethod
    def require_failure_reason_when_failed(cls, v: Optional[str], info) -> Optional[str]:
        if info.data.get("pass_status") is False and not v:
            raise ValueError("failure_reason is required when pass_status is False")
        return v


class EvalRecord(CoreModel):
    input: EvalRecordInput
    output: EvalRecordOutput


# ─────────────────────────────────────────────
# ResponseRecord
# ─────────────────────────────────────────────

class ToolCall(CoreModel):
    tool_name: str
    parameters: Dict[str, Any]
    result: Optional[str] = None


class ResponseRecordInput(CoreModel):
    prompt_id: str
    model_version: str
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = None
    plugins_enabled: Optional[List[str]] = None


class ResponseRecordOutput(CoreModel):
    response_id: str
    prompt_id: str
    response_text: str
    latency_ms: int = Field(..., ge=0)
    token_count: int = Field(..., ge=0)
    finish_reason: FinishReason
    tool_calls: Optional[List[ToolCall]] = None
    error_message: Optional[str] = None
    timestamp: datetime


class ResponseRecord(CoreModel):
    input: ResponseRecordInput
    output: ResponseRecordOutput


# ─────────────────────────────────────────────
# PromptRecord
# ─────────────────────────────────────────────

class ConversationTurn(CoreModel):
    role: str  # user, assistant, system
    content: str


class PromptRecordInput(CoreModel):
    prompt_text: str
    category: str
    source: str
    system_prompt: Optional[str] = None
    conversation_history: Optional[List[ConversationTurn]] = None
    metadata: Optional[Dict[str, Any]] = None


class PromptRecordOutput(CoreModel):
    prompt_id: str
    prompt_text: str
    category: str
    source: str
    token_count: int = Field(..., ge=0)
    created_at: datetime
    eval_count: int = Field(..., ge=0)


class PromptRecord(CoreModel):
    input: PromptRecordInput
    output: PromptRecordOutput


# ─────────────────────────────────────────────
# RiskRecord
# ─────────────────────────────────────────────

class RiskRecordInput(CoreModel):
    change_id: str
    change_type: ChangeType
    affected_evals: List[str]
    safety_critical: bool


class RiskRecordOutput(CoreModel):
    id: str
    change_id: str
    risk_level: RiskLevel
    impact_score: float = Field(..., ge=0.0, le=1.0)
    risk_score: float = Field(..., ge=0.0)
    affected_evals: List[str]
    rationale: str
    gate_decision: GateDecision
    timestamp: datetime


class RiskRecord(CoreModel):
    input: RiskRecordInput
    output: RiskRecordOutput


# ─────────────────────────────────────────────
# OverrideRecord
# ─────────────────────────────────────────────

class OverrideRecordInput(CoreModel):
    target_id: str
    target_type: OverrideTargetType
    original_decision: str
    override_decision: str
    justification: str = Field(..., min_length=20)
    operator_id: str
    operator_role: str
    expires_at: Optional[datetime] = None
    tags: Optional[List[str]] = None
    evidence_links: Optional[List[str]] = None


class OverrideRecordOutput(CoreModel):
    override_id: str
    target_id: str
    target_type: OverrideTargetType
    status: OverrideStatus
    original_decision: str
    override_decision: str
    justification: str
    operator_id: str
    operator_role: str
    reviewed_by: Optional[str] = None
    review_comment: Optional[str] = None
    created_at: datetime
    applied_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    audit_trail_id: str


class OverrideRecord(CoreModel):
    input: OverrideRecordInput
    output: OverrideRecordOutput


# ─────────────────────────────────────────────
# SupplyChainContract
# ─────────────────────────────────────────────

class SupplyChainInput(CoreModel):
    dependency_id: str
    dependency_type: DependencyType
    name: str
    version: str
    source: str
    expected_hash: Optional[str] = None
    license: Optional[str] = None
    last_verified_at: Optional[datetime] = None
    known_vulnerabilities: Optional[List[str]] = None


class SupplyChainOutput(CoreModel):
    dependency_id: str
    integrity_status: IntegrityStatus
    risk_level: RiskLevel
    vulnerability_count: int = Field(..., ge=0)
    last_scan_at: datetime
    remediation_required: bool
    sbom_entry_id: str


class SupplyChainContract(CoreModel):
    input: SupplyChainInput
    output: SupplyChainOutput


# ─────────────────────────────────────────────
# PluginSecurityContract
# ─────────────────────────────────────────────

class PluginSecurityInput(CoreModel):
    plugin_id: str
    plugin_name: str
    version: str
    permissions: List[str]
    action_boundaries: List[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    requires_human_approval: bool
    max_calls_per_session: Optional[int] = None
    owner: str


class PluginSecurityOutput(CoreModel):
    plugin_id: str
    registration_status: PluginRegistrationStatus
    permission_violations: int = Field(..., ge=0)
    last_violation_at: Optional[datetime] = None
    validation_passed: bool
    risk_score: float = Field(..., ge=0.0, le=1.0)
    audit_trail_id: str


class PluginSecurityContract(CoreModel):
    input: PluginSecurityInput
    output: PluginSecurityOutput


# ─────────────────────────────────────────────
# Test Case (JSONL registry format)
# ─────────────────────────────────────────────

class RequiresContext(CoreModel):
    system_prompt: Optional[str] = None
    conversation_history: Optional[List[ConversationTurn]] = None
    plugins_enabled: Optional[List[str]] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = None


class DependencyCheck(CoreModel):
    dependency_name: str
    expected_version: str
    expected_hash: Optional[str] = None
    source: str  # pypi, huggingface, github, internal


class AttackVector(str, Enum):
    DIRECT = "direct"
    INDIRECT = "indirect"
    MULTI_TURN = "multi_turn"
    API = "api"
    FILE_UPLOAD = "file_upload"


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class OwaspId(str, Enum):
    LLM01 = "LLM01"
    LLM02 = "LLM02"
    LLM03 = "LLM03"
    LLM04 = "LLM04"
    LLM05 = "LLM05"
    LLM06 = "LLM06"
    LLM07 = "LLM07"
    LLM08 = "LLM08"
    LLM09 = "LLM09"
    LLM10 = "LLM10"


class TestCase(CoreModel):
    id: str
    owasp_id: OwaspId
    category: str
    subcategory: str
    severity: Severity
    attack_vector: AttackVector
    description: str
    input: str  # the prompt/payload to send
    expected_behavior: str
    success_criteria: str
    eval_method: EvalMethod
    pass_threshold: Optional[float] = Field(None, ge=0.0, le=1.0)
    toxicity_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    token_budget: Optional[int] = None
    dependency_check: Optional[DependencyCheck] = None
    agency_boundary: Optional[List[str]] = None
    human_validation_required: Optional[bool] = None
    mitigation_ref: Optional[List[str]] = None
    requires_context: Optional[RequiresContext] = None
    model_version: Optional[str] = None
    plugin_id: Optional[str] = None
