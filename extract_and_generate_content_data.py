import json
from ollama import chat
from ollama import ChatResponse
from sentence_transformers import SentenceTransformer


def process_content_data(input_json: str) -> dict:
    """
    Create content data from the provided train.json file.

    Using ollama hosted model for summary generation to minimise costs.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    output_json = {}

    for index, item in enumerate(input_json): 
        # Set index to limit number of items written.
        if index < 100:
            index = index
            table = item.get('table', [])
            annotation = item.get('annotation', {})
            amt_pre_text = annotation.get('amt_pre_text', '')
            amt_post_text = annotation.get('amt_post_text', '')

            response: ChatResponse = chat(model='llama3.2', messages=[
                {
                    'role': 'system',
                    'content': '''You are a expert in summarising financial data. Summarise the folllowing 
                        table and text pairs (Table: [], Text: "..") to enable a user to effecitvely 
                        understand what questions the information can be used to answer. Provide date ranges 
                        and key information. Keep the response concise and do not add any non-factual information.
                        Do not use new lines or special characters, provide a single line as per the example.
                        For example: Data provides net cash figures from 2008 to 2009.''',
                },
                {
                'role': 'user',
                    'content': f'Table: {table}, text: {amt_pre_text + amt_post_text}',
                },
                ])
            
            section_summary = str(response.message.content)
            embedding = model.encode(section_summary)
            embedding_list = embedding.tolist() 
 
            output_json[index] = {
                "section_summary": section_summary,
                "embedding": embedding_list,
                "table": table,
                "amt_pre_text": amt_pre_text,
                "amt_post_text": amt_post_text
            }

    return output_json

def read_input_json(input_file: str) -> dict:
    """
    Read in json file.
    """    
    with open(input_file, 'r') as f:
        return json.load(f)

def write_output_json(output_file: str, data: dict) -> None:
    """
    Write to json file
    """
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

input_file = 'train.json'  
output_file = 'main_test/indexed_content_and_embedding_data.json'


input_data = read_input_json(input_file)
output_data = process_content_data(input_data)
write_output_json(output_file, output_data)

print(f"output written to {output_file}")
