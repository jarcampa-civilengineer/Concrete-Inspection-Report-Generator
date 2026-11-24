from datetime import datetime, timezone

def create_report_data(values):
    """Build a consistent report record and add a generation timestamp."""
    return {
        **values,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "observation_count": len(values.get("observations", [])),
        "pass_count": sum(o["status"] == "PASS" for o in values.get("observations", [])),
        "fail_count": sum(o["status"] == "FAIL" for o in values.get("observations", [])),
        "na_count": sum(o["status"] == "N/A" for o in values.get("observations", [])),
    }
