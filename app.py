from flask import Flask, Response,jsonify,make_response
from flask import request
import logging
import uuid
import os
from redis import Redis

from redisutil import initialize, search_chat
LOG_LEVEL= os.getenv("LOG_LEVEL")
app = Flask(__name__)
app.logger.setLevel(app.config.get("LOG_LEVEL", LOG_LEVEL or "INFO"))
chat_model_name= os.getenv("MODEL_NAME")
code_model_name= os.getenv("CODE_MODEL_NAME")
app.logger.handlers.clear()
handler = logging.StreamHandler()
handler.setLevel(app.logger.level)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
app.logger.addHandler(handler)

app.logger.info('loaded Flask')

from chat import chat_with_memory,complete_code,rag_chat,rag_ingest
from memory import ChatMemory
from utils import get_init_system_message

endpoint_busy = False

chat_memory_dict:dict[str,ChatMemory]={}

redis_host= os.getenv("REDIS_HOST")
redis_port= os.getenv("REDIS_PORT")
redis_password= os.getenv("REDIS_PASSWORD")
redis_expiry= os.getenv("REDIS_EXPIRY")

if redis_host and redis_port:
    try:
        r = Redis(host=redis_host,port=redis_port,password=redis_password,decode_responses=True)
        initialize(r)
        response = r.client_list()
    except:
        r = None
        app.logger.info("Redis not loaded")



def retrieveOrCreateChatMemory(chat_id,context=None,context_type=None,language_id=None):
    memory= chat_memory_dict.get(chat_id)
    prev_history= []
    if memory:
        return memory
    if r and chat_id:
        prev_history = r.json().get(f"chathistory:{chat_id}")
    memory= ChatMemory(chat_id,prev_history if prev_history else [])
    memory.augment_memory(get_init_system_message(context,context_type,language_id))
    chat_memory_dict[str(chat_id)]=memory
    return memory


root_chat_id=uuid.uuid1()
root_memory= retrieveOrCreateChatMemory(root_chat_id)

def substring_excluding_stop(original_string: str, stop_string: str):
    index = original_string.find(stop_string)
    if index != -1: 
        return original_string[:index]
    else: 
        return original_string

