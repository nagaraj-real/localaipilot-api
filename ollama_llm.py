
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
import os

ollama_host= os.getenv("OLLAMA_HOST")
ollama_port= os.getenv("OLLAMA_PORT")
ollama_timeout= os.getenv("OLLAMA_TIMEOUT")
api_timeout= os.getenv("API_TIMEOUT")


if ollama_host and ollama_port:
   ollama_url = f"http://{ollama_host}:{ollama_port}"
else:
   ollama_url= "http://localhost:11434"

ollama_timeout = api_timeout if ollama_timeout is None else ollama_timeout

def llm(model_name,**options):
   ollama = Ollama(base_url=ollama_url,model=model_name, request_timeout=ollama_timeout or 30,**options)
   return ollama

def embed_llm(model_name):
   ollama = OllamaEmbedding(base_url=ollama_url,model_name=model_name)
   return ollama