from __future__ import annotations
from openai import OpenAI


class OpenAILLM:
    def __init__(self, model: str="gpt-4o-mini"): 
        self.client, self.model = OpenAI(), model
    def generate(self, system: str, user: str, temperature: float=0.2) -> str:
        r=self.client.chat.completions.create(model=self.model, messages=[{"role":"system","content":system},{"role":"user","content":user}], temperature=temperature)
        return (r.choices[0].message.content or "").strip()