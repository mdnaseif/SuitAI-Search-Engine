import chromadb
import numpy as np
from PIL import Image
import os
import json
import torch
import clip
import torch
import os
from PIL import Image
import re

import json

import os
from PIL import Image
import re

def read_images(folder_path):
    # List to store images
    images_list = []
    
    # Regular expression to extract numbers from the filename
    def numerical_sort(value):
        parts = re.compile(r'(\d+)').findall(value)
        return tuple(map(int, parts))
    
    # Get all file names in the folder and sort them by numerical value
    file_names = sorted([f for f in os.listdir(folder_path) if f.endswith('.jpg')], key=numerical_sort)
    
    # Loop through sorted file names
    for file_name in file_names:
        # Create the full path to the image
        file_path = os.path.join(folder_path, file_name)
        
        # Open and read the image
        image = Image.open(file_path)
        
        # Append the image to the list
        images_list.append(image)
        
    return images_list

# Specify the path to your folder
folder_path = '/media/akoubaa/new_ssd/naseif/Desktop/capstone/data/images'
images = read_images(folder_path)

# Now 'images' is a list containing all the images as Pillow Image objects, sorted numerically


def extract_gpt_conversation_values(json_file_path):
    # List to store "value" fields where "from" is "gpt"
    gpt_values = []
    
    # Open the JSON file and load its content
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    
    # Loop through each element in the JSON data
    for item in data:
        # Loop through each conversation in the "conversations" list
        for conversation in item['conversations']:
            # Check if the "from" key is "gpt"
            if conversation['from'] == 'gpt':
                # Extract the "value" and append it to the list
                gpt_values.append(conversation['value'].strip())
    
    return gpt_values

# Specify the path to your JSON file
json_file_path = '/media/akoubaa/new_ssd/naseif/Desktop/capstone/data/filtered_data.json'
values = extract_gpt_conversation_values(json_file_path)

# 'values' is now a list containing all the extracted "value" strings from "gpt" conversations



# Load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)



data = np.load("/media/akoubaa/new_ssd/naseif/Desktop/capstone/data/images_vecs.npz")

# npz_file is a NpzFile object which behaves like a dictionary.
loaded_images = data['all_features']
loaded_images = loaded_images.tolist()

data = np.load("/media/akoubaa/new_ssd/naseif/Desktop/capstone/data/text_vecs.npz")

# npz_file is a NpzFile object which behaves like a dictionary.
loaded_text = data['all_features']
loaded_text = loaded_text.tolist()

data = np.load("/media/akoubaa/new_ssd/naseif/Desktop/capstone/data/urls.npz")

# npz_file is a NpzFile object which behaves like a dictionary.
loaded_urls = data['all_features']
loaded_urls = loaded_urls.tolist()

#txt_vecs_np = np.array(loaded_text)
#img_vecs_np = np.array(loaded_images)
#loaded_text = ((txt_vecs_np + img_vecs_np)/2).tolist()
#loaded_images = ((txt_vecs_np + img_vecs_np)/2).tolist()


def vector_database_generator(txt_vecs, images_vecs, URLs,
                              txt_data_ids, images_data_ids, image_list,
                              collection_name,
                              txt_meta , image_meta 
                              ):
    """
    txt_vecs: is the list of text vectors
    images_vecs: is the list of images vectors
    URLs: is the list of the directory of the data
    txt_data_ids: is a list with same lingth as the txt_vecs list.
    it is used to give each element in txt_vecs a destinct id
    images_data_ids: is a list with same lingth as the images_vecs list.
    it is used to give each element in images_vecs a destinct id
    collection_name: is the name of the vector database
    txt_meta: if needed it labels the txt_vecs as a text type, True by defult
    txt_meta: if needed it labels the txt_vecs as an image type

    the function will return a generated vector data base consiste of
    to types of data which are:
     -the captions' vectors as an indvidual entitys
     -the images' vectors as an individual entitys
    """
    # create the vector data base
    client = chromadb.Client()

    collection = client.create_collection(
    name = collection_name
    )
    # store the vectors of the texts with the type labeling

    if txt_meta is not None:
        collection.add(
        ids=txt_data_ids,
        embeddings=txt_vecs,
        metadatas=txt_meta,
        uris=URLs,


        )
    # store the vectors of the texts without the type labeling
    else:
        collection.add(
        ids=txt_data_ids,
        embeddings=txt_vecs,
        uris=URLs,
        )


    # store the vectors of the images with the type labeling

    if image_meta is not None:
        collection.add(
        ids=images_data_ids,
        embeddings=images_vecs,
        metadatas=image_meta,
        uris=URLs,
        images=image_list
        )
    # store the vectors of the images without the type labeling
    else:
        collection.add(
        ids=images_data_ids,
        embeddings=images_vecs,
        uris=URLs,
        images=image_list    
        )
    
    return(collection)


# Creating a list of numbers from 1 to 5964
txt_data_ids = [str(i) for i in range(5965, 11929)]
images_data_ids = [str(i) for i in range(1, 5965)]
txt_meta_dicts = [{'description': value} for value in values]



def database(name):
    vector_database = vector_database_generator(
    txt_vecs=loaded_text,
    images_vecs=loaded_images,
    URLs=loaded_urls,
    txt_data_ids=txt_data_ids,
    images_data_ids=images_data_ids,
    image_list=images,
    collection_name=name,
    txt_meta=txt_meta_dicts,  # Pass the list of dictionaries here
    image_meta=txt_meta_dicts
)
    return vector_database

