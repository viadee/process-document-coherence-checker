import os
import xml.etree.ElementTree as ET
import json

def parse_xml_to_string(file_path: str) -> str:
    """Parse an XML file and return a string representation of its root.
    If the input is not XML, return the raw string content of the file."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return ET.tostring(root, encoding='unicode')
    except ET.ParseError:
        # If it's not XML, read it as plain text
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

def find_recent_files_in_directory(directory: str, extension: str, file_count: int) -> list:
    """
    Search for and return the paths of the most recently modified files with the specified extension in the given directory.

    Args:
        directory (str): The path to the directory to search.
        extension (str): The file extension to search for.
        file_count (int): The number of recent files to retrieve.

    Returns:
        list: A list of file paths for the most recently modified files.
    """
    files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(extension)]
    sorted_files = sorted(files, key=os.path.getmtime, reverse=True)
    return sorted_files[:file_count]
    
def extract_outermost_json(input_str):
    """Extract the outermost JSON object from a string containing extra data."""
    open_brackets = 0
    json_str = ''
    is_json_started = False

    for char in input_str:
        if char == '{':
            if not is_json_started:
                is_json_started = True
            open_brackets += 1
        
        if is_json_started:
            json_str += char
        
        if char == '}':
            open_brackets -= 1
            if open_brackets == 0:
                break

    if open_brackets == 0 and json_str:
        try:
            # Validate JSON
            json.loads(json_str)
            return json_str
        except json.JSONDecodeError:
            print("Error: Extracted content is not valid JSON.")
            return None
            
    return None

def calculate_api_costs(model, input_tokens, output_tokens):
    if model == "gpt-4o":
        api_costs = ((input_tokens / 1000) * 0.0047 + (output_tokens / 1000) * 0.0139)
    elif model == "gpt-4o-mini":
        api_costs = ((input_tokens / 1000) * 0.000153 + (output_tokens / 1000) * 0.00062)
    else:
        print("No exact pricing information can be calculated, as the model is not listed. Model type:", model)
        api_costs = ((input_tokens / 1000) * 0.005 + (output_tokens / 1000) * 0.015)
    return api_costs

def convert_to_markdown(text: str) -> str:
    """
    Convert the generated text into human-readable markdown format.
    Args:
        text (str): The text to be converted.
    Returns:
        str: The markdown formatted text.
    """
    # Replace \n with actual new line characters
    text = text.replace("\\n", "\n")

    # Initialize markdown text
    markdown_text = ""

    # Lines split to handle each part individually
    lines = text.strip().split('\n\n')

    for line in lines:
        # Handle headers
        if line.startswith("Dear "):
            markdown_text += f"{line}\n\n"
        elif line.lower().startswith("summary of required changes to the textual document"):
            markdown_text += f"## {line.replace(':', '').strip()}\n\n"
        elif line.lower().startswith("best regards"):
            markdown_text += f"\n{line.replace(':', '').strip()}\n"
        else:
            # Process bullet points and normal text
            if line.startswith("- "):
                bullet_points = line.split('\n')
                for point in bullet_points:
                    markdown_text += f"{point.strip()}\n"
            else:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    markdown_text += f"**{parts[0].strip()}**: {parts[1].strip()}\n\n"
                else:
                    markdown_text += f"{line.strip()}\n\n"

    return markdown_text