from fastapi import FastAPI
from models import MessageInput
from db import conversations_collection
from utils import get_ai_response
from datetime import datetime
from bson import ObjectId

app = FastAPI()

@app.post("/api/chat")
async def chat_with_ai(payload: MessageInput):
    user_msg = {
        "role": "user",
        "content": payload.message,
        "timestamp": datetime.utcnow()
    }

    # Generate AI response
    ai_reply = await get_ai_response(payload.message)
    ai_msg = {
        "role": "assistant",
        "content": ai_reply,
        "timestamp": datetime.utcnow()
    }

    # Store in conversation
    if payload.conversation_id:
        conversations_collection.update_one(
            {"_id": ObjectId(payload.conversation_id)},
            {"$push": {"messages": {"$each": [user_msg, ai_msg]}}}
        )
    else:
        result = conversations_collection.insert_one({
            "user_id": payload.user_id,
            "messages": [user_msg, ai_msg],
            "created_at": datetime.utcnow()
        })
        payload.conversation_id = str(result.inserted_id)

    return {
        "conversation_id": payload.conversation_id,
        "ai_response": ai_reply
    }
