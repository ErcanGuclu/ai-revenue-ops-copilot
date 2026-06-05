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

### Official MVP Output Files

- `outputs/kpi_summary.json`
- `outputs/action_recommendations.json`
- `outputs/weekly_revenue_report.md`


### Optional LLM Output

- `outputs/llm_executive_summary.md`

This output is generated only when the pipeline is executed with:

`python backend/run_pipeline.py --with-llm`


### Internal Pipeline Output

- outputs/anomaly_report.json

This file is an internal analysis artifact used for anomaly detection and action recommendation generation. It is not part of the official MVP output set.

## Current Pipeline

The project has two execution modes.

### Core Deterministic Pipeline

Run:

`python backend/run_pipeline.py`

This mode performs:

1. CSV data loading
2. Data validation
3. KPI calculation
4. Anomaly detection
5. Structured action recommendation generation
6. Markdown executive report generation

### Optional LLM Enrichment Pipeline

Run:

`python backend/run_pipeline.py --with-llm`

This mode performs all core pipeline steps and then generates:

- `outputs/llm_executive_summary.md`

The LLM enrichment layer is optional. The core pipeline does not depend on API access, internet connectivity, or model availability.

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
| `backend/llm_provider.py` | Provides a centralized provider-based LLM access layer. |
| `backend/generate_llm_summary.py` | Generates an optional LLM-powered executive summary from structured JSON outputs. |


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

### LLM Configuration

LLM settings are managed through `.env` and `backend/config.py`.

The repository includes `.env.example` as a safe template.

Example:

- `LLM_PROVIDER=gemini`
- `GEMINI_API_KEY=your_gemini_api_key_here`
- `GEMINI_MODEL=gemini-2.5-flash-lite`

The real `.env` file is excluded from Git through `.gitignore`.

The first active provider is Google Gemini. OpenAI can be added later as an alternative provider.


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
- Provider-based LLM access layer
- Google Gemini integration
- Optional LLM executive summary generation
- `--with-llm` pipeline flag
- Separation between deterministic core pipeline and optional LLM enrichment


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

## LLM Executive Summary

The project includes an optional LLM enrichment layer.

When executed with:

`python backend/run_pipeline.py --with-llm`

the system uses structured pipeline outputs:

- `outputs/kpi_summary.json`
- `outputs/anomaly_report.json`
- `outputs/action_recommendations.json`

and generates:

- `outputs/llm_executive_summary.md`

The LLM does not calculate KPIs directly. It receives already validated and structured outputs from the deterministic pipeline and turns them into a business-oriented executive summary.

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
│   ├── run_pipeline.py
│   ├── llm_provider.py
│   └── generate_llm_summary.py
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
│   ├── anomaly_report.json  # Internal pipeline artifact
│   └── llm_executive_summary.md
│
├── tests/
│   ├── test_config.py
│   └── test_pipeline_outputs.py
│
├── frontend/
├── notebooks/
├── workflows/
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
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

### Run Core Pipeline

`python backend/run_pipeline.py`

This runs the deterministic pipeline without any LLM API call.

### Run Core Pipeline with LLM Enrichment

`python backend/run_pipeline.py --with-llm`

This runs the deterministic pipeline and then generates the optional LLM executive summary.

### Environment Setup for LLM

Copy `.env.example` to `.env` and add your Gemini API key:

- `LLM_PROVIDER=gemini`
- `GEMINI_API_KEY=your_actual_key`
- `GEMINI_MODEL=gemini-2.5-flash-lite`

The `.env` file must not be committed to Git.

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

MVP v0.2 is in progress.

Completed:

- Sample CSV datasets
- CSV data loading
- Data validation layer
- KPI calculation layer
- Rule-based anomaly detection layer
- Structured action recommendation generation
- Markdown executive report generation
- Single-command core pipeline runner
- Centralized configuration module
- Shared utility module
- Configurable anomaly thresholds
- Initial automated tests
- Pipeline smoke test
- Provider-based LLM architecture
- Google Gemini integration
- Optional LLM executive summary generation
- `--with-llm` pipeline flag
- GitHub-ready documentation


## Next Development Steps

Planned next steps:

- Improve LLM prompt structure
- Add LLM output quality checks
- Add structured LLM output mode
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