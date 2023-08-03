import discord
import gspread
import asyncio
import json
import random


from discord.ext import commands
from discord.utils import get
from config import *

from discord import app_commands


intents = discord.Intents.all()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)



# gc = gspread.service_account(filename='secretkey.json')
# sh = gc.open("копия 2.0")
# worksheet = sh.sheet1


########################



########################



########################


@client.event
async def on_ready():
    print(f"Здарова ёпт✌️, это я - {client.user}")
    await client.tree.sync(guild=discord.Object(id=GUILD)) # синхорнизация
    await client.change_presence(status=discord.Status.online, activity = discord.Activity(name = f'на всех свысока.', type = discord.ActivityType.watching))


@client.listen("on_command_error")
async def cooldown_message(ctx, error):
    errorlog = client.get_channel(ERROR_ROOM) # чат
    await errorlog.send(f"```\n\n\n\n\n\n_error_\n\n{error}```")


# @client.command()
# async def qwe(ctx):
#     guild = client.get_guild(GUILD)
#     for guild in client.guilds:
#         for member in guild.members:
#             print(member)


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



def joinToSheet():
    gc = gspread.service_account(filename='secretkey.json') #test
    sh = gc.open("Коквакс новая таблица банов 2.0") #test
    worksheet = sh.sheet1
    return gc, sh, worksheet


async def whatColorYouNeed(row, UserWarnBan='None'):

    if UserWarnBan == 'None':
        return 'None'

    whatColor = 'whatColor'
    whatColor += UserWarnBan

    gc, sh, worksheet = joinToSheet()

    worksheet.format(f'A{row}', {'textFormat': {'foregroundColor': {'red': 255/255, 'green': 255/255, 'blue': 255/255}}})
    worksheet.update(f'A{row}', whatColor)

    await asyncio.sleep(3)

    thisColor = worksheet.get(f'A{row}')
    worksheet.update(f'A{row}', '')

    return thisColor

async def getProfileFromSheet(user, warnCheck, banCheck, testCheck, row, col, worksheet, UserWarnBan):

    async def colorStatus():
        thisColor = await whatColorYouNeed(row=row, UserWarnBan='User')
        thisColor = thisColor[0]
        thisColor = thisColor[0]
        color = thisColor

        h = color.lstrip('#')

        rgb = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

        colour=discord.Colour.from_rgb(rgb[0], rgb[1], rgb[2])

        return colour


    embed = discord.Embed(
        colour=await colorStatus(),
        #description="Информация с таблицы", 
        title=u"Информация с таблицы"
    )
    embed.set_author(name=user)




    warnNullOrNot = worksheet.get_values(f'D{row}:D{row+50}')
    banNullOrNot = worksheet.get_values(f'G{row}:G{row+50}')
    listWarn = ''
    listBan = ''

    warnCount = warnCheck
    for x in warnNullOrNot:
        if warnCount == 0:
            break
        if x == ['']:
            break
        listWarn += f"{x[0]}\n"
        warnCount -= 1

    banCount = banCheck
    for x in banNullOrNot:
        if banCount == 0:
            break
        if x == ['']:
            break
        listBan += f"{x[0]}\n"
        banCount -= 1


    if listWarn == '':
        listWarn = '-'
    if listBan == '':
        listBan = '-'

    embed.add_field(name="⚠️ Варны", value=warnCheck)
    embed.insert_field_at(1,name="⛔ Баны", value=banCheck)
    embed.add_field(name="📃 Тест", value=testCheck)
    embed.add_field(name='список варнов', value=listWarn)
    embed.add_field(name='список банов', value=listBan)


    embed.set_footer(text=f'Строка {row}, столбик {col}')

    return embed



def checkForWarn(row, worksheet):

    ruleNumbers = worksheet.get_values(f'C{row}:C{row+50}')

    try:
        if ruleNumbers[0] == ['']:
            return 0
    except:
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



def checkForBan(row, worksheet):
    
    ruleNumbersSecond = worksheet.get_values(f'F{row}:F{row+50}')

    try:
        if ruleNumbersSecond[0] == ['']:
            return 0
    except:
        return 0

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


def checkForTest(row, sh):


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
    

def checkRole(ctx, user):
    echoRole = discord.utils.find(lambda r: r.name == '☄️', ctx.guild.roles)
    elysiumRole = discord.utils.find(lambda r: r.name == '🌑', ctx.guild.roles)
    solarisRole = discord.utils.find(lambda r: r.name == '🌕', ctx.guild.roles)
    atharaRole = discord.utils.find(lambda r: r.name == '🌌', ctx.guild.roles)
    novaRole = discord.utils.find(lambda r: r.name == '🪐', ctx.guild.roles)
    mainRole = discord.utils.find(lambda r: r.name == '🚀', ctx.guild.roles)
    allRole = discord.utils.find(lambda r: r.name == '🍿', ctx.guild.roles)
    if echoRole in user.roles:
        return discord.Colour(0x00FFFF)
    elif elysiumRole in user.roles:
        return discord.Colour(0x808080)
    elif solarisRole in user.roles:
        return discord.Colour(0xF8FF00)
    elif atharaRole in user.roles:
        return discord.Colour(0xC485F7)
    elif novaRole in user.roles:
        return discord.Colour(0xFFA500)
    elif mainRole in user.roles:
        return discord.Colour(0xFF0000)
    elif allRole in user.roles:
        return discord.Colour(0xFFFFFF)
    else:
        return discord.Colour(0x000000)
    
