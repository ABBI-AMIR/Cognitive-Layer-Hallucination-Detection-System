class Config:
    """Global configuration for the system"""

    # Local Ollama configuration
    OLLAMA_URL = "http://localhost:11434/api/generate"
    OLLAMA_MODEL = "llama2"

    # Wikidata
    WIKIDATA_ENDPOINT = "https://www.wikidata.org/w/api.php"

    # Validation thresholds
    SIMILARITY_THRESHOLD = 0.70
    MAX_RELATED_ENTITIES = 3

    # Network
    REQUEST_TIMEOUT = 10
