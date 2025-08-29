from __future__ import annotations
from typing import Any, Dict, List
from imperialist_agents.core.registry import Registries

class Memory:
    async def put(self, item: Dict[str, Any]): ...
    async def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]: ...

class InMemoryMemory(Memory):
    def __init__(self):
        self._data: List[Dict[str, Any]] = []
    async def put(self, item: Dict[str, Any]):
        self._data.append(item)
    async def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        # naive contains-based search
        results = [d for d in self._data if query.lower() in str(d).lower()]
        return results[:k]

Registries.register("memories", "inmem", InMemoryMemory())

def load_memory(name: str) -> Memory:
    return Registries.get("memories", name)
