from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,SystemMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    temperature=0
)

system_prompt = f"""
You are a Product Manager in a product launch war room.
Your job is to : 
1. Define Success criteria for the launch 
2. Assess User Impact based on metrics and feedback
3. Frame the go/no-go decision based on business priorities
4. Recommend Proceed / Pause / Roll Back with clear reasoning

Be direct and decisive. Reference specific metrics and user impact numbers.
No fluff. This is a war room, decisions matter.
"""

def run_pm(state: dict) -> dict:

    metrics = state["metrics"]
    realease_notes = state["realease_notes"]
    analyst_report = state["analyst_report"]

    print("\n[PM AGENT] Evaluating launch decision...")

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
Release info:
{realease_notes}
Analyst Report:
{analyst_report}

Key Metrics Summary:
- DAU trend: {metrics["dau"]}
- Crash rate trend: {metrics["crash_rate"]}
- Payment failure rate: {metrics["payment_failure_rate"]}
- Retention D1: {metrics["retention_d1"]}
- Retention D7: {metrics["retention_d7"]}

Based on the above:
1. What were the success criteria for this launch?
2. Are we meeting them?
3. What is the user impact (scale + severity)?
4. Your go/no-go recommendation: Proceed / Pause / Roll Back
5. Key reasoning in 3-4 bullet points
        """)
    ])

    print("[PM AGENT] Report ready")

    return {
        "pm_report":response.content
    }