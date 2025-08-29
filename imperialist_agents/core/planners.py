from __future__ import annotations
from typing import List
from manus_style_agent.core.types import Message, ToolCall
from manus_style_agent.core.models import ModelProvider
from manus_style_agent.core.execution import Executor
from manus_style_agent.core.memory import Memory
from manus_style_agent.core.verifier import load_verifier
from manus_style_agent.core.prompts import SYSTEM_BASE, PLAN_PROMPT

class Planner:
    async def run(self, goal: str) -> str: ...

class ReActPlanner(Planner):
    def __init__(self, model: ModelProvider, executor: Executor, memory: Memory, verifier_name: str, max_steps: int = 10):
        self.model = model
        self.executor = executor
        self.memory = memory
        self.verifier = load_verifier(verifier_name)
        self.max_steps = max_steps

    async def run(self, goal: str) -> str:
        history: List[Message] = [
            Message(role="system", content=SYSTEM_BASE),
            Message(role="user", content=goal),
        ]
        for step in range(self.max_steps):
            out = await self.model.generate(history, tools=self.executor.toolspecs)
            text = out.get("text", "")
            tool_calls: List[ToolCall] = out.get("tool_calls", [])
            if tool_calls:
                for call in tool_calls:
                    obs = await self.executor.run(call)
                    history.append(Message(role="tool", name=call.name, tool_call_id=call.id, content=obs.content))
                continue  # next plan step after tool results
            # No tool call: treat as final draft
            ok = await self.verifier.check({"text": text})
            if ok:
                await self.memory.put({"goal": goal, "result": text})
                return text
            else:
                history.append(Message(role="assistant", content="Verifier failed; revise."))
        return "(stopped) max steps reached"

from manus_style_agent.core.registry import Registries
Registries.register("planners", "react", ReActPlanner)

def load_planner(name: str, **kwargs) -> Planner:
    cls = Registries.get("planners", name)
    return cls(**kwargs)