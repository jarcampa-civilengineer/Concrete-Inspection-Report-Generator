# Concrete Inspection Report Generator

A small command-line Python application for preparing structured concrete
inspection reports and maintaining a simple report register.

## Features
- Captures project, inspection location, date, inspector and weather information.
- Records mix design, truck ticket and concrete temperature information.
- Allows multiple inspection observations with PASS / FAIL / N/A status.
- Captures comments, measured values and corrective-action follow-up.
- Generates an HTML report that can be printed or saved as PDF from a browser.
- Exports a JSON copy and appends a summary row to a CSV report register.

## Project files
- `main.py` — interactive data-entry workflow.
- `models.py` — report data structure and summary counts.
- `validators.py` — validates required fields, date and numeric values.
- `checklist.py` — suggested concrete inspection prompts.
- `report_generator.py` — creates HTML and JSON reports.
- `storage.py` — maintains the CSV report register.
- `README.md` — usage and limitations.

## Requirements
Python 3.8 or newer. No third-party packages are required.

## Run
```bash
python main.py
```

Reports are saved in `inspection_reports/`. To use another output folder:
```bash
python main.py --output project_reports
```

Open the generated `.html` file in a browser. Use Print -> Save as PDF to create
a PDF copy.

## Suggested inspection topics
The included prompts are examples, not a complete acceptance checklist. Add
project-specific requirements for reinforcement, formwork, embeds, delivery
tickets, fresh concrete testing, placement, consolidation, finishing, curing,
sampling and environmental conditions as applicable.

## Engineering / QA-QC note
This program organizes observations; it does not determine acceptance, calculate
structural capacity, validate mix-design compliance or replace inspection/testing.
Use the approved drawings, specifications, inspection and testing plan, adopted
building code and applicable referenced standards. Record actual measurements,
units, test methods, sample IDs and results. Attach supporting photographs,
batch tickets and laboratory reports under the project's document-control
procedures. A FAIL status is a prompt for documented review and follow-up, not
an automated engineering disposition.
