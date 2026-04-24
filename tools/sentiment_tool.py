from langchain_core.tools import tool

@tool
def sentiment_summary(feedback:list) -> dict:

    """
    Analyzes user feedback list and returns sentiment summary,
    top issues, and source distribution.
    """

    negative_words = ["crash", "slow", "bug", "error", "frustrat", "broken", "laggy", "unusable", "ruined", "stuck", "fail", "issue", "problem", "terrible", "degraded"]
    positive_words = ["love", "great", "good", "clean", "modern", "useful", "smooth", "happy", "fine"]

    neg,pos,neu = 0,0,0
    issues = {}

    issue_keywords = {
        "crash": "app crashes",
        "slow": "performance/lag",
        "laggy": "performance/lag",
        "payment": "payment failures",
        "fail": "payment failures",
        "sync": "message sync",
        "login": "login issues",
        "freeze": "app freezes",
        "image": "image sending crash",
        "memory": "memory issues"
    }

    for f in feedback:
        text = f.lower()
        neg_flag = any(word in text for word in negative_words)
        pos_flag = any(word in text for word in positive_words)

        if neg_flag and not pos_flag:
            neg += 1
        elif pos_flag and not neg_flag:
            pos += 1
        else:
            neu += 1
        
        for key,label in issue_keywords.items():
            if key in text:
                issues[label] = issues.get(label,0) + 1
    
    total = len(feedback)

    top_issues = sorted(issues.items(), key=lambda x: x[1], reverse=True)[:5]

    if neg > pos:
        overall = "Negative"
    elif pos > neg:
        overall = "Positive"
    else:
        overall = "Neutral"

    return {
        "overall_sentiment":overall,
        "counts": {
            "positive":pos,
            "negative":neg,
            "neutral":neu
        },
        "negative_ratio": round(neg/total,2),
        "top_issues":top_issues,
        "summary": f"{neg} negative, {pos} positive, {neu} neutral feedback points"
    }
    

