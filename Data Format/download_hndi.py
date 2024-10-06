import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import os

# Path to the CSV file - adjust the path as necessary for your environment
csv_file_path = r"C:\Users\4010356\Downloads\archive (7)\Data - Copy.csv"

# Folder where the images will be saved
folder_path = 'images_v2'

# Read the CSV file using pandas
csv_data = pd.read_csv(csv_file_path)

# Ensure the folder exists
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Modify the URLs in the 'img' column to request higher resolution images
csv_data['img'] = csv_data['img'].str.replace('612/612', '3000/3000')

# Function to download images
def download_images(image_urls, folder_path='images_v2', num_images=62199):
    for i, url in enumerate(image_urls[:num_images]):
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img.save(os.path.join(folder_path, f"{i+1}.jpg"))
            print(f"Downloaded image {i+1}")
        except Exception as e:
            print(f"Error downloading image {i+1}: {e}")

# Download the first three images
download_images(csv_data['img'].tolist(), folder_path)
