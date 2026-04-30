from langgraph.graph import START,END
from langchain_groq import ChatGroq
from agents.data_analyst import run_data_analyst
from agents.marketing import run_marketing
from agents.product_manager import run_pm
from agents.risk import run_risk
from langchain_core.messages import HumanMessage,SystemMessage
from typing import TypedDict
from dotenv import load_dotenv
import json

load_dotenv()
# State
class WarRoomState(TypedDict):

    metrics:dict
    feedback:list
    realease_notes:str

    analyst_report:str
    pm_report:str
    marketing_report:str
    risk_report:str

    final_decision:str

# Orchestrator Nodes
llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    temperature=0
)

ORCHESTRATOR_PROMPT = """
You are the War Room Orchestrator. You have received reports from four agents:
Data Analyst agent,Marketing agent,Product Manager agent,Risk agent 

Your job is to synthesize everything and produce a final structured decision.
You must output ONLY valid JSON. No extra text, no markdown, no explanation.
"""

def run_orchestrator(state:dict)-> dict:

    print("\n[ORCHESTRATOR] Synthesizing all reports into final decision...")

    response = llm.invoke([
        SystemMessage(content=ORCHESTRATOR_PROMPT),
        HumanMessage(content=f"""
Analyst Report : {state["analyst_report"]}
PM Report : {state["pm_report"]}
Marketing Report : {state["marketing_report"]}
Risk Report : {state["risk_report"]}

Produce a final JSON structure with exactly this structure:
{
    {
        "Decision": "Proceed | Pause | Roll Back",

        "Rationale": {{
            "key_drivers":["driver1","driver2","driver3"],
            "metric_reference":["metric1 changed by X%", "metric2 at Y"],
            "feedback_summary": "one sentence summary"
            }},
        "Risk register": [{{
        "risk":"description",
        "likelihood":"Low | Medium | High",
        "impact": "Low | Medium | High",
        "mitigation": "action"
        }}
        ],
        "Action Plan":[
            {
                {
                    "timeframe":"0-24h | 24-48h",
                    "action":"description",
                    "owner": "Engineering | PM | Marketing | Support"
                }
            }
        ],
        "Communication plan": {
            {
                "internal": "message to engineering and leadership",
                "external": "message to users on app stores and social media"
            }
        },
        "confidence_score": 0-100,
        "confidence_boosters": ["what would increase confidence"]
    }
}
""")
    ])

    try:
        raw = response.content.strip()

        if raw.startswith("'''"):
            raw = raw.split("'''")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        final_response = json.loads(raw.strip())
    except Exception as e:
        print(f"[ORCHESTRATOR] JSON parse error: {e}")
        final_decision = {"error": "Failed to parse decision", "raw": response.content}

    
    print("[ORCHESTRATOR] Final decision ready")

    return {"final_decision":final_decision}






