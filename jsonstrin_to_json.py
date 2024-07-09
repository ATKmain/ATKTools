import json

def prettify_json_string(file_path):
    try:
        # Read the JSON string from the file
        with open(file_path, 'r') as file:
            json_str = file.read().strip('"')
            json_str = json_str.replace('\\"', '"')
        
        # Convert the JSON string to a Python dictionary
        json_data = json.loads(json_str)
        
        # Convert the Python dictionary back to a JSON string with indentation
        pretty_json_str = json.dumps(json_data, indent=4)
        
        # Save the indented JSON string back to the same file
        with open(file_path, 'w') as file:
            file.write(pretty_json_str)
        
        print("Successfully converted to indented JSON format.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'path_to_your_file.json' with the actual file path
prettify_json_string('tmp/file1_Coles.V2.json')
