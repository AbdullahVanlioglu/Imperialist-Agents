from __future__ import annotations
from typing import Protocol, Dict, Any, List
from manus_style_agent.core.types import ToolSpec

class Skill(Protocol):
    name: str
    spec: ToolSpec
    async def __call__(self, **kwargs): ...

class SkillList(list):
    @property
    def specs(self) -> List[ToolSpec]:
        return [s.spec for s in self]

# Factory from config entries
from manus_style_agent.skills.file_ops import FileRead, FileWrite
from manus_style_agent.skills.web_fetch import WebFetch

def load_skills(cfg_list: List[Dict[str, Any]]):
    name2cls = {"file.read": FileRead, "file.write": FileWrite, "web.fetch": WebFetch}
    skills = []
    for item in cfg_list:
        cls = name2cls.get(item["name"])  # extend via entrypoints or plugin discovery
        if cls:
            skills.append(cls())
    return SkillList(skills)