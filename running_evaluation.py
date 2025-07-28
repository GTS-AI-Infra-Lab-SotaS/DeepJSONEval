import utils
import argparse
import os
import json

def get_args():
    parser = argparse.ArgumentParser('DeepJSON evaluation script') 
    parser.add_argument('--load-path', default='', type=str, help='the path of folder in which the inference result file locates')
    parser.add_argument('--saving-path', default='', type=str, help='the path of folder in which place the evaluation result file')
    return parser.parse_args()



args = get_args()

files = os.listdir(args.load_path)
for file in files:
    file_path = os.path.join(args.load_path, file)
    content = utils.load_excel_data(file_path, 'sheet1')
    to_save = content.to_dict(orient='list')
    to_save["format_score"] = []
    to_save["detailed_score"] = []
    to_save["strict_score"] = []
    to_save["Notes"] = []
    for i in range(len(content["schema"])):
        current_model_output = content["model_output"][i]
        current_answer = content["json"][i]
        current_schema = json.loads(content["schema"][i])
        score =utils.json_evaluation_new(current_model_output,current_answer, current_schema)
        to_save["format_score"].append(score[0])
        to_save["detailed_score"].append(score[1])
        to_save["strict_score"].append(score[2])
        to_save["Notes"].append(score[3])
    
    utils.save_excel_data(os.path.join(args.saving_path, file), 'sheet1', to_save)