import json
import uuid

# Assuming the input data is stored in "input_data.jsnol" with each line as a separate JSON object
input_file_path = r"Data\train\metadata.jsonl"
output_file_path = 'data_for_llava.json'

# Function to generate a conversation based on the additional_feature
def generate_conversation(description):
    # This is a placeholder function. You'll need to replace this with logic that converts
    # the description into a prompt for an image generation model.
    prompt = "Write a detailed description to generate an image based on the text."
    return [
        {"from": "human", "value": "<image>\nWrite a prompt for Stable Diffusion to generate this image."},
        {"from": "gpt", "value": prompt}
    ]

transformed_data = []

with open(input_file_path, 'r') as infile:
    for line in infile:
        # Convert each line of the file into a dictionary
        item = json.loads(line)
        
        # Generate a unique ID for each entry
        unique_id = str(uuid.uuid4())
        
        # Generate the new structure
        new_item = {
            "id": unique_id,
            "image": f"{item['file_name']}",
            "conversations": generate_conversation(item["additional_feature"])
        }
        
        transformed_data.append(new_item)

# Write the transformed data to a new JSON file
with open(output_file_path, 'w') as outfile:
    json.dump(transformed_data, outfile, indent=2)

print(f"Data conversion complete. Output file: {output_file_path}")
