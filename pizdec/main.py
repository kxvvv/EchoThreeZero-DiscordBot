import discord
import json

from datetime import datetime as dt

from discord.ext import commands
from discord import app_commands











intents = discord.Intents.all()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents, help_command=None)



async def get_user_wallet(user_id):
    user_id = str(user_id)

    with open("wallets.json", "r") as file:
        users_wallets = json.load(file)

    if user_id not in users_wallets.keys():
        users_wallets[user_id] = DEFAULT

    with open("wallets.json", "w") as file:
        json.dump(users_wallets, file)

    return users_wallets[user_id]


async def set_user_wallet(user_id, parameter, new_value):
    user_id = str(user_id)

    with open("wallets.json", "r") as file:
        users_wallets = json.load(file)

    if user_id not in users_wallets.keys():
        users_wallets[user_id] = DEFAULT

    users_wallets[user_id][parameter] = new_value

    with open("wallets.json", "w") as file:
        json.dump(users_wallets, file)


counter = False
@client.listen('on_message')
async def on_message(ctx):
    global counter
    if counter == True:
        return
    else:
        print('msg\n\n\n')
        counter = True


    moders = ["ewoni", "slava423", "redwanderer", "funset", "rokkeavgn", "umnaya_svinka", "starforce", "lochde", "merlin_menson", "morry", "dimonsupe", "abyssal", "glaz", "sokiromo", "maksik", "(lawi)", "kern_dog", "wireguard", "sekevir", "tronick", "demur", "phobia", "dark1155", "araks", "resetik", "feonix", "clipsvc", "cartoonm", "shimorio", "kxv", "alexfox", "ksen0morph", "syndicarp", "mrfippik", "cap_of_tea", "ashatears", "neckpuck", "halch", "bloodcanis", "nikita101889", "mr_samuel", "tainakov", "asoidoro", "ronen", "mersen", "qabi", "bopon", "montuenza"]


    listOfMembers = []
    with open ('basa.json', 'r') as file:
        users_ids = json.load(file)
    with open ('wallets.json', 'r') as file:
        users_ahelps = json.load(file)



    for guild in client.guilds:
        for member in guild.members:
            for x in users_ids.keys():
                if int(x) == member.id:

                    users_ids[x].setdefault('discord', member.name)

                    for y in users_ahelps.keys():
                        if str(y).lower() == str(member).lower():
                            ahelpCount = users_ahelps[y]
                            users_ids[x].setdefault('ahelp', ahelpCount['ahelp'])

                    
                    try:
                        users_ids[x]['ahelp']
                    except:
                        users_ids[x].setdefault('ahelp', 0)
                    if '#' in str(member):
                        pass
                    else:
                        #print('\n')
                        #print(member)
                        #print(users_ids[x])
                        pass

    with open ('newbase.json', 'w') as file:
        json.dump(users_ids, file)
    
    with open ('newbase.json', 'r') as file:
        users = json.load(file)

    for x in users.keys():
        print(users[x])

    return







    ahelp = client.get_channel(923319745019801661)
    m = [message async for message in ahelp.history(limit=LIMIT)]

    moders = ["ewoni", "slava423", "redwanderer", "funset", "rokkeavgn", "umnaya_svinka", "starforce", "lochde", "merlin_menson", "morry", "dimonsupe", "abyssal", "glaz", "sokiromo", "maksik", "(lawi)", "kern_dog", "wireguard", "sekevir", "tronick", "demur", "phobia", "dark1155", "araks", "resetik", "feonix", "clipsvc", "cartoonm", "shimorio", "kxv", "alexfox", "ksen0morph", "syndicarp", "mrfippik", "cap_of_tea", "ashatears", "neckpuck", "halch", "bloodcanis", "nikita101889", "mr_samuel", "tainakov", "asoidoro", "ronen", "mersen", "qabi", "bopon", "montuenza"]
    modersCounters = {}

    checkingNow = 0

    

    for x in m:
        checkingNow += 1
        print(f'Проверил {checkingNow} из {LIMIT}')
        m = x
        m = m.embeds
        m=m[0]
        m=m.description
        m = m.lower()

        for x in moders:
            if x in m:
                modersCounters = await get_user_wallet(x)

                modersCounters["ahelp"] += 1

                await set_user_wallet(x, "ahelp", modersCounters["ahelp"])


    with open("wallets.json", "r") as file:
        users_wallets = json.load(file)
        for x in users_wallets:
            ahelps = users_wallets[x]['ahelp']
            print(f'{x}: {ahelps}')








LIMIT = 32600
DEFAULT = {'ahelp': 0}

client.run(token='MTEyNzIxNDUwMTEzNDA3Nzk5Mg.GZsn67.uq1Lvav1-teTrxg1DBYL1aZazGg97f9Y75HqK4')