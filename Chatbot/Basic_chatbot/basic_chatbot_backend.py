from langgraph.graph import StateGraph, START, END
from langchain_community.chat_models import ChatOllama
from typing import TypedDict

model = ChatOllama(model="llama3")

class ChatbotState(TypedDict):
    user_query:str
    llm_response:str

def chatbot_history(state:ChatbotState):
    query = state['user_query']
    response = model.invoke(query).content
    state['llm_response'] = response
    return {'llm_response':response}

graph = StateGraph(ChatbotState)
graph.add_node("chatbot_history", chatbot_history)
graph.add_edge(START, 'chatbot_history')
graph.add_edge('chatbot_history', END)
workflow = graph.compile()

