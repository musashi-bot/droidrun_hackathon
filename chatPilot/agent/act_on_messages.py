#!/usr/bin/env python3
import asyncio
import json
import os
from dotenv import load_dotenv

from droidrun import DroidAgent
from droidrun.config_manager.config_manager import (
    DroidrunConfig,
    TracingConfig,
    LoggingConfig,
    AgentConfig,
)
from llama_index.llms.google_genai import GoogleGenAI

from agent.prompts.whatsapp_prompts import (
    CREATE_REMINDER_GOAL,
    DRAFT_REPLY_GOAL,
    DAILY_SUMMARY_GOAL,
)

load_dotenv()


async def act_on_messages(
    messages_file: str = "data/messages.json",
    decisions_file: str = "data/decisions.json",
):
    # Load data
    with open(messages_file, "r") as f:
        messages = json.load(f)

    with open(decisions_file, "r") as f:
        decisions = json.load(f)

    # LLM
    llm = GoogleGenAI(
        api_key=os.environ["GEMINI_API_KEY"],
        model="gemini-2.5-pro",
    )

    config = DroidrunConfig(
        agent=AgentConfig(reasoning=True, max_steps=30),
        tracing=TracingConfig(enabled=False),
        logging=LoggingConfig(debug=True, save_trajectory="action"),
    )

    daily_summary_tasks = []

    # Iterate message + decision together
    for message, decision in zip(messages, decisions):
        if not decision["action_required"]:
            continue

        action = decision["suggested_action"]

        # 1️⃣ Create Calendar / Reminder
        if action in ["calendar", "reminder"]:
            agent = DroidAgent(
                goal=CREATE_REMINDER_GOAL(
                    reminder_text=message["message_text"],
                    time="Tomorrow 9 AM"
                ),
                config=config,
                llms=llm,
            )
            await agent.run()

        # 2️⃣ Draft Reply
        elif action == "reply":
            agent = DroidAgent(
                goal=DRAFT_REPLY_GOAL(
                    sender_name=message["sender_name"]
                ),
                config=config,
                llms=llm,
            )
            await agent.run()

        # 3️⃣ Save for Daily Summary
        elif action in ["note", "ignore"]:
            daily_summary_tasks.append(
                f"- {message['sender_name']}: {message['message_text']}"
            )

    # 4️⃣ Create Daily Summary Note (if needed)
    if daily_summary_tasks:
        agent = DroidAgent(
            goal=DAILY_SUMMARY_GOAL(
                "\n".join(daily_summary_tasks)
            ),
            config=config,
            llms=llm,
        )
        await agent.run()


if __name__ == "__main__":
    asyncio.run(act_on_messages())
