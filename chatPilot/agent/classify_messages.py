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

from chatPilot.agent.prompts.whatsapp_prompts import CLASSIFY_MESSAGE_GOAL
from chatPilot.schemas.decision_schema import MessageClassification

load_dotenv()


async def classify_messages(messages_file: str):
    """Classify each message and return decisions file path"""
    
    # Load messages
    with open(messages_file, "r") as f:
        messages = json.load(f)

    if not messages:
        print("⚠️ No messages to classify")
        return None

    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )

    config = DroidrunConfig(
        agent=AgentConfig(reasoning=True, max_steps=10),
        tracing=TracingConfig(enabled=False),
        logging=LoggingConfig(debug=True, save_trajectory="action"),
    )

    classifications = []

    # Classify each message
    for idx, message in enumerate(messages):
        print(f"\n🧠 Classifying message {idx+1}/{len(messages)}")
        print(f"   From: {message.get('sender_name', 'Unknown')}")
        print(f"   Text: {message.get('message_text', '')[:50]}...")
        
        agent = DroidAgent(
            goal=CLASSIFY_MESSAGE_GOAL(message),
            config=config,
            llms=llm,
            output_model=MessageClassification,
        )

        result = await agent.run()

        if result.success:
            # Try different attributes where the structured output might be stored
            classification = None
            if hasattr(result, 'structured_output') and result.structured_output:
                classification = result.structured_output
            elif hasattr(result, 'output') and result.output:
                classification = result.output
            elif hasattr(result, 'result') and result.result:
                classification = result.result
            
            if classification:
                # Convert to dict
                if hasattr(classification, 'dict'):
                    classification_dict = classification.dict()
                elif hasattr(classification, 'model_dump'):
                    classification_dict = classification.model_dump()
                else:
                    classification_dict = {
                        'intent': classification.intent,
                        'urgency': classification.urgency,
                        'action_required': classification.action_required,
                        'suggested_action': classification.suggested_action
                    }
                
                classifications.append(classification_dict)
                
                print(f"   ✅ Action: {classification_dict['suggested_action']}")
                print(f"   Urgency: {classification_dict['urgency']}")
        else:
            print(f"   ❌ Classification failed: {result.reason}")
            # Add default classification to maintain alignment
            classifications.append({
                "intent": "casual",
                "urgency": "low",
                "action_required": False,
                "suggested_action": "ignore"
            })

    # Save decisions
    output_directory = "data/"
    os.makedirs(output_directory, exist_ok=True)
    output_path = os.path.join(output_directory, "decisions.json")

    with open(output_path, "w") as f:
        json.dump(classifications, f, indent=4)

    print(f"\n✅ {len(classifications)} decisions saved to {output_path}")
    return output_path


if __name__ == "__main__":
    asyncio.run(classify_messages("data/messages.json"))