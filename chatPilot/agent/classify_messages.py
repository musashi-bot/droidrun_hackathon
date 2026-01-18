#!/usr/bin/env python3
import asyncio
import os
import json
from dotenv import load_dotenv

from droidrun import DroidAgent
from droidrun.config_manager.config_manager import (
    DroidrunConfig,
    TracingConfig,
    LoggingConfig,
    AgentConfig,
)
from llama_index.llms.google_genai import GoogleGenAI

from agent.prompts.whatsapp_prompts import CLASSIFY_MESSAGE_GOAL
from schemas.decision_schema import MessageClassification

load_dotenv()


async def classify_messages(messages_file: str):
    # Load messages
    with open(messages_file, "r") as f:
        messages = json.load(f)

    # LLM
    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )

    # Droidrun config
    config = DroidrunConfig(
        agent=AgentConfig(reasoning=True),
        tracing=TracingConfig(enabled=False),
        logging=LoggingConfig(debug=True, save_trajectory="action"),
    )

    classifications = []

    # Run agent for each message (simple & reliable)
    for message in messages:
        agent = DroidAgent(
            goal=CLASSIFY_MESSAGE_GOAL(message),
            config=config,
            llms=llm,
            output_model=MessageClassification,
        )

        result = await agent.run()

        print(f"Message: {message['raw_text']}")
        print(f"Success: {result.success}")

        if result.success:
            classifications.append(result.output.dict())

    # Save decisions
    output_directory = "data/"
    os.makedirs(output_directory, exist_ok=True)
    output_path = os.path.join(output_directory, "decisions.json")

    with open(output_path, "w") as f:
        json.dump(classifications, f, indent=4)

    print(f"Decisions saved to {output_path}")
    return output_path


if __name__ == "__main__":
    asyncio.run(classify_messages("data/messages.json"))
