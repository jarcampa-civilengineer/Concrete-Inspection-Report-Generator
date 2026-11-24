import argparse
from datetime import datetime
from checklist import DEFAULT_CHECKLIST
from models import create_report_data
from report_generator import generate_html_report, generate_json_report
from storage import save_report_record
from validators import validate_report_data

def ask(label, required=False, default=""):
    prompt = f"{label}"
    if default:
        prompt += f" [{default}]"
    prompt += ": "
    while True:
        value = input(prompt).strip()
        if not value:
            value = default
        if value or not required:
            return value
        print("This field is required.")

def main():
    parser = argparse.ArgumentParser(description="Concrete Inspection Report Generator")
    parser.add_argument("--output", default="inspection_reports", help="Output folder")
    args = parser.parse_args()

    print("\nCONCRETE INSPECTION REPORT GENERATOR")
    print("=" * 38)
    metadata = {
        "report_number": ask("Report number", default=f"CIR-{datetime.now():%Y%m%d-%H%M%S}"),
        "project": ask("Project name", True),
        "location": ask("Inspection location / placement ID", True),
        "inspection_date": ask("Inspection date (YYYY-MM-DD)", True, datetime.now().strftime("%Y-%m-%d")),
        "inspector": ask("Inspector name", True),
        "weather": ask("Weather conditions"),
        "ambient_temperature": ask("Ambient temperature (°F)"),
        "concrete_temperature": ask("Concrete temperature (°F)"),
        "mix_design": ask("Concrete mix design / ID"),
        "truck_ticket": ask("Truck ticket number"),
        "drawing_spec": ask("Drawing / specification references"),
        "work_description": ask("Work inspected / concrete placement description", True),
    }

    observations = []
    print("\nAdd inspection observations. Leave the description blank to finish.")
    while True:
        description = ask("Observation / inspection item")
        if not description:
            break
        while True:
            status = ask("Status [PASS / FAIL / N/A]", default="N/A").upper()
            if status in {"PASS", "FAIL", "N/A"}:
                break
            print("Enter PASS, FAIL, or N/A.")
        observations.append({
            "description": description,
            "status": status,
            "notes": ask("Comments / measured values"),
            "corrective_action": ask("Corrective action / follow-up"),
        })

    metadata["observations"] = observations
    metadata["overall_status"] = (
        "ACTION REQUIRED" if any(o["status"] == "FAIL" for o in observations)
        else "DOCUMENTED - REVIEW REQUIRED"
    )

    errors = validate_report_data(metadata)
    if errors:
        print("\nThe report could not be generated:")
        for error in errors:
            print(f"- {error}")
        return

    data = create_report_data(metadata)
    html_path = generate_html_report(data, args.output)
    json_path = generate_json_report(data, args.output)
    save_report_record(data, args.output)
    print("\nReport generated successfully.")
    print(f"HTML report (open in a browser and print to PDF): {html_path}")
    print(f"JSON report: {json_path}")
    print(f"Report register: {Path(args.output) / 'report_register.csv'}")

if __name__ == "__main__":
    main()
