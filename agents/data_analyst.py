from langchain_groq import ChatGroq
from dotenv import load_dotenv
from tools.metric_tool import analyze_metrics
from langchain_core.messages import SystemMessage,HumanMessage

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

llm_tool = llm.bind_tools([analyze_metrics])

system_prompt = """
You are a data analyst in a product lauch war room.
Your task is to:

1. Analyses quantitative metrics and trends
2. Identify anomalies and critical degradation
3. Highlight which metrics crossed acceptable thresholds
4. Provide a confidence level on your analysis

Always reference specific metric names and numbers in your report.
Be concise and factual. No fluff.
"""

def run_data_analyst(state: dict) -> dict:

    metrics = state["metrics"]

    print("\n[DATA ANALYST] Starting analysis...")

    tool_call_msg = llm_tool([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Analyze these product metrics and call the analyze_metrics tool: {metrics}")
    ])

    tool_result = None

    if tool_call_msg.tool_calls:
        for tc in tool_call_msg.tool_calls:
            if tc["name"] == "analyze_metrics":
                tool_result = analyze_metrics.invoke(tc["args"])
                print(f"[DATA ANALYST] Tool result: {tool_result}")

    final_response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
Metrics data: {metrics}
Tool analysis result: {tool_result}

Now write a concise analyst report covering:

1.Critical metrics that are failing
2. Key trend (pre vs post launch)
3. Health score interpretation
4. Your confidence level (0-100%) in the data 
""")
    ])

    print(f"[DATA ANALYST] Report ready")

    return {
        "analyst_report":final_response.content
    }