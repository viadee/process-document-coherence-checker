import os
from gpt_interaction import llm_coherence_check
from bpmn_preprocessing import BPMNPreprocessing
from utils import find_recent_files_in_directory, parse_xml_to_string

def run_coherence_check(directory):
    """Perform the coherence checking for given directory."""
    recent_bpmn_paths = find_recent_files_in_directory(directory, '.bpmn', 2)
    recent_txt_paths = find_recent_files_in_directory(directory, '.txt', 1)

    result = {
        'bpmn_comparison_result_json': None,
        'txt_coherence_result': None,
        'total_tokens': 0,
        'total_api_cost': 0
    }

    if len(recent_bpmn_paths) < 2 or len(recent_txt_paths) < 1:
        print("Insufficient number of files to perform a comparison.")
        return result

    preprocessor = BPMNPreprocessing(directory)
    processed_bpmn_files = preprocessor.preprocess_files(recent_bpmn_paths)

    bpmn_file_representations = [parse_xml_to_string(file) for file in processed_bpmn_files]
    txt_file_path = recent_txt_paths[0]
    txt_file_name = os.path.basename(txt_file_path)
    
    with open(txt_file_path, 'r') as file:
        txt_file_content = file.read()

    if bpmn_file_representations[0] == bpmn_file_representations[1]:
        print("The two most recently modified BPMN files are identical.")
    else:
        result['bpmn_comparison_result_json'], result['txt_coherence_result'], result['total_tokens'], result['total_api_cost'] = llm_coherence_check(
            os.path.basename(recent_bpmn_paths[0]), bpmn_file_representations[0],
            os.path.basename(recent_bpmn_paths[1]), bpmn_file_representations[1],
            txt_file_name, txt_file_content
        )
    return result