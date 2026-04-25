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
""")
    ])

