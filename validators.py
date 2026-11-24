from datetime import datetime

def validate_report_data(data):
    errors = []
    try:
        datetime.strptime(data["inspection_date"], "%Y-%m-%d")
    except (ValueError, KeyError):
        errors.append("Inspection date must use YYYY-MM-DD format.")

    for field, label in (
        ("project", "Project name"),
        ("location", "Inspection location"),
        ("inspector", "Inspector"),
        ("work_description", "Work description"),
    ):
        if not str(data.get(field, "")).strip():
            errors.append(f"{label} is required.")

    for field, label in (
        ("ambient_temperature", "Ambient temperature"),
        ("concrete_temperature", "Concrete temperature"),
    ):
        value = str(data.get(field, "")).strip()
        if value:
            try:
                float(value)
            except ValueError:
                errors.append(f"{label} must be numeric when provided.")

    for index, observation in enumerate(data.get("observations", []), start=1):
        if observation.get("status") not in {"PASS", "FAIL", "N/A"}:
            errors.append(f"Observation {index} has an invalid status.")
    return errors
