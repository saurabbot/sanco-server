import os
from typing import List, Optional

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from app.core.config import settings

class ChatBotService:
    def __init__(self):
        self.data_path = "app/data/sanco.txt"
        self.vector_store = None
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0
        )

    def _initialize_vector_store(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found at {self.data_path}")
        
        loader = TextLoader(self.data_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents(documents)
        self.vector_store = FAISS.from_documents(docs, self.embeddings)

    async def get_answer(self, question: str, chat_history: List[dict] = None) -> str:
        if self.vector_store is None:
            self._initialize_vector_store()
        
        retriever = self.vector_store.as_retriever()
        
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the "
            "answer concise."
            "\n\n"
            "{context}"
        )
        
        messages = [("system", system_prompt)]
        
        if chat_history:
            for msg in chat_history:
                role = "human" if msg["role"] == "user" else "ai"
                messages.append((role, msg["content"]))
        
        messages.append(("human", "{input}"))
        
        prompt = ChatPromptTemplate.from_messages(messages)
        
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        response = await rag_chain.ainvoke({"input": question})
        return response["answer"]

chatbot_service = ChatBotService()
