from __future__ import annotations
from typing import Any, Dict, List
from imperialist_agents.core.registry import Registries
from imperialist_agents.core.embeddings import load_embedder

try:
    from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
    _HAS_MILVUS = True
except Exception:
    _HAS_MILVUS = False

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



class MilvusMemory(Memory):
    """Milvus-backed semantic memory.

    Configuration via environment variables (simple drop-in):
      MILVUS_URI (default: http://localhost:19530)
      MILVUS_COLLECTION (default: agent_memory)
      MILVUS_DIM (default: 384)
      MILVUS_EMBEDDER (default: hash:384, or sbert:sentence-transformers/all-MiniLM-L6-v2)
    """
    def __init__(self):
        if not _HAS_MILVUS:
            raise RuntimeError("pymilvus not installed. pip install 'manus_style_agent[vector]'")
        self.uri = os.getenv("MILVUS_URI", "http://localhost:19530")
        self.collection_name = os.getenv("MILVUS_COLLECTION", "agent_memory")
        self.dim = int(os.getenv("MILVUS_DIM", "384"))
        self.embedder_name = os.getenv("MILVUS_EMBEDDER", "hash:384")
        self.embed = load_embedder(self.embedder_name, self.dim)
        connections.connect(alias="default", uri=self.uri)
        self._ensure_collection()
        self.col = Collection(self.collection_name)
        self._ensure_index()
        self.col.load()

    def _ensure_collection(self):
        if not utility.has_collection(self.collection_name):
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=self.dim),
                FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=4096),
                FieldSchema(name="meta", dtype=DataType.JSON),
            ]
            schema = CollectionSchema(fields=fields, description="Agent memory store")
            Collection(self.collection_name, schema)

    def _ensure_index(self):
        try:
            self.col.create_index(
                field_name="vector",
                index_params={"index_type": "HNSW", "metric_type": "COSINE", "params": {"M": 8, "efConstruction": 64}},
                index_name="vec_idx",
            )
        except Exception:
            pass

    async def put(self, item: Dict[str, Any]):
        text = item.get("text") or item.get("result") or str(item)
        meta = {k: v for k, v in item.items() if k not in ("text", "result")}
        vec = self.embed.encode([text])[0]
        self.col.insert([[vec], [text], [meta]], insert_param={"fields": ["vector", "text", "meta"]})

    async def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        qv = self.embed.encode([query])[0]
        res = self.col.search([qv], anns_field="vector", param={"metric_type": "COSINE", "params": {"ef": 64}}, limit=k, output_fields=["text", "meta"])  # type: ignore
        out: List[Dict[str, Any]] = []
        for hits in res:
            for h in hits:
                out.append({"text": h.entity.get("text"), "score": float(h.distance), "meta": h.entity.get("meta")})
        return out

# Register in-memory memory
Registries.register("memories", "inmem", InMemoryMemory())
# Register as plugin name 'milvus'
Registries.register("memories", "milvus", MilvusMemory())

def load_memory(name: str) -> Memory:
    return Registries.get("memories", name)
