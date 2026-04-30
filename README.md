# WarRoom AI

A multi-agent system that simulates a cross-functional war room during a product launch. The system analyzes a mock dashboard of metrics and user feedback, then produces a structured launch decision: Proceed, Pause, or Roll Back, along with a full action plan.

---

## Overview

WarRoom AI orchestrates five specialized agents using LangGraph. Each agent has a distinct responsibility and passes its output to the next agent in the pipeline. The final orchestrator synthesizes all reports into a structured JSON decision.

### Agent Pipeline

```
Data Analyst Agent
      |
      v
Product Manager Agent
      |
      v
Marketing Agent
      |
      v
Risk Agent
      |
      v
Orchestrator  -->  output/decision.json
```

### Agent Responsibilities

- **Data Analyst Agent** — calls the `analyze_metrics` tool to detect trends, anomalies, and compute a health score across all product metrics
- **Product Manager Agent** — evaluates success criteria, assesses user impact, and frames the go/no-go decision
- **Marketing Agent** — calls the `sentiment_summary` tool to analyze user feedback, identify top complaints, and assess reputational risk
- **Risk Agent** — challenges assumptions from other agents, identifies worst-case scenarios, and produces a risk register
- **Orchestrator** — synthesizes all four reports into a final structured JSON output

---

## Project Structure

```
WarRoom AI/
├── agents/
│   ├── data_analyst.py
│   ├── product_manager.py
│   ├── marketing.py
│   └── risk.py
├── data/
│   ├── metrics.json
│   ├── user_feedback.json
│   └── release_notes.txt
├── orchestrator/
│   └── flow.py
├── tools/
│   ├── metric_tool.py
│   └── sentiment_tool.py
├── output/
│   └── decision.json
├── main.py
├── requirements.txt
├── .env
└── README.md
```

---

## Setup

### Prerequisites

- Python 3.10 or higher
- A free Groq API key from https://console.groq.com

### Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/warroom-ai.git
cd warroom-ai
```

2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

---

## Running the System

```bash
python main.py
```

The system will run all agents sequentially and print each agent's progress to the console. The final decision will be printed and saved to `output/decision.json`.

---

## Example Output

```json
{
  "decision": "Roll Back",
  "rationale": {
    "key_drivers": [
      "severe degradation in overall product performance",
      "significant decline in key metrics post-launch",
      "high reputational risk"
    ],
    "metric_references": [
      "crash_rate increased by 427.27% to 5.8",
      "payment_failure_rate increased by 172.0% to 6.8%",
      "dau decreased by 30.0% to 8400"
    ],
    "feedback_summary": "Users are experiencing severe issues with the latest update, including app crashes, payment failures, and performance problems."
  },
  "risk_register": [...],
  "action_plan": [...],
  "communication_plan": {
    "internal": "...",
    "external": "..."
  },
  "confidence_score": 90,
  "confidence_boosters": [...]
}
```

---

## Tools

### analyze_metrics (metric_tool.py)

Ingests the metrics JSON and computes for each metric:
- Trend direction (increasing or decreasing)
- Overall percentage change from Day 1 to Day 14
- Post-launch change (pre vs post Day 7 average)
- Severity classification (low, medium, high)
- Critical issues and warnings list
- Overall system health score (0-100)

### sentiment_summary (sentiment_tool.py)

Ingests the user feedback JSON and computes:
- Overall sentiment (Positive, Negative, Neutral)
- Counts and negative ratio
- Top 5 recurring issues by mention frequency
- Per-platform breakdown (Play Store, App Store, Twitter)

---

## Input Data

### metrics.json

Time series data for 14 days covering: DAU, activation rate, D1/D7 retention, crash rate, API latency (p95), payment failure rate, support ticket volume, and funnel completion rate.

### user_feedback.json

30 user feedback entries with text and source fields, sourced from Play Store, App Store, and Twitter. Includes a realistic mix of positive, negative, and neutral entries with recurring themes around crashes, payment failures, and performance.

### release_notes.txt

Describes the v2.5.0 feature release (real-time chat, media sharing, UI redesign) and known risks including high memory usage and increased API load.

---

## Traceability

All agent steps and tool call results are logged to the console during execution. To view the trace, run the system and observe the output prefixed with agent names:

```
[DATA ANALYST] Starting analysis...
[DATA ANALYST] Tool result: {...}
[DATA ANALYST] Report ready

[PM AGENT] Evaluating launch decision...
[PM AGENT] Report ready

[MARKETING AGENT] Analyzing customer sentiment...
[MARKETING AGENT] Sentiment result: {...}
[MARKETING AGENT] Report ready

[RISK AGENT] Challenging assumptions and identifying risks...
[RISK AGENT] Report Ready

[ORCHESTRATOR] Synthesizing all reports into final decision...
[ORCHESTRATOR] Final decision ready
```

The final structured output is saved at `output/decision.json` after every run.

---

## Environment Variables

| Variable | Description |
|---|---|
| GROQ_API_KEY | API key from console.groq.com (free tier) |

---

## Dependencies

```
langchain-groq
langgraph
langchain-core
python-dotenv
```

Install all with:

```bash
pip install -r requirements.txt
```

---

## Model

All agents use `llama-3.3-70b-versatile` via Groq with `temperature=0` for deterministic, structured outputs.
