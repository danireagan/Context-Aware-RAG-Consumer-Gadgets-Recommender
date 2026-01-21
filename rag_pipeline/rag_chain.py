from langchain_groq import ChatGroq
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.history import BaseMessageHistory
from rag_pipeline.config import Config

class RAGChainBuilder:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.rag_model = ChatGroq(model=Config.RAG_MODEL)
