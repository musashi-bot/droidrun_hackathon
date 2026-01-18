from pydantic import BaseModel, Field

class WhatsAppMessage(BaseModel):
    sender_name: str = Field(description="Name of the message sender")
    message_text: str = Field(description="Exact text content of the message")
    timestamp: str = Field(description="Timestamp shown in WhatsApp UI")
    chat_type: str = Field(description="Whether the message is from group or personal chat")
