
from cohere_llm import llm as cohere_llm,embed_llm as cohere_embed_llm
from ollama_llm import llm as ollama_llm,embed_llm as ollama_embed_llm
from gemini_llm import llm as gemini_llm,embed_llm as gemini_embed_llm
from openai_llm import llm as openai_llm,embed_llm as openai_embed_llm
from anthropic_llm import llm as anthropic_llm,embed_llm as voyage_embed_llm
import os

from utils import extract_after_slash, stop_tokens
import logging

log = logging.getLogger('app.llm')

def extract_after_local_slash(text):
  if "local/" in text:
    parts = text.split("local/")
    return parts[1]
  else:
    return None
  
def get_llm():
  model_name= os.getenv("MODEL_NAME")
  if model_name is None:
     raise Exception(f"Model not found: {model_name}") 
  local_model_name=extract_after_local_slash(model_name)
  if local_model_name is not None:
     log.info(f"using local model: {local_model_name}")
     return ollama_llm(local_model_name)
  (provider,model)=extract_after_slash(model_name)
  log.info(f"using provider: {provider}")
  match provider:
    case "cohere":
        return cohere_llm(model)
    case "gemini":
        return gemini_llm(model)
    case "openai":
        return openai_llm(model)
    case "anthropic":
        return anthropic_llm(model)
    case _:
        raise Exception(f"Model not found: {model}")

def get_code_llm():
  code_model_name= os.getenv("CODE_MODEL_NAME")
  if code_model_name is None:
     raise Exception(f"Code Model not found: {code_model_name}") 
  local_model_name=extract_after_local_slash(code_model_name)
  if local_model_name is not None:
     log.info(f"using local code model: {local_model_name}")
     options= {
          'temperature': 0,
          'top_p': 0.9,
          'num_predict': 256,
          'stop': stop_tokens()
      }
     return ollama_llm(local_model_name,**options)
  else:
     raise Exception(f"Code Model not supported: {code_model_name}")  
  

def get_embed_llm():
  embed_model_name= os.getenv("EMBED_MODEL_NAME")
  if embed_model_name is None:
     raise Exception(f"Embed Model not found: {embed_model_name}") 
  local_model_name=extract_after_local_slash(embed_model_name)
  if local_model_name is not None:
     log.info(f"using local embed model: {local_model_name}")
     return ollama_embed_llm(local_model_name)
  (provider,model)=extract_after_slash(embed_model_name)
  log.info(f"using embed provider: {provider}")
  match provider:
    case "cohere":
        return cohere_embed_llm(model)
    case "gemini":
        return gemini_embed_llm(model)
    case "openai":
        return openai_embed_llm(model)
    case "voyageai":
        return voyage_embed_llm(model)
    case _:
        raise Exception(f"Embed Model not supported: {model}")