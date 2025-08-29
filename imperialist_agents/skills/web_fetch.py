from __future__ import annotations
import httpx
from manus_style_agent.core.types import ToolSpec

class WebFetch:
    name = "web.fetch"
    spec = ToolSpec(
        name=name,
        description="Fetch a URL (GET) and return text content (first 2000 chars).",
        schema={
            "type": "object",
            "properties": {
                "url": {"type": "string", "format": "uri"}
            },
            "required": ["url"],
        },
    )
    async def __call__(self, url: str) -> str:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url)
            r.raise_for_status()
            text = r.text
            return text[:2000]