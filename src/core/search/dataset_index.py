from src.core.search.client import get_opensearch_client

async def create_index_for_dataset(dataset_id: int, version: int):
    client = get_opensearch_client()
    index_name = f"dataset_{dataset_id}_v{version}"

    # Generic mapping, we allow dynamic fields but define basic types if needed
    mapping = {
        "mappings": {
            "dynamic": True,
            "properties": {
                "__dataset_id": {"type": "integer"},
                "__raw_line": {"type": "text", "index": False} # Opt out of indexing the full raw line if we want to save space, or keep it.
            }
        },
        "settings": {
            "index": {
                "number_of_shards": 1, # Can be increased for scale
                "number_of_replicas": 0 # Local testing, normally 1+
            }
        }
    }

    if not await client.indices.exists(index=index_name):
        await client.indices.create(index=index_name, body=mapping)

    await client.close()
    return index_name

async def search_dataset(dataset_alias: str, query_string: str, limit: int = 10):
    client = get_opensearch_client()
    query = {
        "size": limit,
        "query": {
            "query_string": {
                "query": query_string,
                "default_operator": "AND"
            }
        }
    }

    try:
        response = await client.search(index=dataset_alias, body=query)
        hits = response['hits']['hits']
        return [hit['_source'] for hit in hits]
    finally:
        await client.close()

async def activate_dataset_version(dataset_id: int, version: int):
    """
    Points the alias `dataset_{id}_active` to `dataset_{id}_v{version}`
    This provides zero-downtime dataset updates.
    """
    client = get_opensearch_client()
    alias_name = f"dataset_{dataset_id}_active"
    new_index = f"dataset_{dataset_id}_v{version}"

    actions = []

    # Check if alias exists and get current indices pointing to it
    try:
        alias_info = await client.indices.get_alias(name=alias_name)
        for old_index in alias_info.keys():
            actions.append({"remove": {"index": old_index, "alias": alias_name}})
    except Exception:
        pass # Alias doesn't exist yet

    actions.append({"add": {"index": new_index, "alias": alias_name}})

    await client.indices.update_aliases(body={"actions": actions})
    await client.close()
