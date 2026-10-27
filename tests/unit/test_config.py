from __future__ import annotations

import pytest

from incident_investigator.config import get_config


class TestGetConfig:
    def test_defaults_when_env_absent(self, monkeypatch: pytest.MonkeyPatch) -> None:
        for var in ("INCIDENT_DB_PATH", "MAX_DIAGNOSTIC_ROUNDS", "MAX_TOOL_EXECUTIONS", "LLM_MODEL"):
            monkeypatch.delenv(var, raising=False)

        config = get_config()

        assert config.incident_db_path == "data/incident_data.db"
        assert config.max_diagnostic_rounds == 3
        assert config.max_tool_executions == 10
        assert config.llm_model == "gpt-4o"

    def test_env_overrides(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("INCIDENT_DB_PATH", "/tmp/test.db")
        monkeypatch.setenv("MAX_DIAGNOSTIC_ROUNDS", "5")
        monkeypatch.setenv("MAX_TOOL_EXECUTIONS", "20")
        monkeypatch.setenv("LLM_MODEL", "gpt-3.5-turbo")

        config = get_config()

        assert config.incident_db_path == "/tmp/test.db"
        assert config.max_diagnostic_rounds == 5
        assert config.max_tool_executions == 20
        assert config.llm_model == "gpt-3.5-turbo"

    def test_config_is_frozen(self) -> None:
        config = get_config()
        with pytest.raises(AttributeError):
            config.llm_model = "different"  # type: ignore[misc]

    def test_partial_env_overrides(self, monkeypatch: pytest.MonkeyPatch) -> None:
        for var in ("INCIDENT_DB_PATH", "MAX_DIAGNOSTIC_ROUNDS", "MAX_TOOL_EXECUTIONS", "LLM_MODEL"):
            monkeypatch.delenv(var, raising=False)
        monkeypatch.setenv("LLM_MODEL", "custom-model")

        config = get_config()

        assert config.incident_db_path == "data/incident_data.db"
        assert config.max_diagnostic_rounds == 3
        assert config.max_tool_executions == 10
        assert config.llm_model == "custom-model"
