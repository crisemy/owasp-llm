# Rollback Procedure

This document outlines the standardized rollback procedure for any QA, AI, or software system.

## Purpose

To provide a standardized procedure for rolling back changes when critical KPI violations are detected or when issues are identified post-deployment.

## Scope

This procedure applies to:
- Changes to system configurations, models, or critical components
- Changes that affect evaluation pipelines or KPI calculations
- Any change deployed to a production or staging environment

## Prerequisites

- Monitoring system must detect critical violations
- Rollback mechanism must be available (e.g., version control, deployment scripts)
- Communication channels must be established for notifying stakeholders

## Procedure

### 1. Detection

Critical violations are detected by the monitoring system or through automated alerts.

Examples of critical violations:
- Attack Success Rate (ASR) exceeds 15%
- Injection Detection Rate drops below 80%
- Output Toxicity Score exceeds 0.3
- Agency Violation Rate exceeds 1%
- Latency P99 exceeds 2000ms
- Token Exhaustion Incidents exceed 5/hour
- Supply Chain Vulnerability Score exceeds 0.5
- Any Severity 5 (Critical) failure in red team results

### 2. Alerting

Upon detection of a critical violation:
- An alert is triggered via the configured channels
- The alert includes:
  - Timestamp of detection
  - Which KPI(s) violated
  - Current values and thresholds
  - Link to the monitoring dashboard for detailed investigation

### 3. Initial Response

The on-call engineer should:
1. Acknowledge the alert
2. Verify the KPI violation is not a false positive (check dashboard, logs)
3. If confirmed, proceed to rollback

### 4. Rollback Execution

The rollback procedure consists of the following steps:

#### 4.1 Halt Deployments
- Prevent any new deployments from being promoted to the affected environment
- This can be done by:
  - Pausing the CI/CD pipeline
  - Setting a lock or flag in the deployment system

#### 4.2 Identify Last Known Good Version
- Determine the most recent version that was known to satisfy all critical KPIs
- This information should be available from:
  - Deployment history
  - KPI trend data
  - Release notes

#### 4.3 Execute Rollback
- Deploy the last known good version to the affected environment
- This may involve:
  - Running a specific deployment script
  - Using a rollback feature in the deployment tool (e.g., kubectl rollout undo, AWS CodeDeploy rollback)
  - Manually restoring from backup

#### 4.4 Validate Rollback
After rollback, verify that:
- The system is running the expected version
- Critical KPIs have returned to acceptable levels
- Basic functionality tests pass

#### 4.5 Notify Stakeholders
- Inform relevant teams (product, engineering, customer support) that rollback has been completed
- Provide a summary of the incident and next steps

#### 4.6 Post-Mortem Analysis
- Schedule a post-mortem meeting to investigate:
  - Root cause of the KPI degradation
  - Effectiveness of the detection and rollback procedure
  - Actions to prevent recurrence
- Document findings and update procedures as needed

## Roles and Responsibilities

- **On-Call Engineer**: Primary responder responsible for executing the rollback procedure
- **Platform Owner**: Responsible for maintaining the rollback mechanism and monitoring system
- **Release Manager**: Responsible for coordinating releases and ensuring rollback procedures are integrated
- **Product Owner**: Responsible for business impact assessment and communication

## Tools and Systems

- Monitoring dashboard
- Alerting system (email, Slack, PagerDuty, etc.)
- Version control system (Git, etc.)
- Deployment system (CI/CD pipeline, Kubernetes, etc.)
- Incident management system (if applicable)

## Testing and Drills

This procedure should be tested regularly to ensure:
- Detection mechanisms work
- Alerting is functional
- Rollback execution is timely and correct
- Stakeholder notification is effective

## Revision History

- Version 1.0: Initial version (2026-05-14)

---
*Last updated: 2026-05-14*