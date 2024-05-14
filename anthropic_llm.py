
import os
import logging

log = logging.getLogger('app.llm')

def llm(model):
    model= "command" if model is None else model
    log.info(f"using model: {model}")
    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise Exception('API_KEY not found in environment')
    from llama_index.llms.anthropic import Anthropic
    anthropic = Anthropic(api_key=api_key,model=model)
    return anthropic


def embed_llm(model):
    model= "voyage-2" if model is None else model
    log.info(f"using embed model: {model}")
    api_key = os.getenv("EMBED_API_KEY")
    if api_key is None:
        raise Exception('EMBED_API_KEY not found in environment')
    from llama_index.embeddings.voyageai import VoyageEmbedding
    voyage_embed = VoyageEmbedding(voyage_api_key=api_key,model_name= model)
    return voyage_embed