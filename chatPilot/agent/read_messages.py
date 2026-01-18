import asyncio
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from droidrun import DroidAgent
from droidrun.config_manager.config_manager import (
    DroidrunConfig,
    TracingConfig,
    LoggingConfig,
    AgentConfig,
)
from llama_index.llms.google_genai import GoogleGenAI
from chatPilot.agent.prompts.whatsapp_prompts import READ_WHATSAPP_MESSAGES_GOAL
from chatPilot.schemas.message_schema import WhatsAppMessage

load_dotenv()

async def read_messages():
    """Read a single WhatsApp message and save it to JSON"""
    
    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )

    config = DroidrunConfig(
        agent=AgentConfig(reasoning=True, max_steps=20),
        tracing=TracingConfig(enabled=False),
        logging=LoggingConfig(debug=True, save_trajectory="action"),
    )

    agent = DroidAgent(
        goal=READ_WHATSAPP_MESSAGES_GOAL(),
        config=config,
        llms=llm,
        output_model=WhatsAppMessage,
    )

    result = await agent.run()

    print(f"Success: {result.success}")
    print(f"Reason: {result.reason}")
    
    # Try different attributes where the structured output might be stored
    message = None
    if result.success:
        # Check various possible locations for the structured output
        if hasattr(result, 'structured_output') and result.structured_output:
            message = result.structured_output
            print("✅ Found structured_output")
        elif hasattr(result, 'output') and result.output:
            message = result.output
            print("✅ Found output")
        elif hasattr(result, 'result') and result.result:
            message = result.result
            print("✅ Found result")
        else:
            print(f"❌ No structured output found. Available attributes: {dir(result)}")
            return None
    
    if message and result.success:
        # Validate message has content
        if not hasattr(message, 'message_text') or not message.message_text or not message.message_text.strip():
            print("⚠️ Message text is empty, skipping")
            return None
        
        # Convert to dict and wrap in list for consistency
        if hasattr(message, 'dict'):
            message_dict = message.dict()
        elif hasattr(message, 'model_dump'):
            message_dict = message.model_dump()
        else:
            # Fallback: manually create dict
            message_dict = {
                'sender_name': message.sender_name,
                'message_text': message.message_text,
                'timestamp': message.timestamp,
                'chat_type': message.chat_type
            }
        
        messages_list = [message_dict]
        
        # Save output
        output_directory = "data/"
        os.makedirs(output_directory, exist_ok=True)
        file_path = os.path.join(output_directory, "messages.json")

        with open(file_path, "w") as f:
            json.dump(messages_list, f, indent=4)

        print(f"✅ Message saved to {file_path}")
        print(f"   Sender: {message_dict['sender_name']}")
        print(f"   Text: {message_dict['message_text'][:50]}...")
        
        return file_path
    else:
        print(f"❌ Failed to read message: {result.reason if hasattr(result, 'reason') else 'Unknown error'}")
        return None


if __name__ == "__main__":
    asyncio.run(read_messages())