@app.errorhandler(400)
def bad_request(error):
    message = str(error)
    app.logger.error(f"An unhandled error occurred: {error}")
    return make_response(jsonify({"error": message}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Resource not found"}), 404)

@app.errorhandler(Exception)
def handle_error(error):
    app.logger.error(f"An unhandled error occurred: {error}")
    return make_response(jsonify({"error": "Unhandled error"}), 500)


@app.route('/api/hello',methods = ['GET'])
def hello():
    return 'Hello, World!'

@app.route('/api/healthz',methods = ['GET'])
def health():
    app.logger.info("System Healthy")
    app.logger.info(f"Using chat model:{chat_model_name}")
    app.logger.info(f"Using code model:{code_model_name}")
    return 'Healthy!'

@app.route("/api/query", methods = ['POST'])
def query():
    data = request.get_json()
    app.logger.debug(f"Chat Request Recieved: {data}")
    query = data.get('query')
    chatId = data.get('chatId')
    context= data.get('context')
    context_type= data.get('contextType')
    language_id= data.get('languageid')
    stream = data.get('stream')
    chatId= str(uuid.uuid1()) if chatId is None else chatId
    memory= retrieveOrCreateChatMemory(chatId,context,context_type,language_id)
    if memory is None:
        response = jsonify({"chatId":chatId,"chatResponse": "No memory found for this chat id"})
    else:
        chat_response = chat_with_memory(query,memory,stream)
        if stream:
            def gen():
                yield str(chatId)
                final_response=''
                for r in chat_response:
                    final_response = r.message
                    yield r.message.content
                app.logger.debug(f"Chat Response Recieved: {final_response}")
                memory.augment_memory([final_response])
            return Response(gen())
        else:
            response = jsonify({"chatId":chatId,"chatResponse": str(chat_response),"memory": str(memory.memory)})
            app.logger.debug(f"Chat Response Recieved: {response}")
    return response


@app.route("/api/complete", methods = ['POST'])
def chat_complete():
    data = request.get_json()
    app.logger.debug(f"Completion Request Recieved: {data}")
    prefix_code = data.get('prefix_code')
    suffix_code = data.get('suffix_code')
    pre_context = data.get('pre_context')
    is_stream = data.get('stream')
    stop_string= '<|file_separator|>'
    if is_stream:
        completion_response = complete_code(prefix_code,suffix_code,pre_context,is_stream)
        app.logger.debug(f"completion_response: {completion_response}")
        def gen():
            for r in completion_response:
                if stop_string in r.delta:
                    index = r.delta.index(stop_string)
                    app.logger.debug(f"Delta from llm: {r.delta}")
                    yield r.delta[:index]  # Yield text before stop string
                    break
                app.logger.debug(f"Delta from llm: {r.delta}")
                yield r.delta
        return Response(gen())
    else:
        completion_response = complete_code(prefix_code,suffix_code,pre_context)
        return jsonify({"chatResponse": substring_excluding_stop(str(completion_response),stop_string)})

@app.route("/api/ragingest", methods = ['POST'])
def ragingest():
    try:
        rag_ingest()
        return jsonify({"chatResponse": "Ingestion complete !!"})
    except Exception as e:
        app.logger.error(f"error: {e}")
        raise Exception("Ingestion failed")

@app.route("/api/chatHistory/<chat_id>", methods = ['DELETE'])
def deleteChatHistory(chat_id):
    try:
        chat_history= chat_memory_dict.get(chat_id)
        if chat_history:
            if r:
                r.json().set(f"chathistory:{chat_id}",'$',chat_history.memory_json())
                r.hset(f"chatmessage:{chat_id}",mapping=chat_history.chat_history_condensed())
                if redis_expiry:
                    r.expire(f"chathistory:{chat_id}",redis_expiry)
                    r.expire(f"chatmessage:{chat_id}",redis_expiry)
            del chat_history
            app.logger.debug(f"chatHistoryDict after deletion: {chat_memory_dict}")
            return jsonify({"chatResponse": f"{chat_id} deletion complete"})
        else:
            return jsonify({"chatResponse": f"{chat_id} not found to delete"}),404
    except Exception as e:
        app.logger.error(f"error: {e}")
        raise Exception("Deletion failed")

@app.route("/api/chatHistory/<chat_id>", methods = ['GET'])
def getChatHistory(chat_id):
    try:
        if r:
            chat_history=r.json().get(f"chathistory:{chat_id}")
        if chat_history:
            return chat_history
        else:
            return jsonify({'error': 'No data found'}), 404
    except Exception as e:
        app.logger.error(f"error: {e}")
        raise Exception("Chat History retrieval failed")
    
@app.route("/api/chatHistory/search", methods = ['POST'])
def searchChatHistory():
    try:
        data = request.get_json()
        search_term = data.get('search_term')
        if search_term and r:
            (chat_history,chatid)=search_chat(r,search_term)
        if chat_history and chatid:
            return jsonify({'messages': chat_history,'chatid':chatid}),200
        else:
            return jsonify({'error': 'No data found'}), 404
    except Exception as e:
        app.logger.error(f"error: {e}")
        raise Exception("Chat search failed")

@app.route("/api/ragchat", methods = ['POST'])
def ragchat():
    data = request.get_json()
    app.logger.debug(f"Chat Request Recieved: {data}")
    query = data.get('query')
    is_stream = data.get('stream')
    chat_response = rag_chat(query,stream=is_stream)
    if is_stream:
        def gen():
            response_txt=""
            for r in chat_response.response_gen:
                app.logger.debug(f"Delta from llm: {r}")
                response_txt+=r
                yield response_txt
        return Response(gen())
    else:
        return jsonify({"chatResponse": str(chat_response)})

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=5000)