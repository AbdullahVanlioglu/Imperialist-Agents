from __future__ import annotations
from typing import Dict, Any, List
from pathlib import Path
from imperialist_agents.core.types import ToolSpec, ToolCall, Observation
from imperialist_agents.core.registry import Registries

class Executor:
    def __init__(self, skills: List[Dict[str, Any]], connectors: Dict[str, Any], workspace_dir: str):
        self.workspace = Path(workspace_dir)
        self.workspace.mkdir(parents=True, exist_ok=True)
        self._skills = {s.name: s for s in skills}
        self._connectors = connectors

    @property
    def toolspecs(self) -> List[ToolSpec]:
        return [s.spec for s in self._skills.values()]

    async def run(self, call: ToolCall) -> Observation:
        tool = self._skills.get(call.name)
        if not tool:
            return Observation(tool_call_id=call.id, content=f"Unknown tool {call.name}", ok=False)
        try:
            result = await tool(**call.args)
            return Observation(tool_call_id=call.id, content=result if isinstance(result, str) else str(result), ok=True)
        except Exception as e:
            return Observation(tool_call_id=call.id, content=f"{type(e).__name__}: {e}", ok=False)