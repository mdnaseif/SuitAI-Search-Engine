import json
import os
import shutil

# Path to the JSON file containing the data
json_file_path = r"data\amazon\captions\data_amazon_folder_4.json"

# Paths to the source and destination folders
source_folder_path = r'data\amazon\split_images\folder_4'
destination_folder_path = r'C:\Users\4010356\Downloads\diffusers\Data\train\folder_4'

def copy_images(data, source_folder, destination_folder):
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Created directory: {destination_folder}")

    for item in data:
        image_name = item.get('image')
        source_image_path = os.path.join(source_folder, image_name)
        destination_image_path = os.path.join(destination_folder, image_name)
        
        # Check if the source image exists
        if os.path.exists(source_image_path):
            # Copy the image to the destination folder
            shutil.copy2(source_image_path, destination_image_path)
            print(f"Copied {image_name} to {destination_folder}")
        else:
            print(f"Image {image_name} not found in source folder.")

# Read the JSON data from the file
# Read the JSON data from the file with UTF-8 encoding
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)


# # Copy the images from the source to the destination folder
copy_images(data, source_folder_path, destination_folder_path)
