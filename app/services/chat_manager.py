from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma
from typing import Dict, Optional
import os
from app.core.config import settings
from app.services.prompts import CHAT_PROMPT
import logging

class ChatManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
    
    def __init__(self):
        if not self.initialized:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.3,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                google_api_key=settings.GOOGLE_API_KEY,
            )
            self.conversations = {}
            self.vectorstores = {}
            self.initialized = True
    
    def initialize_conversation(self, user_id: str, user_name: str, vectorstore: Chroma) -> None:
        """Initialize or reinitialize a conversation for a user"""
        try:
            memory = ConversationBufferMemory(
                memory_key="chat_history",
                output_key="answer",
                input_key="question",
                return_messages=True
            )
            
            qa_chain = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
                memory=memory,
                combine_docs_chain_kwargs={"prompt": CHAT_PROMPT},
                return_source_documents=True,
                verbose=True
            )
            
            self.conversations[user_id] = {
                "chain": qa_chain,
                "user_name": user_name,
                "memory": memory
            }
            self.vectorstores[user_id] = vectorstore
            
            # Verify initialization
            if not self.has_active_conversation(user_id):
                raise ValueError("Failed to initialize conversation")
                
        except Exception as e:
            logging.error(f"Error initializing conversation: {str(e)}", exc_info=True)
            raise ValueError(f"Failed to initialize conversation: {str(e)}")
            
    
       
    def get_vectorstore(self, user_id: str) -> Optional[Chroma]:
        """Get the vectorstore for a user if it exists"""
        return self.vectorstores.get(user_id)
        
    async def get_response(self, user_id: str, query: str) -> Dict:
        """Get a response from the conversation chain"""
        if user_id not in self.conversations:
            raise ValueError("No active conversation found for this user. Please upload a document first.")
            
        conversation = self.conversations[user_id]
        result = await conversation["chain"].ainvoke({
            "question": query,
            "user_name": conversation["user_name"]
        })
        
        return {
            "answer": result["answer"],
            "sources": [doc.page_content for doc in result["source_documents"]]
        }
        
    def clear_conversation(self, user_id: str) -> None:
        """Clear a user's conversation history"""
        if user_id in self.conversations:
            self.conversations[user_id]["memory"].clear()
            
    def has_active_conversation(self, user_id: str) -> bool:
        """Check if a user has an active conversation"""
        has_conversation = user_id in self.conversations
        has_vectorstore = user_id in self.vectorstores
        return has_conversation and has_vectorstore