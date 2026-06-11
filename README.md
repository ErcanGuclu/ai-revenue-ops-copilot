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


### Optional LLM Outputs

- `outputs/llm_executive_summary.md`
- `outputs/llm_quality_report.json`

`llm_executive_summary.md` is generated when the pipeline is executed with:

`python backend/run_pipeline.py --with-llm`

`llm_quality_report.json` is generated when the pipeline is executed with:

`python backend/run_pipeline.py --with-llm --check-llm-quality`

Alternatively, the quality check can be run manually after generating the LLM executive summary:

`python backend/check_llm_output_quality.py`


### Internal Pipeline Output

- outputs/anomaly_report.json

This file is an internal analysis artifact used for anomaly detection and action recommendation generation. It is not part of the official MVP output set.

## Current Pipeline

The project has three execution modes.

### 1. Core Deterministic Pipeline

Run:

`python backend/run_pipeline.py`

This mode performs:

1. CSV data loading
2. Data validation
3. KPI calculation
4. Anomaly detection
5. Structured action recommendation generation
6. Markdown executive report generation

This mode does not require an LLM API key, internet access, or model availability.

### 2. Core Pipeline with Optional LLM Enrichment

Run:

`python backend/run_pipeline.py --with-llm`

This mode performs all core pipeline steps and then generates:

- `outputs/llm_executive_summary.md`

The LLM enrichment layer is optional and depends on the configured LLM provider.

### 3. Core Pipeline with LLM Enrichment and Quality Check

Run:

`python backend/run_pipeline.py --with-llm --check-llm-quality`

This mode performs all core pipeline steps, generates the optional LLM executive summary, and then runs the LLM output quality check.

It generates:

- `outputs/llm_executive_summary.md`
- `outputs/llm_quality_report.json`

The `--check-llm-quality` flag requires `--with-llm`, because the quality check can only validate an existing LLM summary.

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
| `backend/check_llm_output_quality.py` | Validates the optional LLM executive summary and generates a quality report. |
| `outputs/llm_quality_report.json` | Stores the LLM output quality check result. |


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

Note: `gemini-2.5-flash-lite` is used as the default Gemini model for this project because it is more suitable for lightweight, portfolio-level LLM enrichment tasks.

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
- LLM output quality check layer
- LLM quality report generation
- Basic validation for required LLM summary sections
- Basic validation for source file references
- Risky LLM phrase detection
- Initial FastAPI backend layer
- Health check endpoint
- Pipeline status endpoint
- API-based output availability check


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


## LLM Output Quality Check

The project includes a basic quality check layer for the optional LLM executive summary.

The quality check can be run through the main pipeline:

`python backend/run_pipeline.py --with-llm --check-llm-quality`

or manually after generating the LLM summary:

`python backend/check_llm_output_quality.py`

This script validates:

- whether the LLM summary file exists and is readable
- whether required Markdown sections are present
- whether expected source file references are included
- whether the output meets a minimum length threshold
- whether risky LLM phrases are present
- whether structured JSON input files are readable

The script generates:

- `outputs/llm_quality_report.json`

This quality check is not a full hallucination detector. It is a first-level quality gate that checks structure, completeness, and basic reliability signals.


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
│   ├── generate_llm_summary.py
│   ├── check_llm_output_quality.py
│   └── api.py
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
│   ├── anomaly_report.json  # Internal pipeline artifact
│   ├── action_recommendations.json
│   ├── weekly_revenue_report.md
│   ├── llm_executive_summary.md
│   └── llm_quality_report.json
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

### Run Core Pipeline with LLM Enrichment and Quality Check

`python backend/run_pipeline.py --with-llm --check-llm-quality`

This runs the deterministic pipeline, generates the optional LLM executive summary, and then validates the LLM output through the quality check layer.

### Run API Server

`python -m uvicorn backend.api:app --reload`

Health endpoint:

`GET /health`

Local URL:

`http://127.0.0.1:8000/health`

Interactive API docs:

`http://127.0.0.1:8000/docs`


Pipeline status endpoint:

`GET /pipeline/status`

Local URL:

`http://127.0.0.1:8000/pipeline/status`


### Invalid Usage

The following command is intentionally not allowed:

`python backend/run_pipeline.py --check-llm-quality`

The quality check requires an LLM summary to exist, so it must be used together with:

`--with-llm`

### Environment Setup for LLM

Copy `.env.example` to `.env` and add your Gemini API key:

- `LLM_PROVIDER=gemini`
- `GEMINI_API_KEY=your_actual_key`
- `GEMINI_MODEL=gemini-2.5-flash-lite`

The `.env` file must not be committed to Git.

## Expected Result

After running the core pipeline, the following official MVP output files are generated or updated:

- `outputs/kpi_summary.json`
- `outputs/action_recommendations.json`
- `outputs/weekly_revenue_report.md`

The following internal pipeline artifact is also generated:

- `outputs/anomaly_report.json`

If the pipeline is run with `--with-llm`, the following optional LLM output is also generated:

- `outputs/llm_executive_summary.md`

If the pipeline is run with `--with-llm --check-llm-quality`, the following optional LLM quality output is also generated:

- `outputs/llm_quality_report.json`


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
- LLM output quality check layer
- LLM quality report generation
- Basic LLM summary structure validation
- Basic source reference validation
- Three-mode pipeline execution
- Optional LLM quality check pipeline flag
- Guardrail preventing LLM quality check without LLM summary generation
- Pipeline status API endpoint



## Next Development Steps

Planned next steps:

- Improve LLM prompt structure
- Add structured LLM output mode
- Add FastAPI backend endpoint
- Add simple dashboard interface
- Add RAG/document intelligence layer for business context
- Add agentic workflow orchestration
- Add CRM/API integration mock layer
- Add stronger LLM factual consistency checks
- Validate numeric claims against structured JSON outputs
- Add structured LLM output mode


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