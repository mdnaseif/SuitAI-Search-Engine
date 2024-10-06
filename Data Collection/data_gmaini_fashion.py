# import pathlib
# import json
# import os
# import pandas as pd
# import re
# from tqdm import tqdm

# # Assuming 'google.generativeai' and 'GenModel' are placeholders for actual API usage,
# # replace them with your actual API client and model if different.
# import google.generativeai as genai

# # Configure the API
# genai.configure(api_key="AIzaSyCFf-8Pte-vOemfu9V8Z6ZbVrSlSoBfOGM")

# # Initialize the model
# model = genai.GenerativeModel('gemini-pro-vision')

# # Define the directory containing images
# directory_path = pathlib.Path("images")

# # Define the output JSON file path
# output_json_path = 'updated_descriptions.json'

# # Function to generate content for each question
# def generate_content_for_questions(image_data, questions):
#     responses = []
#     for question in questions:
#         try:
#             response = model.generate_content(contents=[question, {'mime_type': 'image/jpeg', 'data': image_data}])
#             responses.append({"from": "gpt", "value": response.text})
#         except Exception as e:
#             print(f"An error occurred while generating content for question: {e}")
#             responses.append({"from": "gpt", "value": "Error occurred in generating content"})
#     return responses

# # Load existing data to resume from where it left off
# def load_existing_data(output_json_path):
#     if os.path.exists(output_json_path):
#         with open(output_json_path, 'r', encoding='utf-8') as json_file:
#             data = json.load(json_file)
#         print("Resuming from where left off, already processed images:")
#         for item in data:
#             print(item["image"])
#         return data
#     return []

# # Save data to JSON file
# def save_data(json_data, output_json_path):
#     with open(output_json_path, 'w', encoding='utf-8') as json_file:
#         json.dump(json_data, json_file, ensure_ascii=False, indent=4)

# # Read the CSV file into a DataFrame
# df = pd.read_csv(r'C:\Users\4010356\Desktop\Mufleh\image super resulstion\captions.csv')

# # Prepare the list of questions
# questions = [
#     "Describe this product generally in 10 words",
#     "Describe the visual features of this product like colors or specific visual features",
#     "What is the material of this product",
#     "What is written or drawn on this product",
#     "For whom this product is and in which season it's best to wear it"
# ]

# # Load existing JSON data
# json_data = load_existing_data(output_json_path)

# processed_images = {entry["image"] for entry in json_data}

# # Initialize counter for batches
# batch_size = 5
# processed_counter = 0

# # Calculate total number of batches
# total_batches = (len(df) + batch_size - 1) // batch_size

# # Process images in batches of 5
# for batch in range(total_batches):
#     start_index = batch * batch_size
#     end_index = start_index + batch_size
#     batch_df = df.iloc[start_index:end_index]

#     with tqdm(total=min(batch_size, len(batch_df)), desc=f"Processing batch {batch+1}/{total_batches}") as pbar:
#         for row_index, row in batch_df.iterrows():
#             image_name = row['image']
#             if image_name in processed_images:
#                 pbar.update(1)  # Skip already processed images but update progress
#                 continue

#             image_path = directory_path / image_name

#             if image_path.is_file():
#                 with open(image_path, 'rb') as file:
#                     image_data = file.read()

#                 conversations = [{"from": "human", "value": question} for question in questions]
#                 gpt_responses = generate_content_for_questions(image_data, questions)
#                 conversations.extend(gpt_responses)

#                 json_data.append({
#                     "id": f"{row_index}_{image_name.split('.')[0]}",  # Corrected to use row_index
#                     "image": image_name,
#                     "conversations": conversations
#                 })

#                 processed_counter += 1
#                 pbar.update(1)  # Update the progress bar for each processed image

#     # Optionally, save data after each batch regardless of size
#     save_data(json_data, output_json_path)











