# Cognitive-Layer-Hallucination-Detection-System
A local, privacy-first hallucination detection pipeline for LLM responses. Combines a locally-running Ollama model with Wikidata knowledge graph lookups and NLP-based constraint validation to flag factual drift, unauthorized entities, and unverifiable claims — all without sending your data to the cloud.

How It Works
User Query
    │
    ▼
QueryParser (spaCy)          → Extracts entities, intent, topic
    │
    ▼
OllamaClient (local LLM)     → Generates a response
    │
    ▼
┌───────────────────────────────────────────┐
│              Validation Layer             │
│                                           │
│  EntityConstraintValidator  (spaCy NER)   │
│  TopicConstraintValidator   (MiniLM)      │
│  KnowledgeGraphValidator    (Wikidata)    │
└───────────────────────────────────────────┘
    │
    ▼
Structured ValidationResult  (pass/fail + violations)
    ▼
    ValidatorWhat It ChecksEntityFlags entities in the response that weren't in the original queryTopicUses semantic similarity to detect topic drift sentence-by-sentenceKnowledge GraphExtracts SPO triples from the response and verifies them against Wikidata

Features

🔒 Fully local LLM inference via Ollama — no data leaves your machine
🌐 Wikidata-backed fact checking — validates subject-predicate-object triples against a real knowledge graph
🧬 Semantic topic drift detection — uses all-MiniLM-L6-v2 to catch off-topic sentences
🏷️ Entity constraint validation — ensures the response stays scoped to query-relevant entities
🖥️ Streamlit UI + CLI — run it however you prefer

Project Structure

├── app.py                      # Streamlit web UI
├── main.py                     # CLI entry point
├── config/
│   └── config.py               # Global settings (model, thresholds, endpoints)
├── core/
│   └── hallucination_detector.py  # Orchestrates the full pipeline
├── models/
│   └── data_models.py          # SPOTriple, Entity, ValidationResult dataclasses
├── nlp/
│   └── query_parser.py         # spaCy-based query parser
├── llm/
│   └── ollama_client.py        # Ollama HTTP client
├── knowledge_graph/
│   └── wikidata_kg.py          # Wikidata search + claim validation
└── validators/
    ├── entity_validator.py     # NER-based entity scope checking
    ├── topic_validator.py      # Semantic similarity topic drift detection
    └── kg_validator.py         # SPO triple extraction + KG verification
