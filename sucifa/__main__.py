import glob
import os
import sys
from pathlib import Path

import telethon.utils
from telethon import TelegramClient
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest

from sucifa import LOGS, bot, tbot
from sucifa.config import Config
from sucifa.utils import load_module
from sucifa.version import __hell__ as hellver
hl = Config.HANDLER
HELL_PIC = Config.ALIVE_PIC or "https://i.ibb.co/8m4Wssg/uci.jpg"

# let's get the bot ready
async def hell_bot(bot_token):
    try:
        await bot.start(bot_token)
        bot.me = await bot.get_me()
        bot.uid = telethon.utils.get_peer_id(bot.me)
    except Exception as e:
        LOGS.error(f"[Session:Andini] - {str(e)}")
        sys.exit()


# sucifa starter...
if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    try:
        if Config.BOT_USERNAME is not None:
            LOGS.info("Checking Telegram Bot Username...")
            bot.tgbot = TelegramClient(
                "BOT_TOKEN", api_id=Config.APP_ID, api_hash=Config.API_HASH
            ).start(bot_token=Config.BOT_TOKEN)
            LOGS.info("Checking Completed. Proceeding to next step...")
            LOGS.info("🔰 Starting Andini 🔰")
            bot.loop.run_until_complete(hell_bot(Config.BOT_USERNAME))
            LOGS.info("🔥 Andini Startup Completed 🔥")
        else:
            bot.start()
    except Exception as e:
        LOGS.error(f"BOT_TOKEN - {str(e)}")
        sys.exit()

# imports plugins...
path = "sucifa/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        load_module(shortname.replace(".py", ""))

# let the party begin...
LOGS.info("Starting Bot Mode !")
tbot.start()
LOGS.info("⚡ Your Andini Is Now Working ⚡")
LOGS.info(
    "dm instagram to @jenovafm for Updates."
)

# that's life...
async def hell_is_on():
    try:
        if Config.LOGGER_ID != 0:
            await bot.send_file(
                Config.LOGGER_ID,
                HELL_PIC,
                caption=f"#START \n\nDeployed Andini Successfully\n\n**Andini - {hellver}**\n\nType `{hl}ping` or `{hl}alive` to check! \n\nFollow [Instagram](instagram.com/jenovafm)",
            )
    except Exception as e:
        LOGS.info(str(e))

# Join HellBot Channel after deploying 🤐😅
    try:
        await bot(JoinChannelRequest("@sfa_enterprise"))
    except BaseException:
        pass

# Why not come here and chat??
    try:
        await bot(JoinChannelRequest("@aesdcrypt"))
    except BaseException:
        pass


bot.loop.create_task(hell_is_on())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    bot.tgbot = None
    bot.run_until_disconnected()

# sucifa
