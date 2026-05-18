# Skill: Applied Machine Learning for QA

## Goal
Use ML to improve testing efficiency, risk detection, and LLM security evaluation.

## Techniques
- Classification
- Ranking models
- Time series analysis
- Anomaly detection (poisoning detection, model theft detection)
- Adversarial example classification
- Embedding-based similarity analysis

## Preferred Models
- Logistic Regression
- Random Forest
- Gradient Boosting
- Statistical tests (for poisoning detection)
- Embedding similarity models (for model theft detection)

## Neural Networks
Used selectively for:
- log analysis
- NLP tasks
- injection pattern classification
- toxicity scoring

## LLM Security ML Applications

### Supply Chain Verification (LLM05)
- Model provenance verification via hash comparison and behavioral fingerprinting
- Dataset integrity checking through statistical distribution analysis
- Dependency vulnerability correlation using SBOM data and CVE databases
- Anomaly detection in model outputs compared to baseline behavior

### Model Theft Detection (LLM10)
- Query pattern analysis to detect systematic extraction attempts
- API fingerprinting detection through output similarity analysis
- Rate-based anomaly detection for unusual query volumes
- Behavioral analysis to identify distillation attack patterns

### Data Poisoning Detection (LLM03)
- Statistical outlier detection in training data distributions
- Backdoor trigger pattern recognition in text/image datasets
- Fine-tuning impact analysis comparing pre/post behavior
- RAG corpus validation through source trust scoring

## Anti-Patterns
- Using black-box models for security decisions without explainability
- Training security detectors on insufficient adversarial examples
- Ignoring false positive rates in security ML models
- Deploying models without behavioral regression testing

---
*Last updated: 2026-05-18*
