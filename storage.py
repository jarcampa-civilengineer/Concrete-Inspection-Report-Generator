import csv
from pathlib import Path

REGISTER_FIELDS = [
    "report_number", "inspection_date", "project", "location", "inspector",
    "overall_status", "observation_count", "pass_count", "fail_count", "na_count"
]

def save_report_record(data, output_dir="inspection_reports"):
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "report_register.csv"
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=REGISTER_FIELDS)
        if new_file:
            writer.writeheader()
        writer.writerow({field: data.get(field, "") for field in REGISTER_FIELDS})
    return path
