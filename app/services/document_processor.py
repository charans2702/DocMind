from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredPowerPointLoader,
    TextLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from fastapi import UploadFile, HTTPException
from typing import Dict, List
import os
import tempfile
import shutil
import logging
from app.core.config import settings

SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.pptx', '.txt'}

class DocumentProcessor:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)
        
        try:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=settings.GOOGLE_API_KEY
            )
        except Exception as e:
            logging.error(f"Failed to initialize embeddings: {str(e)}")
            raise
            
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
    def _get_loader(self, file_path: str, extension: str):
        try:
            if extension == '.pdf':
                return PyPDFLoader(file_path)
            elif extension == '.docx':
                return Docx2txtLoader(file_path)
            elif extension == '.pptx':
                return UnstructuredPowerPointLoader(file_path)
            elif extension == '.txt':
                return TextLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {extension}")
        except Exception as e:
            logging.error(f"Error creating loader for {extension}: {str(e)}")
            raise
        
    async def process_file(self, file: UploadFile, user_id: str) -> Dict:
        logging.info(f"Processing file: {file.filename} for user: {user_id}")
        
        # Validate file extension
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in SUPPORTED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Supported types: {', '.join(SUPPORTED_EXTENSIONS)}"
            )

        # Create user directory
        user_db_path = f"{self.persist_directory}/{user_id}"
        os.makedirs(user_db_path, exist_ok=True)
        
        # Create temp file
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                content = await file.read()
                if not content:
                    raise ValueError("Empty file uploaded")
                temp_file.write(content)
                temp_path = temp_file.name
                
            logging.info(f"Temporary file created at: {temp_path}")
            
            # Load and process document
            loader = self._get_loader(temp_path, file_extension)
            documents = loader.load()
            logging.info(f"Loaded {len(documents)} documents")
            
            # Split documents
            splits = self.text_splitter.split_documents(documents)
            logging.info(f"Created {len(splits)} splits")
            
            if not splits:
                raise ValueError("No content could be extracted from the document")
            
            # Create vectorstore with explicit persistence
            logging.info(f"Creating vectorstore in {user_db_path}")
            vectorstore = Chroma(
                persist_directory=user_db_path,
                embedding_function=self.embeddings,
                collection_name=f"user_{user_id}"
            )
            # Add documents to the vectorstore
            vectorstore.add_documents(splits)
            
            return {
                "status": "success",
                "message": f"Processed {file.filename} successfully",
                "chunks": len(splits),
                "vectorstore": vectorstore
            }
            
        except Exception as e:
            logging.error(f"Error processing document: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Error processing document: {str(e)}"
            )
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
                logging.info(f"Cleaned up temporary file: {temp_path}")

    def get_relevant_chunks(self, user_id: str, query: str, k: int = 4) -> List[str]:
        user_db_path = f"{self.persist_directory}/{user_id}"
        if not os.path.exists(user_db_path):
            raise ValueError("No documents found for this user")
            
        vectorstore = Chroma(
            persist_directory=user_db_path,
            embedding_function=self.embeddings
        )
        
        docs = vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]

    def clear_user_documents(self, user_id: str):
        user_db_path = f"{self.persist_directory}/{user_id}"
        if os.path.exists(user_db_path):
            shutil.rmtree(user_db_path)