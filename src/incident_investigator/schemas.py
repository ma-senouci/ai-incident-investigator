from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel


class RootCauseCategory(StrEnum):
    AUTHENTICATION_FAILURE = "AUTHENTICATION_FAILURE"
    DATABASE_PERFORMANCE_DEGRADATION = "DATABASE_PERFORMANCE_DEGRADATION"
    RESOURCE_EXHAUSTION = "RESOURCE_EXHAUSTION"


class ApplicationLog(BaseModel):
    id: int
    scenario_id: str
    timestamp: str
    severity: str
    service: str
    endpoint: str
    message: str
    request_id: str


class DatabaseLog(BaseModel):
    id: int
    scenario_id: str
    timestamp: str
    duration_ms: float
    query_description: str
    error_details: str | None = None
    correlation_id: str


class SystemMetric(BaseModel):
    id: int
    scenario_id: str
    timestamp: str
    metric_name: str
    value: float
    host: str
