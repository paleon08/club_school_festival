from __future__ import annotations
import math, re
from typing import List


class EmbeddingClient:
    def embed(self, texts: List[str]) -> List[List[float]]: raise NotImplementedError


class HashBoWEmbedding(EmbeddingClient):
    def __init__(self, n_features: int = 4096): self.n_features = n_features
    def _tok(self, t: str):
        t = re.sub(r"[^0-9a-zA-Z가-힣_]+", " ", t.lower()); toks = t.split()
        return toks + [toks[i]+"_"+toks[i+1] for i in range(len(toks)-1)] if len(toks)>1 else toks
    def embed(self, texts: List[str]) -> List[List[float]]:
        out=[]
        for txt in texts:
            v=[0.0]*self.n_features
        for tok in self._tok(txt): v[hash(tok)%self.n_features]+=1.0
        n=math.sqrt(sum(x*x for x in v)) or 1.0
        out.append([x/n for x in v])
        return out


class OpenAIEmbedding(EmbeddingClient):
    def __init__(self, model: str = "text-embedding-3-small"):
        from openai import OpenAI
        self.client, self.model = OpenAI(), model
    def embed(self, texts: List[str]) -> List[List[float]]:
        resp = self.client.embeddings.create(model=self.model, input=texts)
        return [d.embedding for d in resp.data]