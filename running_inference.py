import utils
from tqdm import tqdm
import os
import argparse

def get_args():
    parser = argparse.ArgumentParser('DeepJSON inference script')
    parser.add_argument('--base-url', default='', type=str, help="base url of LLM chat api")
    parser.add_argument('--key', default='', type=str, help='api key for using the LLM chat api')    
    parser.add_argument('--model-name', default='', type=str, help='name of model when post request to the LLM chat api')
    parser.add_argument('--saving-path', default='', type=str, help='the path of folder in which the inference result file locates')
    return parser.parse_args()



args = get_args()

benchmark_file = 'DeepJSON_benchmark.xlsx'

benchmark_info = utils.load_excel_data(benchmark_file, 'sheet1')

to_save = benchmark_info.to_dict(orient='list')

to_save["model_output"] = []
to_save["prompt_tokens"] = []
to_save["completion_tokens"] = []

for i in tqdm(range(len(benchmark_info['schema']))):
    current_text = benchmark_info['text'][i]
    curent_schema = benchmark_info['schema'][i]
    first_half = utils.load_file(r'JSON_Output_meta_prompt.txt')
    second_half = f"*** JSON Schema\n{curent_schema}\n\n*** Text Description\n{current_text}"
    input_message = [{"role": "user", "content": first_half + '\n' + second_half}]
    try:
        result = utils.post_request_by_openai_format(args.base_url, args.key, args.model_name, input_message)   ## openai style of calling LLM API
    except:
        result = ["Need Retry"] * 3
    to_save["model_output"].append(result[0])
    to_save["prompt_tokens"].append(result[1])
    to_save["completion_tokens"].append(result[2])
save_file_name = args.model_name.split('/')[-1].split(':')[0] + '.xlsx'
utils.save_excel_data(os.path.join(args.saving_path, save_file_name), 'sheet1', to_save)
