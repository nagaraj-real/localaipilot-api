
import os
import logging

log = logging.getLogger('app.llm')

def llm(model):
    model= "command" if model is None else model
    log.info(f"using model: {model}")
    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise Exception('API_KEY not found in environment')
    from llama_index.llms.cohere import Cohere
    cohere = Cohere(api_key=api_key,model=model)
    return cohere


def embed_llm(model):
    model= "embed-english-v3.0" if model is None else model
    log.info(f"using embed model: {model}")
    api_key = os.getenv("EMBED_API_KEY")
    if api_key is None:
        raise Exception('EMBED_API_KEY not found in environment')
    from llama_index.embeddings.cohere import CohereEmbedding
    cohere_embed = CohereEmbedding(cohere_api_key=api_key,model_name= model)
    return cohere_embed