from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import yaml
import os

class RuntimeCfg(BaseModel):
    workspace_dir: str = "./workspace"
    max_steps: int = 10
    model: str = "noop"

class PlanningCfg(BaseModel):
    style: str = "react"
    verifier: str = "rule"

class MemoryCfg(BaseModel):
    impl: str = "inmem"

class ConnectorGroupCfg(BaseModel):
    impl: str
    enabled: bool = False
    params: Dict[str, Any] = {}

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    runtime: RuntimeCfg = RuntimeCfg()
    planning: PlanningCfg = PlanningCfg()
    memory: MemoryCfg = MemoryCfg()
    skills: List[Dict[str, Any]] = []
    connectors: Dict[str, ConnectorGroupCfg] = {}

    @classmethod
    def load(cls, path: str = "config/settings.yaml") -> "Settings":
        data = {}
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                raw = os.path.expandvars(f.read())
                data = yaml.safe_load(raw) or {}
        return cls(**data)