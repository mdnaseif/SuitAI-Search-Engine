all_question_sets = [
    [
        "Considering the title '{image_title}', give a brief description of this item in 10 words.",
        "With the title '{image_title}', what are the key visual features of this item?",
        "Given the title '{image_title}', what material is this item made from?",
        "With '{image_title}' in mind, is there any branding or logos on this item?",
        "Considering '{image_title}', who is the target audience for this item and when is it most useful?"
    ],
    [
        "Considering the title '{image_title}', describe this product generally in 10 words.",
        "With the title '{image_title}', describe the visual features of this product like colors or specific visual features.",
        "Given the title '{image_title}', what is the material of this product?",
        "With '{image_title}' in mind, what is written or drawn on this product?",
        "Considering '{image_title}', for whom is this product and in which season is it best to wear it?"
    ],
    [
        "Considering the title '{image_title}', briefly describe this product in 10 words.",
        "With the title '{image_title}', what are the prominent visual features of this product?",
        "Given the title '{image_title}', what is the main material of this product?",
        "With '{image_title}' in mind, are there any distinctive marks or features on this product?",
        "Considering '{image_title}', who would typically use this product and in what situations?"
    ],
    [
        "Considering the title '{image_title}', say short about this thing in 10 words.",
        "With the title '{image_title}', what do you see on this thing? Tell main things.",
        "Given the title '{image_title}', this thing is made from what?",
        "With '{image_title}' in mind, does it have special marks or looks?",
        "Considering '{image_title}', who uses this? When do they use it?"
    ],
    [
        "Considering the title '{image_title}', describe this item succinctly in 10 words.",
        "With the title '{image_title}', explain the visual characteristics of this item.",
        "Given the title '{image_title}', what material is used for this item?",
        "With '{image_title}' in mind, does this item have any decorations or markings?",
        "Considering '{image_title}', who is the target market for this item and where can it be used?"
    ],
    [
        "Considering the title '{image_title}', quickly describe this object in 10 words.",
        "With the title '{image_title}', what visual details stand out for this object?",
        "Given the title '{image_title}', what's the manufacturing material for this object?",
        "With '{image_title}' in mind, is there any text or graphic on this object?",
        "Considering '{image_title}', what's the intended use and ideal user for this object?"
    ],
    [
        "Considering the title '{image_title}', summarize this product in 10 words.",
        "With the title '{image_title}', detail the visual aspects of this product.",
        "Given the title '{image_title}', what is the primary material of this product?",
        "With '{image_title}' in mind, are there any inscriptions or designs on this product?",
        "Considering '{image_title}', who would find this product useful and in which context?"
    ]
]


import pathlib
import json
import os
import pandas as pd
from tqdm import tqdm

import google.generativeai as genai

genai.configure(api_key="AIzaSyA3Tj-r_lveVipFFzbur9TLYsJoQbQS-z8")
model = genai.GenerativeModel('gemini-pro-vision')
directory_path = pathlib.Path("images_amazon")
output_json_path = 'data_amazon.json'

def generate_content_for_question_with_title(image_data, question, image_title):
    try:
        modified_question = question.format(image_title=image_title)  # Incorporate the image title into the question
        response = model.generate_content(contents=[modified_question, {'mime_type': 'image/jpeg', 'data': image_data}])
        return {"from": "gpt", "value": response.text}
    except Exception as e:
        print(f"An error occurred while generating content for question with title: {e}")
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

df = pd.read_csv('images_data_amazon.csv')

json_data = load_existing_data(output_json_path)
processed_images = {item["image"]: len(item["conversations"]) // 2 for item in json_data}

batch_size = 5
total_images = len(df)
batches = (total_images + batch_size - 1) // batch_size

for batch in range(batches):
    start_index = batch * batch_size
    end_index = min(start_index + batch_size, total_images)
    with tqdm(total=(end_index - start_index), desc=f"Batch {batch + 1}/{batches}") as pbar:
        for i in range(start_index, end_index):
            row = df.iloc[i]
            image_name = row['image_name']
            image_title = row['image_title']  # Ensure your CSV has an 'image_title' column
            if processed_images.get(image_name, 0) >= len(all_question_sets[0]):
                pbar.update(1)
                continue

            image_path = directory_path / image_name
            question_set_index = i % len(all_question_sets)  # Cycle through question sets
            questions = all_question_sets[question_set_index]
            if image_path.is_file():
                with open(image_path, 'rb') as file:
                    image_data = file.read()

                for question in questions:
                    if processed_images.get(image_name, 0) >= len(questions):
                        break
                    human_conversation = {"from": "human", "value": question.format(image_title=image_title)}
                    gpt_response = generate_content_for_question_with_title(image_data, question, image_title)

                    entry = next((item for item in json_data if item["image"] == image_name), None)
                    if not entry:
                        entry = {"id": f"{i}_{image_name.split('.')[0]}", "image": image_name, "conversations": []}
                        json_data.append(entry)
                    entry["conversations"].extend([human_conversation, gpt_response])
                    processed_images[image_name] = processed_images.get(image_name, 0) + 1

                pbar.update(1)
                save_data(json_data, output_json_path)

save_data(json_data, output_json_path)








