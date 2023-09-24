import time

def print_colored(text, color_code):
    print(f"\033[{color_code}m{text}\033[0m")

def display_intro():
    logo = f"""
\033[32m _________   
|  _______|
| |_____     
|  _____|  _____  ____     ____ ___    ___    ____     _____  __  __   ____    __ 
| |       / ___/ / __ `   / __ `__ \  / _ \  /  __|   / ___/ / / / /  / __ \  / /_
| |      / /    / /_/ /  / / / / / / /  __/ |  |     / /    / /_/ /  / /_/ / / __/
|_|     /_/     \__,_/| /_/ /_/ /_/  \___/   \____| /_/     \__, /  / .___/ / / 
                                                           /____/  /_/      \__|
 [Dikshit Singh]\033[0m
    """

    lines = logo.split("\n")

    for line in lines:
        print_colored(line, "32")
        time.sleep(0.1)

    print_colored("   Loading...", "33")
    print_colored("   v1.0.0", "33")

if __name__ == "__main__":
    display_intro()