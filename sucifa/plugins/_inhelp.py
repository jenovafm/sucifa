from math import ceil
from re import compile
import asyncio
import html
import os
import re
import sys

from telethon import Button, custom, events, functions
from telethon.tl.functions.users import GetFullUserRequest
from telethon.events import InlineQuery, callbackquery
from telethon.sync import custom
from telethon.errors.rpcerrorlist import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ExportChatInviteRequest

from . import *

hell_row = Config.BUTTONS_IN_HELP
hell_emoji = Config.EMOJI_IN_HELP
hell_pic = Config.PMPERMIT_PIC or "https://i.ibb.co/8m4Wssg/uci.jpg"
cstm_pmp = Config.CUSTOM_PMPERMIT
ALV_PIC = Config.ALIVE_PIC

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

mybot = Config.BOT_USERNAME
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"
LOG_GP = Config.LOGGER_ID
mssge = (
    str(cstm_pmp)
    if cstm_pmp
    else "**You Have Trespassed To My Master's PM!\nThis Is Illegal And Regarded As Crime.**"
)

USER_BOT_WARN_ZERO = "Enough Of Your Flooding In My Master's PM!! \n\n**π« Blocked and Reported**"

HELL_FIRST = (
    "**π₯ [ Andini:Security - System Protection ]**\n\nThis is to inform you that "
    "{} is currently unavailable.\nThis is an automated message.\n\n"
    "{}\n\n**Please Choose Why You Are Here!!**".format(hell_mention, mssge))

alive_txt = """
**βοΈ Andini <3 ΞΉΡ ΟΠΈβΞΉΠΈΡ βοΈ**
{}
**π π±ππ ππππππ π**

**Telethon :**  `{}`
**SFA  :**  **{}**
**Uptime   :**  `{}`
**Abuse    :**  **{}**
**Sudo      :**  **{}**
"""

def button(page, modules):
    Row = hell_row
    Column = 3

    modules = sorted([modul for modul in modules if not modul.startswith("_")])
    pairs = list(map(list, zip(modules[::2], modules[1::2])))
    if len(modules) % 2 == 1:
        pairs.append([modules[-1]])
    max_pages = ceil(len(pairs) / Row)
    pairs = [pairs[i : i + Row] for i in range(0, len(pairs), Row)]
    buttons = []
    for pairs in pairs[page]:
        buttons.append(
            [
                custom.Button.inline(f"{hell_emoji} " + pair + f" {hell_emoji}", data=f"Information[{page}]({pair})")
                for pair in pairs
            ]
        )

    buttons.append(
        [
            custom.Button.inline(
               f"βοΈ Back {hell_emoji}", data=f"page({(max_pages - 1) if page == 0 else (page - 1)})"
            ),
            custom.Button.inline(
               f"β’ β β’", data="close"
            ),
            custom.Button.inline(
               f"{hell_emoji} Next βΆοΈ", data=f"page({0 if page == (max_pages - 1) else page + 1})"
            ),
        ]
    )
    return [max_pages, buttons]


    modules = CMD_HELP
