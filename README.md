# DeepJSON: Benchmarking Complex Nested JSON Generation in Large Language Models

- [DeepJSON: Benchmarking Complex Nested JSON Generation in Large Language Models](#deepjson--benchmarking-complex-nested-json-generation-in-large-language-models)
  * [Introduction](#introduction)
  * [Dataset Generation](#dataset-generation)
    + [Tree Based Pseudo-Schema Candidates Generation](#tree-based-pseudo-schema-candidates-generation)
    + [Standard JSON Schema Generation](#standard-json-schema-generation)
    + [JSON Object Generation](#json-object-generation)
    + [Text Generation](#text-generation)
  * [Evaluation Criteria](#evaluation-criteria)
  * [Inference and Evaluation](#inference-and-evaluation)
    + [Environment](#environment)
    + [Data](#data)
    + [Running Inference](#running-inference)
    + [Continue Running Inference](#continue-running-inference)
    + [Running Evaluation](#running-evaluation)
  * [Cite](#cite)
 
## Introduction
We propose Deep-JSON, a pioneering deep-nested JSON evaluation benchmark and framework designed to comprehensively assess LLM capabilities in complex structured output generation.
Our approach introduces several groundbreaking innovations: 
* We introduce an innovative DFS subtree search-based schema generation algorithm that effectively supports the construction of complex nested structures.
* We implement comprehensive data type coverage, incorporating strings, numbers, boolean values, string enumerations, and lists to systematically evaluate LLM robustness across different data types. Third, we develop a novel multidimensional fine-grained evaluation framework encompassing format matching accuracy, field correctness, and complete structural correctness, providing multi-perspective and detailed assessment of JSON generation quality. 
* We design the evaluation framework specifically targeting deep nesting structures, featuring JSON schemas with 3 to 7 levels of nesting depth, significantly enhancing evaluation complexity and real-world applicability.
Each field includes detailed descriptions to rigorously examine LLMs’ instruction-following capabilities and precise information extraction under complex format constraints and semantic understanding requirements. 


DeepJSON establishes a new standard for objective and comprehensive evaluation of LLM structured output capabilities through its innovative evaluation dimensions, rigorous difficulty classification, detailed field descriptions, and large-scale multi-domain coverage. 
Our benchmark comprises **525** high-quality data instances spanning ten diverse domains including **tourism attractions, digital devices, healthcare, athletes, natural plants, stocks, student records, vehicles, movies, and video games**. 
We implement systematic difficulty grading based on nesting depth, categorizing 3-4 level structures as **Medium** and 5-7 level structures as **Hard**, providing progressive evaluation benchmarks for model capabilities. 
The comprehensive evaluation framework reveals significant performance gaps in current stateof-the-art models when handling complex nested structures, highlighting critical areas for improvement in LLM development.
Our multi-dimensional assessment approach enables precise identification of specific failure modes, from format compliance issues to semantic understanding deficiencies.


The performance of 12 representative SOTA LLMs with leading capabilities on our **DeepJSON** benchmark is presented.

## Dataset Generation
### Tree Based Pseudo-Schema Candidates Generation
Given the inherently nested and hierarchical structure of JSON schemas, we propose a novel tree-based iterative search methodology for systematically generating diverse schema variants. 
This approach addresses the fundamental challenge of exploring the vast combinatorial space of possible schema configurations while maintaining structural validity and semantic coherence.

### Standard JSON Schema Generation 
Given the pseudoschemas derived from our tree-based methodology, we employ a large language model (LLM) to transform these intermediate structures into standardized JSON schemas. 
The transformation process involves prompting the LLM with carefully designed instructions to generate syntactically correct and semantically valid JSON schema specifications that
conform to established standards

### JSON Object Generation 
With validated JSON schemas in hand, we subsequently employ the LLM to generate corresponding JSON objects that strictly adhere to the structural and semantic constraints defined by each schema. 
Through a carefully designed prompt template, the LLM produces JSON objects that maintain rigorous compliance with their respective schemas.

### Text Generation 
In the final stage of our data synthesis pipeline, we integrate the validated JSON schemas with their corresponding JSON objects and employ the LLM to generate coherent natural language text that encompasses the structural and semantic information encoded within these paired elements. 
This process yields a comprehensive synthetic dataset comprising triplets of natural language text, JSON schemas, and JSON objects, where each component maintains strict correspondence with the others.

## Evaluation Criteria
* **Criterion 1: Format Score**  
This criterion evaluates LLMs’ ability to generate syntactically
valid JSON outputs through sequential validation
of parsing and schema conformance,
* **Criterion 2: Detailed Content Score**
This criterion performs comprehensive property-wise comparison with uniform weighting across all hierarchical levels, computing weighted differences through systematic
structural traversal
* **Criterion 3: Strictly Score**  
This criterion implements binary exact-match evaluation through strict equality verification between LLM output and ground truth JSON

## Inference and Evaluation
### Environment
Before using the benchmark for Model inference and evaluation, make sure all the package in the `requirements.txt` are installed. Or you can install the packages by

```bash
pip install -r requirements.txt
```
### Data
Download `DeepJSON_benchmark.xlsx` in this Github project or [HuggingFace](https://huggingface.co/datasets/GTSAIInfraLabSOTAS/DeepJSON)

The benchmark dataset has 5 columns: `schema`, `text`, `json`, `category` and `true_depth`.
* `schema`: the JSON schema for JSON output
* `text`: the plain text in natrual language to be extract
* `json`: the ground truth matching the `schema`
* `category`: domain of the data peice
* `true_depth`: the number of levels of nesting depth
### Running Inference
We use API in OpenRouter website to run the infernece: 
```python
python running_infenrence.py --base-url 'url' --key 'api-key' --model-name 'model_name' --saving-path 'whre to save the inference result'
```
* `--base-url`: base url of LLM chat api
* `--key`: api key for using the LLM chat api
* `--model-name`: name of model when post request to the LLM chat api
* `--saving-path`: the path of folder in which the inference result file locates

If do not use the API in OpenRouter website, users can create your own method of geetting inference result and change **line 35** in `running_infenrence.py`
### Continue Running Inference 
The online LLM API could be unstale as running out of credits or request congestion, some result in the inference result will be marked as **"Need Retry"**. Use `running_infenrence_continue.py` to post requests on those data pieces need retry.
```python
python running_infenrence_continue.py --base-url 'url' --key 'api-key' --model-name 'model_name' --saving-path 'whre to save the inference result'
```
### Running Evaluation
```python
python running_evaluation.py --load-path 'whre to save the inference result'  --saving-path 'where to save the evaluation result'
```
* `--load-path`: the path of folder in which the inference result file locates
* `--saving-path`: the path of folder in which place the evaluation result file
## Cite
