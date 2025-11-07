from __future__ import annotations
from typing import Any, Dict, List, Tuple
from core.types_kb import KnowledgeBase, Entity
from retrievers.vector_store import VectorStore


class KBRetriever:
    def __init__(self, kb: KnowledgeBase, vs: VectorStore): self.kb, self.vs = kb, vs
    def build(self):
        for e in self.kb.entities: self.vs.add(self.kb.combined_text(e), id=e.id, type="entity")
    def retrieve_for_attribute(self, attr: str, candidates: List[Entity], topk: int=5) -> List[Tuple[str,str,str]]:
        q = f"{attr} of: "+", ".join(e.name for e in candidates[:10])
        docs = self.vs.search(q, k=topk)
        out=[]
        for _, m, t in docs:
            if m.get("type")=="entity": out.append((m.get("id",""), t[:300], "kb://"+m.get("id","")))
        return out