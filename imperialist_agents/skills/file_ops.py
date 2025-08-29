from __future__ import annotations
from pathlib import Path
from manus_style_agent.core.types import ToolSpec

_WORKSPACE_ROOT = Path("./workspace").resolve()

class _BaseFile:
    def _resolve(self, path: str) -> Path:
        p = (Path(path) if not Path(path).is_absolute() else Path(path)).resolve()
        if not str(p).startswith(str(_WORKSPACE_ROOT)):
            # Sandbox: restrict to workspace
            p = _WORKSPACE_ROOT / Path(path).name
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

class FileWrite(_BaseFile):
    name = "file.write"
    spec = ToolSpec(
        name=name,
        description="Write text to a file within the workspace sandbox.",
        schema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path (relative or absolute)"},
                "text": {"type": "string", "description": "Content to write"}
            },
            "required": ["path", "text"],
        },
    )
    async def __call__(self, path: str, text: str) -> str:
        p = self._resolve(path)
        p.write_text(text, encoding="utf-8")
        return f"Wrote {len(text)} chars to {p}"

class FileRead(_BaseFile):
    name = "file.read"
    spec = ToolSpec(
        name=name,
        description="Read text from a file within the workspace sandbox.",
        schema={
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"}
            },
            "required": ["path"],
        },
    )
    async def __call__(self, path: str) -> str:
        p = self._resolve(path)
        if not p.exists():
            return f"File not found: {p}"
        return p.read_text(encoding="utf-8")