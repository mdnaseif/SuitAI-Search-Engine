import csv
import json

# Read the CSV data
csv_file_path = 'updated_descriptions.csv'
data = []
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Construct the data in the desired format
        data.append({
            "id": row["id"],
            "image": row["image"],
            "conversations": [
                {
                    "from": "human",
                    "value": "Illustrate the image through a descriptive explanation\n<image>"
                },
                {
                    "from": "gpt",
                    "value": row["caption"]
                }
            ]
        })

# Since the same image can have multiple captions, we need to aggregate captions under the same image ID
transformed_data = {}
for item in data:
    if item['image'] not in transformed_data:
        transformed_data[item['image']] = {
            "id": item['id'],
            "image": item['image'],
            "conversations": []
        }
    transformed_data[item['image']]['conversations'].extend(item['conversations'])

# Convert the dictionary to a list format as required
final_data = list(transformed_data.values())

# Write the transformed data to a JSON file
json_file_path = 'transformed_data.json'
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(final_data, json_file, indent=4)

print(f"Data transformation complete. JSON saved to {json_file_path}")
