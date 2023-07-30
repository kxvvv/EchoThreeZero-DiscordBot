import discord
import gspread
import asyncio
import json
#import httplib2 
#import apiclient.discovery

#from apiclient import discovery

#from oauth2client.service_account import ServiceAccountCredentials


from discord.ext import commands
from discord.utils import get
from config import *

from discord import app_commands


intents = discord.Intents.all()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)



gc = gspread.service_account(filename='secretkey.json')
sh = gc.open("копия 2.0")
worksheet = sh.sheet1


########################


# user = 'bbbaka'

# cell = worksheet.find(user)
# row = cell.row
# col = cell.col


########################





########################


@client.event
async def on_ready():
    print(f"Я СНОВА ЖИВУ - {client.user}")
    await client.tree.sync(guild=discord.Object(id=GUILD)) # синхорнизация
    await client.change_presence(status=discord.Status.online, activity = discord.Activity(name = f'на всех свысока.', type = discord.ActivityType.watching))


# @client.listen("on_command_error")
# async def cooldown_message(error):
#     errorlog = client.get_channel(ERROR_ROOM) # чат
#     await errorlog.send(f"```\n\n\n\n\n\n_error_\n\n{error}```")



# @client.command()
# async def qwe(ctx, member: discord.Member = None):
#     if member == None:
#         member = ctx.author
#     print(member)
#     print(type(member))
#     embed = discord.Embed(title = member).set_image(url=member.avatar.url)
#     await ctx.send(embed=embed)



async def get_user_profile(user_id):
    user_id = str(user_id)

    with open("basa.json", "r") as file:
        profile = json.load(file)

    if user_id not in profile.keys():
        profile[user_id] = PROFILE_DEFAULT
    
        logs = client.get_channel(LOGS)
        await logs.send(f'❗ <@{user_id}> создаёт себе БД.')

    with open("basa.json", "w") as file:
        json.dump(profile, file)

    return profile[user_id]

async def set_user_profile(user_id, parameter, new_value):
    user_id = str(user_id)

    with open("basa.json", "r") as file:
        profile = json.load(file)

    if user_id not in profile.keys():
        profile[user_id] = PROFILE_DEFAULT

        logs = client.get_channel(LOGS)
        await logs.send(f'❗ <@{user_id}> создаёт себе БД, и записывает туда данные.')

    profile[user_id][parameter] = new_value

    with open("basa.json", "w") as file:
        json.dump(profile, file)


@client.tree.command(name = "addreport", description= 'выдать жалобу, указывать нужно айди', guild=discord.Object(id=GUILD))
async def report(ctx, user: str=None):


    #вавден
    echoRole = discord.utils.find(lambda r: r.name == 'вавден', ctx.guild.roles)
    if echoRole not in ctx.user.roles:
        await ctx.response.send_message('❌ У Вас нет доступа к данной команде.')
        return

    if user == None:
        await ctx.response.send_message('❌ Не указан модератор.')
        return

    profile = await get_user_profile(user)
    user_id = user
    new_value = profile['report'] + 1
    parameter = 'report'
    await set_user_profile(user_id, parameter, new_value)

    logs = client.get_channel(LOGS)
    await logs.send(f'⏰ {ctx.user} записал <@{user}> новую жалобу')
    await ctx.response.send_message('✅ Успешно выдано.')


@client.tree.command(name = "profile", description = 'твой профиль', guild=discord.Object(id=GUILD))
async def profile(ctx):

    member = ctx.user

    def checkRole():
        echoRole = discord.utils.find(lambda r: r.name == '☄️', ctx.guild.roles)
        if echoRole in ctx.user.roles:
            return discord.Colour.blue()
        else:
            return discord.Colour.red()
        
    def checkFooter():
        echoRole = discord.utils.find(lambda r: r.name == '☄️', ctx.guild.roles)
        if echoRole in ctx.user.roles:
            return f'{ctx.user.id}, echo'
        else:
            return f'{ctx.user.id}, ???'

    await ctx.response.defer()
    profile = await get_user_profile(ctx.user.id)


    embed = discord.Embed(
        colour=checkRole(), 
        #description="Твой профиль.", 
        title=ctx.user
    )
    #embed.set_author(name=user, url="https://docs.google.com/spreadsheets/d/1R9kxpwp9PopkUoiF2DXTVphvwLDepJ0gkwDV8a2_8tQ/edit?pli=1#gid=0")


    embed.add_field(name="⚠️ Варны", value=f'{profile["warn"]}')
    embed.add_field(name="⛔ Баны", value=f'{profile["ban"]}')
    embed.add_field(name="⏰ Жалобы", value=f'{profile["report"]}')
    
    
    #embed.set_image(url=member.avatar.url)
    embed.set_thumbnail(url=member.avatar.url)

    embed.set_footer(text=checkFooter())


    #await asyncio.sleep(3)
    await ctx.followup.send(embed=embed)


