from pathlib import Path
from datetime import datetime
import html
import json
import re

def _safe_name(value):
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_")
    return cleaned or "inspection"

def generate_html_report(data, output_dir="inspection_reports"):
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{_safe_name(data['report_number'])}.html"

    def esc(value):
        return html.escape(str(value or "Not recorded"))

    rows = []
    for number, item in enumerate(data.get("observations", []), start=1):
        rows.append(
            "<tr>"
            f"<td>{number}</td><td>{esc(item['description'])}</td>"
            f"<td class='status'>{esc(item['status'])}</td>"
            f"<td>{esc(item.get('notes'))}</td>"
            f"<td>{esc(item.get('corrective_action'))}</td></tr>"
        )
    observation_rows = "\n".join(rows) or "<tr><td colspan='5'>No observations entered.</td></tr>"

    fields = [
        ("Report number", "report_number"), ("Project", "project"),
        ("Inspection location", "location"), ("Inspection date", "inspection_date"),
        ("Inspector", "inspector"), ("Weather", "weather"),
        ("Ambient temperature (°F)", "ambient_temperature"),
        ("Concrete temperature (°F)", "concrete_temperature"),
        ("Mix design / ID", "mix_design"), ("Truck ticket", "truck_ticket"),
        ("Drawing / specification references", "drawing_spec"),
    ]
    details = "\n".join(
        f"<tr><th>{html.escape(label)}</th><td>{esc(data.get(key))}</td></tr>"
        for label, key in fields
    )

    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Concrete Inspection Report - {esc(data['report_number'])}</title>
<style>
body{{font-family:Arial,sans-serif;color:#222;margin:32px;line-height:1.4}}
h1{{margin-bottom:4px}} .sub{{color:#555;margin-top:0}}
table{{border-collapse:collapse;width:100%;margin:14px 0 22px}}
th,td{{border:1px solid #bbb;padding:8px;text-align:left;vertical-align:top}}
th{{background:#f1f3f5;width:28%}}
.status{{font-weight:bold;white-space:nowrap}}
.banner{{padding:12px;border:1px solid #999;margin:18px 0;font-weight:bold}}
.notes{{white-space:pre-wrap;border:1px solid #bbb;padding:12px}}
footer{{margin-top:32px;font-size:12px;color:#555}}
@media print{{body{{margin:15mm}} .no-print{{display:none}}}}
</style></head><body>
<h1>CONCRETE INSPECTION REPORT</h1>
<p class="sub">Generated: {esc(data['generated_at_utc'])}</p>
<div class="banner">Overall status: {esc(data['overall_status'])}
&nbsp; | &nbsp; PASS: {data['pass_count']} &nbsp; FAIL: {data['fail_count']}
&nbsp; N/A: {data['na_count']}</div>
<h2>Project and Inspection Information</h2>
<table>{details}</table>
<h2>Work Description</h2>
<div class="notes">{esc(data['work_description'])}</div>
<h2>Inspection Observations</h2>
<table><thead><tr><th>#</th><th>Inspection item / observation</th>
<th>Status</th><th>Comments / measured values</th><th>Corrective action / follow-up</th>
</tr></thead><tbody>{observation_rows}</tbody></table>
<h2>Inspector Sign-off</h2>
<table><tr><th>Inspector signature</th><td style="height:42px"></td>
<th>Date</th><td></td></tr><tr><th>Reviewed by</th><td style="height:42px"></td>
<th>Date</th><td></td></tr></table>
<footer>
This report is a field documentation aid. It does not independently establish
acceptance or code compliance. Verify observations and test results against
approved drawings, specifications, the project inspection and testing plan,
applicable codes and referenced standards. Attach supporting test reports,
delivery tickets and photographs as required by project document control.
</footer>
<p class="no-print">To create a PDF, use your browser's Print function and select “Save as PDF”.</p>
</body></html>"""
    path.write_text(document, encoding="utf-8")
    return path

def generate_json_report(data, output_dir="inspection_reports"):
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{_safe_name(data['report_number'])}.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path
