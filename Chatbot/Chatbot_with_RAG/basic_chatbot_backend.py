from langgraph.graph import StateGraph, START, END
from langchain_community.chat_models import ChatOllama
from typing import TypedDict
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# set the splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# Load the pdf document
docs = PyPDFLoader('../../Documents/attention.pdf').load()
# split document in chunks
chunks = splitter.split_documents(docs)
# Create a Retriever
embeddings = OllamaEmbeddings(model="nomic-embed-text")
# Store chunks in database
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
# select specified number (k) of results
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

model = ChatOllama(model="llama3")

class ChatbotState(TypedDict):
    user_query:str
    context: str
    llm_response:str

# Retrieval Node
def retrieve_docs(state: ChatbotState):

    query = state["user_query"]

    docs = retriever.invoke(query)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    return {"context": context}

# Generation Node
def generate_answer(state: ChatbotState):
    print("state['context']", state['context'])
    prompt = f"""
    Answer using only the provided context.

    Context:
    {state['context']}

    Question:
    {state['user_query']}
    """

    response = model.invoke(prompt)

    return {
        "llm_response": response.content
    }
# def chatbot_history(state:ChatbotState):
#     query = state['user_query']
#     response = model.invoke(query).content
#     state['llm_response'] = response
#     return {'llm_response':response}

# graph = StateGraph(ChatbotState)
# graph.add_node("chatbot_history", chatbot_history)
# graph.add_edge(START, 'chatbot_history')
# graph.add_edge('chatbot_history', END)
# workflow = graph.compile()

 #####################
graph = StateGraph(ChatbotState)

graph.add_node("retrieve_docs", retrieve_docs)
graph.add_node("generate_answer", generate_answer)

graph.add_edge(START, "retrieve_docs")
graph.add_edge("retrieve_docs", "generate_answer")
graph.add_edge("generate_answer", END)

workflow = graph.compile()

initial_state = {"user_query": "What is the capital of France?"}
final_state = workflow.invoke(initial_state)

print(final_state)

