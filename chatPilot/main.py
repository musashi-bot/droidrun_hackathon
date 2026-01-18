import asyncio
from dotenv import load_dotenv
load_dotenv()

from colorama import init, Fore, Style
init(autoreset=True)

# IMPORT AGENT TASKS
from chatPilot.agent.read_messages import read_messages
from chatPilot.agent.classify_messages import classify_messages
from chatPilot.agent.act_on_messages import act_on_messages



def print_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
██████╗ ██╗  ██╗ █████╗ ████████╗██████╗ ██╗██╗ ██████╗ ████████╗
██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔══██╗██║██║ ██╔═══██╗╚══██╔══╝
██║     ███████║███████║   ██║   ██████╔╝██║██║ ██║   ██║   ██║
██║     ██╔══██║██╔══██║   ██║   ██╔═══╝ ██║██║ ██║   ██║   ██║
██████╗ ██║  ██║██║  ██║   ██║   ██║     ██║██║ ╚██████╔╝   ██║
{Style.RESET_ALL}
{Fore.YELLOW}{Style.BRIGHT} 🚀 CHATPILOT – AI That Pilots Your Chats and Actions 🚀{Style.RESET_ALL}
{Fore.GREEN} Press Enter to start processing WhatsApp messages...{Style.RESET_ALL}
"""
    print(banner)


async def run_chat_pilot_app_cycle():
    cycle_count = 1
    max_retries = 3

    while True:
        print(
            f"\n{Fore.MAGENTA}{Style.BRIGHT}🔄 Starting ChatPilot Cycle #{cycle_count}{Style.RESET_ALL}"
        )
        print(f"{Fore.MAGENTA}{'=' * 60}{Style.RESET_ALL}")

        # ---------- TASK 1: READ MESSAGES ----------
        messages_file = None
        for attempt in range(max_retries):
            try:
                print(f"{Fore.CYAN}📱 Reading WhatsApp messages...{Style.RESET_ALL}")
                messages_file = await read_messages()

                print(messages_file)

                if messages_file:
                    print(
                        f"{Fore.GREEN}✅ Messages saved to {messages_file}{Style.RESET_ALL}"
                    )
                    break
                else:
                    raise RuntimeError("read_messages returned None")

            except Exception as e:
                print(
                    f"{Fore.RED}❌ READ_MESSAGES failed "
                    f"(attempt {attempt + 1}/{max_retries}): {e}{Style.RESET_ALL}"
                )

        if not messages_file:
            print(f"{Fore.RED}⏭️ Skipping cycle due to read failure{Style.RESET_ALL}")
            cycle_count += 1
            continue

        # ---------- TASK 2: CLASSIFY MESSAGES ----------
        decisions_file = None
        for attempt in range(max_retries):
            try:
                print(f"{Fore.CYAN}🧠 Classifying messages...{Style.RESET_ALL}")
                decisions_file = await classify_messages(messages_file)

                if decisions_file:
                    print(
                        f"{Fore.GREEN}✅ Decisions saved to {decisions_file}{Style.RESET_ALL}"
                    )
                    break
                else:
                    raise RuntimeError("classify_messages returned None")

            except Exception as e:
                print(
                    f"{Fore.RED}❌ CLASSIFY_MESSAGES failed "
                    f"(attempt {attempt + 1}/{max_retries}): {e}{Style.RESET_ALL}"
                )

        if not decisions_file:
            print(f"{Fore.RED}⏭️ Skipping execution phase{Style.RESET_ALL}")
            cycle_count += 1
            continue

        # ---------- TASK 3: ACT ON MESSAGES ----------
        for attempt in range(max_retries):
            try:
                print(
                    f"{Fore.CYAN}⚙️ Executing actions (Calendar / WhatsApp / Notes)...{Style.RESET_ALL}"
                )

                await act_on_messages(
                    messages_file=messages_file,
                    decisions_file=decisions_file,
                )

                print(f"{Fore.GREEN}✅ Actions executed successfully{Style.RESET_ALL}")
                break

            except Exception as e:
                print(
                    f"{Fore.RED}❌ ACT_ON_MESSAGES failed "
                    f"(attempt {attempt + 1}/{max_retries}): {e}{Style.RESET_ALL}"
                )

        # ---------- CYCLE SUMMARY ----------
        print(
            f"\n{Fore.MAGENTA}{Style.BRIGHT}📊 Cycle #{cycle_count} completed{Style.RESET_ALL}"
        )

        print(
            f"\n{Fore.BLUE}🤔 Run another cycle? (y/n): {Style.RESET_ALL}",
            end="",
        )
        user_input = input().strip().lower()

        if user_input not in ["y", "yes", ""]:
            print(
                f"{Fore.CYAN}👋 ChatPilot session ended. Stay productive!{Style.RESET_ALL}"
            )
            break

        cycle_count += 1


async def main():
    print_banner()
    input()
    print(f"{Fore.GREEN}{Style.BRIGHT}🚀 ChatPilot is starting...{Style.RESET_ALL}")
    await run_chat_pilot_app_cycle()


if __name__ == "__main__":
    asyncio.run(main())
