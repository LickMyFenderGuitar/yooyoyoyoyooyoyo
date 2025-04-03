import os
import time

# ANSI escape sequences for colors and styling
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
GRAY = "\033[90m"
WHITE_BG = "\033[47m\033[30m"
CLEAR_SCREEN = "\033[H\033[J"

# Store command history
command_history = []

def display_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%Y-%m-%d")

    # UI Header
    print(f"{CYAN}{BOLD}╔════════════════════════════════════════════╗{RESET}")
    print(f"{CYAN}{BOLD}║      flux terminal v1.0 - Python           ║{RESET}")
    print(f"{CYAN}{BOLD}╠════════════════════════════════════════════╣{RESET}")
    print(f"{YELLOW}║  Time: {CYAN}{current_time}   {YELLOW}|  Date: {CYAN}{current_date}  {YELLOW}║{RESET}")
    print(f"{CYAN}{BOLD}╚════════════════════════════════════════════╝{RESET}")
    for i in range(0,46):
        print(f"{WHITE_BG}║{RESET}", end="")
    print('\n')
    # Display Command History
    for command in command_history[-10:]:  # Show last 10 commands
        print(f"{GRAY}{command}{RESET}")

while True:
    display_terminal()  # Refresh screen and show UI
    user_input = input(f"{BLUE}flux 1.0 >>> {RESET}").strip()
    
    if user_input.lower() == "exit":
        print(f"{RED}Exiting flux terminal...{RESET}")
        break
    elif user_input.lower() == "clear":
        command_history.clear()  # Clears stored history
    else:
        # Handle commands
        if user_input.lower() == "help":
            result = (f"{YELLOW}Available commands:{RESET}\n"
                      f"{GREEN}exit{RESET} - Exit the terminal\n"
                      f"{GREEN}clear{RESET} - Clear the output\n"
                      f"{GREEN}help{RESET} - Show this message\n"
                      f"{GREEN}time{RESET} - Show the current time\n"
                      f"{GREEN}date{RESET} - Show the current date\n"
                      f"{GREEN}execute <file>{RESET} - Execute a .flx file")
        elif user_input.lower() == "time":
            result = f"{CYAN}Current time: {time.strftime('%H:%M:%S')}{RESET}"
        elif user_input.lower() == "date":
            result = f"{CYAN}Current date: {time.strftime('%Y-%m-%d')}{RESET}"
        elif user_input.lower().startswith("execute "):
            file_name = user_input[8:].strip()
            if os.path.exists(file_name):
                try:
                    with open(file_name, 'r') as file:
                        code = file.read()
                        exec(code)  # Runs the .flx script
                    result = f"{GREEN}Executed {file_name} successfully{RESET}"
                except Exception as e:
                    result = f"{RED}Error executing {file_name}: {str(e)}{RESET}"
            else:
                result = f"{RED}File {file_name} not found.{RESET}"
        else:
            result = f"{RED}Unknown command: '{user_input}'. Type 'help' for available commands.{RESET}"

        # Store the command and its output
        command_history.append(f">>> {user_input}")
        command_history.append(result)
