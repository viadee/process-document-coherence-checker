import os
import time
from dotenv import load_dotenv
from openai import AzureOpenAI
import json
from utils import extract_outermost_json, calculate_api_costs
from llm_prompt_generator import task_bpmn_comparison_generator, task_txt_coherence_generator

def chat_completion(task: str):
    """Process and handle calling out to the AI service with a specific task."""
    load_dotenv()
    # Create client
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_API_KEY"),
        api_version="2024-07-01-preview",
        azure_endpoint=os.getenv("AZURE_API_URL"),
    )

    cooldown = 60
    MAX_RETRIES = 5
    attempt = 0
    while attempt < MAX_RETRIES:
        system_msg = {
            "role": "system",
            "content": """
            Below you can see your task. 
            """
        }

        task_msg = {
            "role": "user",
            "content": f"Your task: {task}"
        }

        messages = [system_msg, task_msg]
        gpt_model = "gpt-4o"

        try:
            # The API call is placed inside the try block to handle potential exceptions directly related to the API interaction
            chat_completion_response = client.chat.completions.create(
                model=gpt_model,
                temperature=0,
                messages=messages,
                response_format={"type": "json_object"},
            )
        except Exception as e:  # Catching a general exception
            print(f"API call failed due to {e}, retrying in {cooldown} seconds...")
            time.sleep(cooldown)
            attempt += 1
            continue

        response_text = chat_completion_response.choices[0].message.content
        input_tokens = chat_completion_response.usage.prompt_tokens
        output_tokens = chat_completion_response.usage.completion_tokens
        api_costs = calculate_api_costs(gpt_model, input_tokens, output_tokens)

        print("\nNumber of Input Tokens:", input_tokens)
        print("Number of Output Tokens:", output_tokens)
        print("\nTotal api costs for this query are approximately", "{:.6f} €".format(api_costs))

        return response_text, input_tokens, output_tokens, api_costs
    
    print("Maximum retries reached, operation failed.")
    return None, 0, 0, 0

def llm_coherence_check(filename1: str, content1: str, filename2: str, content2: str, txt_filename: str, txt_content: str):
    """Generate management summaries of differences in content between two BPMN models and their coherence with a text file."""
    
    #TODO: First only test whether check is needed using GPT4o-mini    
    task_bpmn_comparison = task_bpmn_comparison_generator(filename1, content1, filename2, content2)

    bpmn_comparison_output = chat_completion(task_bpmn_comparison)
    bpmn_comparison_result = bpmn_comparison_output[0]
    bpmn_comparison_input_tokens = bpmn_comparison_output[1]
    bpmn_comparison_output_tokens = bpmn_comparison_output[2]
    bpmn_comparison_api_costs = bpmn_comparison_output[3]

    print("\n" + "Answer of the LLM-enabled Coherence Checking for BPMN Comparison:" + "\n")
    print(bpmn_comparison_result)

    # Extract JSON from the response, for the case that the output has text outside of the json format
    bpmn_comparison_result_json = extract_outermost_json(bpmn_comparison_result)

    if not bpmn_comparison_result_json:
        print("Failed to find JSON in the response.")
        print("Response was:", bpmn_comparison_result)
        return None, None

    try:
        bpmn_comparison_data = json.loads(bpmn_comparison_result_json)
    except json.JSONDecodeError as e:
        print("JSON decoding failed:", e)
        return None, None, None, None
    
    incoherence_risk = bpmn_comparison_data.get("incoherence_risk", True)
    technical_comparison_empty = not bpmn_comparison_data.get("technical_comparison", False)

    if not incoherence_risk or technical_comparison_empty:
        print("Process terminated because no incoherence risk was detected in the given files.")
        return bpmn_comparison_result_json, None, (bpmn_comparison_input_tokens+bpmn_comparison_output_tokens), (bpmn_comparison_api_costs)
    else:
        print("Incoherence Risk is True \n")
        try:
            management_summary_bpmn = json.dumps(bpmn_comparison_data.get("management_summary", "No management_summary found"), indent=2)
            print("\n" + "Management Summary from BPMN Comparison:" + "\n" + management_summary_bpmn)
        except (json.JSONDecodeError, TypeError) as e:
            print("Error parsing bpmn_comparison_result JSON:", e)

    # Remove the 'initial_chain_of_thought' key from the copied dictionary
    stripped_bpmn_comparison_data = bpmn_comparison_data.copy()
    stripped_bpmn_comparison_data.pop("initial_chain_of_thought", None)  # Use None as the default value to avoid KeyError if key doesn't exist

    # print("Pausing API requests for 30 seconds.")
    # time.sleep(30)

    # Step 2: Check coherence with the latest .txt file
    task_txt_coherence = task_txt_coherence_generator(filename1, content1, txt_filename, txt_content, stripped_bpmn_comparison_data)
    
    txt_coherence_output = chat_completion(task_txt_coherence)
    txt_coherence_result = txt_coherence_output[0]
    txt_coherence_input_tokens = txt_coherence_output[1]
    txt_coherence_output_tokens = txt_coherence_output[2]
    txt_coherence_api_costs = txt_coherence_output[3]
    
    print("\n" + "Answer of the LLM-enabled Coherence Check with Textual Documentation:" + "\n")
    print(txt_coherence_result)


    # Extract management_summary and print it
    try:
        txt_coherence_data = json.loads(extract_outermost_json(txt_coherence_result))
        management_summary = json.dumps(txt_coherence_data.get("management_summary", "No management_summary found"), indent=2)
        print("\n" + "Management Summary:" + "\n" + management_summary)
    except (json.JSONDecodeError, TypeError) as e:
        print("Error parsing txt_coherence_result JSON:", e)

    try:
        txt_coherence_data = json.loads(extract_outermost_json(txt_coherence_result))
        management_summary = json.dumps(txt_coherence_data.get("changes_needed", "No changes_needed found"), indent=2)
        print("\n" + "Changes needed to restore coherence with the updated source document:" + "\n" + management_summary)
    except (json.JSONDecodeError, TypeError) as e:
        print("Error parsing txt_coherence_result JSON:", e)

    return bpmn_comparison_result, txt_coherence_result, (bpmn_comparison_input_tokens+bpmn_comparison_output_tokens+txt_coherence_input_tokens+txt_coherence_output_tokens), (bpmn_comparison_api_costs+txt_coherence_api_costs)


