from fastapi import APIRouter, Depends, HTTPException
from app.schemas import ChatQuery, User
from app.core.deps import get_current_user
from app.services.chat_manager import ChatManager
import logging

router = APIRouter()
chat_manager = ChatManager()

@router.post("/")
async def chat(
    query: ChatQuery,
    current_user: User = Depends(get_current_user)
):
    try:
        user_id = str(current_user.id)
        
        # Add debug logging
        logging.debug(f"Checking conversation for user {user_id}")
        logging.debug(f"Active conversations: {chat_manager.conversations.keys()}")
        
        # Check if user has an active conversation
        if not chat_manager.has_active_conversation(user_id):
            # Try to reinitialize from existing vectorstore
            vectorstore = chat_manager.get_vectorstore(user_id)
            if vectorstore:
                chat_manager.initialize_conversation(
                    user_id,
                    current_user.name,
                    vectorstore
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Please upload a document before starting a chat. No active conversation found."
                )
            
        response = await chat_manager.get_response(user_id, query.query)
        return response
        
    except ValueError as e:
        logging.error(f"ValueError in chat endpoint: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")