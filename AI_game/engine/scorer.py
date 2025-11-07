from __future__ import annotations
import math
from typing import Dict, List, Tuple
from core.types_kb import Entity


class CandidateScorer:
    def __init__(self): self.logp: Dict[str,float]={}
    def reset(self, candidates: List[Entity]): self.logp={e.id:0.0 for e in candidates}
    def update(self, candidates: List[Entity], attr: str, answer: str):
        for e in candidates:
            v=e.attributes.get(attr,None)
            if isinstance(v,bool): prob_yes=0.85 if v else 0.15
            else: prob_yes=0.6
            prob_no=1.0-prob_yes
            incr = math.log((prob_yes if answer=="yes" else prob_no if answer=="no" else 0.5)+1e-6)
            self.logp[e.id]=self.logp.get(e.id,0.0)+incr
    def topk(self, candidates: List[Entity], k:int=3)->List[Tuple[Entity,float]]:
        arr=[(e, self.logp.get(e.id,0.0)) for e in candidates]
        arr.sort(key=lambda x:x[1], reverse=True); return arr[:k]