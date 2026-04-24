def analyze_metrics(metrics):

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
            "change":change,
            "severity":severity,
            "is_bad":is_bad
        }

        if is_bad and severity == "high":
            critical_issues.append(key)
        elif is_bad:
            warnings.append(key)

        return {
            "insights":insights,
            "critical_issues":critical_issues,
            "warnings":warnings
        }