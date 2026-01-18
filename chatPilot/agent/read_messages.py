# schemas/message_schema.py
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
from agent.prompts import whatsapp_prompts as READ_WHATSAPP_MESSAGES_GOAL
from schemas.message_schema import WhatsAppMessage # Importing the schema abhi tak set nhi hai

load_dotenv()

async def read_messages():
    # LLM
    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )

    # Droidrun config (same as example)
    config = DroidrunConfig(
        agent=AgentConfig(reasoning=True),
        tracing=TracingConfig(enabled=False),
        logging=LoggingConfig(debug=True, save_trajectory="action"),
    )

    # Create agent
    agent = DroidAgent(
        goal=READ_WHATSAPP_MESSAGES_GOAL(),
        config=config,
        llms=llm,
        output_model=list[WhatsAppMessage],
    )

    # Run agent
    result = await agent.run()

    print(f"Success: {result.success}")
    print(f"Reason: {result.reason}")
    print(f"Steps: {result.steps}")

    if result.success:
        messages = result.output

        # Save output
        output_directory = "data/"
        os.makedirs(output_directory, exist_ok=True)
        file_path = os.path.join(output_directory, "messages.json")

        with open(file_path, "w") as f:
            json.dump(
                [m.dict() for m in messages],
                f,
                indent=4
            )

        print(f"Messages saved to {file_path}")
        return file_path
    else:
        return None


if __name__ == "__main__":
    asyncio.run(read_messages())
