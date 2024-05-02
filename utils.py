
from llama_index.core.llms import ChatMessage


def get_init_system_message(context=None,context_type=None,language_id=None):
    messages = [
        ChatMessage(
            role="system", content="You are technical programming expert who can answer queries on programming code."
        ),
    ]
    if context_type == 'code':
        messages = [
            ChatMessage(
                role="system", 
                content=f"""You are technical programming expert who can answer queries on programming.
                Your answers will be based on the below code block.
                
                ## Code block
                ```{language_id}
                  {context}
                ```
                """
            ),
        ]
    if context_type == 'bugfix':
        messages = [
            ChatMessage(
                role="system", 
                content=f"""You are technical programming expert who can fix errors on a given code.
                Your answers will include the fixed code and explanation.
                
                ## Code block
                ```{language_id}
                  {context}
                ```
                """
            ),
        ]
    if context_type == 'codereview':
        messages = [
            ChatMessage(
                role="system", 
                content=f"""You are a technical programming expert who can review code and provide suggestions.
                Review the below code block for adherence to coding style guidelines and best practices for readability. 
                Recommend improvements where necessary. Also reply with optimized code if possible.
                
                ## Code block
                ```{language_id}
                  {context}
                ```
                """
            ),
        ]
    return messages

def get_user_message_code_query(code,query):
    messages = [
         ChatMessage(role="user", 
        content=f"""  {query}     
        ```typescript
        {code}
        ```
        """),
    ]
    return messages


def get_user_message_query(query):
    messages = [
         ChatMessage(role="user", 
        content=f"""  {query}  """),
    ]
    return messages

def extract_after_slash(text):
  if "/" in text:
    parts = text.split("/")
    return (parts[0],parts[1])
  else:
    return (text,None)