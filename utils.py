import json
import pandas as pd
from openai import OpenAI
from jsonschema import validate


def load_file(file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        data = file.read()
    return data


def load_excel_data(data_path, sheet):
    data = pd.read_excel(data_path, sheet_name=sheet)
    return data


def save_excel_data(data_path, sheet, data):
    writer = pd.ExcelWriter(data_path)
    data = pd.DataFrame(data)
    data.to_excel(writer, sheet_name=sheet)
    writer.close()
    return


def post_request_by_openai_format(input_base_url, key, model_name, input_message):
    client = OpenAI(
        base_url=input_base_url,
        api_key=key
    )

    completion = client.chat.completions.create(
        extra_headers={},
        extra_body={},
        model=model_name,
        messages=input_message,
        temperature=0
    )

    return completion.choices[0].message.content, completion.usage.prompt_tokens, completion.usage.completion_tokens


'''
you can add your own method of calling LLM inference API and replace the method in running_inference.py or running_inference_continue.py
'''

def compare_values(answer, model_output):
    # base case
    if isinstance(answer, (str, bool, int, float)):
            return 1 if answer == model_output else 0

    # list case
    elif isinstance(answer, list):
        # if list is empty, return 1 when model output is also empty
        if not answer:
            return 1 if (isinstance(model_output, list) and not model_output) else 0

        # if list of dict, compare index by index
        if all(isinstance(item, dict) for item in answer):
            if not isinstance(model_output, list) or not all(isinstance(item, dict) for item in model_output):
                return 0
            
            score = 0
            min_len = min(len(answer), len(model_output))
            max_len = max(len(answer), len(model_output)) ## as it is hard for list of dict to calculate union, use max length to substitute

            for i in range(min_len):
                score += compare_values(answer[i], model_output[i])

            return score / max_len if (max_len > 0) else 1
        
        # if list of base data types, compute Jaccard similarity
        else:
            if not isinstance(model_output, list):
                return 0
            
            answer_set = set(answer)
            model_output_set = set(model_output)

            common_elements = answer_set & model_output_set
            all_elements = answer_set | model_output_set

            return len(common_elements) / len(all_elements) if all_elements else 1

    # dict case   
    elif isinstance(answer, dict):
        if not isinstance(model_output, dict):
            return 0
        
        answer_keys = set(answer.keys())
        if not answer_keys: # empty dict
                return 1 if not model_output else 0
        
        all_keys = answer_keys.union(set(model_output.keys()))

        score = 0
        for key in answer_keys:
            if key in model_output:
                # compare the value in common keys recursively
                score += compare_values(answer[key], model_output[key])

        return score / len(all_keys) if all_keys else 1
    
    # other data types 
    else:
        return 0



def json_evaluation_new(model_output: str, answer: str, schema: dict):
    try:
        raw_json_answer = model_output.split("```json")[-1].split("```")[0]
    except:
        return 0, 0, 0, "No markdown style JSON Pattern found"
    
    try:
        model_output_json = json.loads(raw_json_answer)
    except:
        return 0, 0, 0, "Not a invalid JSON"
    
    answer_json = json.loads(answer)
    try:
        validate(instance=model_output_json, schema=schema)
    except:
        return 0, 0, 0, "JSON output doesn't match the schema"
    
    format_score = 1

    if model_output_json == answer_json:
        strict_score = 1
    else:
        strict_score = 0

    similarity_score = compare_values(answer_json, model_output_json)

    return format_score, similarity_score, strict_score, "Give score in 3 criteria"