import json
from orchestrator.flow import warRoom
from dotenv import load_dotenv
import os

load_dotenv()

def load_data():

    with open("data/metrics.json","r") as f:
        metrics = json.load(f)

    with open("data/user_feedback.json","r") as f:
        user_feedback = json.load(f)
    with open("data/release_notes.txt","r") as f:
        release_notes = f.read()

    return metrics,user_feedback,release_notes

def save_output(final_decision:dict):
    os.makedirs("output",exist_ok=True)
    with open("output/decision.json","w") as f:
        json.dump(final_decision,f,indent=2)
    print("\n[MAIN] Final decision saved to output/decision.json")


def main():

    print("=" * 50)
    print("       WARROOM AI - LAUNCH DECISION SYSTEM")
    print("=" * 50)

    metrics,user_feedback,release_notes = load_data()

    initial_state = {
    "metrics":metrics,
    "feedback":user_feedback,
    "release_notes":release_notes,
    "analyst_report": "",
    "pm_report": "",
    "marketing_report": "",
    "risk_report": "",
    "final_decision": {}
    }

    print("\n[MAIN] Starting WarRoom AI...\n")
    final_state = warRoom.invoke(initial_state)

    print("\n" + "=" * 50)
    print("           FINAL DECISION")
    print("=" * 50)

    print(json.dumps(final_state["final_decision"],indent = 2))

    save_output(final_state["final_decision"])

if __name__ == "__main__":
    main()
