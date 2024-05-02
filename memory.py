

from uuid import UUID
import logging
from llama_index.core.types import ChatMessage

log = logging.getLogger('app.memory')

class ChatMemory:
    def __init__(self, chatId:UUID,memory=[]):
        self.chatId = chatId
        self.memory=[ChatMessage.parse_obj(m) for m in memory]

    def augment_memory(self,message:list[ChatMessage] ):
        self.memory+= message
        log.debug(f"ChatId: {self.chatId} Memory:{self.memory}")
        return self.memory

    def clear_memory(self):
        self.memory = []
        return self.memory
    
    def memory_json(self):
        return [m.dict() for m in self.memory]
    
    def chat_history_condensed(self)->dict:
        result_dict={}
        result_dict["chatid"]=self.chatId
        result_dict["query"]=self.firstQuery()
        result_dict["content"]=self.combined_message()
        return result_dict
    
        
    def combined_message(self)->str:
        combined_message=""
        for m in self.memory:
            if m.role =="system":
                continue 
            combined_message+=m.content
        return combined_message

    def firstQuery(self)->str:
        first_query=""
        for m in self.memory:
            if m.role =="user": 
                first_query=m.content
                break
        return first_query






