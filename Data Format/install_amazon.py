# import asyncio
# import aiohttp
# import pandas as pd
# from pathlib import Path
# import hashlib
# from aiohttp import ClientTimeout

# # Function to calculate the SHA-256 hash of the image content
# async def calculate_image_hash(image_content):
#     return hashlib.sha256(image_content).hexdigest()

# # Function to download an image and handle the response
# async def handle_image_response(session, url, filename, existing_hashes, title, images_data, retry_images):
#     try:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 content = await response.read()
#                 image_hash = await calculate_image_hash(content)
#                 if image_hash not in existing_hashes:
#                     with open(filename, 'wb') as f:
#                         f.write(content)
#                     existing_hashes.add(image_hash)
#                     print(f"Downloaded: {filename}")
#                     images_data.append((filename.name, title, "Downloaded successfully"))
#                 else:
#                     reason = "Duplicate image not downloaded"
#                     print(f"{reason}: {filename}")
#                     if filename.name in retry_images:
#                         images_data.append((filename.name, title, reason))
#             else:
#                 reason = f"Failed to download, HTTP Status {response.status}"
#                 print(reason)
#                 if filename.name in retry_images:
#                     images_data.append((filename.name, title, reason))
#     except aiohttp.ClientError as e:
#         reason = f"Failed to download due to client error: {e}"
#         print(reason)
#         if filename.name in retry_images:
#             images_data.append((filename.name, title, reason))
#     except asyncio.TimeoutError:
#         reason = "Request timed out"
#         print(reason)
#         if filename.name in retry_images:
#             images_data.append((filename.name, title, reason))

# # Main function to orchestrate the download process
# async def main():
#     df = pd.read_csv("images_data_amazon_1.csv")
#     retry_df = pd.read_csv('images_data_amazon.csv')
#     images_folder = Path("images_amazon_11")
#     images_folder.mkdir(parents=True, exist_ok=True)

#     existing_hashes = set()
#     for existing_image in images_folder.iterdir():
#         with open(existing_image, 'rb') as file:
#             existing_hashes.add(hashlib.sha256(file.read()).hexdigest())

#     retry_images = retry_df[retry_df['reason'] == 'Request timed out']['image_name'].tolist()

#     timeout = ClientTimeout(total=60)  # Adjust the total timeout as needed

#     images_data = []  # List to store image names, titles, and reasons

#     async with aiohttp.ClientSession(timeout=timeout) as session:
#         tasks = []
#         for index, row in df.iterrows():
#             image_url = row['src']
#             title = row.get('title', 'No Title')
#             file_extension = Path(image_url).suffix
#             filename = images_folder / f"{index + 1}{file_extension}"
#             if filename.name in retry_images:
#                 task = asyncio.create_task(handle_image_response(session, image_url, filename, existing_hashes, title, images_data, retry_images))
#                 tasks.append(task)

#         await asyncio.gather(*tasks)

#     # Update the DataFrame with the new attempts
#     for image_data in images_data:
#         retry_df.loc[retry_df['image_name'] == image_data[0], 'reason'] = image_data[2]

#     retry_df.to_csv('images_data_amazon.csv', index=False)

#     print("Retry attempts have been made for timed-out downloads.")

# if __name__ == "__main__":
#     asyncio.run(main())












import asyncio
import aiohttp
import pandas as pd
from pathlib import Path
import hashlib
from aiohttp import ClientTimeout
import os
import shutil

# Load the dataframe containing image URLs and names
df = pd.read_csv("images_data_amazon_1.csv")
df_src = pd.read_csv("images_data_amazon.csv")
async def calculate_image_hash(image_content):
    """Calculate the SHA-256 hash of the image content."""
    return hashlib.sha256(image_content).hexdigest()

async def handle_image_response(session, url, filename, existing_hashes, images_data):
    """Handle downloading an image and checking for duplicates."""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                image_hash = await calculate_image_hash(content)
                if image_hash not in existing_hashes:
                    with open(filename, 'wb') as f:
                        f.write(content)
                    existing_hashes.add(image_hash)
                    print(f"Downloaded: {filename}")
                    images_data.append((filename.name, "Downloaded successfully"))
                else:
                    print(f"Duplicate image not downloaded: {filename}")
    except aiohttp.ClientError as e:
        print(f"Failed to download due to client error: {e}")
    except asyncio.TimeoutError:
        print("Request timed out")

async def download_missing_images(source_dir, target_dir, df):
    """Download images that are missing from the source directory."""
    images_folder = Path(target_dir)
    images_folder.mkdir(parents=True, exist_ok=True)

    existing_hashes = set()
    images_data = []
    timeout = ClientTimeout(total=60)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = []
        for _, row in df.iterrows():
            image_name = row['image_name']
            source_path = os.path.join(source_dir, image_name)
            target_path = os.path.join(target_dir, image_name)
            if not os.path.exists(source_path):
                image_url = row['src']
                task = asyncio.create_task(handle_image_response(session, image_url, Path(target_path), existing_hashes, images_data))
                tasks.append(task)
            else:
                # shutil.move(source_path, target_path)
                print(f"Moved {image_name} to {target_dir}")

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    source_directory = "images_amazon"
    target_directory = r"data\amazon\split_images\s_images"

    # Ensure the dataframe 'df' includes a column 'image_name' that lists the names of the images
    # and a column 'src' with the corresponding URLs for each image.
    asyncio.run(download_missing_images(source_directory, target_directory, df))

