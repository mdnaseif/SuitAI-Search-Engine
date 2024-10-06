import os
import shutil
import json

def copy_specified_images(json_data, source_dir, target_dir_base):
    """
    Copies images specified in the JSON data from source_dir to target_dir_base.

    :param json_data: JSON data containing image names.
    :param source_dir: Directory where images are stored.
    :param target_dir_base: Base directory to copy the images to.
    """
    # Initial target directory
    target_dir = os.path.join(target_dir_base, "s_images")
    
    # Create target directory if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Extract image names from JSON data
    images_to_copy = [item['image'] for item in json_data]

    # Copy specified images
    for image_name in images_to_copy:
        source_path = os.path.join(source_dir, image_name)
        target_path = os.path.join(target_dir, image_name)
        if os.path.exists(source_path):
            shutil.move(source_path, target_path)
            print(f"Copied {image_name} to {target_dir}")
        else:
            print(f"Image {image_name} does not exist in {source_dir}")

def move_non_specified_images(json_data, source_dir, target_dir_base, folder_limits):
    """
    Moves images from source_dir to target_dir_base excluding the ones specified in the JSON data.
    Creates folders based on the folder_limits list, with each folder containing a number of images as specified.

    :param json_data: JSON data containing image names to exclude.
    :param source_dir: Directory where images are stored.
    :param target_dir_base: Base directory to start creating subdirectories for copied images.
    :param folder_limits: List specifying the number of images each folder should contain.
    """
    # Extract image names from JSON data to exclude
    images_to_exclude = set(item['image'] for item in json_data)

    # Initialize counters
    folder_index = 0
    copied_count = 0
    total_copied = 0

    # Get the first folder limit
    limit = folder_limits[folder_index]

    # Create the first target directory
    target_dir = os.path.join(target_dir_base, f"folder_{folder_index + 1}")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for image_name in os.listdir(source_dir):
        if image_name not in images_to_exclude and total_copied < sum(folder_limits):
            if copied_count >= limit:
                # Move to the next folder
                folder_index += 1
                if folder_index < len(folder_limits):  # Ensure we do not exceed the specified number of folders
                    limit = folder_limits[folder_index]
                    copied_count = 0  # Reset counter for the new folder
                    target_dir = os.path.join(target_dir_base, f"folder_{folder_index + 1}")
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                else:
                    break  # Stop if we have reached the specified number of folders

            source_path = os.path.join(source_dir, image_name)
            target_path = os.path.join(target_dir, image_name)
            shutil.move(source_path, target_path)  # Move the file
            copied_count += 1
            total_copied += 1
            print(f"Moved {image_name} to {target_dir}")



# Example usage
json_file_path = 'data_amazon.json'

# Reading JSON data from a file
with open(json_file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

source_directory = r'data\amazon\split_images\specified_images'
target_directory_base = r'C:\Users\4010356\Desktop\New folder\data\amazon\split_images'
folder_limits = [20000, 20000,20000]  # Example: First folder will contain 4000 images, second will contain 5000, etc.

# Copy images specified in JSON
# copy_specified_images(json_data, source_directory, target_directory_base)

# Copy non-specified images to dynamically created directories
move_non_specified_images(json_data, source_directory, target_directory_base, folder_limits)
