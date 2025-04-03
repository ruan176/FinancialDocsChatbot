import json
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np

def calculate_matches(content_data_path: str, question_data_path: str) -> tuple:
    """
    TOOO: This method is generated to assess design performance, for a prototype, this would need to be modified to
        return the 'closest match' content itself from the content_data_path json file which would be used as
        'CONTEXT' in the response_test.py file.

    Method iterates through content and questions, embedding questions and using a cosine similarity to match
    question to closest section summary. If a correct match is made, match_count is incremented by 1.

    returns: match_count (number of correct section matches) and total iterations to generate precision score.
    """
    with open(content_data_path, 'r') as f1:
        content_data = json.load(f1)
    
    with open(question_data_path, 'r') as f2:
        question_data = json.load(f2)

    # create instance to embed questions
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # define counters for precision metric calculation
    match_count = 0
    total_loops = 0

    # Loop through questions
    for item in question_data:
        # double check the item has a valid 'index' that matches a key in the content data - this lets you provide a subset
        # of random questions to test over ALL content data.
        if str(item['index']) in content_data:
            total_loops += 1

            # create embedding representation of question to complete cosine similarity..
            question_text = item['question']
            question_embedding = model.encode([question_text])

            closest_match_index = None
            # set initially to -1 and iterate to find closest match
            closest_cosine_sim = -1 

            # Compare with all items in the content
            for key, first_item in content_data.items():
                first_item_embedding = np.array(first_item['embedding']).reshape(1, -1)
                # skip any empty embeddings...
                if first_item_embedding.size == 0:
                    continue

                cosine_sim = cosine_similarity(question_embedding, first_item_embedding)[0][0]
                
                # check if result is the closest match so far and update closest_cosine_sim if it is.
                if cosine_sim > closest_cosine_sim:
                    closest_cosine_sim = cosine_sim
                    closest_match_index = key 

            # Check if match found is 'correct' 
            if closest_match_index == str(item['index']):
                match_count += 1

            # NOTE: Code below commented out follows similar logic above but returns the top X cosine matches,
            # as discussed in README.md this could be used to prompt the LLM X times and enable answer options to
            # be generated and a 'best answer' returned..

            # cosine_similarities = []

            # for key, first_item in first_json.items():
            #     first_item_embedding = np.array(first_item['embedding']).reshape(1, -1)
            #     if first_item_embedding.size == 0:
            #         continue

            #     cosine_sim = cosine_similarity(question_embedding, first_item_embedding)[0][0]
            #     cosine_similarities.append((key, cosine_sim))

            # # Sort the cosine similarities in descending order
            # cosine_similarities.sort(key=lambda x: x[1], reverse=True)

            # # Check if any of the top 3 matches have the same index as the current question's index
            # top_3_matches = cosine_similarities[:3]

            # for match in top_3_matches:
            #     match_key = match[0]
            #     if match_key == str(item['index']):
            #         match_count += 1
            #         break  # Exit the loop as we've found the match

    return match_count, total_loops

content_data_path = 'main_test/deduplicated_content_json.json'
question_data_path = 'main_test/indexed_output_rag_data_main.json'

match_count, total_loops = calculate_matches(content_data_path, question_data_path)
print(f"Total matches: {match_count}")
print(f"Total loops: {total_loops}")
