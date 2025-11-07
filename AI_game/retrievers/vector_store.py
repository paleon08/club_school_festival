from __future__ import annotations
from typing import Any, Dict, List, Tuple
from core.embeddings import EmbeddingClient


class VectorStore:
    def __init__(self, embedder: EmbeddingClient):
        self.embedder=embedder; self.doc_texts: List[str]=[]; self.doc_meta: List[Dict[str,Any]]=[]; self.doc_vecs=None
    def add(self, text: str, **meta): self.doc_texts.append(text); self.doc_meta.append(meta); self.doc_vecs=None
    def _ensure(self):
        if self.doc_vecs is None: self.doc_vecs = self.embedder.embed(self.doc_texts)
    def _cos(self, a, b): return float(sum(x*y for x,y in zip(a,b)))
    def search(self, query: str, k: int=5) -> List[Tuple[float, Dict[str,Any], str]]:
        self._ensure(); q=self.embedder.embed([query])[0]
        scored=[(self._cos(q,v),m,t) for v,m,t in zip(self.doc_vecs,self.doc_meta,self.doc_texts)]
        scored.sort(key=lambda x:x[0], reverse=True); return scored[:k]