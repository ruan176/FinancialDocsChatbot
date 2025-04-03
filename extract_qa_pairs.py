import json

def process_qa_rag_data(input_json: dict) -> dict:
    """
    Extract question and answer pairs for prototype testing.
    """
    output_list = []

    for index, item in enumerate(input_json):
        # start by checking the if 'qa' key is present.
        qa = item.get('qa', {})
        if qa:
            output_list.append({
                'index': index,  
                'section': 'qa',
                'question': qa.get('question', ''),
                'answer': qa.get('answer', '')
            })

        # if no qa key, then loop through the qa_0 to qa_n
        # define i for incremental numbering...
        i = 0 
        while True:
            qa_section = item.get(f'qa_{i}', {})
            # exit the loop when no more sections exist
            if not qa_section:
                break
            output_list.append({
                'index': index,  
                'section': f'qa_{i}',
                'question': qa_section.get('question', ''),
                'answer': qa_section.get('answer', '')
            })
            # increment i for next section
            i += 1

    return [dict(t) for t in {tuple(d.items()) for d in output_list}]

def read_input_json(input_file_path: str) -> dict:
    """
    read json file in as dict.
    """
    with open(input_file_path, 'r') as f:
        return json.load(f)

def write_output_json(output_file_path: str, data: dict) -> None:
    """
    write output to json file.
    """
    with open(output_file_path, 'w') as f:
        json.dump(data, f, indent=4)


input_file = 'train.json'  
output_file = 'main_test/indexed_qa_data_main.json'

input_data = read_input_json(input_file)
output_data = process_qa_rag_data(input_data)
write_output_json(output_file, output_data)

print(f"Output written to {output_file}")
