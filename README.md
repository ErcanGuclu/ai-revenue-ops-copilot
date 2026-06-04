# AI Revenue Operations & Reporting Copilot

## One-Line Value Proposition

A portfolio-grade Python MVP that turns sales and marketing CSV data into KPI summaries, anomaly insights, structured action recommendations, and an executive Markdown report.

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

## Why This Project Matters

This project demonstrates how a business reporting workflow can be transformed into a repeatable data pipeline.

Instead of manually preparing weekly revenue operations reports, the system automatically:

- validates business data,
- calculates sales and marketing KPIs,
- detects risk signals,
- generates structured action recommendations,
- produces an executive-ready Markdown report.

The MVP is intentionally small, but it is designed around a real B2B workflow pattern: turning operational data into decision-support outputs.

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

## Technical Architecture

The backend is organized into small, focused Python modules.

| Module | Responsibility |
|---|---|
| backend/config.py | Stores project paths, input/output file names, and anomaly thresholds. |
| backend/utils.py | Provides shared file loading and saving utilities. |
| backend/validate_data.py | Validates CSV schemas, required fields, numeric ranges, dates, and relationships. |
| backend/calculate_kpis.py | Calculates sales, marketing, and target comparison KPIs. |
| backend/detect_anomalies.py | Detects rule-based business anomalies using configurable thresholds. |
| backend/generate_action_recommendations.py | Converts anomalies into structured business action recommendations. |
| backend/generate_report.py | Generates the Markdown executive report. |
| backend/run_pipeline.py | Runs the full pipeline in the correct order. |


## Configuration

Project-level settings are managed in:

- backend/config.py

The configuration file currently includes:

- BASE_DIR
- DATA_DIR
- OUTPUT_DIR
- INPUT_FILES
- OUTPUT_FILES
- ANOMALY_THRESHOLDS

Anomaly detection thresholds are not hardcoded inside the analysis logic. They are centralized in `ANOMALY_THRESHOLDS`, which makes the rule engine easier to maintain and extend.


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
- Centralized project configuration
- Shared file utility functions
- Configurable anomaly thresholds


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

Anomaly thresholds are managed centrally in `backend/config.py` through the `ANOMALY_THRESHOLDS` dictionary.

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
│   ├── config.py
│   ├── utils.py
│   ├── check_data.py
│   ├── validate_data.py
│   ├── calculate_kpis.py
│   ├── detect_anomalies.py
│   ├── generate_action_recommendations.py
│   ├── generate_report.py
│   └── run_pipeline.py
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
│   ├── test_config.py
│   └── test_pipeline_outputs.py
│
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


## Demo Outputs

The repository includes generated sample outputs under the `outputs/` folder.

Official MVP outputs:

- `outputs/kpi_summary.json`
- `outputs/action_recommendations.json`
- `outputs/weekly_revenue_report.md`

Internal pipeline artifact:

- `outputs/anomaly_report.json`

The main business-facing artifact is:

- `outputs/weekly_revenue_report.md`


## Current Status

MVP v0.1 is functional.

Completed:

- Sample CSV datasets
- CSV data loading
- Data validation layer
- KPI calculation layer
- Rule-based anomaly detection layer
- Structured action recommendation generation
- Markdown executive report generation
- Single-command pipeline runner
- Centralized configuration module
- Shared utility module
- Configurable anomaly thresholds
- Initial automated tests
- Pipeline smoke test
- GitHub-ready documentation


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


## Portfolio Relevance

This project is designed to demonstrate practical applied AI engineering skills beyond a basic chatbot or notebook demo.

It shows the ability to:

- structure a real business workflow,
- build a repeatable Python data pipeline,
- separate configuration, utilities, business logic, and orchestration,
- generate machine-readable JSON outputs,
- generate human-readable executive reports,
- create tests for configuration and pipeline behavior,
- maintain the project with Git and clear documentation.

Future versions can extend this MVP with FastAPI, LLM-generated summaries, RAG-based business context, agentic workflow orchestration, and dashboard interfaces.

## Interview Summary

This project demonstrates an end-to-end business data workflow: CSV data ingestion, validation, KPI calculation, anomaly detection, structured action recommendation generation, and executive Markdown reporting.

The current MVP intentionally focuses on a deterministic and explainable analytics pipeline before adding LLM, RAG, API, or agentic workflow layers.