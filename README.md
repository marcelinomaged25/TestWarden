# TestWarden

TestWarden is a practical test-management planning package for organizing agile QA work. It provides a structured backlog, sprint breakdown, and weekly team plan that can be used to coordinate testing activities across a software project.

## Contents

- `TestWarden_Agile_Backlog_and_Sprints.pdf` — prioritized testing backlog and sprint planning reference.
- `TestWarden_Weekly_Sprint_Team_Plan.pdf` — weekly plan for assigning and tracking team testing work.
- `create_testwarden_backlog_pdf.py` — generates the backlog and sprint PDF.
- `create_testwarden_weekly_team_plan.py` — generates the weekly team-plan PDF.
- `arc.png` and `mermaid-diagram.png` — supporting project diagrams.

## Requirements

- Python 3.10+
- The Python packages imported by the generation scripts (for example, `reportlab` and `matplotlib`, if not already installed)

Install dependencies with:

```bash
pip install reportlab matplotlib
```

## Generate the PDFs

Run the scripts from the project directory:

```bash
python create_testwarden_backlog_pdf.py
python create_testwarden_weekly_team_plan.py
```

The generated PDF files are written to the project directory. Temporary rendering and validation output should remain under `tmp/`, which is ignored by Git.

## Purpose

The project is intended to make QA planning visible and actionable by connecting testing objectives, sprint deliverables, ownership, and weekly execution in a single set of artifacts.
