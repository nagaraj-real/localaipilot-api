
import os
import logging

log = logging.getLogger('app.llm')

def llm(submodel):
    submodel= "gpt-3.5-turbo" if submodel is None else submodel
    log.info(f"using submodel: {submodel}")
    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise Exception('API_KEY not found in environment')
    from llama_index.llms.openai import OpenAI
    openai = OpenAI(api_key=api_key,model=submodel)
    return openai

def embed_llm(submodel):
    submodel= "text-embedding-3-large" if submodel is None else submodel
    log.info(f"using embed submodel: {submodel}")
    api_key = os.getenv("EMBED_API_KEY")
    if api_key is None:
        raise Exception('EMBED_API_KEY not found in environment')
    from llama_index.embeddings.openai import OpenAIEmbedding
    openai_embed = OpenAIEmbedding(api_key=api_key,model_name= submodel)
    return openai_embed