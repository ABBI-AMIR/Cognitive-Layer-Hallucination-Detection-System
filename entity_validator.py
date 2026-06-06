import spacy
from models.data_models import ValidationResult
from knowledge_graph.wikidata_kg import WikidataKnowledgeGraph


class EntityConstraintValidator:

    def __init__(self, kg: WikidataKnowledgeGraph):
        self.kg = kg
        self.nlp = spacy.load("en_core_web_sm")

    def validate(self, query_entities, response):
        doc = self.nlp(response)
        response_entities = {ent.text.lower() for ent in doc.ents}
        allowed = {e.text.lower() for e in query_entities}

        violations = [
            f"Unauthorized entity: {e}"
            for e in response_entities - allowed
        ]

        return ValidationResult(
            is_valid=len(violations) == 0,
            violations=violations,
            validated_triples=[],
            rejected_content=list(response_entities - allowed)
        )
