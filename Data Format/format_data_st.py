# import csv
# import json

# # The path to your CSV file
# csv_file_path = r"C:\Users\4010356\Downloads\updated_descriptions 8.csv"
# # The path to your output JSON Lines file
# jsonl_file_path = 'data_v1.jsonl'

# # Open the CSV file and read its content
# with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
#     # Create a CSV reader object
#     csv_reader = csv.DictReader(csv_file)
    
#     # Open the JSON Lines file for writing
#     with open(jsonl_file_path, mode='w', encoding='utf-8') as jsonl_file:
#         # Iterate over each row in the CSV
#         for row in csv_reader:
#             # Convert each row into the desired JSON object
#             json_object = {
#                 "file_name": row["image"],
#                 "additional_feature": row["caption"]
#             }
            
#             # Write the JSON object to the JSON Lines file
#             jsonl_file.write(json.dumps(json_object) + '\n')





# import csv
# import os
# import shutil

# # Define the paths
# csv_file_path = r"C:\Users\4010356\Downloads\updated_descriptions 8.csv"
# source_directory = 'C:/Users/4010356/Downloads/archive/fashion-dataset/images'
# destination_directory = r'C:\Users\4010356\Desktop\New folder\data_fashion'

# # Make sure the destination directory exists
# os.makedirs(destination_directory, exist_ok=True)

# # Keep track of images that have already been copied to avoid repetition
# copied_images = set()

# # Open and read the CSV file
# with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
#     csv_reader = csv.DictReader(csv_file)
#     for row in csv_reader:
#         image_name = row['image']
        
#         # Check if the image has already been copied
#         if image_name not in copied_images:
#             source_path = os.path.join(source_directory, image_name)
#             destination_path = os.path.join(destination_directory, image_name)
            
#             # Check if the image exists in the source directory
#             if os.path.exists(source_path):
#                 # Copy the image to the destination directory
#                 shutil.copy2(source_path, destination_path)
#                 # Mark the image as copied
#                 copied_images.add(image_name)
#                 print(f'Copied {image_name} to {destination_directory}')
#             else:
#                 print(f'{image_name} not found in source directory.')










# import csv
# import json

# # Path to the CSV file containing the first data format
# csv_file_path = r'c:\Users\4010356\Desktop\New folder\fffffff.csv'
# # Path to the JSON file where the second data format will be saved
# json_file_path = 'metadata_v2.jsonl'

# # Function to transform and save data
# def transform_data(csv_path, json_path):
#     transformed_data = []

#     with open(csv_path, mode='r', encoding='utf-8') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for i, row in enumerate(reader):
#             # Assuming you want to keep the GPT Conversations as the additional feature
#             additional_feature = row['GPT Conversations']
#             # Construct the file_name based on a sequence, starting from 0001.png
#             file_name = f"{i+1:04d}.png"
#             transformed_data.append({
#                 "file_name": file_name,
#                 "additional_feature": additional_feature
#             })

#     # Save the transformed data into a JSON file
#     with open(json_path, mode='w', encoding='utf-8') as jsonfile:
#         for item in transformed_data:
#             json.dump(item, jsonfile)
#             jsonfile.write('\n')  # Write each item on a new line

# # Call the function with your file paths
# transform_data(csv_file_path, json_file_path)

# print("Data transformation complete.")



















# # Define the paths to your original jsonl files
# jsonl_file_path1 = 'metadata_v2.jsonl'
# jsonl_file_path2 = 'metadata.jsonl'

# # Define the path for the merged output file
# merged_jsonl_file_path = 'vvvvvv.jsonl'

# # Open the new file in write mode
# with open(merged_jsonl_file_path, 'w', encoding='utf-8') as merged_file:
#     # Process the first file
#     with open(jsonl_file_path1, 'r', encoding='utf-8') as file1:
#         for line in file1:
#             merged_file.write(line)
    
#     # Process the second file
#     with open(jsonl_file_path2, 'r', encoding='utf-8') as file2:
#         for line in file2:
#             merged_file.write(line)

# print("Files have been merged successfully.")











# import json
# import os
# import shutil

# # Path to the JSON file containing the data
# json_file_path = r'C:\Users\4010356\Desktop\New folder\updated_descriptions copy 2.json'

# # Paths to the source and destination folders
# source_folder_path = r'C:\Users\4010356\Downloads\archive\fashion-dataset\images'
# destination_folder_path = r'C:\Users\4010356\Desktop\New folder\images_fashion'

# def copy_images(data, source_folder, destination_folder):
#     for item in data:
#         image_name = item.get('image')
#         source_image_path = os.path.join(source_folder, image_name)
#         destination_image_path = os.path.join(destination_folder, image_name)
        
#         # Check if the source image exists
#         if os.path.exists(source_image_path):
#             # Copy the image to the destination folder
#             shutil.copy2(source_image_path, destination_image_path)
#             print(f"Copied {image_name} to {destination_folder}")
#         else:
#             print(f"Image {image_name} not found in source folder.")

# # Read the JSON data from the file
# # Read the JSON data from the file with UTF-8 encoding
# with open(json_file_path, 'r', encoding='utf-8') as file:
#     data = json.load(file)


# # # Copy the images from the source to the destination folder
# copy_images(data, source_folder_path, destination_folder_path)









# import json

# # Assuming 'data' is already loaded from the 'updated_descriptions copy 2.json' file
# # with the structure similar to the provided JSON content.

# json_file_path = r'C:\Users\4010356\Desktop\New folder\updated_descriptions copy 2.json'

# with open(json_file_path, 'r', encoding='utf-8') as file:
#     data = json.load(file)

