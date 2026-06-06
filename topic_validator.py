import re
import numpy as np
from sentence_transformers import SentenceTransformer
from config.config import Config
from models.data_models import ValidationResult


class TopicConstraintValidator:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def validate(self, topic, response):
        sentences = re.split(r"[.!?]", response)
        topic_emb = self.model.encode([topic])

        violations = []
        rejected = []

        for s in sentences:
            if len(s.strip()) < 10:
                continue
            sim = np.dot(topic_emb, self.model.encode([s]).T)[0][0]
            if sim < Config.SIMILARITY_THRESHOLD:
                violations.append("Topic drift detected")
                rejected.append(s)

        return ValidationResult(
            is_valid=len(violations) == 0,
            violations=violations,
            validated_triples=[],
            rejected_content=rejected
        )
