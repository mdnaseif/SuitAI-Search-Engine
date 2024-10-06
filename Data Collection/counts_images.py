import os
import json

def load_existing_data(output_json_path):
    image_count = 0  # Initialize a counter for the images
    if os.path.exists(output_json_path):
        with open(output_json_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        print("Resuming from where left off, already processed images:")
        for item in data:
            # print(item["image"])
            image_count += 1  # Increment the counter for each image
        print(f"Total number of images processed: {image_count}")  # Print the total count of images
        return image_count
    return []


path = r'C:\Users\4010356\Downloads\diffusers\output_full.jsonl'
load_existing_data(path)