def checkFooter(ctx, user):
    echoRole = discord.utils.find(lambda r: r.name == '☄️', ctx.guild.roles)
    elysiumRole = discord.utils.find(lambda r: r.name == '🌑', ctx.guild.roles)
    solarisRole = discord.utils.find(lambda r: r.name == '🌕', ctx.guild.roles)
    atharaRole = discord.utils.find(lambda r: r.name == '🌌', ctx.guild.roles)
    novaRole = discord.utils.find(lambda r: r.name == '🪐', ctx.guild.roles)
    mainRole = discord.utils.find(lambda r: r.name == '🚀', ctx.guild.roles)
    allRole = discord.utils.find(lambda r: r.name == '🍿', ctx.guild.roles)
    if echoRole in user.roles:
        return f'{user.id}, echo☄️'
    elif elysiumRole in user.roles:
        return f'{user.id}, elysium🌑'
    elif solarisRole in user.roles:
        return f'{user.id}, solaris🌕'
    elif atharaRole in user.roles:
        return f'{user.id}, athara🌌'
    elif novaRole in ctx.user.roles:
        return f'{user.id}, nova🪐'
    elif mainRole in user.roles:
        return f'{user.id}, main🚀'
    elif allRole in user.roles:
        return f'{user.id}, all🍿'
    else:
        return f'{user.id}, ???'
    
#await msgToLOGG(ctx, worksheet, user, msgAuthor, reason)
async def msgToLOGG(ctx, worksheet, user, msgAuthor, clrColor=None, clrColum=None, clrNumber=None, choose=None, rule=None, reason=None, isPerma=False, isColor=False):

    logs = client.get_channel(LOGS)

    try:
        cell = worksheet.find(user)
        row = cell.row
        col = cell.col
    except AttributeError:
        row = '-'
        col = '-'


    member = msgAuthor

        
    def checkForAction():
        if isPerma == True:
            return f'Записал ПЕРМУ игроку.'
        elif isColor == True:
            return f'Поменял цвет игроку'
        elif choose != None:
            return f'Обновил тест игроку.'
        elif rule != None:
            return f'Записал новое наказание.'
        


        elif reason != None:
            return f'Записал новую заметку.'
        else:
            return f'Что то сделал, но не могу зафиксировать.'
    
    def checkForReason():
        if reason == 'None':
            return 'БЕЗ ПРИЧИНЫ.'
        elif reason != None:
            return reason
        else:
            return ''
        



    embed = discord.Embed(
        colour=checkRole(ctx=ctx, user=ctx.user), 
        description=checkForReason(), 
        title=checkForAction()
    )
    embed.set_author(name=ctx.user)

    embed.add_field(name="Игрок", value=user)
    if choose != None:
        embed.add_field(name="Тест", value=choose.name)
    if rule != None:
        embed.add_field(name="Правило", value=rule)

    if clrColor != None:
        embed.add_field(name="Цвет", value=clrColor)
    if clrColum != None:
        embed.add_field(name="Столбик", value=clrColum)
    if clrNumber != None:
        embed.add_field(name="Номер", value=clrNumber)
    

    embed.set_thumbnail(url=member.avatar.url)

    embed.set_footer(text=f'{checkFooter(ctx=ctx, user=ctx.user)}, {row}')


    await logs.send(embed=embed)



@client.tree.command(name = "выдать-заметку", description= 'записывает заметку игроку в таблице', guild=discord.Object(id=GUILD))
async def note(ctx, игрок: str=None, причина: str=None):

    user = игрок
    reason = причина

    await ctx.response.defer()

    gc, sh, worksheet = joinToSheet()

    values_list = worksheet.col_values(2)

    


    if user in values_list:
        user = f'{user}'
    elif (f'{user} ' in values_list):
        user = f'{user} '
    elif (f'{user}  ' in values_list):
        user = f'{user}  '
    else:
        await ctx.response.send_message(f"❌ Игрока `{user}` нет в таблице.")
        return


    infochat = ctx.channel_id # чат
    infochat = client.get_channel(infochat)
    msg = await infochat.send(f'**🔄 поиск {user}...**')

    cell = worksheet.find(user)
    
    row = cell.row
    col = cell.col


    embed = await getProfileFromSheet(user, checkForWarn(row, worksheet), checkForBan(row, worksheet), checkForTest(row, sh), row, col, worksheet, UserWarnBan='User')
    await asyncio.sleep(3)
    await ctx.followup.send(embed=embed)



    
 

    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

    await msg.edit(content=f'**❓ Вы уверены что хотите вписать игроку следующее сообщение: ```{reason}```**')

    trueUser = ctx.user
    
    def check(reaction, msgAuthor): # trueUser = ctx.user
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
            await msgToLOGG(ctx, worksheet, user, msgAuthor, reason=reason)
            try:
                worksheet.insert_note(f'B{row}', f'{reason}')
                
                await msg.edit(content=f'**✅ Успешно вписал заметку новому игроку!**')
            except:
                await msg.edit(content='❌ Произошла техническая ошибка, пингуй идиота ксова.')
        else:
            await msg.edit(content='❌ чета случилась ошибочка. либо **реакция не правильная**, либо **время вышло.**')

