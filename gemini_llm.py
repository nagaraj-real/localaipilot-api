
import os


def llm(model):
    model= "models/gemini-pro" if model is None else f"models/{model}"
    api_key = os.getenv("API_KEY")
    if api_key is None:
        raise Exception('API_KEY not found in environment')
    from llama_index.llms.gemini import Gemini
    gemini = Gemini(api_key=api_key,model_name=model)
    return gemini


def embed_llm(model):
    model= "models/embedding-001" if model is None else f"models/{model}"
    api_key = os.getenv("EMBED_API_KEY")
    if api_key is None:
        raise Exception('EMBED_API_KEY not found in environment')
    from llama_index.embeddings.gemini import GeminiEmbedding
    gemini_embed = GeminiEmbedding(api_key=api_key,model_name=model)
    return gemini_embed