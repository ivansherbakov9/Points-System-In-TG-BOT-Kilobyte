#────────────────────────────── ❑ ──────────────────────────────
#Created by Ivan Shcherbakov (github: https://github.com/ivansherbakov9) (telegram: https://t.me/Gunner951)
#────────────────────────────── ❑ ──────────────────────────────
import os
import json
import time
from colorama import Fore, Style, init

init(autoreset=True)

title = f"{Fore.GREEN}────────────────────────────── ADMIN CONSOLE ──────────────────────────────"

LANG_FILE = "lang.txt"
USER_POINTS_FILE = "user_points.json"

LANG_FILE = "lang.txt"
USER_POINTS_FILE = "user_points.json"

class Debug:
    @staticmethod
    def info(message):
        print(f"{Fore.WHITE}[INFO] {message}")

    @staticmethod
    def warn(message):
        print(f"{Fore.YELLOW}[WARN] {message}")

    @staticmethod
    def error(message):
        print(f"{Fore.RED}[ERROR] {message}")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_lang(lang):
    if lang not in ["ru", "eng"]:
        Debug.error("Invalid language. Available: ru, eng")
        return

    with open(LANG_FILE, "w") as f:
        f.write(lang)
    Debug.info(f"Language changed to {lang}")

def set_points(username, points):

    if username[0] == "@":
        username = username[1:]
    
    try:
        with open(USER_POINTS_FILE, "r") as f:
            user_data = json.load(f)
    except FileNotFoundError:
        Debug.error(f"File {USER_POINTS_FILE} not found.")
        return

    user_id = None
    for uid, data in user_data.items():
        if data.get("username") == username:
            user_id = uid
            break

    if not user_id:
        Debug.error(f"User with username '{username}' not found.")
        return

    try:
        points = int(points)
        user_data[user_id]["points"] = points
        with open(USER_POINTS_FILE, "w") as f:
            json.dump(user_data, f, indent=4)
        Debug.info(f"Points for user {username} set to {points}.")
        Debug.warn(f"Send this command to the chat: /u {user_id}")
    except ValueError:
        Debug.error("Points must be a number.")

while True:
    clear_console()

    print(title)
    
    command = input("$ ").strip()

    if command in ["quit", "q", "exit", "stop"]:
        break

    elif command.startswith("setlang") or command.startswith("sl") or command.startswith("l"):
        parts = command.split()
        if len(parts) == 2:
            set_lang(parts[1])
        else:
            Debug.error("Invalid command format. Use: setlang <ru/eng>")

    elif command.startswith("setpoints") or command.startswith("sp") or command.startswith("p"):
        parts = command.split()
        if len(parts) == 3:
            set_points(parts[1], parts[2])

            time.sleep(5)
            continue

        else:
            Debug.error("Invalid command format. Use: setpoints <telegram-username> <points>")

    elif command in ["help", "h"]:
        Debug.info('''
l <ru/eng> - set the language
p <username> <points> - set points
h - print a list of commands
q - close the console
''')
        time.sleep(2.7)
        continue

    else:
        Debug.error("Unknown command.")

    time.sleep(0.7)
#────────────────────────────── ❑ ──────────────────────────────
#Created by Ivan Shcherbakov (https://github.com/ivansherbakov9/Points-System-In-TG-BOT-Kilobyte)
#────────────────────────────── ❑ ──────────────────────────────
