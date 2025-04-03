import json

def deduplicate_json(content_data_path: str, output_json_path: str) -> None:
    """
    deduplicate given content json and write to new json file preserving keys.

    TODO: More perfromant to just dedupe on raw data before embeddings and summaries generated, avoids having to
          create 'deduplication_key' subset here, etc...
    """
    # Load indexed, embedded context data
    with open(content_data_path, 'r') as f:
        content_json = json.load(f)
    
    # seen will store unique items and add them to unique items - used to generate deduped json. 
    seen = set()
    unique_items = {}

    # iterate through content
    for key, item in content_json.items():
        deduplication_key = (
            item['amt_pre_text'],
            item['amt_post_text'],
            tuple(map(tuple, item['table']))
        )
        
        # if unique 'amt_pre_text', 'amt_post_text', and 'table' add it
        if deduplication_key not in seen:
            seen.add(deduplication_key)
            # Keep the original key and item
            unique_items[key] = item  

    # once dedupe complete - save to new JSON file (with original keys)
    with open(output_json_path, 'w') as out_file:
        json.dump(unique_items, out_file, indent=4)

    print(f"Deduplication complete. {len(content_json) - len(unique_items)} duplicate items removed.")

content_data_path = 'main_test/indexed_content_and_embedding_data.json'
output_json_path = 'main_test/deduplicated_content_json_1.json'

deduplicate_json(content_data_path, output_json_path)
