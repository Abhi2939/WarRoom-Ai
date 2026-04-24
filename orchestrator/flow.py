from typing import TypedDict

class WarRoomState(TypedDict):

    metrics:dict
    feedback:list
    realease_notes:str
    analyst_report:str
    pm_report:str
    marketing_report:str
    risk_report:str
    final_decision:str