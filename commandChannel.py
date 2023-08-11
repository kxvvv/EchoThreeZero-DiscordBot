import discord
import json
from config import *



async def commandChannelCheck(ctx):
    print(ctx.channel.id)
    print(COMMAND_ROOM)
    if ctx.channel.id != COMMAND_ROOM:
        return False
    else:
        return True