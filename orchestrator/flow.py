from langgraph.graph import StateGraph,START,END
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
    release_notes:str

    analyst_report:str
    pm_report:str
    marketing_report:str
    risk_report:str

    final_decision:dict

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

    json_template = """
{
    "decision": "Proceed | Pause | Roll Back",
    "rationale": {
        "key_drivers": ["driver1", "driver2", "driver3"],
        "metric_references": ["metric1 changed by X%", "metric2 at Y"],
        "feedback_summary": "one sentence summary"
    },
    "risk_register": [
        {
            "risk": "description",
            "likelihood": "Low | Medium | High",
            "impact": "Low | Medium | High",
            "mitigation": "action"
        }
    ],
    "action_plan": [
        {
            "timeframe": "0-24h | 24-48h",
            "action": "description",
            "owner": "Engineering | PM | Marketing | Support"
        }
    ],
    "communication_plan": {
        "internal": "message to engineering and leadership",
        "external": "message to users on app stores and social media"
    },
    "confidence_score": 85,
    "confidence_boosters": ["what would increase confidence"]
}
"""

    response = llm.invoke([
        SystemMessage(content=ORCHESTRATOR_PROMPT),
        HumanMessage(content=f"""
Analyst Report : {state["analyst_report"]}
PM Report : {state["pm_report"]}
Marketing Report : {state["marketing_report"]}
Risk Report : {state["risk_report"]}

Produce a final JSON structure with exactly this structure:
{json_template}
""")
    ])

    try:
        raw = response.content.strip()
        print(f"[ORCHESTRATOR] Raw response: {raw[:200]}")
        
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0]
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0]

        final_decision = json.loads(raw.strip())
    except Exception as e:
        print(f"[ORCHESTRATOR] JSON parse error: {e}")
        final_decision = {"error": "Failed to parse decision", "raw": response.content}

    
    print("[ORCHESTRATOR] Final decision ready")

    return {"final_decision":final_decision}

# Graph

def build_graph():

    graph = StateGraph(WarRoomState)
    
    #add nodes
    graph.add_node("Data_Analyst_Agent",run_data_analyst)
    graph.add_node("Marketing_Agent",run_marketing)
    graph.add_node("PM_Agent",run_pm)
    graph.add_node("Risk_Agent",run_risk)
    graph.add_node("Orchestrator",run_orchestrator)

    #add edges
    graph.add_edge(START,"Data_Analyst_Agent")
    graph.add_edge("Data_Analyst_Agent","PM_Agent")
    graph.add_edge("PM_Agent","Marketing_Agent")
    graph.add_edge("Marketing_Agent","Risk_Agent")
    graph.add_edge("Risk_Agent","Orchestrator")
    graph.add_edge("Orchestrator",END)

    #compile graph  

    return graph.compile()

warRoom = build_graph()





