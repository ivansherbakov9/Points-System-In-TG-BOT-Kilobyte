#────────────────────────────── ❑ ──────────────────────────────
#Created by Ivan Shcherbakov (github: https://github.com/ivansherbakov9) (telegram: https://t.me/Gunner951)
#────────────────────────────── ❑ ──────────────────────────────
import os
import json
import asyncio
#aiogram==2.25.1
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatAdministratorRights
from aiogram.contrib.middlewares.logging import LoggingMiddleware

def load_translations(file_path="translations.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

translations = load_translations()

TOKEN_FILE = "token.txt"
LANG_FILE = "lang.txt"
POINTS_FILE = "user_points.json"
AUTHORIZED_USERS_FILE = "authorized_users.json"
ADMIN_ID = 1808806022 #or your telegram-id
CREATOR_ID = 1808806022 #MIT License

#to change the language, delete the contents of the file "lang.txt "and launch the bot.
LANG = ""

try:
    with open(LANG_FILE, 'r') as file:
        LANG = file.readline().strip()
        if LANG != "ru" and LANG != "eng":
            raise ValueError("Incorrect format.")
        elif LANG:
            print("INFO: The language is set.")
        else:
            raise ValueError("The file is empty.")
except (FileNotFoundError, ValueError):
    LANG = input("Enter the language('ru'/'eng'): ")
    
    while LANG != "ru" and LANG != "eng":
        LANG = input("Enter the language('ru'/'eng'): ")
        
    with open(LANG_FILE, 'w') as file:
        file.write(LANG)
        
    print("The language is saved.")

try:
    with open(TOKEN_FILE, 'r') as file:
        API_TOKEN = file.readline().strip()
        if API_TOKEN:
            print("INFO: The token was found.")
        else:
            raise ValueError("The file is empty.")
except (FileNotFoundError, ValueError):
    API_TOKEN = input("Enter your token: ")
    with open(TOKEN_FILE, 'w') as file:
        file.write(API_TOKEN)
    print("The token is saved.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

user_points = {}
authorized_users = set()

def get_rank(points):
    if points > 20:
        return "♛"
    elif points > 10:
        return "♜"
    else:
        return "♝"

def load_points():
    if os.path.exists(POINTS_FILE):
        try:
            with open(POINTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                data = {int(k): v for k, v in data.items()}
                return data
        except json.JSONDecodeError:
            print("ERROR: json.JSONDecodeError. Error reading the score file. Starting with an empty list.")
    return {}

def save_points():
    with open(POINTS_FILE, "w", encoding="utf-8") as f:
        data_to_save = {str(k): v for k, v in user_points.items()}
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

def load_authorized_users():
    if os.path.exists(AUTHORIZED_USERS_FILE):
        try:
            with open(AUTHORIZED_USERS_FILE, "r", encoding="utf-8") as f:
                return set(json.load(f))
        except json.JSONDecodeError:
            print("ERROR: json.JSONDecodeError. Error reading a file with authorized users. We start with an empty list.")
    return set()

def save_authorized_users():
    with open(AUTHORIZED_USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(authorized_users), f, ensure_ascii=False, indent=4)

def get_translation(key, **kwargs):
    template = translations.get(LANG, {}).get(key, key)
    return template.format(**kwargs)

user_points = load_points()
authorized_users = load_authorized_users()

print(f"INFO: Uploaded User scores:\n{user_points}")
print(f"INFO: Uploaded authorized Users:\n{authorized_users}")

@dp.message_handler(commands=["pi", "points_info", "ip", "info_points"])
async def info(message: types.Message):
    msg = await message.reply(get_translation("system_points_info"))

    await asyncio.sleep(60)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(f"ERROR: {e}. The message could not be deleted.")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nERROR: {e}. The message could not be deleted.")

@dp.message_handler(commands=["v"])
async def verification(message: types.Message):
    user_id = message.from_user.id

    if user_id not in authorized_users:
        authorized_users.add(user_id)
        save_authorized_users()

    msg = await message.reply(get_translation("verification_success"))

    await asyncio.sleep(5)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(f"ERROR: {e}. The message could not be deleted.")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nERROR: {e}. The message could not be deleted.")

@dp.message_handler(commands=["pa", "point_add", "ap", "add_point", "дб", "добавить_балл"])
async def add_points(message: types.Message):
    if not message.reply_to_message:
        msg = await message.reply(get_translation("reply_to_add_point"))

        await asyncio.sleep(5)

        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
        except Exception as e:
            print(f"ERROR: {e}. The message could not be deleted.")
            await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nERROR: {e}. The message could not be deleted.")
        
        return

    target_user_id = message.reply_to_message.from_user.id
    target_username = message.reply_to_message.from_user.username
    
    if message.from_user.id not in authorized_users:
        msg = await message.reply(get_translation("cannot_add_point"))

        await asyncio.sleep(5)

        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
        except Exception as e:
            print(f"ERROR: {e}. The message could not be deleted.")
            await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nERROR: {e}. The message could not be deleted.")
            
        return

    if user_points.get(target_user_id):
        user_points[target_user_id]["points"] += 1
        # Обновляем username, если он изменился
        if user_points[target_user_id]["username"] != target_username:
            user_points[target_user_id]["username"] = target_username
    else:
        # Добавляем нового пользователя
        user_points[target_user_id] = {"username": target_username, "points": 1}   

    try:
        member_status = await bot.get_chat_member(message.chat.id, target_user_id)
        if member_status.status not in ['creator', 'владелец', 'points sys.(/pi)', 'Владелец', 'админ', 'bot-admin']:
            await bot.promote_chat_member(
                chat_id=message.chat.id,
                user_id=target_user_id,
                can_manage_chat=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_delete_messages=False,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_promote_members=False,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False
            )

    except Exception as e:
        print(f"ERROR: {e}. Failed to issue a score.")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nERROR: {e}. Failed to issue a score.")
        return

    prefix = f"{(get_rank(user_points[target_user_id]['points'])) if target_user_id != CREATOR_ID else '❑'}{('Знаток' if LANG == 'ru' else 'Expert')}: {user_points[target_user_id]['points']}"
    try:
        await bot.set_chat_administrator_custom_title(
            chat_id=message.chat.id,
            user_id=target_user_id,
            custom_title=prefix
        )
    except Exception as e:
        print(f"ERROR: {e}. Failed to issue a score.")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nERROR: {e}. Failed to issue a score.")
        return

    save_points()

    msg = await message.reply(get_translation("point_added"))

    await asyncio.sleep(5)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(f"ERROR: {e}. The message could not be deleted.")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nERROR: {e}. The message could not be deleted.")

@dp.message_handler(commands=["pb"])
async def points_balance(message: types.Message):
    user_id = message.from_user.id

    if user_points.get(user_id) is not None:
        user_balance = user_points[user_id]['points']
    else:
        user_balance = 0
    msg = await message.reply(get_translation("your_profile", rank=get_rank(user_balance), points=user_balance))

    await asyncio.sleep(7)

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)
    except Exception as e:
        print(f"ERROR: {e}. The message could not be deleted.")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nERROR: {e}. The message could not be deleted.")

@dp.message_handler(commands=["u"])
async def update_prefix(message: types.Message):
    command_args = message.get_args().strip()

    target_user_id = int(command_args)

    user_points = load_points()
    
    try:
        member_status = await bot.get_chat_member(message.chat.id, target_user_id)
        if member_status.status not in ['creator', 'владелец', 'points sys.(/pi)', 'Владелец', 'админ', 'bot-admin']:
            await bot.promote_chat_member(
                chat_id=message.chat.id,
                user_id=target_user_id,
                can_manage_chat=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_delete_messages=False,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_promote_members=False,
                can_change_info=False,
                can_invite_users=True,
                can_pin_messages=False
            )

    except Exception as e:
        print(f"ERROR: {e}. Failed to issue a score.")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nERROR: {e}. Failed to issue a score.")
        return

    prefix = f"{(get_rank(user_points[target_user_id]['points'])) if target_user_id != CREATOR_ID else '❑'}{('Знаток' if LANG == 'ru' else 'Expert')}: {user_points[target_user_id]['points']}"
    try:
        await bot.set_chat_administrator_custom_title(
            chat_id=message.chat.id,
            user_id=target_user_id,
            custom_title=prefix
        )
    except Exception as e:
        print(f"ERROR: {e}. Failed to issue a score.")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nERROR: {e}. Failed to issue a score.")
        return

    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        print(f"ERROR: {e}. The message could not be deleted.")
        await bot.send_message(chat_id=ADMIN_ID, text=f"Console by Kilobyte\nERROR: {e}. The message could not be deleted.")
    
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
#────────────────────────────── ❑ ──────────────────────────────
#Created by Ivan Shcherbakov (https://github.com/ivansherbakov9/Points-System-In-TG-BOT-Kilobyte)
#────────────────────────────── ❑ ──────────────────────────────
