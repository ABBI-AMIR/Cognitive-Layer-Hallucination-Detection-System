import spacy
from models.data_models import ValidationResult, SPOTriple
from knowledge_graph.wikidata_kg import WikidataKnowledgeGraph


class KnowledgeGraphValidator:

    def __init__(self, kg: WikidataKnowledgeGraph):
        self.kg = kg
        self.nlp = spacy.load("en_core_web_sm")

    def validate(self, response, entities):
        doc = self.nlp(response)
        violations = []
        validated = []

        for sent in doc.sents:
            for token in sent:
                if token.pos_ == "VERB":
                    subj = next((c.text for c in token.children if c.dep_ == "nsubj"), None)
                    obj = next((c.text for c in token.children if c.dep_ in ["dobj", "attr"]), None)
                    if subj and obj:
                        if self.kg.validate_relation(subj, token.lemma_, obj):
                            validated.append(SPOTriple(subj, token.lemma_, obj))
                        else:
                            violations.append(f"Unverified: {subj} {token.lemma_} {obj}")

        return ValidationResult(
            is_valid=len(violations) == 0,
            violations=violations,
            validated_triples=validated,
            rejected_content=[]
        )
