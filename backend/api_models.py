from typing import Literal

from pydantic import BaseModel


class PipelineRunRequest(BaseModel):
    with_llm: bool = False
    check_llm_quality: bool = False


class PipelineOutputsStatus(BaseModel):
    kpi_summary: bool
    anomaly_report: bool
    action_recommendations: bool
    weekly_revenue_report: bool
    llm_executive_summary: bool
    llm_quality_report: bool


class PipelineStatusResponse(BaseModel):
    status: Literal["ok"]
    outputs: PipelineOutputsStatus


class PipelineRunSuccessResponse(BaseModel):
    status: Literal["success"]
    message: str
    mode: Literal[
        "core",
        "core_with_llm",
        "core_with_llm_and_quality_check",
    ]
    outputs: PipelineOutputsStatus


class PipelineErrorDetail(BaseModel):
    status: Literal["error"]
    message: str
    details: str