from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.schemas import User
from app.core.deps import get_current_user
from app.services.document_processor import DocumentProcessor
from app.services.chat_manager import ChatManager
import logging

router = APIRouter()
doc_processor = DocumentProcessor()
chat_manager = ChatManager()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    logging.info(f"Starting document upload for user: {current_user.id}")
    
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
        
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
    
    try:
        # Process the document and get the vectorstore
        user_id = str(current_user.id)
        logging.info(f"Processing document {file.filename} for user {user_id}")
        
        result = await doc_processor.process_file(file, user_id)
        
        # Initialize conversation with the vectorstore
        if result.get("vectorstore"):
            logging.info(f"Initializing conversation for user {user_id}")
            chat_manager.initialize_conversation(
                user_id,
                current_user.name,
                result["vectorstore"]
            )
            
            # Verify conversation was initialized
            if not chat_manager.has_active_conversation(user_id):
                raise HTTPException(
                    status_code=500,
                    detail="Failed to initialize conversation after document upload"
                )
                
            logging.info(f"Successfully processed document and initialized conversation for user {user_id}")
            
            return {
                "status": result["status"],
                "message": result["message"],
                "chunks": result["chunks"]
            }
            
    except ValueError as e:
        logging.error(f"ValueError in document upload: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error in document upload: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )