import os
import json
from coherence_checker import run_coherence_check
from llm_prompt_generator import management_summary_generator
from gpt_interaction import chat_completion
from utils import find_recent_files_in_directory, parse_xml_to_string, convert_to_markdown

def run_single_process_check(directory):
    """Run a single coherence check and generate a management summary."""
    try:
        # Fetch the two most recent BPMN files and the most recent text file
        recent_bpmn_paths = find_recent_files_in_directory(directory, '.bpmn', 2)
        recent_txt_paths = find_recent_files_in_directory(directory, '.txt', 1)

        if len(recent_bpmn_paths) < 2 or len(recent_txt_paths) < 1:
            print("Insufficient number of files to perform a comparison.")
            return

        # Run coherence check and get initial API costs
        coherence_result = run_coherence_check(directory)
        total_api_costs = coherence_result['total_api_cost']

        if coherence_result['txt_coherence_result']:
            try:
                # Parse BPMN files and read the text file content
                recent_bpmn_1_content = parse_xml_to_string(recent_bpmn_paths[0])
                recent_bpmn_2_content = parse_xml_to_string(recent_bpmn_paths[1])
                with open(recent_txt_paths[0], 'r') as file:
                    txt_file_content = file.read()

                # Create a management summary prompt
                management_summary_prompt = management_summary_generator(
                    filename1=os.path.basename(recent_bpmn_paths[0]),
                    content1=recent_bpmn_1_content,
                    txt_filename=os.path.basename(recent_txt_paths[0]),
                    txt_content=txt_file_content,
                    txt_coherence_result=coherence_result['txt_coherence_result']
                )

                # Call the LLM to generate the management summary
                management_summary_response, input_tokens, output_tokens, api_costs = chat_completion(management_summary_prompt)
                
                # Add the management summary API costs to the total
                total_api_costs += api_costs

                # Parse the JSON response
                try:
                    summary_response_json = json.loads(management_summary_response)
                except json.JSONDecodeError:
                    print("Failed to decode the JSON response from the LLM.")
                    return

                # Extract management summary and email title
                management_summary = summary_response_json.get('management_summary', 'No management summary provided.')
                email_title = summary_response_json.get('Email title', {}).get('Email Title', 'No email title provided.')
                urgency_rating = summary_response_json.get('Email title', {}).get('Urgency and Importancy Rating', '')

                # Convert the management summary to markdown format
                markdown_summary = convert_to_markdown(management_summary)

                # Print the generated management summary and total API costs
                print("""\n--------------------------------------------------------------------------------------------------------------------------------\n""")
                print(f"\nEmail Title: {urgency_rating} {email_title}")
                print("\nGenerated Management Summary (Markdown Format):\n")
                print(markdown_summary)
                print("\nTotal API Costs: {:.6f} €".format(total_api_costs))
            
            except Exception as e:
                print(f"An error occurred while generating the management summary: {e}")
        else:
            print("No coherence result generated to form a management summary.")

    except Exception as e:
        print(f"An error occurred during the process check: {e}")

if __name__ == "__main__":
    directory = r'C:\Users\B229\OneDrive - viadee Unternehmensberatung AG\Masterarbeit\Code\Data'
    run_single_process_check(directory)
