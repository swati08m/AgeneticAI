from langgraph.graph import StateGraph, START, END
from langchain_community.chat_models import ChatOllama
from typing import TypedDict, Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langgraph.graph.message import add_messages

model = ChatOllama(model="llama3")

class ChatbotState(TypedDict):
    # user_query:str
    # llm_response:str
    messages: Annotated[list, add_messages]

def chatbot_history(state:ChatbotState):
    query = state['messages']
    # query = state['user_query']
    response = model.invoke(query).content
    # state['llm_response'] = response

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
checkpointer = InMemorySaver()
workflow = graph.compile(checkpointer)

