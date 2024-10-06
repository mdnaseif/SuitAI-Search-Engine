# import pathlib
# import json
# import os
# import pandas as pd
# from tqdm import tqdm

# import google.generativeai as genai

# # Configure the API with your key
# genai.configure(api_key="AIzaSyCFf-8Pte-vOemfu9V8Z6ZbVrSlSoBfOGM")
# # Use the text-based model
# model = genai.GenerativeModel('gemini-pro')
# directory_path = pathlib.Path("images")
# output_json_path = 'metadata.jsonl'

# # Function to generate a single consolidated description
# def generate_consolidated_description(responses):
#     # Combine all responses into a single prompt
#     prompt = " ".join(responses)
#     try:
#         # Generate a consolidated description based on the combined prompt
#         response = model.generate_content(contents=[prompt])
#         return {"description": response.text}
#     except Exception as e:
#         print(f"An error occurred while generating consolidated description: {e}")
#         return {"description": "Error occurred in generating content"}

# def load_existing_data(output_json_path):
#     if os.path.exists(output_json_path):
#         with open(output_json_path, 'r', encoding='utf-8') as json_file:
#             data = json.load(json_file)
#         print("Resuming from where left off, already processed images:")
#         for item in data:
#             print(item["image"])
#         return data
#     return []

# def save_data(json_data, output_json_path):
#     # Modify to save data in the new format using jsonlines
#     with open(output_json_path, 'w', encoding='utf-8') as json_file:
#         for entry in json_data:
#             json.dump(entry, json_file)
#             json_file.write('\n')  # Write each entry on a new line

# # Load your data (note: adjust path as needed)
# df = pd.read_csv(r'C:\Users\4010356\Desktop\Mufleh\image super resulstion\captions.csv')

# json_data = load_existing_data(output_json_path)
# processed_images = {item["image"]: item for item in json_data}

# # Organize processing in batches
# batch_size = 5
# total_images = len(df)
# batches = (total_images + batch_size - 1) // batch_size

# for batch in range(batches):
#     start_index = batch * batch_size
#     end_index = min(start_index + batch_size, total_images)
#     with tqdm(total=(end_index - start_index), desc=f"Batch {batch + 1}/{batches}") as pbar:
#         for i in range(start_index, end_index):
#             row = df.iloc[i]
#             image_name = row['image']
#             if image_name in processed_images:
#                 pbar.update(1)
#                 continue

#             # Accumulate responses for this image
#             responses = []
#             for question in questions:
#                 response = generate_content_for_question(question)  # Assuming this still generates individual responses
#                 responses.append(response["value"])

#             # Generate a consolidated description based on accumulated responses
#             consolidated_description = generate_consolidated_description(responses)

#             # Save the consolidated description for this image
#             json_data.append({
#                 "file_name": image_name,
#                 "additional_feature": consolidated_description["description"]
#             })

#             pbar.update(1)
#             # Save data after processing each image or batch for safety
#             save_data(json_data, output_json_path)

# # Ensure all data is saved at the end
# save_data(json_data, output_json_path)




import pandas as pd
import json



# Path to your JSON file
file_path = r'C:\Users\4010356\Downloads\diffusers\updated_descriptions.json'

# Reading the JSON file
# Reading the JSON file with UTF-8 encoding
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

json_data = data
# Adjusting the code to include the image name for each item along with the GPT conversations
data_gpt_with_image = []
for item in json_data:
    gpt_values = " ".join([conv["value"] for conv in item["conversations"] if conv["from"] == "gpt"])
    image_name = item["image"]  # Extracting the image name
    data_gpt_with_image.append([image_name, gpt_values])

# Creating a DataFrame with two columns: one for the image name and one for the concatenated GPT conversation values
df_with_image = pd.DataFrame(data_gpt_with_image, columns=["Image Name", "GPT Conversations"])

# Saving the DataFrame to a CSV file
csv_file_path = "fffffff.csv"
df_with_image.to_csv(csv_file_path, index=False)

