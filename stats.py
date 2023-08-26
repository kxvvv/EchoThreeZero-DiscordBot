import discord
import json
from config import *




async def stats(ctx, client):


    echoRole = discord.utils.find(lambda r: r.name == '☄️', ctx.guild.roles)
    elysiumRole = discord.utils.find(lambda r: r.name == '🌑', ctx.guild.roles)
    solarisRole = discord.utils.find(lambda r: r.name == '🌕', ctx.guild.roles)
    atharaRole = discord.utils.find(lambda r: r.name == '🌌', ctx.guild.roles)
    novaRole = discord.utils.find(lambda r: r.name == '🪐', ctx.guild.roles)
    mainRole = discord.utils.find(lambda r: r.name == '🚀', ctx.guild.roles)
    allRole = discord.utils.find(lambda r: r.name == '🍿', ctx.guild.roles)


    with open("basa.json", "r") as file:
        profile = json.load(file)

    # for x in profile:
    #     id = x
    #     x = profile.get(x)
    #     ban = x['ban']
    #     warn = x['warn']
    #     report = x['report']
    #     ahelp = x['ahelp']


    # embed = discord.Embed(
    #     colour=discord.Colour(0xB03060),
    #     title='Статистика неизвестных модераторов'
    # )

    embedEcho = discord.Embed(
        colour=discord.Colour(0x00FFFF),
        title='Статистика Эхо модераторов'
    )

    embedElysium = discord.Embed(
        colour=discord.Colour(0x808080),
        title='Статистика Элизиум модераторов'
    )

    embedSolaris = discord.Embed(
        colour=discord.Colour(0xF8FF00),
        title='Статистика Солярис модераторов'
    )

    embedAthara = discord.Embed(
        colour=discord.Colour(0xC485F7),
        title='Статистика Атара модераторов'
    )

    embedNova = discord.Embed(
        colour=discord.Colour(0xFFA500),
        title='Статистика Нова модераторов'
    )

    embedMain = discord.Embed(
        colour=discord.Colour(0xFF0000),
        title='Статистика Мейн модераторов'
    )

    embedAllRole = discord.Embed(
        colour=discord.Colour(0xFFFFFF),
        title='Статистика Одиночки модератора'
    )




    guild = client.get_guild(GUILD)
    members = {}
    for x in guild.members:
        id = x.id
        name = x.name
        members[id] = {"name": '', "server": ''}

        newName = members['name'] = name

        members[id]['name'] = newName

        if echoRole in x.roles:
            newServer = members['server'] = 'echo'
            members[id]['server'] = newServer


    with open("basa.json", "r") as file:
        profile = json.load(file)

    allMembers = client.get_all_members()


    def takeStats(x, text=None):
            x = profile.get(x)

                
            ban = x['ban']
            warn = x['warn']
            report = x['report']
            
            try:
                ahelp = x['ahelp']
            except:
                ahelp = 0

            try:
                ckey = x['ckey']
            except:
                ckey = '-'

            
            if int(ban) + int(warn) + int(report) != 0:
                ban = 'Баны: ' +str(ban)
                warn = 'Варны: ' + str(warn)
                report = 'Жалобы: ' + str(report)
                ahelp = 'Ахелпы: ' + str(ahelp)
                ckey = 'Сикей: ' + str(ckey)

                li = []
                li.append(ban)
                li.append(warn)
                li.append(report)
                li.append(ahelp)
                li.append(ckey)
                text = ''

            
                for x in li:
                    text += x + '\n'




                return text
            else:
                ban = 'Баны: 0'
                warn = 'Варны: 0'
                report = 'Жалобы: 0'
                ahelp = 'Ахелпы: 0'
                ckey = 'Сикей: -'

                li = []
                li.append(ban)
                li.append(warn)
                li.append(report)
                li.append(ahelp)
                li.append(ckey)
                text = ''

            
                for x in li:
                    text += x + '\n'

                return text


            




    for x in profile:
        id = x
        for y in guild.members:
            try:
                id = int(id)
            except:
                id = 0
            if y.id == id:
                name = y.name#ubrat

                if echoRole in y.roles:
                    embedEcho.add_field(name=f'{y.name}', value=takeStats(x))
                elif solarisRole in y.roles:
                    embedSolaris.add_field(name=f'{y.name}', value=takeStats(x))
                elif novaRole in y.roles:
                    embedNova.add_field(name=f'{y.name}', value=takeStats(x))
                elif atharaRole in y.roles:
                    embedAthara.add_field(name=f'{y.name}', value=takeStats(x))
                elif elysiumRole in y.roles:
                    embedElysium.add_field(name=f'{y.name}', value=takeStats(x))
                elif allRole in y.roles:
                    embedAllRole.add_field(name=f'{y.name}', value=takeStats(x))
                elif mainRole in y.roles:
                    embedMain.add_field(name=f'{y.name}', value=takeStats(x))


                    
    return embedEcho, embedSolaris, embedNova, embedAthara, embedElysium, embedAllRole, embedMain
            


            
