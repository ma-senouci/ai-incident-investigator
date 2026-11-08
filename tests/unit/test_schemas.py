from __future__ import annotations

from incident_investigator.schemas import (
    ApplicationLog,
    DatabaseLog,
    RootCauseCategory,
    SystemMetric,
)


class TestRootCauseCategory:
    def test_has_exactly_three_values(self) -> None:
        assert len(RootCauseCategory) == 3

    def test_values(self) -> None:
        assert RootCauseCategory.AUTHENTICATION_FAILURE == "AUTHENTICATION_FAILURE"
        assert RootCauseCategory.DATABASE_PERFORMANCE_DEGRADATION == "DATABASE_PERFORMANCE_DEGRADATION"
        assert RootCauseCategory.RESOURCE_EXHAUSTION == "RESOURCE_EXHAUSTION"


class TestApplicationLog:
    def test_construction(self) -> None:
        log = ApplicationLog(
            id=1,
            scenario_id="db_connection",
            timestamp="2026-01-15T10:30:00Z",
            severity="ERROR",
            service="api-gateway",
            endpoint="/api/data",
            message="Connection refused",
            request_id="req-001",
        )
        assert log.scenario_id == "db_connection"
        assert log.severity == "ERROR"


class TestDatabaseLog:
    def test_construction(self) -> None:
        log = DatabaseLog(
            id=1,
            scenario_id="api_latency",
            timestamp="2026-01-15T10:30:00Z",
            duration_ms=1500.0,
            query_description="SELECT * FROM users",
            correlation_id="corr-001",
        )
        assert log.duration_ms == 1500.0
        assert log.error_details is None

    def test_with_error_details(self) -> None:
        log = DatabaseLog(
            id=2,
            scenario_id="api_latency",
            timestamp="2026-01-15T10:31:00Z",
            duration_ms=3000.0,
            query_description="INSERT INTO orders",
            error_details="lock timeout exceeded",
            correlation_id="corr-002",
        )
        assert log.error_details == "lock timeout exceeded"


class TestSystemMetric:
    def test_construction(self) -> None:
        metric = SystemMetric(
            id=1,
            scenario_id="memory_leak",
            timestamp="2026-01-15T10:30:00Z",
            metric_name="memory",
            value=82.5,
            host="web-01",
        )
        assert metric.metric_name == "memory"
        assert metric.value == 82.5
