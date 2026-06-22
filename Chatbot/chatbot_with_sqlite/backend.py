from langgraph.graph import StateGraph, START, END
from langchain_community.chat_models import ChatOllama
from typing import TypedDict, Annotated
# from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langgraph.graph.message import add_messages

model = ChatOllama(model="llama3")

class ChatbotState(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot_history(state:ChatbotState):
    query = state['messages']
    response = model.invoke(query).content
    return {
        "messages": [
            AIMessage(content=response)
        ]
    }

    # return {'llm_response':response}

graph = StateGraph(ChatbotState)
graph.add_node("chatbot_history", chatbot_history)
graph.add_edge(START, 'chatbot_history')
graph.add_edge('chatbot_history', END)

# persistence concept saves data
connection = sqlite3.connect(database='chatbot.db', check_same_thread=False)
checkpointer = SqliteSaver(conn=connection)
# checkpointer = InMemorySaver()
workflow = graph.compile(checkpointer)

# Config = {'configurable':{'thread_id':'thread1'}}
# # Config = {'configurable':{'thread_id':'thread2'}}
#
# # initial_state={'messages':HumanMessage(content='My name is Swati Jadhav')}
# initial_state={'messages':HumanMessage(content='what is My name?')}
#
# response = workflow.invoke(initial_state, config=Config)
# print(response)

def retrieve_all_threads():
    unique_thread_ids = set()
    for checkpoint_item in checkpointer.list(None):
        unique_thread_ids.add(checkpoint_item.config['configurable']['thread_id'])
    return list(unique_thread_ids)

