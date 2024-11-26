import time
import asyncio
from pyrogram.errors import UserAlreadyParticipant
from pyrogram.errors import UserNotParticipant
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch
import config
from LOVEMUSIC.misc import _boot_
from LOVEMUSIC.utils import bot_up_time
from LOVEMUSIC.plugins.sudo.sudoers import sudoers_list
from LOVEMUSIC.utils.database import (
    add_served_chat_clone,
    add_served_user_clone,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from LOVEMUSIC.utils.decorators.language import LanguageStart
from LOVEMUSIC.utils.formatters import get_readable_time
from LOVEMUSIC.utils.inline import first_page, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string
from LOVEMUSIC.utils.database import get_assistant
from time import time
import random
from LOVEMUSIC.utils.extraction import extract_user

# Define a dictionary to track the last message timestamp for each user
user_last_message_time = {}
user_command_count = {}
# Define the threshold for command spamming (e.g., 20 commands within 60 seconds)
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5

YUMI_PICS = [
    "https://telegra.ph/file/3134ed3b57eb051b8c363.jpg",
    "https://telegra.ph/file/5a2cbb9deb62ba4b122e4.jpg",
    "https://telegra.ph/file/cb09d52a9555883eb0f61.jpg",
]


# Function to send the start video
async def send_start_video(client, message, _):
    video_url = "https://envs.sh/z7S.mp4"  # Change with your actual video URL
    await message.reply_video(
        video_url,
        caption=_["start_video_caption"],
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🎵 Play Music", callback_data="play_music")]
        ])
    )


@Client.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client: Client, message: Message, _):
    a = await client.get_me()
    user_id = message.from_user.id
    current_time = time()

    # Update the last message timestamp for the user
    last_message_time = user_last_message_time.get(user_id, 0)

    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        # If less than the spam window time has passed since the last message
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            # Block the user if they exceed the threshold
            hu = await message.reply_text(
                f"**{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴᴛ ᴅᴏ sᴘᴀᴍ, ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄ**"
            )
            await asyncio.sleep(3)
            await hu.delete()
            return
    else:
        # If more than the spam window time has passed, reset the command count and update the message timestamp
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    await add_served_user_clone(message.from_user.id)

    # Send the start video first
    await send_start_video(client, message, _)

    # Wait for the video to send, then send the rest of the response
    await asyncio.sleep(3)  # Adjust this as per video duration or user preference

    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = first_page(_)
            return await message.reply_photo(
                photo=config.START_IMG_URL,
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, a.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="📥 ᴠɪᴅᴇᴏ", callback_data=f"downloadvideo {query}"
                        ),
                        InlineKeyboardButton(
                            text="📥 ᴀᴜᴅɪᴏ", callback_data=f"downloadaudio {query}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(text="🎧 sᴇᴇ ᴏɴ ʏᴏᴜᴛᴜʙᴇ 🎧", url=link),
                    ],
                ]
            )
            await m.delete()
            await client.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
    else:
        out = private_panel(_)
        await message.reply_photo(
            photo=config.START_IMG_URL,
            caption=_["start_2"].format(message.from_user.mention, a.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )


@Client.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    a = await client.get_me()
    user_id = message.from_user.id
    current_time = time()

    # Update the last message timestamp for the user
    last_message_time = user_last_message_time.get(user_id, 0)

    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        # If less than the spam window time has passed since the last message
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            # Block the user if they exceed the threshold
            hu = await message.reply_text(
                f"**{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴᴛ ᴅᴏ sᴘᴀᴍ, ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄ**"
            )
            await asyncio.sleep(3)
            await hu.delete()
            return
    else:
        # If more than the spam window time has passed, reset the command count and update the message timestamp
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    # Send the start video first
    await send_start_video(client, message, _)

    # Wait for the video to send, then send the rest of the response
    await asyncio.sleep(3)  # Adjust this as per video duration or user preference

    out = start_panel(_)
    BOT_UP = await bot_up_time()
    await message.reply_photo(
        photo=config.START_IMG_URL,
        caption=_["start_1"].format(a.mention, BOT_UP),
        reply_markup=InlineKeyboardMarkup(out),
    )
    await add_served_chat_clone(message.chat.id)

    # Check if Userbot is already in the group
    try:
        userbot = await get_assistant(message.chat.id)
        message = await message.reply_text(
            f"**ᴄʜᴇᴄᴋɪɴɢ [ᴀssɪsᴛᴀɴᴛ](tg://openmessage?user_id={userbot.id}) ᴀᴠᴀɪʟᴀʙɪᴛʟʏ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ...**"
        )
        is_userbot = await client.get_chat_member(message.chat.id, userbot.id)
        if is_userbot:
            await message.edit_text(
                f"**[ᴀssɪsᴛᴀɴᴛ](tg://openmessage?user_id={userbot.id}) ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.**"
            )
        else:
            await message.edit_text(
                f"**[ᴀssɪsᴛᴀɴᴛ](tg://openmessage?user_id={userbot.id}) ɪs ɴᴏᴛ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.**"
            )
    except UserNotParticipant:
        await message.reply_text(
            f"**[ᴀssɪsᴛᴀɴᴛ](tg://openmessage?user_id={userbot.id}) ɪs ɴᴏᴛ ᴘᴀʀᴛɪᴄɪᴘᴀᴛɪɴɢ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ!**"
        )
    except Exception as e:
        await message.reply_text(f"**Error checking assistant: {str(e)}**")
        print(e)
    
    await add_served_chat_clone(message.chat.id)
    # Send user a message for group-specific welcome
    if message.chat.type == "supergroup":
        welcome_msg = _["start_3"].format(message.chat.title, a.mention)
        await message.reply_text(welcome_msg)
    

# Handle banned users or any user blacklist check in start command for both PM and Group
async def check_if_banned(client, message: Message):
    user_id = message.from_user.id
    if await is_banned_user(user_id):
        await message.reply_text(
            f"**{message.from_user.mention}, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛʀᴏᴍ ᴜѕɪɴɢ ᴛʜɪs ʙᴏᴛ.**"
        )
        return True
    return False


# Optional: Monitor unban or commands on group level
@Client.on_message(filters.command("unban") & filters.group)
async def unban_user(client, message: Message):
    user_id = message.from_user.id
    if not await is_banned_user(user_id):
        await message.reply_text("**You are not banned.**")
    else:
        await message.reply_text("**Unbanning user...**")
        # Implement unbanning logic if required here
        # For example: remove from blacklist, etc.


@Client.on_message(filters.command("ban") & filters.group)
async def ban_user(client, message: Message):
    user_id = message.from_user.id
    if await is_banned_user(user_id):
        await message.reply_text("**User is already banned.**")
    else:
        await message.reply_text("**Banning user...**")
        # Implement banning logic here
        # For example: add to blacklist, etc.
