from PIL import Image
import streamlit as st
from chromadb.api.client import Client
from translator import detect_and_translate
import torch
from recommend import get_completion
# Clear any unnecessary variables from the GPU
torch.cuda.empty_cache()

def main():
    st.set_page_config(page_title="Fake Google Search", layout="centered", page_icon=":mag:")
    st.markdown("<h1 style='text-align: center;'>Suit AI Search Engine</h1>", unsafe_allow_html=True)
    
    image_path = "/media/akoubaa/new_ssd/naseif/Desktop/capstone/logo.png"
    st.image(image_path, use_column_width=True, caption='ourlogo')

    # Define different pages
    def page1():
        st.title("VectorDB and CLIP Searching")
        torch.cuda.empty_cache()
        from data_generator import database
        from data_retriver import get_results_text, get_results_image

        # Initialize the ChromaDB client and check collection
        client = Client()
        try:
            vectordb = client.get_collection("caap")
        except Exception as e:
            vectordb = database("caap")

        def search_by_text(query_text):
            query_text = detect_and_translate(query_text)
            results = get_results_text(vectordb, user_text_input=query_text)
            uris = [url for sublist in results['uris'] for url in sublist]
            descriptions = [meta['description'] for sublist in results['metadatas'] for meta in sublist]
            return uris, descriptions

        def search_by_image(image_file):
            if image_file is not None:
                image = Image.open(image_file)
                results = get_results_image(vectordb, user_image_input=image)
                uris = [url for sublist in results['uris'] for url in sublist]
                descriptions = [meta['description'] for sublist in results['metadatas'] for meta in sublist]
                return uris, descriptions
            return [], []

        st.write("Welcome to our search engine")

        query_text = st.text_input("Enter your search query:")
        query_image = st.file_uploader("Or upload an image:", type=['jpg', 'png'])

        if st.button('Search', key='search'):
            st.subheader(f"Top Results for ({query_text})")
            urls, captions = [], []
            if query_text:
                urls, captions = search_by_text(query_text)
            elif query_image:
                urls, captions = search_by_image(query_image)

            # CSS for card style
 # CSS for card style with fixed height
            card_style = """
            <style>
            .card {
                background-color: #f9f9f9;
                padding: 15px;
                margin: 10px;
                border-radius: 10px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
                text-align: center;
                height: 400px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            .card img {
                border-radius: 10px;
                max-height: 200px;
                object-fit: cover;
            }
            .card p {
                flex-grow: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 10px 0;
            }
            .card a {
                text-decoration: none;
                color: #1f77b4;
                font-weight: bold;
            }
            .card a:hover {
                color: #0056b3;
            }
            </style>
            """

            # Apply card style
            st.markdown(card_style, unsafe_allow_html=True)

            if urls and captions:
                for i in range(0, len(urls), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        index = i + j
                        if index < len(urls):
                            with cols[j]:
                                st.markdown(
                                    f"""
                                    <div class="card">
                                        <img src="{urls[index]}" alt="{captions[index]}" width="150">
                                        <p>{captions[index]}</p>
                                        <a href="{urls[index]}" target="_blank">Go to store</a>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
            #keywords = get_completion(query_text)
            st.subheader(f"Because you searched for ({query_text})")
            urls, captions = [], []
            if query_text:
                urls, captions = search_by_text(query_text)
            elif query_image:
                urls, captions = search_by_image(query_image)

            if urls and captions:
                for i in range(0, len(urls), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        index = i + j
                        if index < len(urls):
                            with cols[j]:
                                st.image(urls[index], caption=captions[index], width=150)
            else:
                st.warning("No results found. Please try a different query.")

        if st.button('Restart', key='restart'):
            st.experimental_rerun()

    def page2():
        st.write("Product generation page")
        st.title("Diffusion Product Description")
        st.write("Input a product description to get a generated image.")
        torch.cuda.empty_cache()
        import warnings
        warnings.filterwarnings("ignore", category=FutureWarning)
        from diffusers import StableDiffusionPipeline

        product_description = st.text_input("Product Description")
        generate_button = st.button("Generate Image")

        @st.cache_resource
        def load_sd_model():
            model_id = "CompVis/stable-diffusion-v1-4"
            pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
            pipe = pipe.to("cuda:1")
            return pipe

        pipe = load_sd_model()

        if generate_button:
            with st.spinner("Generating image..."):
                result = pipe(product_description)
                image = result.images[0]
                st.image(image, caption=product_description, width=500)

    def page3():
        torch.cuda.empty_cache()
        st.write("Product captioning page")
        from transformers import AutoProcessor, LlavaForConditionalGeneration

        @st.cache_resource
        def load_llava_model():
            model_id = "llava-hf/llava-1.5-13b-hf"
            model = LlavaForConditionalGeneration.from_pretrained(
                model_id, 
                torch_dtype=torch.float16, 
                low_cpu_mem_usage=True
            )
            if torch.cuda.device_count() > 1:
                model = torch.nn.DataParallel(model)
            model.to('cuda:2')
            processor = AutoProcessor.from_pretrained(model_id)
            return model, processor

        model, processor = load_llava_model()
        prompt = "USER: <image>\nDescribe the product shown in the image, excluding any person wearing it.\nASSISTANT:"

        st.title("LLaVA Product Description")
        st.write("Upload an image and get a description of the product.")

        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

        if uploaded_file is not None:
            raw_image = Image.open(uploaded_file)
            st.image(raw_image, caption='Uploaded Image', width=500)

            inputs = processor(prompt, raw_image, return_tensors='pt').to('cuda:2', torch.float16)

            with torch.no_grad():
                output = model.module.generate(**inputs, max_new_tokens=50, do_sample=False) if torch.cuda.device_count() > 1 else model.generate(**inputs, max_new_tokens=50, do_sample=False)

            decoded_output = processor.decode(output[0], skip_special_tokens=True)
            description_start = decoded_output.find("ASSISTANT:") + len("ASSISTANT:")
            description = decoded_output[description_start:].strip()
            filtered_description = '. '.join([sentence for sentence in description.split('. ') if 'person' not in sentence])
            
            st.write("Description:")
            st.write(filtered_description)

            del inputs
            del output
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

    st.sidebar.title('Navigation')
    option = st.sidebar.selectbox('Choose a feature:', ['Search Engine', 'Product Generation', 'Product Captioning'])

    if option == 'Search Engine':
        page1()
    elif option == 'Product Generation':
        page2()
    elif option == 'Product Captioning':
        page3()

if __name__ == "__main__":
    main()
