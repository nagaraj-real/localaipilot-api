
from cohere_llm import llm as cohere_llm,embed_llm as cohere_embed_llm
from ollama_llm import llm as ollama_llm,embed_llm as ollama_embed_llm
from gemini_llm import llm as gemini_llm,embed_llm as gemini_embed_llm
import os

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
     return ollama_llm(local_model_name)
  match model_name:
    case "cohere":
        return cohere_llm()
    case "gemini":
        return gemini_llm()
    case _:
        raise Exception(f"Model not found: {model_name}")

def get_code_llm():
  code_model_name= os.getenv("CODE_MODEL_NAME")
  if code_model_name is None:
     raise Exception(f"Model not found: {code_model_name}") 
  local_model_name=extract_after_local_slash(code_model_name)
  if local_model_name is not None:
     return ollama_llm(local_model_name)
  else:
     raise Exception(f"Model not found: {code_model_name}")  
  

def get_embed_llm():
  embed_model_name= os.getenv("EMBED_MODEL_NAME")
  if embed_model_name is None:
     return None
  local_model_name=extract_after_local_slash(embed_model_name)
  if local_model_name is not None:
     return ollama_embed_llm(local_model_name)
  match embed_model_name:
    case "cohere":
        return cohere_embed_llm()
    case "gemini":
        return gemini_embed_llm()
    case _:
        return None