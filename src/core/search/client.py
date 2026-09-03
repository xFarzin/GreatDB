from opensearchpy import OpenSearch, AsyncOpenSearch
from src.core.config import settings

def get_opensearch_client() -> AsyncOpenSearch:
    return AsyncOpenSearch(
        hosts=[settings.opensearch_url],
        http_auth=(settings.opensearch_user, settings.opensearch_password),
        use_ssl=settings.opensearch_url.startswith("https"),
        verify_certs=False,
        ssl_show_warn=False
    )
