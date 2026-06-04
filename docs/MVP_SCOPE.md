# MVP Scope - AI Revenue Operations & Reporting Copilot

## MVP Version

v0.1

## Problem

B2B şirketlerde haftalık satış, pazarlama ve gelir operasyon raporları çoğunlukla manuel hazırlanır. Bu süreç zaman kaybı, hata riski ve geç karar alma problemi yaratır.

## Target User

Revenue Operations Manager, Sales Operations Manager, Growth Manager veya küçük/orta ölçekli B2B şirket yöneticisi.

## Input Files

- sales_pipeline.csv
- marketing_leads.csv
- weekly_targets.csv

## Core Features

- CSV data loading
- KPI calculation
- Sales pipeline summary
- Lead source performance analysis
- Target vs actual comparison
- Basic anomaly detection
- Executive summary generation
- Action recommendation generation
- Markdown report output
- JSON KPI output
- Structured action recommendation generation
- Centralized configuration management
- Shared utility functions for file operations
- Configurable anomaly thresholds


## Out of Scope

- Real CRM integration
- Real ad platform integration
- Authentication
- Multi-user support
- SaaS billing
- Advanced frontend
- Advanced RAG
- Advanced agent orchestration

## Expected Outputs

Official MVP outputs:

- weekly_revenue_report.md
- kpi_summary.json
- action_recommendations.json

Internal pipeline artifact:

- anomaly_report.json

## Success Criteria

The MVP is successful if it can read sample CSV files, validate business data, calculate key business metrics, detect simple anomalies, generate structured action recommendations, and produce a clear weekly executive report with actionable recommendations.

## Technical Design Notes

The MVP uses a modular backend structure.

| Module | Role |
|---|---|
| backend/config.py | Central configuration for paths, file names, and anomaly thresholds. |
| backend/utils.py | Shared CSV, JSON, and text file utilities. |
| backend/validate_data.py | Data validation layer. |
| backend/calculate_kpis.py | KPI calculation layer. |
| backend/detect_anomalies.py | Rule-based anomaly detection layer. |
| backend/generate_action_recommendations.py | Structured action recommendation layer. |
| backend/generate_report.py | Markdown executive report generation layer. |
| backend/run_pipeline.py | Single-command pipeline runner. |

This structure separates configuration, utilities, business logic, and pipeline orchestration.

