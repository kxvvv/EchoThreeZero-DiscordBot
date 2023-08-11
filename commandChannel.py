import discord
import json
from config import *



async def commandChannelCheck(ctx):
    if ctx.channel.id != COMMAND_ROOM:
        return False
    else:
        return True