if Config.BOT_USERNAME is not None and tgbot is not None:
    @tgbot.on(InlineQuery)  # pylint:disable=E0602
    async def inline_handler(event):
        builder = event.builder
        result = None
        query = event.text
        if event.query.user_id == bot.uid and query == "sucifa_help":
            rev_text = query[::-1]
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            result = await builder.article(
                f"Hey! Only use .help please",
                text=f"π° **{hell_mention}**\n\nπ __No.of Plugins__ : `{len(CMD_HELP)}` \nποΈ __Commands__ : `{len(apn)}`\nποΈ __Page__ : 1/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False,
            )
        elif event.query.user_id == bot.uid and query.startswith("fsub"):
            hunter = event.pattern_match.group(1)
            hell = hunter.split("+")
            user = await bot.get_entity(int(hell[0]))
            channel = await bot.get_entity(int(hell[1]))
            msg = f"**π Welcome** [{user.first_name}](tg://user?id={user.id}), \n\n**π You need to Join** {channel.title} **to chat in this group.**"
            if not channel.username:
                link = (await bot(ExportChatInviteRequest(channel))).link
            else:
                link = "https://t.me/" + channel.username
            result = [
                await builder.article(
                    title="force_sub",
                    text = msg,
                    buttons=[
                        [Button.url(text="Channel", url=link)],
                        [custom.Button.inline("π Unmute Me", data=unmute)],
                    ],
                )
            ]

        elif event.query.user_id == bot.uid and query == "alive":
            he_ll = alive_txt.format(Config.ALIVE_MSG, tel_ver, hell_ver, uptime, abuse_m, is_sudo)
            alv_btn = [
                [Button.url(f"{HELL_USER}", f"tg://openmessage?user_id=bytewritter")],
                [Button.url("My Channel", f"https://t.me/{my_channel}"), 
                Button.url("My Group", f"https://t.me/{my_group}")],
            ]
            if ALV_PIC and ALV_PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    ALV_PIC,
                    text=he_ll,
                    buttons=alv_btn,
                    link_preview=False,
                )
            elif ALV_PIC:
                result = builder.document(
                    ALV_PIC,
                    text=he_ll,
                    title="[ Andini <3 Alive ]",
                    buttons=alv_btn,
                    link_preview=False,
                )
            else:
                result = builder.article(
                    text=he_ll,
                    title="[ Andini <3 Alive ]",
                    buttons=alv_btn,
                    link_preview=False,
                )

        elif event.query.user_id == bot.uid and query == "pm_warn":
            hel_l = HELL_FIRST.format(hell_mention, mssge)
            result = builder.photo(
                file=hell_pic,
                text=hel_l,
                buttons=[
                    [
                        custom.Button.inline("π Request π", data="req"),
                        custom.Button.inline("π¬ Chat π¬", data="chat"),
                    ],
                    [custom.Button.inline("π« Spam π«", data="heheboi")],
                    [custom.Button.inline("Curious β", data="pmclick")],
                ],
            )

        elif event.query.user_id == bot.uid and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**β‘ Andini <3 β‘**",
                buttons=[
                    [Button.url("π Queen π", "https://instagram.com/suciandni_")],
                    [Button.url("π King π", "https://instagram.com/jenovafm")],
                ],
            )

        elif query.startswith("http"):
            part = query.split(" ")
            result = builder.article(
                "File uploaded",
                text=f"**File uploaded successfully to {part[2]} site.\n\nUpload Time : {part[1][:3]} second\n[βββ β]({part[0]})",
                buttons=[[custom.Button.url("URL", part[0])]],
                link_preview=True,
            )

        else:
            result = builder.article(
                "Your love desire what've been done...",
                text="""**Hi, it's me [Andini](https://instagram.com/suciandni_) \nKamu bakal tahu tentang aku dari link di bawah π**""",
                buttons=[
                    [
                        custom.Button.url("π₯ Channel π₯", "https://t.me/sfa_enterprise"),
                        custom.Button.url(
                            "β‘ Group β‘", "https://t.me/aesdcrypt"
                        ),
                    ],
                    [
                        custom.Button.url(
                            "π° King π°", "https://instagram.com/jenovafm"),
                        custom.Button.url
                    (
                            "β¨ Queen β¨", "https://instagram.com/suciandni_"
                    )
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"pmclick")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for Other Users..."
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"π° This is Andini PM Security for {hell_mention} to keep away unwanted retards from spamming PM..."
            )

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"req")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"β **Request Registered** \n\n{hell_mention} will now decide to look for your request or not.\nπ Till then wait patiently and don't spam!!"
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            first_name = html.escape(target.user.first_name)
            ok = event.query.user_id
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**π Hey {hell_mention} !!** \n\nβοΈ You Got A Request From [{first_name}](tg://user?id={ok}) In PM!!"
            await bot.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"chat")))
    async def on_pm_click(event):
        event.query.user_id
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"Ahh!! You here to do chit-chat!!\n\nPlease wait for {hell_mention} to come. Till then keep patience and don't spam."
            )
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            tosend = f"**π Hey {hell_mention} !!** \n\nβοΈ You Got A PM from  [{first_name}](tg://user?id={ok})  for random chats!!"
            await bot.send_message(LOG_GP, tosend)


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"heheboi")))
    async def on_pm_click(event):
        if event.query.user_id == bot.uid:
            reply_pop_up_alert = "This is for other users!"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        else:
            await event.edit(
                f"π₯΄ **Getting Out...**"
            )
            await bot(functions.contacts.BlockRequest(event.query.user_id))
            target = await event.client(GetFullUserRequest(event.query.user_id))
            ok = event.query.user_id
            first_name = html.escape(target.user.first_name)
            if first_name is not None:
                first_name = first_name.replace("\u2060", "")
            first_name = html.escape(target.user.first_name)
            await bot.send_message(
                LOG_GP,
                f"**Blocked**  [{first_name}](tg://user?id={ok}) \n\nReason:- Spam",
            )


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"unmute")))
    async def on_pm_click(event):
        hunter = (event.data_match.group(1)).decode("UTF-8")
        hell = hunter.split("+")
        if not event.sender_id == int(hell[0]):
            return await event.answer("This Ain't For You!!", alert=True)
        try:
            await bot(GetParticipantRequest(int(hell[1]), int(hell[0])))
        except UserNotParticipantError:
            return await event.answer(
                "You need to join the channel first.", alert=True
            )
        await bot.edit_permissions(
            event.chat_id, int(hell[0]), send_message=True, until_date=None
        )
        await event.edit("Yay! You can chat now !!")


    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"reopen")))
    async def reopn(event):
            if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
                current_page_number=0
                simp = button(current_page_number, CMD_HELP)
                veriler = button(0, sorted(CMD_HELP))
                apn = []
                for x in CMD_LIST.values():
                    for y in x:
                        apn.append(y)
                await event.edit(
                    f"π° **{hell_mention}**\n\nπ __No.of Plugins__ : `{len(CMD_HELP)}` \nποΈ __Commands__ : `{len(apn)}`\nποΈ __Page__ : 1/{veriler[0]}",
                    buttons=simp[1],
                    link_preview=False,
                )
            else:
                reply_pop_up_alert = "Hoo gya aapka. Kabse tapar tapar dabae jaa rhe h. Khudka bna lo na agr chaiye to. Β© HΓͺllαΊΓΈβ  β’"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
        

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            veriler = custom.Button.inline(f"{hell_emoji} Re-Open Menu {hell_emoji}", data="reopen")
            await event.edit(f"**βοΈ Andini <3 Service Closed βοΈ**\n\n**Bot Of :**  {hell_mention}\n\n        [Β©οΈSFA-EnterpriseοΈ]({chnl_link})", buttons=veriler, link_preview=False)
        else:
            reply_pop_up_alert = "Suci Fitri Andini <3"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
   

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"page\((.+?)\)")))
    async def page(event):
        page = int(event.data_match.group(1).decode("UTF-8"))
        veriler = button(page, CMD_HELP)
        apn = []
        for x in CMD_LIST.values():
            for y in x:
                apn.append(y)
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                f"π° **{hell_mention}**\n\nπ __No.of Plugins__ : `{len(CMD_HELP)}`\nποΈ __Commands__ : `{len(apn)}`\nποΈ __Page__ : {page + 1}/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False,
            )
        else:
            return await event.answer(
                "Suci Fitri Andini <3",
                cache_time=0,
                alert=True,
            )


    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"Information\[(\d*)\]\((.*)\)"))
    )
    async def Information(event):
        page = int(event.data_match.group(1).decode("UTF-8"))
        commands = event.data_match.group(2).decode("UTF-8")
        try:
            buttons = [
                custom.Button.inline(
                    "β‘ " + cmd[0] + " β‘", data=f"commands[{commands}[{page}]]({cmd[0]})"
                )
                for cmd in CMD_HELP_BOT[commands]["commands"].items()
            ]
        except KeyError:
            return await event.answer(
                "No Description is written for this plugin", cache_time=0, alert=True
            )

        buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        buttons.append([custom.Button.inline(f"{hell_emoji} Main Menu {hell_emoji}", data=f"page({page})")])
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                f"**π File :**  `{commands}`\n**π’ Number of commands :**  `{len(CMD_HELP_BOT[commands]['commands'])}`",
                buttons=buttons,
                link_preview=False,
            )
        else:
            return await event.answer(
                "Suci Fitri Andini <3",
                cache_time=0,
                alert=True,
            )


    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"commands\[(.*)\[(\d*)\]\]\((.*)\)"))
    )
    async def commands(event):
        cmd = event.data_match.group(1).decode("UTF-8")
        page = int(event.data_match.group(2).decode("UTF-8"))
        commands = event.data_match.group(3).decode("UTF-8")
        result = f"**π File :**  `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**β οΈ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n\n"
        else:
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**β οΈ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**βΉοΈ Info :**  {CMD_HELP_BOT[cmd]['info']['info']}\n\n"
        command = CMD_HELP_BOT[cmd]["commands"][commands]
        if command["params"] is None:
            result += f"**π  Commands :**  `{HANDLER[:1]}{command['command']}`\n"
        else:
            result += f"**π  Commands :**  `{HANDLER[:1]}{command['command']} {command['params']}`\n"
        if command["example"] is None:
            result += f"**π¬ Explanation :**  `{command['usage']}`\n\n"
        else:
            result += f"**π¬ Explanation :**  `{command['usage']}`\n"
            result += f"**β¨οΈ For Example :**  `{HANDLER[:1]}{command['example']}`\n\n"
        if event.query.user_id == bot.uid or event.query.user_id in Config.SUDO_USERS:
            await event.edit(
                result,
                buttons=[
                    custom.Button.inline(f"{hell_emoji} Return {hell_emoji}", data=f"Information[{page}]({cmd})")
                ],
                link_preview=False,
            )
        else:
            return await event.answer(
                "Suci Fitri Andini <3",
                cache_time=0,
                alert=True,
            )


# sucifa