@client.tree.command(name = "перма", description= 'запись пермы', guild=discord.Object(id=GUILD))
async def perma(ctx, игрок: str=None, правило: str=None, причина: str=None):

    user = игрок
    rule = правило
    reason = причина
    gc, sh, worksheet = joinToSheet()
    values_list = worksheet.col_values(2)
    playerIsNew = False

    if user in values_list:
        user = f'{user}'
    elif (f'{user} ' in values_list):
        user = f'{user} '
    elif (f'{user}  ' in values_list):
        user = f'{user}  '
    else:
        await ctx.response.send_message(f"⚠️ Игрока `{user}` нет в таблице.")
        playerIsNew = True
        

    try:
        if 'Правило' in rule or 'правило' in rule:
            await ctx.response.send_message('❌ Не корректно выбрано правило, **используй только числа.**')
            return
    except:
        await ctx.response.send_message('❌ Не корректно выбрано правило, **используй только числа.**')
        return


    if reason == None:
        await ctx.response.send_message('❌ Не выбрана причина.')
        return

    if playerIsNew == False:
        await ctx.response.defer()

    def newPlayer():
        lastdude = values_list[-1]

        cell = worksheet.find(lastdude)
        row = cell.row

        banCount = checkForBan(row, worksheet)
        warnCount = checkForWarn(row, worksheet)
        mainCount = max(banCount, warnCount)

        if mainCount != 0:
            row += mainCount
        else:
            row += 1


        def ruleFormat():
            worksheet.format(f"G{row}:G{row}", { 'backgroundColor': {
                'red':234/255,
                'green':67/255,
                'blue':53/255}})

        def playerFormat():
            worksheet.format(f"B{row}", {
                "backgroundColor": {
                "red": 255.0,
                "green": 255.0,
                "blue": 255.0
                },
                "textFormat": {
                "foregroundColor": {
                    "red": 1.0,
                    "green": 1.0,
                    "blue": 1.0
                },
                }
            })
        
        worksheet.update(f'B{row}', user)
        playerFormat()

        worksheet.update(f'F{row}', '1')
        worksheet.update(f'G{row}', str(f'PERMA: Правило {rule}'))
        ruleFormat()
        worksheet.insert_note(f'G{row}', f'{reason}')



    async def oldPlayer(embedOrWrite):

            


        cell = worksheet.find(user)
        
        row = cell.row
        col = cell.col
        banCount = checkForBan(row, worksheet)
        


        if embedOrWrite == 'embed':
            warnCount = checkForWarn(row, worksheet)
            embed = await getProfileFromSheet(user, warnCount, banCount, checkForTest(row, sh), row, col, worksheet)
            return embed

        if embedOrWrite == 'write':
            warnCount = checkForWarn(row, worksheet)
            #needToAdd = banCount
            mainCount = max(banCount, warnCount)
            def ruleFormat(count):
                worksheet.format(f"G{row+count}:G{row+count}", { 'backgroundColor': {
                    'red':234/255,
                    'green':67/255,
                    'blue':53/255}})

            def playerFormat():
                worksheet.format(f"B{row}", {
                    "backgroundColor": {
                    "red": 255.0,
                    "green": 255.0,
                    "blue": 255.0
                    },
                    "textFormat": {
                    "foregroundColor": {
                        "red": 1.0,
                        "green": 1.0,
                        "blue": 1.0
                    },
                    }
                })

            def addField(count):
                worksheet.insert_row(['', '', '', '', '', '', ''], index=row+count) #count+1
                worksheet.merge_cells(f'B{row}:B{row+count}', 'MERGE_ALL')
            
            worksheet.update(f'B{row}', user)
            playerFormat()

            banNullOrNot = worksheet.get_values(f'G{row}:G{row+50}')
            
            needToAdd = 0
            if banNullOrNot[0] != ['']:
                for x in banNullOrNot:
                    if x == ['']:
                        break
                    needToAdd += 1
            if banCount > needToAdd:
                worksheet.update(f'G{row+needToAdd}', str(f'PERMA: Правило {rule}'))
                worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                ruleFormat(needToAdd)

            elif banCount < needToAdd:
                addField(banCount)
                worksheet.update(f'F{row+banCount}', str(f'{banCount+1}')) # test
                worksheet.update(f'G{row+banCount}', str(f'PERMA: Правило {rule}'))
                worksheet.insert_note(f'G{row+banCount}', f'{reason}')
                worksheet.format(f'G{row+banCount}', {'textFormat': {'strikethrough': False}})
                ruleFormat(banCount)

            elif banCount == needToAdd:
                if banCount == 0 and needToAdd == 0:
                    worksheet.update(f'F{row+needToAdd}', str(f'1'))
                    worksheet.update(f'G{row+needToAdd}', str(f'PERMA: Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                    ruleFormat(needToAdd)
                elif banCount < mainCount:
                    worksheet.update(f'F{row+needToAdd}', str(f'{banCount+1}'))
                    worksheet.update(f'G{row+needToAdd}', str(f'PERMA: Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                    ruleFormat(needToAdd)
                else:
                    addField(banCount)
                    worksheet.update(f'F{row+banCount}', str(f'{banCount+1}')) # test
                    worksheet.update(f'G{row+needToAdd}', str(f'PERMA: Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                    ruleFormat(needToAdd)
            return

    
        





    trueUser = ctx.user

    infochat = ctx.channel_id # чат
    infochat = client.get_channel(infochat)
    
    if playerIsNew == False:
        msg = await infochat.send(f'🔄 загружаю данные о {user}...')
        embed = oldPlayer('embed')
        await asyncio.sleep(3)
        await ctx.followup.send(embed=embed)

    if playerIsNew == True:
        msg = await infochat.send(f'**🔄 ожидай...**')

    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

    
    if playerIsNew == True:
        await msg.edit(content=f'**❓ Вы уверены что хотите добавить нового игрока с причиной:** ```{reason}``` ')
    if playerIsNew == False:
        await msg.edit(content=f'**❓ Вы уверены что хотите приписать уже существующему игроку данную причину пермы:** ```{reason}```')

    trueUser = ctx.user
    
    def check(reaction, msgAuthor): # trueUser = ctx.user
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
            try:
                if playerIsNew == True:
                    newPlayer()
                    await msg.edit(content=f'**✅ Успешно вписал ПЕРМУ новому игроку!**')
                if playerIsNew == False:
                    oldPlayer('write')
                    await msg.edit(content=f'**✅ Успешно вписал ПЕРМУ старому игроку!**')
                await msgToLOGG(ctx, worksheet, user, msgAuthor, rule=rule, reason=reason, isPerma=True)
                profile = await get_user_profile(ctx.user.id)
                user_id = ctx.user.id
                new_value = profile['ban'] + 1
                parameter = 'ban'
                await set_user_profile(user_id, parameter, new_value)

                logs = client.get_channel(LOGS)
                await logs.send(f'⛔ {ctx.user} записал себе банчик')
            except:
                await msg.edit(content='❌ Произошла техническая ошибка, пингуй идиота ксова.')
        else:
            await msg.edit(content='❌ чета случилась ошибочка. либо **реакция не правильная**, либо **время вышло.**')
    

@client.tree.command(name = "выдать-тест", description= 'записывает тест игроку в таблице', guild=discord.Object(id=GUILD))
@app_commands.choices(выбор=[
    discord.app_commands.Choice(name='Прошёл', value=1),
    discord.app_commands.Choice(name='Не прошёл', value=2),
    discord.app_commands.Choice(name='Убрать', value=3),
])
async def giveTest(ctx, игрок: str=None, выбор: app_commands.Choice[int]=0):

    user = игрок
    choose = выбор

    gc, sh, worksheet = joinToSheet()

    access = discord.utils.find(lambda r: r.name == '📝', ctx.guild.roles)
    if access not in ctx.user.roles:
        await ctx.response.send_message('❌ У Вас нет доступа к данной команде.')
        return

    if user == None:
        await ctx.response.send_message(f"❌ Не указан игрок.")
        return
    
    if choose.value == 0:
        await ctx.response.send_message(f"❌ Не выбрано что записывать в строку теста.")
        return

    skipOrNot = False

    def newPlayer():
        lastdude = values_list[-1]

        cell = worksheet.find(lastdude)
        row = cell.row

        banCount = checkForBan(row, worksheet)
        warnCount = checkForWarn(row, worksheet)
        mainCount = max(banCount, warnCount)

        if mainCount != 0:
            row += mainCount
        else:
            row += 1

        def testFormat():
            worksheet.format(f"H{row}", {
                "horizontalAlignment": "CENTER",
                "textFormat": {
                "fontSize": 12,
                "bold": True
                }
            })

        worksheet.update(f'B{row}', user)
        if choose.value == 1: # прошел
            worksheet.update(f'H{row}', 'Да')
            testFormat()
        elif choose.value == 2: # не прошел
            worksheet.update(f'H{row}', 'Нет')
            testFormat()
        elif choose.value == 3: # убрать
            worksheet.update(f'H{row}', '')

    values_list = worksheet.col_values(2)

    if user in values_list:
        user = f'{user}'
    elif (f'{user} ' in values_list):
        user = f'{user} '
    elif (f'{user}  ' in values_list):
        user = f'{user}  '
    else:
        skipOrNot = True
        await ctx.response.send_message(f"⚠️ Игрока `{user}` нет в таблице.")
        infochat = ctx.channel_id # чат
        infochat = client.get_channel(infochat)
        
        msg = await infochat.send(f'**🔄 ожидай...**')
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
        await msg.edit(content='❓ Добавляем в таблицу?')

        trueUser = ctx.user
        
        def check(reaction, msgAuthor): # trueUser = ctx.user
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
                try:
                    newPlayer()
                    await msg.edit(content=f'✅ Успешно вписал тест новому игроку!')
                except:
                    await msg.edit(content='❌ Произошла техническая ошибка, пингуй идиота ксова.')
            else:
                await msg.edit(content='❌ чета случилась ошибочка. либо **реакция не правильная**, либо **время вышло.**')




    if skipOrNot == True:
        return
    await ctx.response.defer()

    cell = worksheet.find(user)
    
    row = cell.row
    col = cell.col

        
    banCount = checkForBan(row, worksheet)
    warnCount = checkForWarn(row, worksheet)
    embed = await getProfileFromSheet(user, warnCount, banCount, checkForTest(row, sh), row, col, worksheet)

    await asyncio.sleep(3)
    await ctx.followup.send(embed=embed)
    infochat = ctx.channel_id # чат
    infochat = client.get_channel(infochat)
    
    msg = await infochat.send(f'**🔄 поиск {user}...**')
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')
    await msg.edit(content='❓ Это тот самый игрок?')

    trueUser = ctx.user
    
    def check(reaction, msgAuthor): # trueUser = ctx.user
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
            return

        logs = client.get_channel(LOGS)

        try:
            cell = worksheet.find(user)
            row = cell.row
            col = cell.col
        except AttributeError:
            row = '-'
            col = '-'


        member = msgAuthor

        await msgToLOGG(ctx, worksheet, user, msgAuthor, choose=choose)

        
        def oldPlayer():
            def testFormat():
                worksheet.format(f"H{row}", {
                    "horizontalAlignment": "CENTER",
                    "textFormat": {
                    "fontSize": 12,
                    "bold": True
                    }
                })

            if choose.value == 1: # прошел
                worksheet.update(f'H{row}', 'Да')
                testFormat()
            elif choose.value == 2: # не прошел
                worksheet.update(f'H{row}', 'Нет')
                testFormat()
            elif choose.value == 3: # убрать
                worksheet.update(f'H{row}', '')


            mainCount = max(warnCount, banCount)
            
            if mainCount > 1:
                try:
                    worksheet.merge_cells(f'H{row}:H{row+mainCount}', 'MERGE_ALL')
                except:
                    pass
                


        emoji = (reaction.emoji)
        emoji = str(emoji)
        if reaction.emoji == '✅':                
            try:
                oldPlayer()
                await msg.edit(content='✅ Успешно обновил данные игрока.')
            except:
                await msg.edit(content='❌ Произошла техническая ошибка, пингуй идиота ксова.')
        if reaction.emoji == '❌':
            return


@client.tree.command(name = "сменить-цвет", description= 'смена цвета в таблице', guild=discord.Object(id=GUILD))
@app_commands.choices(цвет=[
    discord.app_commands.Choice(name='очистить', value=1),
    discord.app_commands.Choice(name='зелёный', value=2),
    discord.app_commands.Choice(name='оранжевый', value=3),
    discord.app_commands.Choice(name='красный', value=4),
    discord.app_commands.Choice(name='чёрный', value=5),
], 
столбик=[
discord.app_commands.Choice(name='игрок', value=1),
discord.app_commands.Choice(name='варн', value=2),
discord.app_commands.Choice(name='бан', value=3),
])
async def change_color(ctx, ник: str=None, столбик: app_commands.Choice[int]=0, цвет: app_commands.Choice[int]=0, номер_наказания: int=0):

    user = ник
    color = цвет
    punish = столбик
    rule_number = номер_наказания

    access = discord.utils.find(lambda r: r.name == '📝', ctx.guild.roles)
    if access not in ctx.user.roles:
        await ctx.response.send_message('❌ У Вас нет доступа к данной команде.')
        return


    if user == None:
        await ctx.response.send_message(f"❌ Не указан игрок.")
        return

    
    try:
        if color.value == 0:
            await ctx.response.send_message('❌ Не выбран цвет.')
            return
    except AttributeError:
        await ctx.response.send_message('❌ Не выбран цвет.')
        return

    try:
        if punish.value == 0:
            await ctx.response.send_message('❌ Не выбрано правило.')
            return
    except AttributeError:
        await ctx.response.send_message('❌ Не выбрано правило.')
        return





    if punish.value != 1:
        if rule_number == 0:
            await ctx.response.send_message('❌ Не выбран номер наказания.')
            return

    await ctx.response.defer()
    gc, sh, worksheet = joinToSheet()
    values_list = worksheet.col_values(2)

    if user in values_list:
        user = f'{user}'
        await ctx.followup.send(f"✅ Игрок `{user}` найден.")
    elif (f'{user} ' in values_list):
        user = f'{user} '
        await ctx.followup.send(f"✅ Игрок `{user}` найден.")
    elif (f'{user}  ' in values_list):
        user = f'{user}  '
        await ctx.followup.send(f"✅ Игрок `{user}` найден.")
    else:
        await ctx.followup.send(f"❌ Игрок `{user}` не найден, проверяйте регистр.")
        return


    
    
    infochat = ctx.channel_id # чат
    infochat = client.get_channel(infochat)
    trueUser = ctx.user

    msg = await infochat.send(f'**🔄 поиск {user}...**')
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')
    await msg.edit(content='❓ Это тот самый игрок?')



    def check(reaction, msgAuthor): # trueUser = ctx.user
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
            await msg.edit(content=f'**🔄 Крашу {user}...**')
        else:
            await msg.edit(content='❌ чета случилась ошибочка. либо **реакция не правильная**, либо **время вышло.**')
            return



    cell = worksheet.find(user)
    row = cell.row
    
    match color.value:
        case 1: # clear
            colorUserArg = 'c'
            colorEmoji = '⬜'
        case 2: # green
            colorUserArg = 'g'
            colorEmoji = '🟩'
        case 3: # orange
            colorUserArg = 'o'
            colorEmoji = '🟧'
        case 4: # red
            colorUserArg = 'r'
            colorEmoji = '🟥'
        case 5: # black
            colorUserArg = 'b'
            colorEmoji = '◼️'

    match punish.value:
        case 1: # user
            colorUserArg += 'User'
            punishWord = 'игрок'
        case 2: # warn
            colorUserArg += 'Warn'
            punishWord = 'варн'
        case 3: # ban
            colorUserArg += 'Ban'
            punishWord = 'бан'


    async def checkLenRule():
        if punish.value == 2:
            if sh.sheet1.get(f'D{str(row)}') == []:
                await msg.edit(content=f'❌ У игрока нет указного **варна.**')
                return None
            ruleCount = checkForWarn(row, worksheet)
        elif punish.value == 3:
            if sh.sheet1.get(f'G{str(row)}') == []:
                await msg.edit(content=f'❌ У игрока нет указного **бана.**')
                return None
            ruleCount = checkForBan(row, worksheet)
        if rule_number > ruleCount:
            await msg.edit(content=f'❌ Выбрана не верное число у игрока.')
            return None
        return int(rule_number)
        

    if punish.value != 1:
        if rule_number != 0:
            rowNumberToAdd = await checkLenRule()
            if rowNumberToAdd == None:
                return
            else:
                rowNumberToAdd -= 1
    else:
        rowNumberToAdd = 0



    if rowNumberToAdd == None:
        return
    else:
        def gUser():
            worksheet.format(f"B{row}", { 'backgroundColor': {
                'red':52/255,
                'green':168/255,
                'blue':83/255}})
        
        def oUser():
            worksheet.format(f"B{row}", { 'backgroundColor': {
                'red':251/255,
                'green':188/255,
                'blue':4/255}})

        def rUser():
            worksheet.format(f"B{row}", { 'backgroundColor': {
                'red':234/255,
                'green':67/255,
                'blue':53/255}})

        def bUser():
            worksheet.format(f"B{row}", {
                "backgroundColor": {
                "red": 255.0,
                "green": 255.0,
                "blue": 255.0
                },
                "textFormat": {
                "foregroundColor": {
                    "red": 1.0,
                    "green": 1.0,
                    "blue": 1.0
                },
                }
            })

        def oWarn():
            worksheet.format(f"D{row+rowNumberToAdd}", { 'backgroundColor': {
                'red':251/255,
                'green':188/255,
                'blue':4/255}})
        
        def oBan():
            worksheet.format(f"G{row+rowNumberToAdd}", { 'backgroundColor': {
                'red':251/255,
                'green':188/255,
                'blue':4/255}})
        
        def rBan():
            worksheet.format(f"G{row+rowNumberToAdd}", { 'backgroundColor': {
                'red':234/255,
                'green':67/255,
                'blue':53/255}})
        
        def cUser():
            worksheet.format(f"B{row}", {
                "backgroundColor": {
                "red": 255/255,
                "green": 255/255,
                "blue": 255/255
                },
                "textFormat": {
                "foregroundColor": {
                    "red": 0/255,
                    "green": 0/255,
                    "blue": 0/255
                },
                }
            })
        
        def cWarn():
            worksheet.format(f"D{row+rowNumberToAdd}", {
                "backgroundColor": {
                "red": 255/255,
                "green": 255/255,
                "blue": 255/255
                },
                "textFormat": {
                "foregroundColor": {
                    "red": 0/255,
                    "green": 0/255,
                    "blue": 0/255
                },
                }
            })
        
        def cBan():
            worksheet.format(f"G{row+rowNumberToAdd}", {
                "backgroundColor": {
                "red": 255/255,
                "green": 255/255,
                "blue": 255/255
                },
                "textFormat": {
                "foregroundColor": {
                    "red": 0/255,
                    "green": 0/255,
                    "blue": 0/255
                },
                }
            })

        allowed_list = ['gUser', 'oUser', 'rUser', 'bUser', 'oWarn', 'oBan', 'rBan', 'cUser', 'cWarn', 'cBan']
        if colorUserArg in allowed_list:
            if punishWord == 'игрок':
                match colorUserArg:
                    case 'gUser':
                        gUser()
                    case 'oUser':
                        oUser()
                    case 'rUser':
                        rUser()
                    case 'bUser':
                        bUser()
                    case 'cUser':
                        cUser()
                await msg.edit(content=f'✅ **Игрок покрашен в {colorEmoji}!**')
            elif punishWord == 'варн':
                match colorUserArg:
                    case 'oWarn':
                        oWarn()
                    case 'cWarn':
                        cWarn()
                await msg.edit(content=f'✅ **Варн #{rule_number} покрашен в {colorEmoji}!**')
            elif punishWord == 'бан':
                match colorUserArg:
                    case 'oBan':
                        oBan()
                    case 'rBan':
                        rBan()
                    case 'cBan':
                        cBan()
                await msg.edit(content=f'✅ **Бан #{rule_number} покрашен в {colorEmoji}!**')
            await msgToLOGG(ctx, worksheet, user, msgAuthor, clrColor=colorEmoji, clrColum=punishWord, clrNumber=rule_number, isColor=True)
        else:
            await msg.edit(content=f'❌ В такой цвет - {colorEmoji}, {punishWord} красить нельзя.')





@client.tree.command(name = "выдать-жалобу", description= 'выдает жалобу в статистику модератору, указывать нужно айди в дискорде', guild=discord.Object(id=GUILD))
async def report(ctx, user: str=None):


    #вавден
    echoRole = discord.utils.find(lambda r: r.name == '✌️', ctx.guild.roles)
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




@client.tree.command(name = "профиль", description = 'твой профиль', guild=discord.Object(id=GUILD))
async def profile(ctx, модератор: discord.Member = None):

    user = модератор
    if user == None:
        user = ctx.user
    

    await ctx.response.defer()
    profile = await get_user_profile(user.id)


    embed = discord.Embed(
        colour=checkRole(ctx=ctx, user=user), 
        #description="Твой профиль.", 
        title=user
    )
    #embed.set_author(name=user, url="https://docs.google.com/spreadsheets/d/1R9kxpwp9PopkUoiF2DXTVphvwLDepJ0gkwDV8a2_8tQ/edit?pli=1#gid=0")


    embed.add_field(name="⚠️ Варны", value=f'{profile["warn"]}')
    embed.add_field(name="⛔ Баны", value=f'{profile["ban"]}')
    embed.add_field(name="⏰ Жалобы", value=f'{profile["report"]}')
    
    
    #embed.set_image(url=member.avatar.url)
    embed.set_thumbnail(url=user.avatar.url)

    embed.set_footer(text=checkFooter(ctx=ctx, user=user))


    #await asyncio.sleep(3)
    await ctx.followup.send(embed=embed)




@client.tree.command(name = "поиск", description = "поиск игрока в таблице", guild=discord.Object(id=GUILD))
async def first_command(ctx, игрок: str = None):

    user = игрок

    gc, sh, worksheet = joinToSheet()


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

    
    await ctx.response.defer() # ephemeral=True

    
    cell = worksheet.find(user)
    
    row = cell.row
    col = cell.col


    embed = await getProfileFromSheet(user, checkForWarn(row, worksheet), checkForBan(row, worksheet), checkForTest(row, sh), row, col, worksheet, UserWarnBan='User')

    await asyncio.sleep(3)
    await ctx.followup.send(embed=embed)


    
@client.tree.command(name = "выдать-наказание", description = "записывает наказание игроку в таблице", guild=discord.Object(id=GUILD))
@app_commands.choices(наказание=[
    discord.app_commands.Choice(name='варн', value=1),
    discord.app_commands.Choice(name='бан', value=2),
])
async def second_command(ctx, ник: str=None, наказание: app_commands.Choice[int]=0, правило: str=None, причина: str='None'):

    user = ник
    punish = наказание
    rule = правило
    reason = причина

    gc, sh, worksheet = joinToSheet()

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
        
        banCount = checkForBan(row, worksheet)
        warnCount = checkForWarn(row, worksheet)
        mainCount = max(banCount, warnCount)

        if mainCount != 0:
            row += mainCount
        else:
            row += 1

        worksheet.update(f'B{row}', user)
        if punish.value == 1:
            worksheet.update(f'C{row}', '1')
            worksheet.update(f'D{row}', str(f'Правило {rule}'))
            worksheet.insert_note(f'D{row}', f'{reason}')
            worksheet.format(f'D{row}', {'textFormat': {'strikethrough': False}})

        if punish.value == 2:
            worksheet.update(f'F{row}', '1')
            worksheet.update(f'G{row}', str(f'Правило {rule}'))
            worksheet.insert_note(f'G{row}', f'{reason}')
            worksheet.format(f'G{row}', {'textFormat': {'strikethrough': False}})


    
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

        ruleNumbers = worksheet.get_values(f'C{row}:C{row+50}')
        ruleNumbersSecond = worksheet.get_values(f'F{row}:F{row+50}')

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
            warnNullOrNot = worksheet.get_values(f'D{row}:D{row+50}')
            
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
                worksheet.format(f'D{row+needToAdd}', {'textFormat': {'strikethrough': False}})

            elif warnCount < needToAdd:
                addField(warnCount)
                worksheet.update(f'C{row+warnCount}', str(f'{warnCount+1}')) # testt
                worksheet.update(f'D{row+warnCount}', str(f'Правило {rule}'))
                worksheet.insert_note(f'D{row+warnCount}', f'{reason}')
                worksheet.format(f'D{row+warnCount}', {'textFormat': {'strikethrough': False}})

            elif warnCount == needToAdd:
                if warnCount == 0 and needToAdd == 0:
                    worksheet.update(f'C{row+needToAdd}', str(f'1'))
                    worksheet.update(f'D{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'D{row+needToAdd}', f'{reason}')
                    worksheet.format(f'D{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                elif warnCount < mainCount:
                    worksheet.update(f'C{row+needToAdd}', str(f'{warnCount+1}'))
                    worksheet.update(f'D{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'D{row+needToAdd}', f'{reason}')
                    worksheet.format(f'D{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                else:
                    addField(warnCount)
                    worksheet.update(f'C{row+warnCount}', str(f'{warnCount+1}')) # testt
                    worksheet.update(f'D{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'D{row+needToAdd}', f'{reason}')
                    worksheet.format(f'D{row+needToAdd}', {'textFormat': {'strikethrough': False}})
            
            else:
                print('это ПИЗДец')


            
        if punish.value == 2:
            banNullOrNot = worksheet.get_values(f'G{row}:G{row+50}')
            
            needToAdd = 0
            try:
                if banNullOrNot[0] != ['']:
                    for x in banNullOrNot:
                        if x == ['']:
                            break
                        needToAdd += 1
            except:
                needToAdd = 0
            if banCount > needToAdd:
                worksheet.update(f'G{row+needToAdd}', str(f'Правило {rule}'))
                worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})

            elif banCount < needToAdd:
                addField(banCount)
                worksheet.update(f'F{row+banCount}', str(f'{banCount+1}')) # test
                worksheet.update(f'G{row+banCount}', str(f'Правило {rule}'))
                worksheet.insert_note(f'G{row+banCount}', f'{reason}')
                worksheet.format(f'G{row+banCount}', {'textFormat': {'strikethrough': False}})

            elif banCount == needToAdd:
                if banCount == 0 and needToAdd == 0:
                    worksheet.update(f'F{row+needToAdd}', str(f'1'))
                    worksheet.update(f'G{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                elif banCount < mainCount:
                    worksheet.update(f'F{row+needToAdd}', str(f'{banCount+1}'))
                    worksheet.update(f'G{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                else:
                    addField(banCount)
                    worksheet.update(f'F{row+banCount}', str(f'{banCount+1}')) # test
                    worksheet.update(f'G{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})



    async def nextStep(choose):
        match choose:
            case 'old':
                cell = worksheet.find(user)
                row = cell.row
                col = cell.col

                infochat = ctx.channel_id # чат
                infochat = client.get_channel(infochat)
                msg = await infochat.send(f'🔄 загружаю данные о {user}..')
                embed = await getProfileFromSheet(user, checkForWarn(row, worksheet), checkForBan(row, worksheet), checkForTest(row, sh), row, col, worksheet, UserWarnBan='User')
                await asyncio.sleep(3)
                await ctx.followup.send(embed=embed)
            case 'new':
                infochat = ctx.channel_id # чат
                infochat = client.get_channel(infochat)
                msg = await infochat.send(f'🔄 ожидай..')
        trueUser = ctx.user



        
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
        await msg.edit(content=f' \n\nНаказание:  {punishEmoji}\n\nПравило: **{rule}**\n\nПричина: ```{reason}```')

        def check(reaction, msgAuthor): # trueUser = ctx.user
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

            await msgToLOGG(ctx, worksheet, user, msgAuthor, rule=rule, reason=reason)
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
    

    if punish.value == 1:
        punishEmoji = '⚠️'
    elif punish.value == 2:
        punishEmoji = '⛔'
    else:
        punishEmoji = '❓'
    


    try:
        if 'Правило' in rule or 'правило' in rule:
            await ctx.response.send_message('❌ Не корректно выбрано правило, **используй только числа.**')
            return
    except:
        await ctx.response.send_message('❌ Не корректно выбрано правило, **используй только числа.**')
        return



    values_list = worksheet.col_values(2)

    if user in values_list:
        user = f'{user}'
        await ctx.response.defer()
        await nextStep('old')
    elif (f'{user} ' in values_list):
        await ctx.response.defer()
        user = f'{user} '
        await nextStep('old')
    elif (f'{user}  ' in values_list):
        await ctx.response.defer()
        user = f'{user}  '
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