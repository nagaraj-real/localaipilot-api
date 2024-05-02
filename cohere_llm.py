
import os
import logging

log = logging.getLogger('app.llm')

def llm():
    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise Exception('API_KEY not found in environment')
    from llama_index.llms.cohere import Cohere
    cohere = Cohere(api_key=api_key)
    return cohere


def embed_llm(submodel):
    submodel= "embed-english-v3.0" if submodel is None else submodel
    log.info(f"using embed submodel: {submodel}")
    api_key = os.getenv("EMBED_API_KEY")
    if api_key is None:
        raise Exception('EMBED_API_KEY not found in environment')
    from llama_index.embeddings.cohere import CohereEmbedding
    cohere_embed = CohereEmbedding(cohere_api_key=api_key,model_name= submodel)
    return cohere_embed