
from redis import Redis, ResponseError
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query


def initialize(r:Redis):
    schema = (
        TextField("content", as_name="content"),
        TextField("query", as_name="query"),
        TextField("chatid", as_name="chatid")
    )

    index = r.ft("idx:chatmessage")
    try:
        index.info()
    except ResponseError:
        index.create_index(
            schema,
            definition=IndexDefinition(prefix=["chatmessage:"], index_type=IndexType.HASH),
        )


def search_chat(r:Redis,search_term:str):
     chat_id=""
     chat_history= r.json().get(f"chathistory:{search_term}")
     if chat_history:
         return (chat_history,search_term)
     rs= r.ft("idx:chatmessage")
     res= rs.search(Query(search_term))
     if res.docs:
         chat_id= res.docs[0].chatid
         if chat_id:
            chat_history = r.json().get(f"chathistory:{chat_id}")
     return (chat_history,chat_id)