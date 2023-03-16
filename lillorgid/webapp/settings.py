import os

# No / at end of SOLR_URL please
SOLR_URL = os.getenv("SOLR_URL", "http://localhost:8983/solr")

SOLR_LISTS_CORE = os.getenv("SOLR_LISTS_CORE", "lillorgidlists")
SOLR_DATA_CORE = os.getenv("SOLR_DATA_CORE", "lillorgiddata")
