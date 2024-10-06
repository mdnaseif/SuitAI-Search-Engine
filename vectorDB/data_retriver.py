import chromadb
import numpy as np
from PIL import Image
import torch
import clip

# Load the model
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-L/14", device=device)


def query(vector_database,
          user_text_input=None, 
          user_image_input=None,):
    """
    vector_data base: is the databse where you stored the vectors of you data
    user_text_input: is the textual query from the user.
    user_image_input: is the imagary query from the user.

    the function will return the directory of the result
    """
    
    # Calculate features

    



    # use the texual query
    if user_text_input is not None and user_image_input is None:
        text_input = clip.tokenize(user_text_input).to(device)
        with torch.no_grad():
            text_feature = model.encode_text(text_input).detach().cpu().numpy()
        text_feature = text_feature.tolist()
        txt_query_vec = text_feature
        result = vector_database.query(
        query_embeddings=txt_query_vec,
        include= ['distances','metadatas','uris'],
        n_results=6
        )
        return result
    # use the imagary query
    elif user_image_input is not None and user_text_input is None:
        image_input = preprocess(user_image_input).unsqueeze(0).to(device)
        with torch.no_grad():
            image_vecs = model.encode_image(image_input).detach().cpu().numpy()
        image_vecs = image_vecs.tolist()

        result = vector_database.query(
        query_embeddings=image_vecs,
        include= ['distances','metadatas','uris'],
        n_results=6
        )
        return result
    # use the averege of both queries
    elif user_image_input is not None and user_text_input is not None:
        txt_vecs_np = np.array(txt_query_vec)
        img_vecs_np = np.array(image_vecs)
        av_vecs = ((txt_vecs_np + img_vecs_np)/2).tolist()
        result = vector_database.query(
        query_embeddings=av_vecs,
        include= ['distances','metadatas','uris'],
        n_results=6
        )
        return result['uris']   
    # if both queries are None  
    else:
        return None
    

def get_results_text(vector_database,user_text_input):
    results = query(vector_database=vector_database,
          user_text_input=user_text_input, 
          user_image_input=None)
    return results

def get_results_image(vector_database, user_image_input):
    results = query(vector_database=vector_database,
          user_text_input=None, 
          user_image_input=user_image_input)
    return results