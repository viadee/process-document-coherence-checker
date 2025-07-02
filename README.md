# Digital Appendix: LLM-Enabled Business Process Coherence Checking

## Description

This repository serves as the digital appendix for the paper:

**Title:** 'LLM-Enabled Business Process Coherence Checking Based on Multi-Level Process Documentation'  
**Authors:** Schulte, M.; Franzoi\*, S.; Köhne, F.; vom Brocke, J.  
**Submitted to:** _Process Science_ (Springer) - [Journal Link](https://link.springer.com/journal/44311)

The files provide supplementary information referenced in the paper.

## Contents

This appendix contains the following documents:

*   `Section A - Methodology - aProCheCk Appendix.pdf`
*   `Section B - Proof of Concept - aProCheCk Appendix.pdf`
*   `Section C - Interviews and Framework - aProCheCk Appendix.pdf`
*   `Section D - Development - aProCheCk Appendix.pdf`
*   `Section E - Dataset and Focus Group - aProCheCk Appendix.pdf`
*   `Section F - Notification Examples - aProCheCk Appendix.pdf`
*   `Section G - Software Instantiation - aProCheCk Appendix`

## Related Dataset

The dataset used for the empirical validation in the paper can be found here:

[Business Process Coherence Checking Dataset](https://github.com/viadee/Thesis-Business-Process-Coherence-Checking)

## Citation

If you use this appendix or the concepts from the paper, please cite the main publication.

_Preliminary Citation:_

Schulte, M., Franzoi, S., Köhne, F., & vom Brocke, J. (2025). LLM-Enabled Business Process Coherence Checking Based on Multi-Level Process Documentation. _Submitted to Process Science_.

# Software Prototype

This project leverages advanced AI models to check for incoherencies in business process documentation. The project directory is structured as follows:

Link to open-source dataset: https://github.com/viadee/Thesis-Business-Process-Coherence-Checking

## Project Structure

```
ProjectRoot/
│
├── main.py
│   └── (Entry point for running experiments or single process checks)
│
├── experiment_runner.py
│   └── run_experiment_for_directory(directory, num_runs)
│       └── log_results(directory, results)
│       └── (Calls functions in coherence_checker.py, utils.py, and result_comparison.py)
│
├── single_process_checker.py
│   └── run_single_process_check(directory)
│       └── (Handles single coherence check for files within a directory and generates a management summary)
│
├── coherence_checker.py
│   └── run_coherence_check(directory)
│       └── (Processes BPMN and text files with preprocessing & utils, then calls Azure OpenAI via gpt_interaction.py)
│
├── gpt_interaction.py
│   └── chat_completion(task)
│       └── calculate_api_costs(model, input_tokens, output_tokens)
│       └── llm_coherence_check(filename1, content1, filename2, content2, txt_filename, txt_content)
│       └── (Manages Azure OpenAI API calls, processes tasks and responses)
│
├── bpmn_preprocessing.py
│   └── BPMNPreprocessing
│       └── preprocess_files(file_paths)
│       └── remove_visual_elements(root)
│       └── save_modified_file(tree, filename)
│
├── result_comparison.py
│   └── compare_results_with_config(config, result)
│       └── (Compares AI results to expected config)
│
├── utils.py
│   └── Utility functions:
│       └── parse_xml_to_string(file_path)
│       └── find_recent_files_in_directory(directory, extension, file_count)
│       └── extract_outermost_json(input_str)
│       └── calculate_api_costs(model, input_tokens, output_tokens)
│       └── convert_to_markdown(text)
│
├── llm_prompt_generator.py
│   └── Prompt generators for AI tasks:
│       └── task_bpmn_comparison_generator(filename1, content1, filename2, content2)
│       └── task_txt_coherence_generator(filename1, content1, txt_filename, txt_content, stripped_bpmn_comparison_data)
│       └── management_summary_generator(filename1, content1, txt_filename, txt_content, txt_coherence_result)
│
├── .env
│   └── (Environment variables like AZURE_API_KEY, AZURE_API_URL)
│
├── Data/
│   └── (Contains folders with BPMN and text files for experiments)
```

## How to Run

**Setup Environment Variables:**

*   Create a `.env` file in the project root.
*   Add the necessary environment variables, including `AZURE_API_KEY` and `AZURE_API_URL`.

**Run the Program:**

*   Execute `main.py` to run experiments on all eligible subfolders within the `Data/` directory or a single process check if there are no eligible subfolders.

**Experiment Run:**

*   If there are subfolders in the `Data/` directory (excluding those named "modified"), the program will run experiments.
*   Each subfolder should contain:
    *   At least two BPMN files.
    *   At least one text file.
    *   `solution_config.json` specifying the expected changes.
*   You can set the number of runs per folder by modifying the `num_runs` variable in `main.py`:

**Single Process Check:**

*   If there are no eligible subfolders (excluding "modified") in the `Data/` directory, the program will run a single process check.
*   The `Data` directory should contain:
    *   At least two BPMN files.
    *   At least one text file.
*   The management summary and total API costs will be printed to the console.

**Review Results:**

*   For experiments: Results are logged in each folder within the `Data/` directory, under an `ExperimentLog` subdirectory. The logs include CSV files with detailed accuracy and cost metrics.
*   For a single process check: The management summary and total API costs are printed to the console.

This setup ensures a clear, modular approach to checking coherence in business process documentation, leveraging pre-built utilities and advanced AI capabilities.

## File Descriptions

**main.py**

Entry point for running multiple experiments or a single process check. It iterates over each folder in the `Data` directory, executing the coherence-checking experiments specified in each folder's `solution_config.json`. If no eligible subfolders are found, it triggers a single process check for the files directly in the `Data` directory.

**experiment\_runner.py**

Contains functions to run coherence checking experiments and log results.

*   `run_experiment_for_directory(directory, num_runs)`: Runs the coherence checking experiment for a specific directory.
*   `log_results(directory, results)`: Logs the results of the experiments into CSV and JSON files and calculates the summary.

**single\_process\_checker.py**

Handles a single coherence check for files directly within a directory and generates a management summary.

*   `run_single_process_check(directory)`: Orchestrates the coherence checking process for a single set of files, including preprocessing, AI interaction, and generating a markdown summary.

**coherence\_checker.py**

The core module that processes BPMN and text files, performs preprocessing, and calls the Azure OpenAI model via `gpt_interaction.py`.

*   `run_coherence_check(directory)`: Orchestrates the coherence checking process, including preprocessing and interaction with the AI model.

**gpt\_interaction.py**

Handles interactions with the Azure OpenAI API. It includes detailed functions to calculate API costs and manage different tasks.

*   `chat_completion(task)`: Manages chat completions with the AI model, handling retries and exceptions.
*   `llm_coherence_check(...)`: Conducts coherence checking for BPMN and text files, using AI for verification and producing management summaries.

**bpmn\_preprocessing.py**

Contains functionality to preprocess BPMN files by removing visual elements and saving the modified files.

*   `BPMNPreprocessing`: A class handling BPMN file preprocessing.
    *   `preprocess_files(file_paths)`: Preprocesses BPMN files.
    *   `remove_visual_elements(root)`: Removes visual elements from BPMN XML.
    *   `save_modified_file(tree, filename)`: Saves the modified XML tree to a new file.

**result\_comparison.py**

Compares results from the AI model with the expected changes defined in the configuration files.

*   `compare_results_with_config(config, result)`: Compares AI results with expected configurations and calculates accuracy and coherence indicators.

**utils.py**

Utility functions for various operations such as reading files, parsing XML, extracting JSON, and calculating API costs.

*   `parse_xml_to_string(file_path)`: Parses an XML file to a string representation.
*   `find_recent_files_in_directory(directory, extension, file_count)`: Finds the most recent files in a directory.
*   `extract_outermost_json(input_str)`: Extracts the outermost JSON object from a string.
*   `calculate_api_costs(model, input_tokens, output_tokens)`: Calculates the costs of API usage.
*   `convert_to_markdown(text)`: Converts plain text to markdown format.

**llm\_prompt\_generator.py**

Stores all prompt templates used for generating tasks for the AI model.

*   `task_bpmn_comparison_generator(filename1, content1, filename2, content2)`: Generates a comparison task for BPMN files.
*   `task_txt_coherence_generator(filename1, content1, txt_filename, txt_content, stripped_bpmn_comparison_data)`: Generates a coherence check task for BPMN and text files.
*   `management_summary_generator(filename1, content1, txt_filename, txt_content, txt_coherence_result)`: Generates a management summary for the detected incoherency.

**.env**

Contains environment variables required for the project, such as `AZURE_API_KEY` and `AZURE_API_URL`.

**Data/**

Directory containing folders with BPMN and text files for running experiments. Each folder should have a `solution_config.json` file specifying the expected changes.

```python
num_runs = 5  # Adjust the number of runs as needed
```
