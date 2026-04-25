from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    temperature=0
)

system_prompt = f"""
You are a Risk and critic expert in a product lauch war room.
Your job is to:
1. Challenges assumptions made by other agents.
2. Identify risks that others may have missed or downplayed.
3. Request additional evidence where confidence is low.
4. Produce a structured risk register with mitigation strategies

Be skeptical. Be thorough. Your job is to poke holes.
Reference specific metrics, feedback themes, and agent reports.
No fluff. This is a war room.
"""

def run_risk(state:dict) -> dict:

    analyst_report = state["analyst_report"]
    pm_report = state["pm_report"]
    marketing_report = state["marketing_report"]
    metrics = state["metrics"]

    print("\n[RISK AGENT] Challenging assumptions and identifying risks...")

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
You have recieved reports from three agents.Review them critically.
                     
Data Analyst Report:
{analyst_report}

PM Report:
{pm_report}

Marketing Report:
{marketing_report}

Raw Metrics (for reference):
        - Crash rate: {metrics["crash_rate"]}
        - Payment failure rate: {metrics["payment_failure_rate"]}
        - API latency p95: {metrics["api_latency_p95"]}
        - Support tickets: {metrics["support_tickets"]}

        Now produce a risk report covering:
        1. Assumptions being made that may be wrong
        2. Risks that are being underplayed
        3. Worst case scenario if rollout continues as-is
        4. Risk register (at least 3 risks):
           - Risk description
           - Likelihood (Low/Medium/High)
           - Impact (Low/Medium/High)
           - Mitigation strategy
        5. What additional evidence or data would increase confidence?
""")
    ])

    print("[RISK AGENT] Report Ready")

    return {"risk_report": response.content}