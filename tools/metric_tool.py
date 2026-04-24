from langchain_core.tools import tool

@tool
def analyze_metrics(metrics):

    """Analyzes product metrics, detects trends, anomalies and returns health score"""

    insights = {}
    critical_issues = []
    warnings = []

    for key, values in metrics.items():
        if key == "dates":
            continue

        start = values[0]
        end = values[-1]

        change = round(((end-start)/start)*100,2) if start != 0 else 0
        trend = "increasing" if end > start else "decreasing"

        mid = len(values) // 2
        pre_avg = sum(values[:mid]) / mid
        post_avg = sum(values[mid:]) / mid
        post_launch_change = round(((post_avg - pre_avg) / pre_avg) * 100, 2)


        if key in ["crash_rate","api_latency_p95","payment_failure_rate"]:
            is_bad = trend == "increasing"
        else:
            is_bad = trend == "decreasing"

        if abs(change)>50:
            severity = "high"
        elif abs(change)>20:
            severity = "medium"
        else:
            severity = "low"
        
        insights[key] = {
            "trend":trend,
            "change_pct":change,
            "post_launch_change_pct": post_launch_change,
            "severity":severity,
            "is_bad":is_bad
        }

        if is_bad and severity == "high":
            critical_issues.append(key)
        elif is_bad:
            warnings.append(key)

    total = len(insights)
    bad_count = len(critical_issues) + len(warnings)
    health_score = round((1 - bad_count / total) * 100, 1)

    return {
        "insights":insights,
        "critical_issues":critical_issues,
        "warnings":warnings,
        "health_score":health_score
    }