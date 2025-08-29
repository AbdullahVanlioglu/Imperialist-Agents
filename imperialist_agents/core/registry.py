from __future__ import annotations
from typing import Any, Callable, Dict

class Registries:
    """Central plugin registries; avoids if-else switching."""
    models: Dict[str, Any] = {}
    skills: Dict[str, Any] = {}
    memories: Dict[str, Any] = {}
    planners: Dict[str, Any] = {}
    verifiers: Dict[str, Any] = {}
    connectors: Dict[str, Any] = {}

    @classmethod
    def register(cls, kind: str, name: str, obj: Any):
        getattr(cls, kind)[name] = obj

    @classmethod
    def get(cls, kind: str, name: str):
        try:
            return getattr(cls, kind)[name]
        except KeyError:
            raise KeyError(f"Unknown {kind} plugin: {name}")
