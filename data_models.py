from dataclasses import dataclass
from typing import List


@dataclass
class SPOTriple:
    subject: str
    predicate: str
    object: str
    confidence: float = 1.0
    source: str = "wikidata"


@dataclass
class Entity:
    text: str
    label: str
    is_primary: bool = False


@dataclass
class ValidationResult:
    is_valid: bool
    violations: List[str]
    validated_triples: List[SPOTriple]
    rejected_content: List[str]
