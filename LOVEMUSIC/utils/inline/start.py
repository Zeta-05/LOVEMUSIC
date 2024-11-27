from pyrogram.types import InlineKeyboardButton

import config
from config import SUPPORT_CHAT
from LOVEMUSIC import app


def start_pannel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="💠 sᴜᴍᴍᴏɴ ᴍᴇ 💠",
                url=f"https://t.me/{app.username}?startgroup=true",
            ),
        ],
        [
            InlineKeyboardButton(text="ᴄᴏᴍᴍᴀɴᴅs", callback_data="settings_back_helper"),
            InlineKeyboardButton(text="ᴄᴏᴍᴍᴀɴᴅs", callback_data="settings_helper"),
        ],
        [
            InlineKeyboardButton(text="ʜᴏᴍᴇᴛᴏᴡɴ", url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="💠 sᴜᴍᴍᴏɴ ᴍᴇ 💠",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text="ʜᴏᴍᴇᴛᴏᴡɴ", url=config.SUPPORT_CHAT),
            InlineKeyboardButton(text="ᴏʀɪɢɪɴ", url=config.SUPPORT_CHANNEL),
        ],
        [
            InlineKeyboardButton(
                text="ᴄᴏᴍᴍᴀɴᴅs", callback_data="settings_back_helper"
            )
        ],
    ]
    return buttons


def alive_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="✿︎ sᴜᴍᴍᴏɴ ✿︎", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_CHAT}"),
        ],
    ]
    return buttons


def music_start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="💠 sᴜᴍᴍᴏɴ ᴍᴇ 💠",
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text="ᴀʙᴏᴜᴛ 📝", callback_data="about"),
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ 🥀", callback_data="support"),
        ],
        [InlineKeyboardButton(text="۞ ᴄᴏᴍᴍᴀɴᴅs ۞", callback_data="feature")],
    ]
    return buttons
