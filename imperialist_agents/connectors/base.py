from __future__ import annotations
from typing import Dict, Any
from imperialist_agents.core.registry import Registries

class Connector:
    async def setup(self, **kwargs): ...

# EMAIL / DB loader factories (adapter pattern)
from imperialist_agents.connectors.email.imap_adapter import IMAPEmail
from imperialist_agents.connectors.db.sqlite_adapter import SQLiteDB

def load_connectors(cfg: Dict[str, Any]):
    out: Dict[str, Any] = {}
    if "email" in cfg and cfg["email"].enabled:
        out["email"] = IMAPEmail(**cfg["email"].params)
    if "db" in cfg and cfg["db"].enabled:
        out["db"] = SQLiteDB(**cfg["db"].params)
    return out