from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    incident_db_path: str
    max_diagnostic_rounds: int
    max_tool_executions: int
    llm_model: str


def get_config() -> Config:
    return Config(
        incident_db_path=os.environ.get("INCIDENT_DB_PATH", "data/incident_data.db"),
        max_diagnostic_rounds=int(os.environ.get("MAX_DIAGNOSTIC_ROUNDS", "3")),
        max_tool_executions=int(os.environ.get("MAX_TOOL_EXECUTIONS", "10")),
        llm_model=os.environ.get("LLM_MODEL", "gpt-4o"),
    )
