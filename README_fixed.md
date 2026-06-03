# AI Revenue Operations & Reporting Copilot

## Project Overview

AI Revenue Operations & Reporting Copilot is a Python-based analytics and reporting pipeline that transforms sales and marketing CSV data into actionable executive reports.

The project is designed as a portfolio MVP for demonstrating practical AI and data workflow capabilities in a B2B business context.

## Business Problem

B2B sales, marketing, and revenue operations teams often prepare weekly performance reports manually.

This creates several operational problems:

- Time-consuming manual reporting
- Delayed visibility into sales pipeline performance
- Missed anomalies in revenue, lead generation, and conversion metrics
- Lack of actionable recommendations
- Repetitive weekly analysis work

This MVP addresses the problem by reading structured business data, calculating KPIs, detecting anomalies, and generating an executive Markdown report.

## MVP Scope

The current MVP works with local CSV files.

It does not include real CRM, advertising platform, or SaaS integrations yet.

### Input Files

- `data/sales_pipeline.csv`
- `data/marketing_leads.csv`
- `data/weekly_targets.csv`

### Output Files

- `outputs/kpi_summary.json`
- `outputs/anomaly_report.json`
- `outputs/weekly_revenue_report.md`

### Internal Pipeline Output

- outputs/anomaly_report.json

This file is an internal analysis artifact used for anomaly detection and action recommendation generation. It is not part of the official MVP output set.

## Current Pipeline

The current pipeline performs the following steps:

1. CSV data loading
2. Data validation
3. KPI calculation
4. Anomaly detection
5. Structured action recommendation generation
6. Markdown executive report generation

## Features

- CSV data loading
- Data schema validation
- Required field validation
- Numeric range validation
- Date validation
- Relationship check between marketing leads and sales deals
- Sales KPI calculation
- Marketing KPI calculation
- Target vs actual comparison
- Basic anomaly detection
- Executive Markdown report generation
- Single-command pipeline runner
- Structured action recommendation generation

## Calculated KPIs

### Sales KPIs

- Total open pipeline value
- Open deal count
- Won revenue
- Lost deal value
- Weighted pipeline
- Average deal value

### Marketing KPIs

- Total lead count
- Converted lead count
- Lead-to-deal conversion rate
- Average lead score
- Total estimated lead value
- Lead source performance

### Target Comparison

- Revenue target vs actual
- New leads target vs actual
- Conversion rate target vs actual
- Pipeline value target vs actual

## Anomaly Detection

The MVP currently detects:

- Revenue achievement below target
- Lead generation below target
- Conversion rate below target
- Pipeline value below target
- High-value deals with low probability
- Low-quality lead sources
- Notable lost deal value

## Action Recommendations

The MVP generates structured business action recommendations based on detected anomalies.

The output file is:

- outputs/action_recommendations.json

Each recommendation includes:

- recommendation_id
- priority
- business_area
- issue
- recommended_action
- owner_team
- time_horizon
- source

This allows the system to move beyond reporting and support decision-oriented business workflows.

## Project Structure

```text
ai-revenue-ops-copilot/
│
├── backend/
│   ├── check_data.py
│   ├── validate_data.py
│   ├── calculate_kpis.py
│   ├── detect_anomalies.py
│   ├── generate_report.py
│   ├── run_pipeline.py
│   └── generate_action_recommendations.py
│
├── data/
│   ├── sales_pipeline.csv
│   ├── marketing_leads.csv
│   └── weekly_targets.csv
│
├── docs/
│   └── MVP_SCOPE.md
│
├── outputs/
│   ├── kpi_summary.json
│   ├── action_recommendations.json
│   ├── weekly_revenue_report.md
│   └── anomaly_report.json  # Internal pipeline artifact
│
├── tests/
├── workflows/
├── notebooks/
├── frontend/
└── README.md
```

## Requirements

The project currently requires:

- Python 3.x
- pandas

Install dependencies:

```powershell
pip install pandas
```

Or, if using a specific Python executable:

```powershell
& "c:\Python314\python.exe" -m pip install pandas
```

## How to Run

Run the complete pipeline from the project root folder:

```powershell
& "c:\Python314\python.exe" backend/run_pipeline.py
```

This command runs:

This command runs:

1. Data validation
2. KPI calculation
3. Anomaly detection
4. Structured action recommendation generation
5. Markdown report generation

## Expected Result

After running the pipeline, the following official MVP output files are generated or updated:

- outputs/kpi_summary.json
- outputs/action_recommendations.json
- outputs/weekly_revenue_report.md

The following internal pipeline artifact is also generated:

- outputs/anomaly_report.json

The main business-facing output is:

- outputs/weekly_revenue_report.md

## Current Status

MVP v0.1 is in progress.

Completed:

- Sample CSV datasets
- CSV data loading
- Data validation layer
- KPI calculation layer
- Basic anomaly detection layer
- Markdown report generation
- Single-command pipeline runner

## Next Development Steps

Planned next steps:

- Add action recommendation output as structured JSON
- Add LLM-generated executive summary
- Add FastAPI backend endpoint
- Add simple dashboard interface
- Add RAG/document intelligence layer for business context
- Add agentic workflow orchestration
- Add CRM/API integration mock layer

## Strategic Positioning

This project is designed to demonstrate applied AI engineering capabilities for B2B business workflows.

It supports the following skill areas:

- AI workflow automation
- LLM-ready backend architecture
- Business data pipeline development
- Revenue operations analytics
- Decision support systems
- API/backend-oriented AI application development
- Portfolio-grade business problem solving
