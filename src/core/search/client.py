from opensearchpy import AsyncOpenSearch
from src.core.config import settings

def get_opensearch_client() -> AsyncOpenSearch:
    # OpenSearch security plugin is disabled internally to save memory and CPU
    # We only use HTTP and don't supply credentials.
    return AsyncOpenSearch(
        hosts=[settings.opensearch_url],
        use_ssl=False,
        verify_certs=False,
        ssl_show_warn=False
    )
