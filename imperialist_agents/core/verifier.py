from __future__ import annotations
from typing import Dict, Any
from imperialist_agents.core.registry import Registries

class Verifier:
    async def check(self, draft: Dict[str, Any]) -> bool: ...

class RuleVerifier(Verifier):
    async def check(self, draft: Dict[str, Any]) -> bool:
        # Very simple: ensure draft has no obvious error markers
        text = draft.get("text", "")
        return "ERROR" not in text

Registries.register("verifiers", "rule", RuleVerifier())

def load_verifier(name: str) -> Verifier:
    return Registries.get("verifiers", name)
