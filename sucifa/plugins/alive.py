from telethon import events
from telethon.events import NewMessage
from telethon.tl.custom import Dialog
from telethon.tl.types import Channel, Chat, User
from telethon.errors import ChatSendInlineForbiddenError as noin
from telethon.errors.rpcerrorlist import BotMethodInvalidError as dedbot

from . import *

#-------------------------------------------------------------------------------

hell_pic = Config.ALIVE_PIC or "https://i.ibb.co/8m4Wssg/uci.jpg"
alive_c = f"__**π₯π₯Andini <3 Online**__\n\n"
alive_c += f"__βΌ ΓwΓ±Γͺr β__ : γ {hell_mention} γ\n\n"
alive_c += f"β’β¦β’ Telethon     :  `{tel_ver}` \n"
alive_c += f"β’β¦β’ Andini       :  __**{hell_ver}**__\n"
alive_c += f"β’β¦β’ Sudo            :  `{is_sudo}`\n"
alive_c += f"β’β¦β’ Channel      :  {hell_channel}\n"

#-------------------------------------------------------------------------------

@bot.on(hell_cmd(outgoing=True, pattern="alive$"))
@bot.on(sudo_cmd(pattern="alive$", allow_sudo=True))
async def up(hell):
    if hell.fwd_from:
        return
    await hell.get_chat()
    await hell.delete()
    await bot.send_file(hell.chat_id, hell_pic, caption=alive_c)
    await hell.delete()

msg = f"""
**β‘ Andini <3 Online β‘**
{Config.ALIVE_MSG}
**π π±ππ ππππππ π**
**Telethon :**  `{tel_ver}`
**Andini  :**  **{hell_ver}**
**Uptime   :**  `{uptime}`
**Abuse    :**  **{abuse_m}**
**Sudo      :**  **{is_sudo}**
"""
botname = Config.BOT_USERNAME

@bot.on(hell_cmd(pattern="ucii$"))
@bot.on(sudo_cmd(pattern="ucii$", allow_sudo=True))
async def hell_a(event):
    try:
        hell = await bot.inline_query(botname, "alive")
        await hell[0].click(event.chat_id)
        if event.sender_id == bytewritter:
            await event.delete()
    except (noin, dedbot):
        await eor(event, msg)


CmdHelp("alive").add_command(
  "alive", None, "Shows the Default Alive Message"
).add_command(
  "ucii", None, "Shows Inline Alive Menu with more details."
).add_warning(
  "β Harmless Module"
).add()
