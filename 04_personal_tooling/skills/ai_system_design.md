# Skill: AI System Design

## Goal
Design systems that integrate AI into software engineering workflows with security-first principles.

## Components
- agents
- orchestration
- data pipelines
- feedback loops
- prompt sanitization
- output validation
- agency boundaries
- plugin security

## Principles
- explainability
- reliability
- human oversight
- defense-in-depth
- least privilege for agents
- secure-by-default outputs

## LLM Security Design Patterns

### Prompt Injection Prevention
- Instruction hierarchy: system > developer > user priority
- Content separation: clear delimiters between user content and instructions
- Override detection: scan inputs for injection patterns
- Indirect injection defense: treat external content (RAG, search) as untrusted

### Output Validation
- Schema validation: validate all LLM output against expected schemas
- Toxicity scoring: score outputs for harmful content before downstream use
- Encoding: encode outputs before rendering (HTML, JS, SQL)
- Sandboxed execution: run LLM-generated code in isolated environments

### Training Data Poisoning Detection
- Data provenance: track and verify origin of all training/fine-tuning data
- Trigger detection: scan training data for known backdoor patterns
- Behavior regression: test model behavior against baseline after training changes
- Split-view validation: detect inconsistent data views across pipeline stages

### Agency Boundary Design
- Action approval: require human confirmation for sensitive actions
- Credential masking: hide credentials from agent context
- Role boundary: enforce strict role-based permissions
- Decision classification: classify decisions by risk level (auto, review, block)

### Plugin Security Architecture
- Least privilege: minimum required permissions per plugin
- Tool validation: validate all tool calls before execution
- Input schema: strict input schema for each plugin
- Response sanitization: sanitize plugin responses before model processing
- Audit logging: log all plugin calls for security review

## Anti-Patterns
- Trusting LLM output without validation
- Granting agents unrestricted access to systems
- Using plugins without input/output validation
- Training on unverified third-party data
- Exposing system prompts or credentials to model context

---
*Last updated: 2026-05-18*
