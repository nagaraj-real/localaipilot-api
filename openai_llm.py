
import os
import logging

log = logging.getLogger('app.llm')

def llm(model):
    model= "gpt-3.5-turbo" if model is None else model
    log.info(f"using model: {model}")
    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise Exception('API_KEY not found in environment')
    from llama_index.llms.openai import OpenAI
    openai = OpenAI(api_key=api_key,model=model)
    return openai

def embed_llm(model):
    model= "text-embedding-3-large" if model is None else model
    log.info(f"using embed model: {model}")
    api_key = os.getenv("EMBED_API_KEY")
    if api_key is None:
        raise Exception('EMBED_API_KEY not found in environment')
    from llama_index.embeddings.openai import OpenAIEmbedding
    openai_embed = OpenAIEmbedding(api_key=api_key,model_name= model)
    return openai_embed