@client.tree.command(name = "check", description = "поиск игрока в таблице", guild=discord.Object(id=GUILD))
async def first_command(ctx, user: str = None):




    if user == None:
        await ctx.response.send_message(f"❌ Не введены аргументы.")
        return

    
    values_list = worksheet.col_values(2)


    user.strip()

    if user in values_list:
        user = f'{user}'
    elif (f'{user} ' in values_list):
        user = f'{user} '
    elif (f'{user}  ' in values_list):
        user = f'{user}  '
    else:
        await ctx.response.send_message(f"❌ Игрок `{user}` не найден, проверяйте регистр.")
        return

    
    await ctx.response.defer()

    
    cell = worksheet.find(user)
    
    row = cell.row
    col = cell.col

        
    def warnCheck():

        ruleNumbers = worksheet.get_values(f'C{row}:C{row+20}')

        if ruleNumbers[0] == ['']:
            return 0
        li = []
        warnCount = 0
        for x in ruleNumbers:
            if x not in li:
                li.append(x)
            else:
                break
        for x in li:
            if x != ['']:               
                warnCount += 1

        return warnCount
    

    def banCheck():
        
        ruleNumbersSecond = worksheet.get_values(f'F{row}:F{row+20}')

        if ruleNumbersSecond[0] == ['']:
            return 0
        li2 = []
        banCount = 0
        for x in ruleNumbersSecond:
            if x not in li2:
                li2.append(x)
            else:
                break
        for x in li2:
            if x != ['']:               
                banCount += 1

        return banCount
        

    def testCheck(row):
        fin = sh.sheet1.get(f'H{str(row)}')
        if fin == []:
            return '-'
        
        fin = fin[0]
        fin = str(fin[0])
        if fin == 'Да':
            return 'Прошёл.'
        elif fin == 'Нет':
            return 'Не прошёл.'
        else:
            return fin

    def colorStatus():
        colour=discord.Colour.dark_gold()
        return colour


    embed = discord.Embed(
        colour=colorStatus(),
        #description="Информация с таблицы", 
        title=u"Информация с таблицы"
    )
    embed.set_author(name=user)


    embed.add_field(name="⚠️ Варны", value=warnCheck())
    embed.insert_field_at(1,name="⛔ Баны", value=banCheck())
    embed.add_field(name="📃 Тест", value=testCheck(row))


    embed.set_footer(text=f'Строка {row}, столбик {col}')


    await asyncio.sleep(3)
    await ctx.followup.send(embed=embed)


    
