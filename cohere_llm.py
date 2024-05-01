
import os


def llm():
    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise Exception('API_KEY not found in environment')
    from llama_index.llms.cohere import Cohere
    cohere = Cohere(api_key=api_key)
    return cohere


def embed_llm():
    api_key = os.getenv("EMBED_API_KEY")
    if api_key is None:
        raise Exception('EMBED_API_KEY not found in environment')
    from llama_index.embeddings.cohere import CohereEmbedding
    cohere_embed = CohereEmbedding(cohere_api_key=api_key,model_name="embed-english-v3.0")
    return cohere_embed