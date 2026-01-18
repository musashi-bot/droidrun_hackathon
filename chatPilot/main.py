import asyncio
import os
from dotenv import load_dotenv
load_dotenv()


from droidrun import DroidAgent
from droidrun.config_manager.config_manager import (
    DroidrunConfig,
    AgentConfig,
    LoggingConfig,
)
from llama_index.llms.google_genai import GoogleGenAI
from colorama import init, Fore, Style

init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
██████╗ ██╗  ██╗ █████╗ ████████╗██████╗ ██╗██╗     ██████╗  ████████╗
██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔══██╗██║██║    ██╔═══██╗╚══██╔══╝
██║     ███████║███████║   ██║   ██████╔╝██║██║    ██║   ██║   ██║   
██║     ██╔══██║██╔══██║   ██║   ██╔═══╝ ██║██║    ██║   ██║   ██║   
██████╗ ██║  ██║██║  ██║   ██║   ██║     ██║███████╗╚██████╔╝  ██║   
{Style.RESET_ALL}
{Fore.YELLOW}{Style.BRIGHT}   🚀 CHATPILOT – AI That Pilots Your Chats and Actions 🚀{Style.RESET_ALL}
{Fore.GREEN}        Press Enter to start scanning prospects...{Style.RESET_ALL}
"""
    print(banner)


if __name__ == "__main__":
    print_banner()
    input()


async def main():
    # Use default configuration with built-in LLM profiles
    config = DroidrunConfig(
        agent=AgentConfig(
            max_steps=100,
            reasoning=True,
        ),
        logging=LoggingConfig(debug=False, save_trajectory="action", rich_text=True),
    )

    llm = GoogleGenAI(model="gemini-2.5-pro", temperature=0, api_key=os.environ["GEMINI_API_KEY"])

    # Create agent
    # LLMs are automatically loaded from config.llm_profiles
    agent = DroidAgent(
        goal="help",
        config=config,
        llms=llm,
    )

    # Run agent
    result = await agent.run()

    # Check results (result is a ResultEvent object)
    print(f"Success: {result.success}")
    print(f"Reason: {result.reason}")
    print(f"Steps: {result.steps}")


if __name__ == "__main__":
    asyncio.run(main())
