
from utils import get_user_message_query

from memory import ChatMemory
from llm_model import get_llm,get_code_llm,get_embed_llm
from code_prompt import code_prompt_tmpl
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader,load_index_from_storage,StorageContext,Settings

import logging
import os

log = logging.getLogger('app.chat')
chat_llm = get_llm()
code_llm= get_code_llm()
embed_llm= get_embed_llm()

Settings.embed_model=embed_llm

PERSIST_DIR = "./storage"

def chat_with_llm(messages):
     resp = chat_llm.chat(messages)
     log.info(f"Response from llm:{resp}")
     return ([resp.message],resp.message.content)
    
def chat_with_llm_stream(messages):
     resp = chat_llm.stream_chat(messages)
     log.info(f"Response from llm:{resp}")
     return resp

def chat_with_memory(query,chat_memory:ChatMemory,stream:bool=False):
     if stream:
          response = chat_with_llm_stream(chat_memory.augment_memory(get_user_message_query(query)))
          return response
     else:
          (resp,resp_string)= chat_with_llm(chat_memory.augment_memory(get_user_message_query(query)))
          chat_memory.augment_memory(resp)
          return resp_string
     
def complete_code(prefix_code,suffix_code,pre_context,is_stream=False):
     resp= ""
     completion_prompt = code_prompt_tmpl().format(
          prefix_code=prefix_code,
          suffix_code=suffix_code,
          pre_context= "" if pre_context is None else pre_context
     )
     log.info(f"Completion prompt:{completion_prompt}")
     if(is_stream):
          resp = code_llm.stream_complete(completion_prompt)
     else:
          resp = code_llm.complete(completion_prompt)
     log.info(f"Response from llm:{resp}")
     return resp



def rag_ingest():
     documents = SimpleDirectoryReader("/ragdir").load_data()
     log.info(f"{len(documents)} documents loaded")
     index = VectorStoreIndex.from_documents(documents,show_progress=True,embed_model=embed_llm)
     index.storage_context.persist(persist_dir=PERSIST_DIR)
     log.info("Ingestion complete")
     return index

def rag_chat(query:str,stream=False):
     if not os.path.exists(PERSIST_DIR):
          index = rag_ingest()
     else:
          storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
          index = load_index_from_storage(storage_context)
     query_engine = index.as_query_engine(streaming=stream, similarity_top_k=5,llm=chat_llm)
     response = query_engine.query(query)
     return response




