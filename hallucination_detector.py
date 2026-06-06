from knowledge_graph.wikidata_kg import WikidataKnowledgeGraph
from nlp.query_parser import QueryParser
from validators.entity_validator import EntityConstraintValidator
from validators.topic_validator import TopicConstraintValidator
from validators.kg_validator import KnowledgeGraphValidator
from llm.ollama_client import OllamaClient


class HallucinationDetector:

    def __init__(self):
        self.kg = WikidataKnowledgeGraph()
        self.parser = QueryParser()
        self.llm = OllamaClient()

        self.entity_validator = EntityConstraintValidator(self.kg)
        self.topic_validator = TopicConstraintValidator()
        self.kg_validator = KnowledgeGraphValidator(self.kg)

    def run(self, query: str):
        parsed = self.parser.parse(query)
        response = self.llm.generate(query)

        entity_v = self.entity_validator.validate(parsed["entities"], response)
        topic_v = self.topic_validator.validate(parsed["topic"], response)
        kg_v = self.kg_validator.validate(response, parsed["entities"])

        return {
            "query": query,
            "response": response,
            "entity_validation": entity_v,
            "topic_validation": topic_v,
            "kg_validation": kg_v
        }
