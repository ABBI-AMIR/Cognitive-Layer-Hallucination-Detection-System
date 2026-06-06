import spacy
from models.data_models import Entity


class QueryParser:

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def parse(self, query: str) -> dict:
        doc = self.nlp(query)

        entities = [Entity(ent.text, ent.label_) for ent in doc.ents]
        if entities:
            entities[0].is_primary = True

        intent = "question" if any(
            token.text.lower() in ["what", "who", "where", "when", "why", "how"]
            for token in doc
        ) else "statement"

        topic = next(
            (token.lemma_ for token in doc if token.dep_ == "ROOT"),
            "general"
        )

        return {
            "query": query,
            "entities": entities,
            "intent": intent,
            "topic": topic
        }