# Combine all question sets into a list of lists
all_question_sets = [
        [
        "Give a brief description of this item in 10 words.",
        "What are the key visual features of this item?",
        "What material is this item made from?",
        "Is there any branding or logos on this item?",
        "Who is the target audience for this item and when is it most useful?"
        ],
        [
        "Describe this product generally in 10 words",
        "Describe the visual features of this product like colors of specific visual features",
        "What is the material of this product",
        "what is written or drawn on this product",
        "for whom this product is and in which season its best to wear it"
        ],
        [            
        "Briefly describe this product in 10 words.",
        "What are the prominent visual features of this product?",
        "What is the main material of this product?",
        "Are there any distinctive marks or features on this product?",
        "Who would typically use this product and in what situations?"
        ],

        [            
        "Say short about this thing in 10 words.",
        "What you see on this thing? Tell main things.",
        "This thing made from what?",
        "It has special marks or looks?",
        "Who use this? When they use?"
        ],
  
        [            
        "Describe this item succinctly in 10 words.",
        "Explain the visual characteristics of this item.",
        "What material is used for this item?",
        "Does this item have any decorations or markings?",
        "Who is the target market for this item and where can it be used?"
        ],    
        [            
        "Quickly describe this object in 10 words.",
        "What visual details stand out for this object?",
        "What's the manufacturing material for this object?",
        "Is there any text or graphic on this object?",
        "What's the intended use and ideal user for this object?"
        ],
        [            
        "Summarize this product in 10 words.",
        "Detail the visual aspects of this product.",
        "What is the primary material of this product?",
        "Are there any inscriptions or designs on this product?",
        "Who would find this product useful and in which context?"
        ] 
]





import pathlib
import json
import os
import pandas as pd
from tqdm import tqdm

import google.generativeai as genai

genai.configure(api_key="AIzaSyCFf-8Pte-vOemfu9V8Z6ZbVrSlSoBfOGM")
model = genai.GenerativeModel('gemini-pro-vision')
directory_path = pathlib.Path("images")
output_json_path = 'updated_descriptions.json'

def generate_content_for_question(image_data, question):
    try:
        response = model.generate_content(contents=[question, {'mime_type': 'image/jpeg', 'data': image_data}])
        return {"from": "gpt", "value": response.text}
    except Exception as e:
        print(f"An error occurred while generating content for question: {e}")
        return {"from": "gpt", "value": "Error occurred in generating content"}

def load_existing_data(output_json_path):
    if os.path.exists(output_json_path):
        with open(output_json_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        print("Resuming from where left off, already processed images:")
        for item in data:
            print(item["image"])
        return data
    return []


def save_data(json_data, output_json_path):
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

df = pd.read_csv(r'C:\Users\4010356\Desktop\Mufleh\image super resulstion\captions.csv')

questions = [
    "Describe this product generally in 10 words",
    "Describe the visual features of this product like colors or specific visual features",
    "What is the material of this product",
    "What is written or drawn on this product",
    "For whom this product is and in which season it's best to wear it"
]

json_data = load_existing_data(output_json_path)
processed_images = {item["image"]: len(item["conversations"]) // 2 for item in json_data}

# Organize processing in batches
batch_size = 5
total_images = len(df)
batches = (total_images + batch_size - 1) // batch_size

for batch in range(batches):
    start_index = batch * batch_size
    end_index = min(start_index + batch_size, total_images)
    with tqdm(total=(end_index - start_index), desc=f"Batch {batch + 1}/{batches}") as pbar:
        for i in range(start_index, end_index):
            row = df.iloc[i]
            image_name = row['image']
            if processed_images.get(image_name, 0) >= len(questions):
                pbar.update(1)
                continue

            image_path = directory_path / image_name
                # Determine which set of questions to use for this image
            question_set_index = i % len(all_question_sets)  # Cycle through question sets
            questions = all_question_sets[question_set_index]
            if image_path.is_file():
                with open(image_path, 'rb') as file:
                    image_data = file.read()

                for question in questions:
                    if processed_images.get(image_name, 0) >= len(questions):
                        break
                    human_conversation = {"from": "human", "value": question}
                    gpt_response = generate_content_for_question(image_data, question)

                    # Find or create new entry for the image
                    entry = next((item for item in json_data if item["image"] == image_name), None)
                    if not entry:
                        entry = {"id": f"{i}_{image_name.split('.')[0]}", "image": image_name, "conversations": []}
                        json_data.append(entry)
                    entry["conversations"].extend([human_conversation, gpt_response])
                    processed_images[image_name] = processed_images.get(image_name, 0) + 1

                pbar.update(1)
                # Save data after processing each image or batch for safety
                save_data(json_data, output_json_path)

# Ensure all data is saved at the end
save_data(json_data, output_json_path)
















