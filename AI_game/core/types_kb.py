from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import json, os


@dataclass
class Entity:
    id: str
    name: str
    category: str
    description: str
    attributes: Dict[str, Any]


@dataclass
class KnowledgeBase:
    entities: List[Entity]
    attribute_meta: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@staticmethod
def load_or_default(path: Optional[str]) -> "KnowledgeBase":
    data = default_kb() if not path or not os.path.exists(path) else json.load(open(path, "r", encoding="utf-8"))
    ents = [Entity(**e) for e in data.get("entities", [])]
    return KnowledgeBase(entities=ents, attribute_meta=data.get("attribute_meta", {}))


def combined_text(self, e: Entity) -> str:
    attrs = " ".join(f"{k}:{v}" for k, v in sorted(e.attributes.items()))
    return f"{e.name}\n{e.category}\n{e.description}\n{attrs}"


def default_kb() -> Dict[str, Any]:
    ents = [
    {"id":"tiger","name":"호랑이","category":"animal","description":"아시아 서식 대형 포식성 포유류","attributes":{"is_animal":True,"is_mammal":True,"is_bird":False,"lives_in_water":False,"continent":"asia","size":"large","diet":"carnivore"}},
    {"id":"dolphin","name":"돌고래","category":"animal","description":"지능 높은 해양 포유류","attributes":{"is_animal":True,"is_mammal":True,"is_bird":False,"lives_in_water":True,"continent":"ocean","size":"medium","diet":"carnivore"}},
    {"id":"penguin","name":"펭귄","category":"animal","description":"남극권의 날지 못하는 새","attributes":{"is_animal":True,"is_mammal":False,"is_bird":True,"lives_in_water":True,"continent":"antarctica","size":"medium","diet":"carnivore"}},
    {"id":"banana","name":"바나나","category":"object","description":"길고 노란 열대 과일","attributes":{"is_animal":False,"is_food":True,"color":"yellow","size":"small","origin":"tropics"}}
    ]
    attribute_meta = {
    "is_animal": {"ko": "동물입니까?", "type":"bool"},
    "is_mammal": {"ko": "포유류입니까?", "type":"bool"},
    "is_bird": {"ko": "새입니까?", "type":"bool"},
    "lives_in_water": {"ko":"주 서식지가 물입니까?", "type":"bool"},
    "is_food": {"ko":"먹는 음식입니까?", "type":"bool"},
    "continent": {"ko":"주 대륙은?", "type":"categorical"},
    "size": {"ko":"크기는? (small/medium/large)", "type":"categorical"},
    "diet": {"ko":"식성은?", "type":"categorical"},
    "color": {"ko":"대표 색은?", "type":"categorical"}
    }
    return {"entities": ents, "attribute_meta": attribute_meta}