
import asyncio
import os
from colorama import init, Fore, Style
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Initialize colorama
init(autoreset=True)

# Import ChatPilot agents
from agent.read_messages import read_messages
from agent.classify_messages import classify_messages
from agent.act_on_messages import act_on_messages


# ---------------- Banner ----------------
def print_banner():
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}
 ██████╗██╗  ██╗ █████╗ ████████╗██████╗ ██╗██╗     ██████╗ ████████╗
██╔════╝██║  ██║██╔══██╗╚══██╔══╝██╔══██╗██║██║    ██╔═══██╗╚══██╔══╝
██║     ███████║███████║   ██║   ██████╔╝██║██║    ██║   ██║   ██║
██║     ██╔══██║██╔══██║   ██║   ██╔═══╝ ██║██║    ██║   ██║   ██║
██████╗ ██║  ██║██║  ██║   ██║   ██║     ██║███████╗╚██████╔╝  ██║
{Style.RESET_ALL}
{Fore.YELLOW}{Style.BRIGHT} 🤖 ChatPilot – AI That Turns WhatsApp Messages Into Actions 🤖{Style.RESET_ALL}
{Fore.GREEN} Press Enter to start the productivity cycle...{Style.RESET_ALL}
"""
    print(banner)


def print_agent_status(agent_name: str, color: str = Fore.BLUE):
    print(f"\n{color}{Style.BRIGHT}🚀 Running Agent: {agent_name}{Style.RESET_ALL}")
    print(f"{color}{'=' * 50}{Style.RESET_ALL}")


# ---------------- Main Cycle ----------------
async def run_chatpilot_cycle():
    cycle_count = 1
    max_retries = 3

    while True:
        print(
            f"\n{Fore.MAGENTA}{Style.BRIGHT}🔄 Starting ChatPilot Cycle #{cycle_count}{Style.RESET_ALL}"
        )
        print(f"{Fore.MAGENTA}{'=' * 60}{Style.RESET_ALL}")

        # ---------- STEP 1: READ MESSAGES ----------
        messages_file = None
        for attempt in range(max_retries):
            try:
                print_agent_status("READ_MESSAGES", Fore.CYAN)

                messages_file = await read_messages()
                if messages_file and os.path.exists(messages_file):
                    print(
                        f"{Fore.GREEN}✅ Messages read successfully → {messages_file}{Style.RESET_ALL}"
                    )
                    break
                else:
                    raise RuntimeError("read_messages returned no file")

            except Exception as e:
                print(
                    f"{Fore.RED}❌ READ_MESSAGES failed "
                    f"(attempt {attempt + 1}/{max_retries}): {e}{Style.RESET_ALL}"
                )

        if not messages_file:
            print(f"{Fore.RED}⏭️ Skipping cycle due to read failure{Style.RESET_ALL}")
            cycle_count += 1
            continue

        # ---------- STEP 2: CLASSIFY MESSAGES ----------
        decisions_file = None
        for attempt in range(max_retries):
            try:
                print_agent_status("CLASSIFY_MESSAGES", Fore.YELLOW)

                decisions_file = await classify_messages(messages_file)
                if decisions_file and os.path.exists(decisions_file):
                    print(
                        f"{Fore.GREEN}✅ Messages classified → {decisions_file}{Style.RESET_ALL}"
                    )
                    break
                else:
                    raise RuntimeError("classify_messages returned no file")

            except Exception as e:
                print(
                    f"{Fore.RED}❌ CLASSIFY_MESSAGES failed "
                    f"(attempt {attempt + 1}/{max_retries}): {e}{Style.RESET_ALL}"
                )

        if not decisions_file:
            print(f"{Fore.RED}⏭️ Skipping execution phase{Style.RESET_ALL}")
            cycle_count += 1
            continue

        # ---------- STEP 3: ACT ON MESSAGES ----------
        for attempt in range(max_retries):
            try:
                print_agent_status("ACT_ON_MESSAGES", Fore.GREEN)

                await act_on_messages(
                    messages_file=messages_file,
                    decisions_file=decisions_file,
                )

                print(
                    f"{Fore.GREEN}✅ Actions executed successfully{Style.RESET_ALL}"
                )
                break

            except Exception as e:
                print(
                    f"{Fore.RED}❌ ACT_ON_MESSAGES failed "
                    f"(attempt {attempt + 1}/{max_retries}): {e}{Style.RESET_ALL}"
                )

        # ---------- Cycle Summary ----------
        print(
            f"\n{Fore.MAGENTA}{Style.BRIGHT}📊 Cycle #{cycle_count} Summary{Style.RESET_ALL}"
        )
        print(f"{Fore.CYAN}   Read Messages: ✅{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}   Classified:   ✅{Style.RESET_ALL}")
        print(f"{Fore.GREEN}   Actions Done: ✅{Style.RESET_ALL}")

        # Ask user to continue
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


# ---------------- Entry Point ----------------
async def main():
    print_banner()
    input()
    print(f"{Fore.GREEN}{Style.BRIGHT}🚀 ChatPilot is starting...{Style.RESET_ALL}")
    await run_chatpilot_cycle()


if __name__ == "__main__":
    asyncio.run(main())
