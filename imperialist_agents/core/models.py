from __future__ import annotations
from typing import List, Dict, Any, Optional
from imperialist_agents.core.types import Message, ToolSpec, ToolCall
from imperialist_agents.core.registry import Registries

# ---- Model Provider Interface ------------------------------------------------
class ModelProvider:
    name: str
    def __init__(self, name: str):
        self.name = name
    async def generate(self, messages: List[Message], tools: Optional[List[ToolSpec]] = None) -> Dict[str, Any]:
        """Return {"text": str, "tool_calls": List[ToolCall]}"""
        raise NotImplementedError

# ---- No-op / Rule-based model (for offline demos) ----------------------------
class NoOpModel(ModelProvider):
    async def generate(self, messages: List[Message], tools: Optional[List[ToolSpec]] = None) -> Dict[str, Any]:
        # Extremely naive heuristic: if user asks to write a file, call file.write; if asks to fetch a URL, call web.fetch
        last = messages[-1].content.lower()
        calls: List[ToolCall] = []
        if "write" in last and "file" in last:
            calls.append(ToolCall(id="1", name="file.write", args={"path": "./workspace/output.txt", "text": last}))
        elif "http" in last or "https" in last:
            calls.append(ToolCall(id="1", name="web.fetch", args={"url": last.split()[-1]}))
        return {"text": "(demo) Using heuristic actions.", "tool_calls": calls}

Registries.register("models", "noop", NoOpModel("noop"))