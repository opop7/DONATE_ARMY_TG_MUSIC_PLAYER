#
# Copyright (C) 2024 by DONATE_ARMY™@Github, < https://github.com/DONATE-ARMY-BOTS >.
#
# This file is part of < https://github.com/DONATE-ARMY-BOTS/DONATE_ARMY_TG_MUSIC_PLAYER > project,
# and is released under the MIT License.
# Please see < https://github.com/DONATE-ARMY-BOTS/DONATE_ARMY_TG_MUSIC_PLAYER/blob/master/LICENSE >
#
# All rights reserved.
#

from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message

from config import BANNED_USERS
from strings import get_command, get_string, languages_present
from DONATE_ARMY_TG_MUSIC_PLAYER import app
from DONATE_ARMY_TG_MUSIC_PLAYER.utils.database import get_lang, set_lang
from DONATE_ARMY_TG_MUSIC_PLAYER.utils.decorators import ActualAdminCB, language, languageCB

# Languages Available


def lanuages_keyboard(_):
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(
        *[
            (
                InlineKeyboardButton(
                    text=languages_present[i],
                    callback_data=f"languages:{i}",
                )
            )
            for i in languages_present
        ]
    )
    keyboard.row(
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data=f"settingsback_helper",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
    )
    return keyboard


LANGUAGE_COMMAND = get_command("LANGUAGE_COMMAND")


@app.on_message(filters.command(LANGUAGE_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def langs_command(client, message: Message, _):
    keyboard = lanuages_keyboard(_)
    await message.reply_text(
        _["setting_1"].format(message.chat.title, message.chat.id),
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@ActualAdminCB
async def language_markup(client, CallbackQuery, _):
    langauge = (CallbackQuery.data).split(":")[1]
    old = await get_lang(CallbackQuery.message.chat.id)
    if str(old) == str(langauge):
        return await CallbackQuery.answer(
            "ʏᴏᴜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ᴜsɪɴɢ sᴀᴍᴇ ʟᴀɴɢᴜᴀɢᴇ", show_alert=True
        )
    try:
        _ = get_string(langauge)
        await CallbackQuery.answer(
            "ʏᴏᴜʀ ʟᴀɴɢᴜᴀɢᴇ ᴄʜᴀɴɢᴇᴅ sᴜᴄᴇssғᴜʟʟʏ..", show_alert=True
        )
    except:
        return await CallbackQuery.answer(
            "ғᴀɪʟᴇᴅ ᴛᴏ ᴄʜᴀɴɢᴇ ʟᴀɴɢᴜᴀɢᴇ ᴏʀ ʟᴀɴɢᴜᴀɢᴇ ɪs ɪɴ ᴜɴᴅᴇʀ ᴜᴘᴅᴀᴛᴇ",
            show_alert=True,
        )
    await set_lang(CallbackQuery.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)
