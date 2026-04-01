# Auto-Eval-Pipeline
A production-ready LLM-as-a-Judge evaluation framework. Automates AI benchmarking using Gemini 2.5 Flash Lite, structured Pydantic outputs, and resilient rate-limit handling. Built for high-velocity, zero-cost AI quality assurance.

# SentinEval: Automated LLM-as-a-Judge Framework

**SentinEval** is a high-velocity, deterministic evaluation pipeline designed to replace manual "vibe checks" with data-driven AI benchmarking. It leverages a strong LLM (the Judge) to audit, score, and provide reasoning for the outputs of other AI systems, ensuring quality at scale without human intervention.

---

## The Core Problem
In production AI engineering, evaluating system prompts is a bottleneck. Manually reviewing 100+ responses for a single prompt change is unscalable. SentinEval automates this QA process by treating the LLM as a logical auditor that outputs structured, parsable performance data.

## 🧠 Technical Highlights
* **Structured Outputs:** Utilizes `Pydantic` and response schemas to force the Judge into returning strict JSON. This ensures the data pipeline never crashes due to "chatty" LLM responses.
* **Rate-Limit Resiliency:** Built-in backoff strategies (`time.sleep`) to handle high-volume batch processing while staying within free-tier API quotas.
* **Deterministic Grading:** Configured with low temperature ($T = 0.1$) to prioritize consistency and accuracy over creativity.
* **High-Velocity Architecture:** Powered by the `gemini-2.5-flash-lite` model for near-instant inference at zero cost.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Auto-Eval-Pipeline.git
cd Auto-Eval-Pipeline
```

