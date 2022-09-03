import asyncio
from asyncirc.protocol import IrcProtocol
from asyncirc.server import Server
import logging
from core.controller import LightController
from core.pytc_logger import PytcLogger
import configparser
config = configparser.ConfigParser()
config.read('config/credentials.cfg')
pytclog = PytcLogger()
logger = pytclog.setup_logger('asyncirc')
loop = asyncio.get_running_loop()
lc = LightController()

servers = [
    Server("irc.chat.twitch.tv", 6697, True),
]

async def check_for_commands(conn, message):
    commands = configparser.ConfigParser()
    commands.read('commands.cfg')
    cmd = await parser(message)
    while True:
        await asyncio.sleep(1)
        if str(cmd).startswith('!'):
            try:
                color_to_change = commands.get('COLOR-COMMANDS', cmd)
                if color_to_change != 'white':
                    await lc.change_color(color_to_change)
                    await conn.send(f"PRIVMSG #{config['TWITCH_CREDS']['channel']} :Renk {cmd} olarak değiştirildi. \r")
                else:
                    await lc.total_white()
                    await conn.send(f"PRIVMSG #{config['TWITCH_CREDS']['channel']} :Renk beyaz olarak değiştirildi. \r")
            except:
                pass
        break
    pass

async def parser(message):
    message = str(message)
    command = str(message).split(':')
    return command[-1]

async def log(conn, message):
    logger.log(logging.INFO, f"[TWITCH]:{message}")

async def main():
    conn = IrcProtocol(servers, nick="ayberkenis", loop=loop, logger=logger)
    conn.register("PRIVMSG", check_for_commands)
    conn.register("PRIVMSG", log)
    await conn.connect()
    conn.send(f"PASS {config['TWITCH_CREDS']['oauth_token']}".encode('utf-8'))
    conn.send(f"NICK {config['TWITCH_CREDS']['nick']}".encode('utf-8'))
    conn.send(f"JOIN #{config['TWITCH_CREDS']['channel']}".encode('utf-8'))

    await asyncio.Event().wait()