# # Convert the data to the specified JSONL format, focusing only on "gpt" responses.
# jsonl_data = []

# for item in data:
#     # Combine all "gpt" responses into a single string for each item.
#     gpt_responses = " ".join([conv["value"] for conv in item["conversations"] if conv["from"] == "gpt"])
#     # Modify here: use "image" directly from the item instead of formatting it as before.
#     formatted_item = {"file_name": item["image"], "additional_feature": gpt_responses}
#     jsonl_data.append(formatted_item)

# # Convert each dictionary to a JSONL string.
# jsonl_strings = [json.dumps(item) for item in jsonl_data]
# jsonl_output = "\n".join(jsonl_strings)

# file_path = 'C:\\Users\\4010356\\Desktop\\New folder\\images_fashion\\captions.json'

# # Write the JSONL data to the file
# with open(file_path, 'w', encoding='utf-8') as file:
#     file.write(jsonl_output)




#===============================================================================================================================================


# import json
# import os

# # Define file paths
# file_1 = r'C:\Users\4010356\Desktop\New folder\updated_descriptions.json'
# file_2 = r'C:\Users\4010356\Desktop\New folder\data_hndi.json'
# file_3 = r'C:\Users\4010356\Desktop\New folder\data\amazon\captions\data_amazon_folder_1.json'
# file_4 = r'C:\Users\4010356\Desktop\New folder\data\amazon\captions\data_amazon_folder_2.json'
# file_5 = r'C:\Users\4010356\Desktop\New folder\data\amazon\captions\data_amazon_folder_3.json'
# file_6 = r'C:\Users\4010356\Desktop\New folder\data\amazon\captions\data_amazon_folder_4.json'

# # Define image paths
# image_paths = [
#     "Data\\train\\fashion",
#     "Data\\train\\hndi",
#     "Data\\train\\folder_1",
#     "Data\\train\\folder_2",
#     "Data\\train\\folder_3",
#     "Data\\train\\folder_4"
# ]

# # List of file paths
# file_paths = [file_1, file_2, file_3, file_4, file_5, file_6]

# # Function to process JSON files
# def process_json(file_path, image_path):
#     with open(file_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)
    
#     jsonl_entries = []
#     for entry in data:
#         new_entry = {}
        
#         new_entry['file_name'] = os.path.join(image_path, entry['image'])
#         gpt_values = [convo['value'] for convo in entry['conversations'] if convo['from'] == 'gpt' and convo['value'] != "Error occurred in generating content"]
#         additional_feature = ' '.join(gpt_values)
#         # Adding newline after each sentence
#         additional_feature = ' '.join([sentence.strip() + '.' for sentence in additional_feature.split('.')])
#         new_entry['additional_feature'] = additional_feature.strip()
#         jsonl_entries.append(new_entry)
    
#     return jsonl_entries

# # Create JSONL file
# output_file = 'output_full.jsonl'
# with open(output_file, 'w') as f_out:
#     for file_path, image_path in zip(file_paths, image_paths):
#         jsonl_entries = process_json(file_path, image_path)
#         for entry in jsonl_entries:
#             f_out.write(json.dumps(entry) + '\n')

# print("JSONL file created successfully!")




#=================================================================================================================================================================================================================






import jsonlines
import os

def add_path_to_file_name(jsonl_path, path_to_add, output_jsonl_path):
    with jsonlines.open(jsonl_path) as reader:
        with jsonlines.open(output_jsonl_path, mode='w') as writer:
            for item in reader:
                item['file_name'] = os.path.join(path_to_add, item['file_name'].replace('\\', os.path.sep))
                writer.write(item)

jsonl_file = "output_full.jsonl"
path_to_add = r"C:\Users\4010356\Downloads\diffusers"
output_jsonl_file ="output_v4.jsonl"

# add_path_to_file_name(jsonl_file, path_to_add, output_jsonl_file)










import os
import shutil
import json

# Function to copy images and update JSON
def copy_images_and_update_json(input_json_path, output_json_path, output_image_folder):
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = f.readlines()

    new_data = []
    counter = 1

    for line in data:
        line_data = json.loads(line)
        file_name = line_data["file_name"]
        additional_feature = line_data["additional_feature"]
        folder_name = os.path.basename(os.path.dirname(file_name))
        image_name = os.path.basename(file_name)
        new_image_name = f"{folder_name}_{image_name}"
        new_file_path = os.path.join(f'{output_image_folder}', new_image_name)
        shutil.copyfile(file_name, new_file_path)
        new_data.append({
                "file_name": new_image_name,
                "folder_name": additional_feature
            })
        counter += 1

    with open(output_json_path, 'w') as f:
        for item in new_data:
            f.write(json.dumps(item) + '\n')

# Paths
input_json_path = 'output_full.jsonl'
output_json_path = "output_v4.json"
output_image_folder = r"Data\train\data_images"

# # Ensure output directory exists
# os.makedirs(output_image_folder, exist_ok=True)

# # Copy images and update JSON
# copy_images_and_update_json(input_json_path, output_json_path, output_image_folder)

# print("Images copied and JSON updated successfully.")








import json


data = []
with open(r'C:\Users\4010356\Downloads\diffusers\Data\train\data_images\metadata.jsonl', 'r') as f:
    for line in f:
        data.append(json.loads(line))

# Modify data structure
for item in data:
    # item['image'] = item.pop('file_name')
    item['file_name'] = item.pop('image_name')
    # item['caption'] = item.pop('folder_name')


# Write modified data back to JSON file
with open(r'C:\Users\4010356\Downloads\diffusers\Data\train\data_images\metadata.jsonl', 'w') as f:
    for item in data:
        json.dump(item, f)
        f.write('\n')
