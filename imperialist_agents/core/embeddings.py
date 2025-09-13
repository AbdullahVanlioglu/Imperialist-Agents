from __future__ import annotations
from typing import List
import hashlib, math

class Embedder:
    def encode(self, texts: List[str]) -> List[List[float]]: ...

class HashingEmbedder(Embedder):
    def __init__(self, dim: int = 384):
        self.dim = dim
    def encode(self, texts: List[str]) -> List[List[float]]:
        vecs = []
        for t in texts:
            v = [0.0] * self.dim
            for token in t.split():
                h = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16)
                v[h % self.dim] += 1.0
            norm = math.sqrt(sum(x*x for x in v)) or 1.0
            vecs.append([x / norm for x in v])
        return vecs

try:
    from sentence_transformers import SentenceTransformer
    _HAS_SBERT = True
except Exception:
    _HAS_SBERT = False

class SbertEmbedder(Embedder):
    def __init__(self, model_name: str):
        if not _HAS_SBERT:
            raise RuntimeError("sentence-transformers not installed. pip install 'manus_style_agent[vector]'")
        self.model = SentenceTransformer(model_name)
    def encode(self, texts: List[str]) -> List[List[float]]:
        embs = self.model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
        return [e.tolist() for e in embs]


def load_embedder(name: str | None, dim: int = 384):
    if name and name.startswith("sbert:"):
        return SbertEmbedder(name.split(":",1)[1])
    if name and name.startswith("hash:"):
        try:
            dim = int(name.split(":",1)[1])
        except Exception:
            pass
    return HashingEmbedder(dim)