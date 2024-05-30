
import os
import logging

log = logging.getLogger('app.llm')

def llm(model):
    model= "codestral-latest" if model is None else model
    log.info(f"using model: {model}")
    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise Exception('API_KEY not found in environment')
    from llama_index.llms.mistralai import MistralAI
    mistral = MistralAI(api_key=api_key,model=model,endpoint="https://codestral.mistral.ai")
    return mistral
