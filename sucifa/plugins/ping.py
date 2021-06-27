import asyncio
import datetime

from . import *

@bot.on(hell_cmd(pattern="ping$"))
@bot.on(sudo_cmd(pattern="ping$", allow_sudo=True))
async def pong(hell):
    if hell.fwd_from:
        return
    start = datetime.datetime.now()
    event = await eor(hell, "`·.·★ ℘ıŋɠ ★·.·´")
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(
        f"╰•★★  Ping ★★•╯\n\n    ⚘  `{ms}`\n    ⚘  __**Owner**__ **:**  {hell_mention}"
    )


CmdHelp("ping").add_command(
  "ping", None, "Checks the ping speed of your Andini <3"
).add_warning(
  "✅ Harmless Module"
).add()

# sucifa
