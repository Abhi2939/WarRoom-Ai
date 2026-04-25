from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage,SystemMessage
from tools.sentiment_tool import sentiment_summary
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model = "llama-3.3-70b-versatile",
    temperature=0
)

llm_with_tool = llm.bind_tools([sentiment_summary])

system_prompt = f"""
You are a Marketing and Communication lead in a product launch war room.
Your job is to 
1. Assess customer perception and sentiment from user feedback
2. Identify the loudest recurring complaints
3. Evaluate reputational risk if the launch continues
4. Recommend internal and external communication actions

Be specific about which platforms have the most negative feedbacks.
Reference actual feedback themes and percentages in your report.
No fluff. Be direct.
"""

def run_marketing(state:dict) -> dict:

    feedback = state["feedback"]
    pm_report = state["pm_report"]

    print("\n[MARKETING AGENT] Analyzing customer sentiment...")

    tool_call_msg = llm_with_tool([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
Analyse this user feedback and call the summerize_sentiment tool : {feedback}
""")
    ])

    if tool_call_msg.tool_calls:
        for tc in tool_call_msg.tool_calls:
            if tc["name"] == "sentiment_summary":
                tool_result = sentiment_summary.invoke(tc["args"])
                print(f"[MARKETING AGENT] Sentiment result: {tool_result}")

    
    final_response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"""
PM Report:
        {pm_report}

        Sentiment Analysis Result:
        {tool_result}

        Raw Feedback Sample:
        {feedback[:5]}

        Now write a concise marketing report covering:
        1. Overall sentiment score and what it signals
        2. Top 3 recurring complaints from users
        3. Platform breakdown (where is noise loudest?)
        4. Reputational risk level (Low / Medium / High / Critical)
        5. Recommended communication actions:
           - Internal message (to engineering/leadership)
           - External message (to users on app stores / social)
""")
    ])

    print("[MARKETING AGENT] Report ready")

    return {
        "marketing_report":final_response.content
    }


