import requests
from typing import Optional, List
from models.data_models import SPOTriple
from config.config import Config


class WikidataKnowledgeGraph:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "HallucinationDetector/1.0"
        })
        self.cache = {}

    def search_entity(self, entity_name: str) -> Optional[str]:
        if entity_name in self.cache:
            return self.cache[entity_name]

        params = {
            "action": "wbsearchentities",
            "format": "json",
            "language": "en",
            "search": entity_name,
            "limit": 1
        }

        try:
            r = self.session.get(Config.WIKIDATA_ENDPOINT, params=params)
            data = r.json()
            if data.get("search"):
                entity_id = data["search"][0]["id"]
                self.cache[entity_name] = entity_id
                return entity_id
        except:
            pass
        return None

    def get_entity_claims(self, entity_id: str) -> List[SPOTriple]:
        params = {
            "action": "wbgetentities",
            "format": "json",
            "ids": entity_id,
            "props": "claims|labels"
        }

        triples = []
        try:
            r = self.session.get(Config.WIKIDATA_ENDPOINT, params=params)
            entity = r.json()["entities"][entity_id]
            subject = entity["labels"]["en"]["value"]

            for prop, claims in entity.get("claims", {}).items():
                for claim in claims[:2]:
                    value = claim["mainsnak"].get("datavalue")
                    if value:
                        triples.append(
                            SPOTriple(subject, prop, str(value["value"]))
                        )
        except:
            pass
        return triples

    def validate_relation(self, subject, predicate, obj) -> bool:
        entity_id = self.search_entity(subject)
        if not entity_id:
            return False

        triples = self.get_entity_claims(entity_id)
        return any(obj.lower() in t.object.lower() for t in triples)