@client.tree.command(name = "new", description = "запись наказания", guild=discord.Object(id=GUILD))
@app_commands.choices(punish=[
    discord.app_commands.Choice(name='warn', value=1),
    discord.app_commands.Choice(name='ban', value=2),
])
async def second_command(ctx, user: str=None, punish: app_commands.Choice[int]=0, rule: str=None, reason: str='None'):


    # 📝
    access = discord.utils.find(lambda r: r.name == '📝', ctx.guild.roles)
    if access not in ctx.user.roles:
        await ctx.response.send_message('❌ У Вас нет доступа к данной команде.')
        return

    values_list = worksheet.col_values(2)



    def newPlayer():
        lastdude = values_list[-1]

        cell = worksheet.find(lastdude)
        row = cell.row
        row += 1


        worksheet.update(f'B{row}', user)
        if punish.value == 1:
            worksheet.update(f'C{row}', '1')
            worksheet.update(f'D{row}', str(f'Правило {rule}'))
            worksheet.insert_note(f'D{row}', f'{reason}')

        if punish.value == 2:
            worksheet.update(f'F{row}', '1')
            worksheet.update(f'G{row}', str(f'Правило {rule}'))
            worksheet.insert_note(f'G{row}', f'{reason}')

        print('govno')


    
    def oldPlayer():

        cell = worksheet.find(user)
        row = cell.row
        col = cell.col



        def warnCountSystem():

            if ruleNumbers[0] == ['']:
                return 0
            li = []
            warnCount = 0
            for x in ruleNumbers:
                if x not in li:
                    li.append(x)
                else:
                    break
            for x in li:
                if x != ['']:               
                    warnCount += 1

            return warnCount


        def banCountSystem():
            if ruleNumbersSecond[0] == ['']:
                return 0
            li2 = []
            banCount = 0
            for x in ruleNumbersSecond:
                if x not in li2:
                    li2.append(x)
                else:
                    break
            for x in li2:
                if x != ['']:               
                    banCount += 1

            return banCount

        ruleNumbers = worksheet.get_values(f'C{row}:C{row+20}')
        ruleNumbersSecond = worksheet.get_values(f'F{row}:F{row+20}')

        try:
            warnCount = warnCountSystem()
        except:
            warnCount = 0
        try:
            banCount = banCountSystem()
        except:
            banCount = 0

        warnCount = int(warnCount)
        banCount = int(banCount)

        mainCount = max(banCount, warnCount)



        def addField(count):
            worksheet.insert_row(['', '', '', '', '', '', ''], index=row+count) #count+1
            worksheet.merge_cells(f'B{row}:B{row+count}', 'MERGE_ALL')

        cell = worksheet.find(user)
        row = cell.row
        if punish.value == 1:
            warnNullOrNot = worksheet.get_values(f'D{row}:D{row+20}')
            
            #print(warnNullOrNot[0])
            needToAdd = 0

            try:
                if warnNullOrNot[0] != ['']:
                    for x in warnNullOrNot:
                        if x == ['']:
                            break
                        needToAdd += 1
            except:
                warnNullOrNot = 0
                needToAdd = 0
            if warnCount > needToAdd:
                worksheet.update(f'D{row+needToAdd}', str(f'Правило {rule}'))
                worksheet.insert_note(f'D{row+needToAdd}', f'{reason}')

            elif warnCount < needToAdd:
                print('he4re')
                addField(warnCount)
                worksheet.update(f'C{row+warnCount}', str(f'{warnCount+1}')) # testt
                worksheet.update(f'D{row+warnCount}', str(f'Правило {rule}'))
                worksheet.insert_note(f'D{row+warnCount}', f'{reason}')

            elif warnCount == needToAdd:
                if warnCount == 0 and needToAdd == 0:
                    worksheet.update(f'C{row+needToAdd}', str(f'1'))
                    worksheet.update(f'D{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'D{row+needToAdd}', f'{reason}')
                elif warnCount < mainCount:
                    worksheet.update(f'C{row+needToAdd}', str(f'{warnCount+1}'))
                    worksheet.update(f'D{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'D{row+needToAdd}', f'{reason}')
                else:
                    addField(warnCount)
                    print('he1re')
                    worksheet.update(f'C{row+warnCount}', str(f'{warnCount+1}')) # testt
                    worksheet.update(f'D{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'D{row+needToAdd}', f'{reason}')
            
            else:
                print('это ПИЗДец')


            
        if punish.value == 2:
            banNullOrNot = worksheet.get_values(f'G{row}:G{row+20}')
            
            needToAdd = 0
            if banNullOrNot[0] != ['']:
                for x in banNullOrNot:
                    if x == ['']:
                        break
                    needToAdd += 1
            if banCount > needToAdd:
                worksheet.update(f'G{row+needToAdd}', str(f'Правило {rule}'))
                worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')

            elif banCount < needToAdd:
                addField(banCount)
                worksheet.update(f'F{row+banCount}', str(f'{banCount+1}')) # test
                worksheet.update(f'G{row+banCount}', str(f'Правило {rule}'))
                worksheet.insert_note(f'G{row+banCount}', f'{reason}')

            elif banCount == needToAdd:
                if banCount == 0 and needToAdd == 0:
                    worksheet.update(f'F{row+needToAdd}', str(f'1'))
                    worksheet.update(f'G{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                elif banCount < mainCount:
                    worksheet.update(f'F{row+needToAdd}', str(f'{banCount+1}'))
                    worksheet.update(f'G{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                else:
                    addField(banCount)
                    worksheet.update(f'F{row+banCount}', str(f'{banCount+1}')) # test
                    worksheet.update(f'G{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
            
            else:
                print('это ПИЗДец')



    async def nextStep(choose):
        infochat = ctx.channel_id # чат
        infochat = client.get_channel(infochat)
        trueUser = ctx.user



        msg = await infochat.send('🔄 секу..')
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
        await msg.edit(content=f' \n\nНаказание:  {punishEmoji}\n\nПравило: **{rule}**\n\nПричина: ```{reason}```')

        def check(reaction, msgAuthor):
            if trueUser == msgAuthor:
                return msgAuthor == ctx.user and str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌'
        try:
            reaction, msgAuthor = await client.wait_for('reaction_add', timeout=25.0, check=check)
        except asyncio.TimeoutError:
            await msg.edit(content='❌ Чета случилась ошибочка. либо **реакция не правильная**, либо **время вышло.**')
        else:
            if reaction.emoji == '❌':
                await msg.edit(content='❌ Отменил операцию.')
                return
            elif reaction.emoji == '✅':
                await msg.edit(content=f'**🔄 Обрабатываю запросик :middle_finger:**') #{reaction.emoji}
            else:
                await msg.edit(content='❌ чета случилась ошибочка. либо **реакция не правильная**, либо **время вышло.**')

            logs = client.get_channel(LOGS)

            try:
                cell = worksheet.find(user)
                row = cell.row
                col = cell.col
            except AttributeError:
                row = '-'
                col = '-'


            member = msgAuthor

            def checkRole():
                echoRole = discord.utils.find(lambda r: r.name == '☄️', ctx.guild.roles)
                if echoRole in ctx.user.roles:
                    return discord.Colour.blue()
                else:
                    return discord.Colour.red()
                
            def checkFooter():
                echoRole = discord.utils.find(lambda r: r.name == '☄️', ctx.guild.roles)
                if echoRole in ctx.user.roles:
                    return f'{ctx.user.id}, echo'
                else:
                    return f'{ctx.user.id}, ???'


            embed = discord.Embed(
                colour=checkRole(), 
                description=reason, 
                title=f'Выдал новый {punish.name} {punishEmoji}'
            )
            embed.set_author(name=ctx.user)

            embed.add_field(name="Игрок", value=user)
            embed.add_field(name="Правило", value=rule)

            embed.set_thumbnail(url=member.avatar.url)

            embed.set_footer(text=f'{checkFooter()}, {row}')


            await logs.send(embed=embed)
            emoji = (reaction.emoji)
            emoji = str(emoji)
            if reaction.emoji == '✅':                
                try:
                    match choose:
                        case 'new':
                            newPlayer()
                        case 'old':
                            oldPlayer()
                    await msg.edit(content='✅ Успешно обновил данные игрока.')
                    if punish.value == 1:
                        profile = await get_user_profile(ctx.user.id)
                        user_id = ctx.user.id
                        new_value = profile['warn'] + 1
                        parameter = 'warn'
                        await set_user_profile(user_id, parameter, new_value)
                        
                        logs = client.get_channel(LOGS)
                        await logs.send(f'⚠️ {ctx.user} записал себе варнчик')
                    elif punish.value == 2:
                        profile = await get_user_profile(ctx.user.id)
                        user_id = ctx.user.id
                        new_value = profile['ban'] + 1
                        parameter = 'ban'
                        await set_user_profile(user_id, parameter, new_value)

                        logs = client.get_channel(LOGS)
                        await logs.send(f'⛔ {ctx.user} записал себе банчик')
                    else:
                        logs = client.get_channel(LOGS)
                        await logs.send(f'❓ {ctx.user} что то сделал, и я должен был чёта записать... похуй)')
                except:
                    await msg.edit(content='❌ Произошла техническая ошибка, пингуй идиота ксова.')
            if reaction.emoji == '❌':
                return
        








    if user == None:
        await ctx.response.send_message('❌ Не выбран игрок.')
        return
    
    try:
        if punish.value == 0:
            await ctx.response.send_message('❌ Не выбрано наказание.')
            return
    except AttributeError:
        await ctx.response.send_message('❌ Не выбрано наказание.')
        return
    

    if punish.name == 'warn':
        punishEmoji = '⚠️'
    elif punish.name == 'ban':
        punishEmoji = '⛔'
    else:
        punishEmoji = '❓'

    try:
        if int(rule) not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            await ctx.response.send_message('❌ Не корекктно выбрано правило, используй **только одну цифру.**')
            return
    except:
        await ctx.response.send_message('❌ Не корекктно выбрано правило, **используй цифры.**')
        return



    values_list = worksheet.col_values(2)

    if user in values_list:
        user = f'{user}'
        await ctx.response.send_message(f"✅ Игрок `{user}` уже есть в табличке.")
        await nextStep('old')
    elif (f'{user} ' in values_list):
        user = f'{user} '
        await ctx.response.send_message(f"✅ Игрок `{user}` уже есть в табличке.")
        await nextStep('old')
    elif (f'{user}  ' in values_list):
        user = f'{user}  '
        await ctx.response.send_message(f"✅ Игрок `{user}` уже есть в табличке.")
        await nextStep('old')
    else:
        await ctx.response.send_message(f"⚠️ Игрок `{user}` не найден.")
        await nextStep('new')

















        
        
                   ##### ######   
                  ##############   
                  ##############   
                  ##############   
                  ######а#######   
                  ######ш#######   
                  ######а#######    
                  ##############
                  ######т#######
                  ######и#######
                  ######р#######
                  ######с#######
                  ##############                    
                  ##############
        ##############      ##############
        ##############      ##############
        ##############      ##############
################################################################################################
client.run(token=TOKEN)
################################################################################################