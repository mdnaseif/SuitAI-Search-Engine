import openai

#OpenAI API key
your_api_key = "openai api"

openai.api_key = your_api_key

def get_completion(product_description, model="gpt-3.5-turbo"):
    prompt=f"What are the most important keywords from this product description i need them so i can recommend a products with the same keywords choose only 1 word: {product_description}"

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(

    model=model,

    messages=messages,

    temperature=0,)

    return response.choices[0].message["content"]


