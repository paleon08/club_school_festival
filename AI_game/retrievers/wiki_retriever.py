from __future__ import annotations
import requests, urllib.parse
from typing import List, Tuple


class WikiRetriever:
    BASES = ["https://ko.wikipedia.org/api/rest_v1/page/summary/", "https://en.wikipedia.org/api/rest_v1/page/summary/"]


    def search_summaries(self, queries: List[str], k: int=5) -> List[Tuple[str,str,str]]:
        out=[]
        seen=set()
        for q in queries:
            q=urllib.parse.quote(q)
            for base in self.BASES:
                try:
                    resp=requests.get(base+q, timeout=4)
                    if resp.status_code==200:
                        j=resp.json(); title=j.get("title","? "); ext=j.get("extract","" ); url=j.get("content_urls",{}).get("desktop",{}).get("page","")
                    key=(title,url)
                    if key in seen: continue
                    seen.add(key); out.append((title, ext[:500], url))
                    break
                except Exception:
                    pass
            if len(out)>=k: break
        return out


    def retrieve_for_attribute(self, attr: str, candidate_names: List[str], topk: int=5) -> List[Tuple[str,str,str]]:
        queries=[f"{name} {attr}" for name in candidate_names[:5]]
        return self.search_summaries(queries, k=topk)