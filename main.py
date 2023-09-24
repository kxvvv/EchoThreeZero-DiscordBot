import discord
import gspread
import asyncio
import json
import random
import gspread_formatting as gf
import logging
import sys

from gspread_formatting import *
from stats import *
from whatColorYouNeed import *
from commandChannel import *
from datetime import datetime as dt

from discord.ext import commands
from discord.utils import get
from config import *

from discord import app_commands


# logging.basicConfig(
#     filename='file.log', 
#     filemode='w', 
#     format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'
# )

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('loginfo.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


logging.info('restart')

# gc = gspread.service_account(filename='secretkey.json')
# sh = gc.open("копия 2.0")
# worksheet = sh.sheet1


########################



########################



########################


@client.event
async def on_ready():
    logging.info(f"запустился как {client.user}")
    await client.tree.sync(guild=discord.Object(id=GUILD)) # синхорнизация
    await client.change_presence(status=discord.Status.online, activity = discord.Activity(name = f'на всех свысока.', type = discord.ActivityType.watching))
    # try:
    #     ctx = client.get_channel(1139276548650848266)
    #     await ctx.send('Я только что обновился.<:catSitting:1089452185122775200>')
    # except:
    #     print('error ctx.send')
    #     pass



    #await cycle('')





async def get_user_profile(user_id):
    user_id = str(user_id)

    with open("basa.json", "r") as file:
        profile = json.load(file)

    if user_id not in profile.keys():
        profile[user_id] = PROFILE_DEFAULT
    
        logs = client.get_channel(ERROR_ROOM)
        await logs.send(f'❗ <@{user_id}> создаёт себе БД.')

    with open("basa.json", "w") as file:
        json.dump(profile, file)

    return profile[user_id]

async def set_user_profile(user_id, parameter, new_value, ckey=False):


    user_id = str(user_id)

    with open("basa.json", "r") as file:
        profile = json.load(file)

    if user_id not in profile.keys():
        profile[user_id] = PROFILE_DEFAULT

        logs = client.get_channel(ERROR_ROOM)
        await logs.send(f'❗ <@{user_id}> создаёт себе БД, и записывает туда данные.')

    if ckey == True:
        profile[user_id].setdefault('ckey', new_value)
        profile[user_id][parameter] = new_value
    else:
        profile[user_id][parameter] = new_value

    with open("basa.json", "w") as file:
        json.dump(profile, file)



def joinToSheet():
    gc = gspread.service_account(filename='secretkey.json')
    sh = gc.open(SHEET)
    worksheet = sh.sheet1
    return gc, sh, worksheet


async def getProfileFromSheet(user, warnCheck, banCheck, testCheck, row, col, worksheet, UserWarnBan='User'):

    async def colorStatus():
        rgb = await whatColorYouNeed(row=row, UserWarnBan='User')

        colour=discord.Colour.from_rgb(rgb[0], rgb[1], rgb[2])
        return colour








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
        warnCheck = 0
    if listBan == '':
        listBan = '-'
        banCheck = 0

    textForEmbedDesc = f'''

*Нажмите на ник, что-бы перейти в таблицу.*

⚠️ Варны: **{warnCheck}**

⛔ Баны: **{banCheck}**

📃 Тест: **{testCheck}**


''' 



    embed = discord.Embed(
        colour=await colorStatus(),
        description=textForEmbedDesc, 
        #title=f"Информация о"
    )
    embed.set_author(name=user, url=LINK+str(row))


    #embed.add_field(name="⚠️ Варны", value=warnCheck)
    #embed.insert_field_at(1,name="⛔ Баны", value=banCheck)

    #embed.add_field(name="📃 Тест", value=testCheck)
    embed.add_field(name='список варнов', value=listWarn)
    embed.add_field(name=' ', value=' ')
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
    

@client.tree.command(name = 'мой-сикей', description='установить сикей из игры, для подсчета ахелпов в течении месяца.', guild=discord.Object(id=GUILD))
async def ckey(ctx, ckey: str=None):


    access = await checkForModeratorRole(ctx)
    if access == False:
        return


    user = ctx.user.id

    if ckey == None:
        await ctx.response.send_message('❌ Не указан ckey.', ephemeral=True)
        return



    profile = await get_user_profile(user)





    user_id = ctx.user.id
    new_value = ckey
    parameter = 'ckey'
    await set_user_profile(user_id, parameter, new_value, ckey=True)

    logs = client.get_channel(ERROR_ROOM)
    await logs.send(f'👤 {ctx.user} установил себе новый ckey - `{ckey}`')
    await ctx.response.send_message(f'✅ Успешно установлен сикей -  `{ckey}`.', ephemeral=True)

@client.tree.command(name = "помощь", description= 'подробное описание всех команд в боте', guild=discord.Object(id=GUILD))
async def perma(ctx):
        
        embed = discord.Embed(
            colour=discord.Colour.dark_purple(),
            #description=checkForReason(), 
            #title='Команды доступные на сегодняшний день:'
        )
        
        text = '''
# БОТ РАБОТАЕТ ТОЛЬКО С ТАБЛИЦЕЙ,
# ОН НЕ БАНИТ В ИГРЕ.
### команды для работы с таблицей:
`/поиск` - ищет игрока в таблице, если такой есть - пишет данные о нём. цвет сообщения - цвет игрока в таблице.

`/внести-наказание` - обычное записывание в таблице. варн/бан.
`/внести-заметку` - записывает заметку в таблицу на __ник__  в __ячейке__ игрока.
`/внести-тест` - устанавливает статус теста на игроке.

`/перма` - быстрая запись пермы, делает игрока сразу чёрным, а 
бан красным.
`/джобка` - быстрая запись джобки.
`/сменить-цвет` - меняет цвет игрока, варна или бана.

### команды вне таблицы:
`/профиль` - ваша или чужая статистика. цвет сообщения - цвет вашего сервера.
`/добавить-жалобу` - даёт +1 к жалобе в статистику.
`/пдк` - делает запрос на пдк.
`/мой-сикей` - устанавливает ваш сикей в профиль, он может пригодиться кодеру для подсчетов ахелпов например.

'''


        embed = discord.Embed(
            colour=discord.Colour.random(),
            description=text, 
            #title='Команды доступные на сегодняшний день:'
        )

        #await ctx.response.send_message('❌ Еще не работает.')
        await ctx.response.send_message(embed=embed, ephemeral=True)
        return

async def msgToLOGG(ctx, worksheet, user, msgAuthor, clrColor=None, clrColum=None, clrNumber=None, choose=None, rule=None, reason=None, isJobka=False, isPerma=False, isColor=False):

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
        elif isJobka == True:
            return f'Записал новую джобку.'
        elif isColor == True:
            return f'Поменял цвет игроку.'
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
    
    try:
        embed.set_thumbnail(url=member.avatar.url)
    except:
        embed.set_thumbnail(url='https://static.wikia.nocookie.net/evade-nextbot/images/b/b5/Nerd.png/revision/latest?cb=20220822144117')

    embed.set_footer(text=f'{checkFooter(ctx=ctx, user=ctx.user)}, {row}')


    await logs.send(embed=embed)




async def juniorCheck(ctx, user, reason, msg, rule=None, punish=None, punishTime=None, jobChoose=None, playerEmbed=None):

    await msg.edit(content=f'**😐 Ожидай одобрения запроса от старшей администрации.**')
    request = client.get_channel(REQUEST_ROOM)

    embed = discord.Embed(
        colour=discord.Colour(0xE6B400), 
        description=
f'''



**Нарушитель:** {user}

**Причина:** {reason}


''', #**Модератор:** {ctx.user}
        title='❗Статус: ожидает одобрения.'
    )
    if punish != None:
        punishIsVisible = False
        if punish == 'варн':
            punish = 'Варн ⚠️'
        elif punish == 'бан':
            punish = 'Бан ⛔'
            punishIsVisible = True
        elif punish == 'джобка':
            punish = f'Джобка 👤'
            punishIsVisible = True
        elif punish == 'перма':
            punish = 'ПЕРМА ❗'
        elif punish == 'ПДК':
            punish = 'ПДК 😡'
        elif punish == 'СНЯТЬ ПДК':
            punish = 'Снять ПДК 🙏'

        embed.add_field(name="Наказание", value=punish)
    if rule != None:
        embed.add_field(name="Правило", value=rule)
    if punishIsVisible == True:
        if punishTime != None:
            embed.add_field(name='Срок', value=punishTime)
    if jobChoose != None:
        embed.add_field(name='Отдел', value=jobChoose)
    embed.set_footer(text=checkFooter(ctx=ctx, user=ctx.user))
    

    

    msg = await request.send(embed=embed)

    await msg.add_reaction('✅')
    await msg.add_reaction('❌')
    try:
        thread = await msg.create_thread(name=f'{user}, {punish}')
        if playerEmbed != None:
            await thread.send(embed=playerEmbed)
        else:
            await thread.send('**⚠️ Не нашёл информацию о игроке. Либо его нет в таблице, либо я его вообще и не искал. 🙂**')
        await thread.send(f'<@{ctx.user.id}> тебе могут задать вопрос по твоему наказанию, обсуди это здесь.')
    except:
        return



    def check(payload):
        reaction = payload.emoji
        rAuth = payload.member
        rMsg = payload.message_id

        if msg.id != rMsg:
            return

        def nextStep():
            return str(payload.emoji) == '✅' or str(payload.emoji) == '❌'

        access = discord.utils.find(lambda r: r.name == 'Модератор', ctx.guild.roles)
        access2 = discord.utils.find(lambda r: r.name == 'Старший Модератор', ctx.guild.roles)
        access3 = discord.utils.find(lambda r: r.name == 'Смотритель Сервера', ctx.guild.roles)
        access4 = discord.utils.find(lambda r: r.name == 'Смотритель Серверов', ctx.guild.roles)
        access5 = discord.utils.find(lambda r: r.name == 'Младший Администратор', ctx.guild.roles)
        access6 = discord.utils.find(lambda r: r.name == 'Администратор', ctx.guild.roles)


        if access in rAuth.roles:
            return nextStep()
        elif access2 in rAuth.roles:
            return nextStep()
        elif access3 in rAuth.roles:
            return nextStep()
        elif access4 in rAuth.roles:
            return nextStep()
        elif access5 in rAuth.roles:
            return nextStep()
        elif access6 in rAuth.roles:
            return nextStep()
        else:
            pass
    try:
        payload = await client.wait_for('raw_reaction_add', timeout=604800.0, check=check)
    except asyncio.TimeoutError:
        await msg.edit(content='❌ **Время на ответ запроса - вышло.**')
    else:
        reaction = str(payload.emoji)
        if reaction == '❌':
            embed = discord.Embed(
                colour=discord.Colour(0xDB042F), 
                description=
        f'''


        
        **Нарушитель:** {user}

        **Причина:** {reason}


        ''', #**Модератор:** {ctx.user}
                title='Статус: Отказано.'
            )
            if punish != None:
                if punish == 'варн':
                    punish = 'Варн ⚠️'
                elif punish == 'бан':
                    punish = 'Бан ⛔'

                embed.add_field(name="Наказание", value=punish)
            if rule != None:
                embed.add_field(name="Правило", value=rule)
            embed.set_footer(text=checkFooter(ctx=ctx, user=ctx.user))
            await msg.edit(embed=embed)
            return False
        elif reaction == '✅':
            embed = discord.Embed(
                colour=discord.Colour(0x00C72B), 
                description=
        f'''


        
        **Нарушитель:** {user}

        **Причина:** {reason}


        ''', #**Модератор:** {ctx.user}
                title='Статус: Одобрено.'
            )
            if punish != None:
                if punish == 'варн':
                    punish = 'Варн ⚠️'
                elif punish == 'бан':
                    punish = 'Бан ⛔'

                embed.add_field(name="Наказание", value=punish)
            if rule != None:
                embed.add_field(name="Правило", value=rule)
            embed.set_footer(text=checkFooter(ctx=ctx, user=ctx.user))
            await msg.edit(embed=embed)
            return True
        else:
            await msg.edit(content='❌ В запросе отказано. `error #451`')
    



async def checkForModeratorRole(ctx, ignoreChannelCheck=False):

    if ignoreChannelCheck == False:            
        checkForChannel = await commandChannelCheck(ctx=ctx)
        if checkForChannel == True:
            pass
        else:
            await ctx.response.send_message(f'❌ Писать команды можно только тут - <#{COMMAND_ROOM}>', ephemeral=True)
            return False

    access = discord.utils.find(lambda r: r.name == 'Младший Модератор', ctx.guild.roles)
    access1 = discord.utils.find(lambda r: r.name == 'Модератор', ctx.guild.roles)
    access2 = discord.utils.find(lambda r: r.name == 'Старший Модератор', ctx.guild.roles)
    access3 = discord.utils.find(lambda r: r.name == 'Смотритель Сервера', ctx.guild.roles)
    access4 = discord.utils.find(lambda r: r.name == 'Смотритель Серверов', ctx.guild.roles)
    access5 = discord.utils.find(lambda r: r.name == 'Младший Администратор', ctx.guild.roles)
    access6 = discord.utils.find(lambda r: r.name == 'Администратор', ctx.guild.roles)


    roles = ctx.user.roles

    accesses = (access, access1, access2, access3, access4, access5, access6)

    if any([True for access in accesses if access in roles]):
        return True
    else:
        await ctx.response.send_message('❌ У Вас нет доступа к данной команде.')
        return False



@client.tree.command(name='пдк', description='сообщение в #запросы, без таблицы', guild=discord.Object(id=GUILD))
@app_commands.choices(пдк=[
    discord.app_commands.Choice(name='дать ПДК', value=1),
    discord.app_commands.Choice(name='снять ПДК', value=2),
])
async def pdk(ctx, игрок: str=None, правило: str=None, причина: str=None, пдк: app_commands.Choice[int]=0):

    user = игрок
    rule = правило
    reason = причина
    pdk = пдк

    access = await checkForModeratorRole(ctx)
    if access == False:
        return
    
    if user == None:
            await ctx.response.send_message('❌ Не указан игрок.')
            return
    if rule == None:
            await ctx.response.send_message('❌ Не указано правило.')
            return
    if reason == None:
            await ctx.response.send_message('❌ Не указана причина.')
            return


    if pdk == 0:    
            await ctx.response.send_message('❌ Не указано дать или снять ПДК.')
            return
    if pdk.value == 0:
            await ctx.response.send_message('❌ Не указано дать или снять ПДК.')
            return

    #msg = client.get_channel(ctx.channel.id)
    junior = discord.utils.find(lambda r: r.name == 'Младший Модератор', ctx.guild.roles)
    if junior in ctx.user.roles:
        msg = await ctx.response.send_message('✅ Запрос отправлен.')
        msg = client.get_channel(ctx.channel.id)
        msg = await ctx.original_response()
        if pdk.value == 1:
            checkForJunior = await juniorCheck(ctx=ctx, user=user, rule=rule, reason=reason, msg=msg, punish='ПДК')
        else:
            checkForJunior = await juniorCheck(ctx=ctx, user=user, rule=rule, reason=reason, msg=msg, punish='СНЯТЬ ПДК')


        try:
            match checkForJunior:
                case False:
                    await msg.edit(content=f'**❌ Твой запрос не одобрили.**') 
                    return
                case True:
                    await msg.edit(content=f'**✅ Твой запрос одобрили.**') 
                    return
        except:
            return
    else:
        msg = await ctx.response.send_message('❌ Вы уже взрослый смешарик, Вам это никчему.')


@client.tree.command(name = 'статистика', description='вся статистика пользователей, команда для смотрителей', guild=discord.Object(id=GUILD))
async def toStats(ctx):

    # access = await checkForModeratorRole(ctx)
    # if access == False:

    #     return

    access2 = discord.utils.find(lambda r: r.name == 'Старший Модератор', ctx.guild.roles)
    access3 = discord.utils.find(lambda r: r.name == 'Смотритель Сервера', ctx.guild.roles)
    access4 = discord.utils.find(lambda r: r.name == 'Смотритель Серверов', ctx.guild.roles)
    access5 = discord.utils.find(lambda r: r.name == 'Младший Администратор', ctx.guild.roles)
    access6 = discord.utils.find(lambda r: r.name == 'Администратор', ctx.guild.roles)
    if access2 in ctx.user.roles:
        pass
    elif access3 in ctx.user.roles:
        pass
    elif access4 in ctx.user.roles:
        pass
    elif access5 in ctx.user.roles:
        pass
    elif access6 in ctx.user.roles:
        pass
    else:
        await ctx.response.send_message('❌ У Вас нет доступа к данной команде.')
        return

    embedEcho, embedSolaris, embedNova, embedAthara, embedElysium, embedAllRole, embedMain = await stats(ctx=ctx, client=client)
    await ctx.response.send_message('Отправляю информацию на Эхо.', ephemeral=True)
    id = ctx.user.id
    ctx = client.get_channel(STAT_ROOM)
    await ctx.send(embed=embedEcho)
    await ctx.send(embed=embedSolaris)
    await ctx.send(embed=embedNova)
    await ctx.send(embed=embedAthara)
    await ctx.send(embed=embedElysium)
    await ctx.send(embed=embedMain)
    #await ctx.send(embed=embedAllRole)
    await ctx.send(f'<@{id}>')


@client.tree.command(name = "внести-заметку", description= 'записывает заметку игроку в таблице', guild=discord.Object(id=GUILD))
async def note(ctx, игрок: str=None, причина: str=None):

    access = await checkForModeratorRole(ctx)
    if access == False:
        
        return

    user = игрок
    reason = причина


    try:
        await ctx.response.defer() # ephemeral=True
    except:
        await errorDeferMessage(ctx=ctx, errorValue='619')
        return

    gc, sh, worksheet = joinToSheet()

    values_list = worksheet.col_values(2)




    if user in values_list:
        user = f'{user}'
    elif (f'{user} ' in values_list):
        user = f'{user} '
    elif (f'{user}  ' in values_list):
        user = f'{user}  '
    else:
        await ctx.followup.send(f"❌ Игрока `{user}` нет в таблице.")
        return


    infochat = ctx.channel.id # чат
    infochat = client.get_channel(infochat)
    msg = await infochat.send(f'**🔄 поиск {user}...**')

    cell = worksheet.find(user)
    
    row = cell.row
    col = cell.col


    embed = await getProfileFromSheet(user, checkForWarn(row, worksheet), checkForBan(row, worksheet), checkForTest(row, sh), row, col, worksheet, UserWarnBan='User')
    await asyncio.sleep(3)
    await ctx.followup.send(embed=embed)



    
 

    embed = discord.Embed(
        colour=discord.Colour.from_rgb(255,255,255),
        description=f'{reason}', 
        title='Всё верно?'
    )
    
    await msg.delete()
    msg = await infochat.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

    trueUser = ctx.user
    
    def check(reaction, msgAuthor):
        if trueUser == msgAuthor:
            return msgAuthor == ctx.user and str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌'
    try:
        reaction, msgAuthor = await client.wait_for('reaction_add', timeout=300.0, check=check)
    except asyncio.TimeoutError:
        await msg.edit(content='❌ **Время вышло.**')
    else:
        if reaction.emoji == '❌':
            await msg.edit(content='❌ **Отменил операцию.**')
            return
        elif reaction.emoji == '✅':
            await msg.edit(content=f'**🔄 Обрабатываю запросик :middle_finger:**')
            await msgToLOGG(ctx, worksheet, user, msgAuthor, reason=reason)

            worksheet.insert_note(f'B{row}', f'{reason}')
            
            await msg.edit(content=f'**✅ Успешно вписал заметку игроку!**')
        else:
            await msg.edit(content='❌ **Время вышло.**')


async def errorDeferMessage(ctx, errorValue):
    # errorCh = client.get_channel(ctx.channel.id)
    print(f'erorr {errorValue}')
    logging.warning(f'error - {errorValue}')
    # await errorCh.send(f'<@{ctx.user.id}> **попробуй еще раз, дискорд не захотел принимать твою команду.**')
    
@client.tree.command(name = "джобка", description='быстрая запись джобки', guild=discord.Object(id=GUILD))
@app_commands.choices(отдел=[
    discord.app_commands.Choice(name='КМД', value=1),
    discord.app_commands.Choice(name='СБ', value=2),
    discord.app_commands.Choice(name='РНД', value=3),
    discord.app_commands.Choice(name='МЕД', value=4),
    discord.app_commands.Choice(name='КАРГО', value=5),
    discord.app_commands.Choice(name='ИНЖ', value=6),
    discord.app_commands.Choice(name='АНТ', value=7),
], 
бан=[
    discord.app_commands.Choice(name='Нет', value=1),
    discord.app_commands.Choice(name='Да', value=2),
]
)


async def jobka(ctx, игрок: str=None, правило: str=None, причина: str=None, отдел: app_commands.Choice[int]=0, срок: str='None', бан: app_commands.Choice[int]=0):

    access = await checkForModeratorRole(ctx)
    if access == False:
        
        return

    user = игрок
    rule = правило
    reason = причина
    jobChoose = отдел
    punishTime = срок
    isNeedToBan = бан


    gc, sh, worksheet = joinToSheet()
    values_list = worksheet.col_values(2)
    playerIsNew = False


    
    if jobChoose.value == 0:
        await ctx.response.send_message('❌ Не выбрана профессия.')
        return

    if rule == None:
        await ctx.response.send_message('❌ Не корректно выбрано правило')
        return

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
    

    if isNeedToBan != 0:
        if isNeedToBan.value == 2:
            ChoosenJob = f"{jobChoose.name} + Бан."
        else:
            ChoosenJob = f"{jobChoose.name}."
    else:
        ChoosenJob = f"{jobChoose.name}."


    if user in values_list:
        user = f'{user}'
    elif (f'{user} ' in values_list):
        user = f'{user} '
    elif (f'{user}  ' in values_list):
        user = f'{user}  '
    else:
        await ctx.response.send_message(f"⚠️ Игрока `{user}` нет в таблице.")
        playerIsNew = True


    if playerIsNew == False:
        try:
            await ctx.response.defer() # ephemeral=True
        except:
            await errorDeferMessage(ctx=ctx, errorValue='743')
            return

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

        logging.info(f'6000, {row}, {banCount}')
        
        worksheet.update(f'B{row}', user)

        worksheet.update(f'F{row}', '1')
        worksheet.update(f'G{row}', str(f'JB: {ChoosenJob} Правило {rule}'))
        worksheet.insert_note(f'G{row}', f'{reason}')



    async def oldPlayer(embedOrWrite):

            


        cell = worksheet.find(user)
        
        row = cell.row
        col = cell.col
        banCount = checkForBan(row, worksheet)
        


        if embedOrWrite == 'embed':
            warnCount = checkForWarn(row, worksheet)
            embed = await getProfileFromSheet(user, warnCount, banCount, checkForTest(row, sh), row, col, worksheet, UserWarnBan='User')
            return embed

        if embedOrWrite == 'write':
            warnCount = checkForWarn(row, worksheet)
            mainCount = max(banCount, warnCount)

            def addField(count):
                worksheet.insert_row(['', '', '', '', '', '', ''], index=row+count) #count+1
                worksheet.merge_cells(f'B{row}:B{row+count}', 'MERGE_ALL')
            
            worksheet.update(f'B{row}', user)

            banNullOrNot = worksheet.get_values(f'G{row}:G{row+50}')
            
            needToAdd = 0
            if banNullOrNot[0] != ['']:
                for x in banNullOrNot:
                    if x == ['']:
                        break
                    needToAdd += 1
            if banCount > needToAdd:
                logging.info(f'5001, {row}, {banCount}, {needToAdd}')
                worksheet.update(f'G{row+needToAdd}', str(f'JB: {ChoosenJob} Правило {rule}'))
                worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})

            elif banCount < needToAdd:
                logging.info(f'5002, {row}, {banCount}, {needToAdd}')
                addField(banCount)
                worksheet.update(f'F{row+banCount}', str(f'{banCount+1}')) # test
                worksheet.update(f'G{row+banCount}', str(f'JB: {ChoosenJob} Правило {rule}'))
                worksheet.insert_note(f'G{row+banCount}', f'{reason}')
                worksheet.format(f'G{row+banCount}', {'textFormat': {'strikethrough': False}})

            elif banCount == needToAdd:
                if banCount == 0 and needToAdd == 0:
                    logging.info(f'5003, {row}, {banCount}, {needToAdd}')
                    worksheet.update(f'F{row+needToAdd}', str(f'1'))
                    worksheet.update(f'G{row+needToAdd}', str(f'JB: {ChoosenJob} Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                elif banCount < mainCount:
                    logging.info(f'5004, {row}, {banCount}, {needToAdd}')
                    worksheet.update(f'F{row+needToAdd}', str(f'{banCount+1}'))
                    worksheet.update(f'G{row+needToAdd}', str(f'JB: {ChoosenJob} Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                else:
                    logging.info(f'5005, {row}, {banCount}')
                    addField(banCount)
                    worksheet.update(f'F{row+banCount}', str(f'{banCount+1}')) # test
                    worksheet.update(f'G{row+needToAdd}', str(f'JB: {ChoosenJob} Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
            return

    
        





    trueUser = ctx.user

    infochat = ctx.channel.id # чат
    infochat = client.get_channel(infochat)
    
    if playerIsNew == False:
        msg = await infochat.send(f'🔄 загружаю данные о {user}...')
        embed = await oldPlayer('embed')
        await asyncio.sleep(3)
        await ctx.followup.send(embed=embed)

    if playerIsNew == True:
        msg = await infochat.send(f'**🔄 ожидай...**')


    embed = discord.Embed(
        colour=discord.Colour(0x800080),
        description=f'**Причина:** {reason}', 
        title='Убедись, правильно ли ты всё записал:'
    )

    embed.add_field(name="Наказание", value=f'JB: {ChoosenJob}')
    embed.add_field(name="Правило", value=rule)
    if punishTime != 'None' and punishTime != None:
        embed.add_field(name="Срок", value=punishTime)
    
    await msg.delete()
    msg = await infochat.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')


    trueUser = ctx.user
    
    def check(reaction, msgAuthor): # trueUser = ctx.user
        if trueUser == msgAuthor:
            return msgAuthor == ctx.user and str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌'
    try:
        reaction, msgAuthor = await client.wait_for('reaction_add', timeout=300.0, check=check)
    except asyncio.TimeoutError:
        await msg.edit(content='❌ **Время вышло.**')
    else:
        if reaction.emoji == '❌':
            await msg.edit(content='❌ **Отменил операцию.**')
            return
        elif reaction.emoji == '✅':



            junior = discord.utils.find(lambda r: r.name == 'Младший Модератор', ctx.guild.roles)
            if junior in ctx.user.roles:
                try:
                    playerEmbed = await oldPlayer('embed')
                    checkForJunior = await juniorCheck(ctx=ctx, user=user, rule=rule, reason=reason, msg=msg, punish='джобка', punishTime=punishTime, jobChoose=jobChoose.name, playerEmbed=playerEmbed)
                except:
                    checkForJunior = await juniorCheck(ctx=ctx, user=user, rule=rule, reason=reason, msg=msg, punish='джобка', punishTime=punishTime, jobChoose=jobChoose.name)
            else:
                checkForJunior = True


            #logging.info(checkForJunior)

            if checkForJunior == False:
                await msg.edit(content=f'**❌ Твой запрос не одобрили.**') 
                return

            elif checkForJunior == True:
                pass


            else:
                await msg.edit(content=f'**❌ Тех. ошибка - пингуй ксова. `error #1086/1` **')
                logging.critical(f'{checkForJunior}, 1134')
                return


            await msg.edit(content=f'**🔄 Обрабатываю запросик :middle_finger:**') #{reaction.emoji}
            if playerIsNew == True:
                newPlayer()
                await msg.edit(content=f'**✅ Успешно вписал джобку новому игроку!**')
            if playerIsNew == False:
                await oldPlayer('write')
                await msg.edit(content=f'**✅ Успешно вписал джобку старому игроку!**')
            await msgToLOGG(ctx, worksheet, user, msgAuthor, rule=rule, reason=reason, isJobka=True)
            profile = await get_user_profile(ctx.user.id)
            user_id = ctx.user.id
            new_value = profile['ban'] + 1
            parameter = 'ban'
            await set_user_profile(user_id, parameter, new_value)

            logs = client.get_channel(ERROR_ROOM)
            await logs.send(f'⛔ {ctx.user} записал себе банчик')
        else:
            await msg.edit(content='❌ **Время вышло.**')


@client.tree.command(name = "перма", description= 'быстрая запись пермы', guild=discord.Object(id=GUILD))
async def perma(ctx, игрок: str=None, правило: str=None, причина: str=None):

    access = await checkForModeratorRole(ctx)
    if access == False:
        
        return

    user = игрок
    rule = правило
    reason = причина
    gc, sh, worksheet = joinToSheet()
    values_list = worksheet.col_values(2)
    playerIsNew = False

    if rule == None:
        await ctx.response.send_message('❌ Не корректно выбрано правило')
        return
        
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


    if user in values_list:
        user = f'{user}'
    elif (f'{user} ' in values_list):
        user = f'{user} '
    elif (f'{user}  ' in values_list):
        user = f'{user}  '
    else:
        await ctx.response.send_message(f"⚠️ Игрока `{user}` нет в таблице.")
        playerIsNew = True


    if playerIsNew == False:
        try:
            await ctx.response.defer() # ephemeral=True
        except:
            await errorDeferMessage(ctx=ctx, errorValue='971')
            return
        
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
        
        logging.info(f'5000, {row}')
        
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
            embed = await getProfileFromSheet(user, warnCount, banCount, checkForTest(row, sh), row, col, worksheet, UserWarnBan='User')
            playerEmbed = embed
            return embed

        if embedOrWrite == 'write':
            warnCount = checkForWarn(row, worksheet)
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
                try:
                    worksheet.insert_row(['', '', '', '', '', '', ''], index=row+count) #count+1
                    worksheet.merge_cells(f'B{row}:B{row+count}', 'MERGE_ALL')
                except:
                    logging.info("addField error =)")
            
            worksheet.update(f'B{row}', user)
            playerFormat()

            banNullOrNot = worksheet.get_values(f'G{row}:G{row+50}')
            
            needToAdd = 0
            try:
                if banNullOrNot[0] != ['']:
                    for x in banNullOrNot:
                        if x == ['']:
                            break
                        needToAdd += 1
            except:
                pass
            if banCount > needToAdd:
                logging.info(f'4001, {row}, {banCount}')
                worksheet.update(f'G{row+needToAdd}', str(f'PERMA: Правило {rule}'))
                worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                ruleFormat(needToAdd)

            elif banCount < needToAdd:
                logging.info(f'4002, {row}, {banCount}')
                addField(banCount)
                worksheet.update(f'F{row+banCount}', str(f'{banCount+1}')) # test
                worksheet.update(f'G{row+banCount}', str(f'PERMA: Правило {rule}'))
                worksheet.insert_note(f'G{row+banCount}', f'{reason}')
                worksheet.format(f'G{row+banCount}', {'textFormat': {'strikethrough': False}})
                ruleFormat(banCount)

            elif banCount == needToAdd:
                if banCount == 0 and needToAdd == 0:
                    logging.info(f'4003, {row}, {banCount}')
                    worksheet.update(f'F{row+needToAdd}', str(f'1'))
                    worksheet.update(f'G{row+needToAdd}', str(f'PERMA: Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                    ruleFormat(needToAdd)
                elif banCount < mainCount:
                    logging.info(f'4004, {row}, {banCount}')
                    worksheet.update(f'F{row+needToAdd}', str(f'{banCount+1}'))
                    worksheet.update(f'G{row+needToAdd}', str(f'PERMA: Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                    ruleFormat(needToAdd)
                else:
                    logging.info(f'4005, {row}, {banCount}')
                    addField(banCount)
                    worksheet.update(f'F{row+banCount}', str(f'{banCount+1}')) # test
                    worksheet.update(f'G{row+needToAdd}', str(f'PERMA: Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                    ruleFormat(needToAdd)
            return

    
        





    trueUser = ctx.user

    infochat = ctx.channel.id # чат
    infochat = client.get_channel(infochat)
    
    if playerIsNew == False:
        msg = await infochat.send(f'🔄 загружаю данные о {user}...')
        embed = await oldPlayer('embed')
        await asyncio.sleep(3)
        await ctx.followup.send(embed=embed)

    if playerIsNew == True:
        msg = await infochat.send(f'**🔄 ожидай...**')


    embed = discord.Embed(
        colour=discord.Colour.red(),
        description=f'**Причина:** {reason}', 
        title='Убедись, правильно ли ты всё записал:'
    )

    embed.add_field(name="Наказание", value='ПЕРМА.')
    embed.add_field(name="Правило", value=rule)
    
    await msg.delete()
    msg = await infochat.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')


    trueUser = ctx.user
    
    def check(reaction, msgAuthor): # trueUser = ctx.user
        if trueUser == msgAuthor:
            return msgAuthor == ctx.user and str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌'
    try:
        reaction, msgAuthor = await client.wait_for('reaction_add', timeout=300.0, check=check)
    except asyncio.TimeoutError:
        await msg.edit(content='❌ **Время вышло.**')
    else:
        if reaction.emoji == '❌':
            await msg.edit(content='❌ **Отменил операцию.**')
            return
        elif reaction.emoji == '✅':



            junior = discord.utils.find(lambda r: r.name == 'Младший Модератор', ctx.guild.roles)
            if junior in ctx.user.roles:
                try:
                    playerEmbed = await oldPlayer('embed')
                    checkForJunior = await juniorCheck(ctx=ctx, user=user, rule=rule, reason=reason, msg=msg, punish='перма', playerEmbed=playerEmbed)
                except:
                    checkForJunior = await juniorCheck(ctx=ctx, user=user, rule=rule, reason=reason, msg=msg, punish='перма')
            else:
                checkForJunior = True


            if checkForJunior == False:
                await msg.edit(content=f'**❌ Твой запрос не одобрили.**') 
                return

            elif checkForJunior == True:
                pass

            else:
                await msg.edit(content=f'**❌ Тех. ошибка - пингуй ксова. `error #1376/1` **')
                logging.critical(f'{checkForJunior}, 1426')
                return


            await msg.edit(content=f'**🔄 Обрабатываю запросик :middle_finger:**') #{reaction.emoji}
            if playerIsNew == True:
                newPlayer()
                await msg.edit(content=f'**✅ Успешно вписал ПЕРМУ новому игроку!**')
            if playerIsNew == False:
                await oldPlayer('write')
                await msg.edit(content=f'**✅ Успешно вписал ПЕРМУ старому игроку!**')
            await msgToLOGG(ctx, worksheet, user, msgAuthor, rule=rule, reason=reason, isPerma=True)
            profile = await get_user_profile(ctx.user.id)
            user_id = ctx.user.id
            new_value = profile['ban'] + 1
            parameter = 'ban'
            await set_user_profile(user_id, parameter, new_value)

            logs = client.get_channel(ERROR_ROOM)
            await logs.send(f'⛔ {ctx.user} записал себе банчик')
        else:
            await msg.edit(content='❌ **Время вышло.**')
    

@client.tree.command(name = "внести-тест", description= 'записывает тест игроку в таблице', guild=discord.Object(id=GUILD))
@app_commands.choices(выбор=[
    discord.app_commands.Choice(name='Прошёл', value=1),
    discord.app_commands.Choice(name='Не прошёл', value=2),
    discord.app_commands.Choice(name='Убрать', value=3),
])
async def giveTest(ctx, игрок: str=None, выбор: app_commands.Choice[int]=0):

    access = await checkForModeratorRole(ctx)
    if access == False:
        
        return

    user = игрок
    choose = выбор

    gc, sh, worksheet = joinToSheet()


    if user == None:
        await ctx.response.send_message(f"❌ Не указан игрок.")
        return
    
    try:
        if choose.value == 0:
            await ctx.response.send_message(f"❌ Не выбрано что записывать в строку теста.")
            return
    except:
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
        infochat = ctx.channel.id # чат
        infochat = client.get_channel(infochat)
        
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(255,255,255),
            #description=f'**Причина:** {reason}', 
            title='Заметь, что игрока в таблице нет, мы пишем нового:'
        )

        embed.add_field(name="Игрок", value=user)
        embed.add_field(name="Выбор", value=choose.name)
        
        msg = await infochat.send(embed=embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

        trueUser = ctx.user
        
        def check(reaction, msgAuthor): # trueUser = ctx.user
            if trueUser == msgAuthor:
                return msgAuthor == ctx.user and str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌'
        try:
            reaction, msgAuthor = await client.wait_for('reaction_add', timeout=300.0, check=check)
        except asyncio.TimeoutError:
            await msg.edit(content='❌ **Время вышло.**')
        else:
            if reaction.emoji == '❌':
                await msg.edit(content='❌ **Отменил операцию.**')
                return
            elif reaction.emoji == '✅':
        
                await msg.edit(content=f'**🔄 Обрабатываю запросик :middle_finger:**') #{reaction.emoji}
                newPlayer()
                await msg.edit(content=f'✅ Успешно вписал тест новому игроку!')
            else:
                await msg.edit(content='❌ **Время вышло.**')




    if skipOrNot == True:
        return
    
    try:
        await ctx.response.defer() # ephemeral=True
    except:
        await errorDeferMessage(ctx=ctx, errorValue='1340')
        return

    cell = worksheet.find(user)
    
    row = cell.row
    col = cell.col

        
    banCount = checkForBan(row, worksheet)
    warnCount = checkForWarn(row, worksheet)
    embed = await getProfileFromSheet(user, warnCount, banCount, checkForTest(row, sh), row, col, worksheet)

    await asyncio.sleep(3)
    await ctx.followup.send(embed=embed)
    infochat = ctx.channel.id # чат
    infochat = client.get_channel(infochat)
    
    embed = discord.Embed(
        colour=discord.Colour.from_rgb(255,255,255),
        #description=f'**Причина:** {reason}', 
        title='Убедись, что ты всё правильно написал:'
    )

    embed.add_field(name="Игрок", value=user)
    embed.add_field(name="Выбор", value=choose.name)
    
    msg = await infochat.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')

    trueUser = ctx.user
    
    def check(reaction, msgAuthor): # trueUser = ctx.user
        if trueUser == msgAuthor:
            return msgAuthor == ctx.user and str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌'
    try:
        reaction, msgAuthor = await client.wait_for('reaction_add', timeout=300.0, check=check)
    except asyncio.TimeoutError:
        await msg.edit(content='❌ **Время вышло.**')
    else:
        if reaction.emoji == '❌':
            await msg.edit(content='❌ **Отменил операцию.**')
            return
        elif reaction.emoji == '✅':
            await msg.edit(content=f'**🔄 Обрабатываю запросик :middle_finger:**') #{reaction.emoji}
        else:
            await msg.edit(content='❌ **Время вышло.**')
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
                mainCount -= 1
                try:
                    worksheet.merge_cells(f'H{row}:H{row+mainCount}', 'MERGE_ALL')
                except:
                    pass
                


        emoji = (reaction.emoji)
        emoji = str(emoji)
        if reaction.emoji == '✅':                
            oldPlayer()
            await msg.edit(content='✅ Успешно обновил данные игрока.')
        if reaction.emoji == '❌':
            return



newDay = True
async def sendDatabaseToEcho(ctx):
    global newDay
    hour = dt.now().hour
    minute = dt.now().minute
    if minute in range(1, 9):
        minute = '0' + str(minute)

    if hour == 23 and newDay == True:
        ctx = client.get_channel(1137687925925093459)
        await ctx.send(content=f'{dt.now()}',file=discord.File('basa.json'))


        ctx = client.get_channel(1139276548650848266)
        await checkAhelps(ctx=ctx)
        newDay = False
    if hour == 0:
        newDay = True

async def cycle(ctx):
    while True:
        await sendDatabaseToEcho(ctx)
        logging.info(f"продолжаю цикл - День: {dt.now().day} Время: {dt.now().hour}:{dt.now().minute}")
        await asyncio.sleep(600)

@client.tree.command(name = "сменить-цвет", description= 'смена цвета в таблице', guild=discord.Object(id=GUILD))
@app_commands.choices(цвет=[
    discord.app_commands.Choice(name='очистить', value=1),
    discord.app_commands.Choice(name='зелёный', value=2),
    discord.app_commands.Choice(name='жёлтый', value=3),
    discord.app_commands.Choice(name='красный', value=4),
    discord.app_commands.Choice(name='чёрный', value=5),
], 
столбик=[
discord.app_commands.Choice(name='сикей', value=1),
discord.app_commands.Choice(name='варн', value=2),
discord.app_commands.Choice(name='бан', value=3),
])
async def change_color(ctx, ник: str=None, столбик: app_commands.Choice[int]=0, цвет: app_commands.Choice[int]=0, номер_наказания: int=0):

    access = await checkForModeratorRole(ctx)
    if access == False:
        
        return

    user = ник
    color = цвет
    punish = столбик
    rule_number = номер_наказания



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

    try:
        await ctx.response.defer() # ephemeral=True
    except:
        await errorDeferMessage(ctx=ctx, errorValue='1509')
        return
    
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


    
    
    infochat = ctx.channel.id # чат
    infochat = client.get_channel(infochat)
    trueUser = ctx.user



    def colorSwitch(value):
        if value == 1:
            return discord.Colour(0xFFFFFF)
        elif value == 2:
            return discord.Colour(0x00FF00)
        elif value == 3:
            return discord.Colour(0xFFA500)
        elif value == 4:
            return discord.Colour(0xFF0000)
        elif value == 5:
            return discord.Colour(0x000000)


    embed = discord.Embed(
        colour=colorSwitch(color.value),
        #description=f'**Причина:** {reason}', 
        title='Убедись, что ты всё правильно указал:'
    )

    embed.add_field(name="Игрок", value=user)
    embed.add_field(name='Столбик', value=punish.name)
    embed.add_field(name="Выбор", value=color.name)
    if punish.value != 1:
        embed.add_field(name='Номер наказания', value=rule_number)
    
    msg = await infochat.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')



    def check(reaction, msgAuthor): # trueUser = ctx.user
        if trueUser == msgAuthor:
            return msgAuthor == ctx.user and str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌'
    try:
        reaction, msgAuthor = await client.wait_for('reaction_add', timeout=300.0, check=check)
    except asyncio.TimeoutError:
        await msg.edit(content='❌ **Время вышло.**')
    else:
        if reaction.emoji == '❌':
            await msg.edit(content='❌ **Отменил операцию.**')
            return
        elif reaction.emoji == '✅':
            await msg.edit(content=f'**🔄 Крашу {user}...**')
        else:
            await msg.edit(content='❌ **Время вышло.**')
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
            try:
                msgAuthor = ctx.user
                await msgToLOGG(ctx, worksheet, user, msgAuthor, clrColor=colorEmoji, clrColum=punishWord, clrNumber=rule_number, isColor=True)
            except:
                msgAuthor = ctx.author
                await msgToLOGG(ctx, worksheet, user, msgAuthor, clrColor=colorEmoji, clrColum=punishWord, clrNumber=rule_number, isColor=True)
        else:
            await msg.edit(content=f'❌ В такой цвет - {colorEmoji}, {punishWord} красить нельзя.')





@client.tree.command(name = "добавить-жалобу", description= 'выдает жалобу в статистику модератору', guild=discord.Object(id=GUILD))
async def report(ctx, модератор: discord.Member = None):

    access = await checkForModeratorRole(ctx)
    if access == False:
        
        return

    user = модератор

    try:
        if user.id:
            user = user.id
            pass
        else:
            await ctx.response.send_message('❌ Указывать нужно айди..')
            return
    except:
        await ctx.response.send_message('❌ Указывать нужно айди..')
        return


    #вавден
    echoRole = discord.utils.find(lambda r: r.name == 'Смотритель Сервера', ctx.guild.roles)
    if echoRole not in ctx.user.roles:
        
        return
    

    if user == None:
        await ctx.response.send_message('❌ Не указан модератор.')
        return

    profile = await get_user_profile(user)
    user_id = user
    new_value = profile['report'] + 1
    parameter = 'report'
    await set_user_profile(user_id, parameter, new_value)

    logs = client.get_channel(ERROR_ROOM)
    await logs.send(f'⏰ {ctx.user} записал <@{user}> новую жалобу')
    await ctx.response.send_message('✅ Успешно выдано.')




@client.tree.command(name = "профиль", description = 'твой профиль', guild=discord.Object(id=GUILD))
async def profile(ctx, модератор: discord.Member = None):

    access = await checkForModeratorRole(ctx, ignoreChannelCheck=True)
    if access == False:
        
        return

    user = модератор
    if user == None:
        user = ctx.user
    

    try:
        await ctx.response.defer() # ephemeral=True
    except:
        await errorDeferMessage(ctx=ctx, errorValue='1832') 
        return
    
    profile = await get_user_profile(user.id)


    embed = discord.Embed(
        colour=checkRole(ctx=ctx, user=user), 
        description=f"# Статистика {user}.", 
        #title=f"# Статистика {user}.", 
    )


    def ckeyNullOrNot():
        try:
            ckey = profile["ckey"]
            if ckey == None:
                ckey = 'Не установлен.'
        except:
            ckey = 'Не установлен.'
        return ckey


    profileStat = f'''

\n
⚠️ Варны: **{profile["warn"]}**

⛔ Баны: **{profile["ban"]}**

⏰ Жалобы: **{profile["report"]}**

🤬 Ахелпы: **{profile["ahelp"]}** *(за месяц)*

👤 Сикей: **{ckeyNullOrNot()}**
\n

'''


    # embed.add_field(name="⚠️ Варны", value=f'{profile["warn"]}')
    # embed.add_field(name="⛔ Баны", value=f'{profile["ban"]}')
    # embed.add_field(name="⏰ Жалобы", value=f'{profile["report"]}')
    # embed.add_field(name="🤬 Ахеплы", value=f'{profile["ahelp"]}')
    # try:
    #     embed.add_field(name="👤 Сикей", value=f'{profile["ckey"]}')
    # except:
    #     embed.add_field(name="👤 Сикей", value=f'-')

    #embed.add_field(name="", value='\n')

    embed.add_field(name="", value=f'{profileStat}')

    embed.add_field(name="", value='\n')
    embed.add_field(name="", value='\n')
    embed.add_field(name="", value='\n')
    
    try:
        embed.set_thumbnail(url=user.avatar.url)
    except:
        embed.set_thumbnail(url='https://static.wikia.nocookie.net/evade-nextbot/images/b/b5/Nerd.png/revision/latest?cb=20220822144117')

    embed.set_footer(text=checkFooter(ctx=ctx, user=user))


    #await asyncio.sleep(3)
    await ctx.followup.send(embed=embed)


@client.tree.command(name = "поиск", description = "поиск игрока в таблице", guild=discord.Object(id=GUILD))
@app_commands.choices(скрыто=[
    discord.app_commands.Choice(name='Показать скрыто', value=1),
    discord.app_commands.Choice(name='Показать всем', value=2),
])
async def first_command(ctx, игрок: str = None, скрыто: app_commands.Choice[int]=1):

    access = await checkForModeratorRole(ctx, ignoreChannelCheck=True)
    if access == False:
        
        return


    user = игрок
    hide = скрыто

    try:
        if hide.value == 2:
            hide == False
        else:
            hide = True
    except:
        hide = True

    if hide == True:
        try:
            await ctx.response.defer(ephemeral=True) # ephemeral=True
        except:
            await errorDeferMessage(ctx=ctx, errorValue='1869')
            return
    else:
        try:
            await ctx.response.defer() # ephemeral=True
        except:
            await errorDeferMessage(ctx=ctx, errorValue='1869')
            return
    
    gc, sh, worksheet = joinToSheet()


    if user == None:
        await ctx.followup.send(f"❌ Не введены аргументы.")
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
        await ctx.followup.send(f"❌ Игрок `{user}` не найден, проверяйте регистр.")
        return

    
    

    
    cell = worksheet.find(user)
    
    row = cell.row
    col = cell.col


    embed = await getProfileFromSheet(user, checkForWarn(row, worksheet), checkForBan(row, worksheet), checkForTest(row, sh), row, col, worksheet, UserWarnBan='User')

    await asyncio.sleep(3)
    await ctx.followup.send(embed=embed)


    
@client.tree.command(name = "внести-наказание", description = "записывает наказание игроку в таблице", guild=discord.Object(id=GUILD))
@app_commands.choices(наказание=[
    discord.app_commands.Choice(name='варн', value=1),
    discord.app_commands.Choice(name='бан', value=2),
])
async def second_command(ctx, ник: str=None, наказание: app_commands.Choice[int]=0, правило: str=None, причина: str='None', срок: str='None'):

    access = await checkForModeratorRole(ctx)
    if access == False:
        
        return

    user = ник
    punish = наказание
    rule = правило
    reason = причина
    punishTime = срок

    gc, sh, worksheet = joinToSheet()


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
            logging.info(f'3001, {row}')
            worksheet.update(f'C{row}', '1')
            worksheet.update(f'D{row}', str(f'Правило {rule}'))
            worksheet.insert_note(f'D{row}', f'{reason}')
            worksheet.format(f'D{row}', {'textFormat': {'strikethrough': False}})

        if punish.value == 2:
            logging.info(f'3002, {row}')
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
                logging.info(f'1001, {warnCount}, {needToAdd}')
                worksheet.update(f'D{row+needToAdd}', str(f'Правило {rule}'))
                worksheet.insert_note(f'D{row+needToAdd}', f'{reason}')
                worksheet.format(f'D{row+needToAdd}', {'textFormat': {'strikethrough': False}})

            elif warnCount < needToAdd:
                logging.info(f'1002, {warnCount}, {needToAdd}')
                addField(warnCount)
                worksheet.update(f'C{row+warnCount}', str(f'{warnCount+1}')) # testt
                worksheet.update(f'D{row+warnCount}', str(f'Правило {rule}'))
                worksheet.insert_note(f'D{row+warnCount}', f'{reason}')
                worksheet.format(f'D{row+warnCount}', {'textFormat': {'strikethrough': False}})

            elif warnCount == needToAdd:
                if warnCount == 0 and needToAdd == 0:
                    logging.info(f'1003, {warnCount}, {needToAdd}')
                    worksheet.update(f'C{row+needToAdd}', str(f'1'))
                    worksheet.update(f'D{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'D{row+needToAdd}', f'{reason}')
                    worksheet.format(f'D{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                elif warnCount < mainCount:
                    logging.info(f'1004, {warnCount}, {needToAdd}')
                    worksheet.update(f'C{row+needToAdd}', str(f'{warnCount+1}'))
                    worksheet.update(f'D{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'D{row+needToAdd}', f'{reason}')
                    worksheet.format(f'D{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                else:
                    logging.info(f'1005, {warnCount}, {needToAdd}')
                    addField(warnCount)
                    worksheet.update(f'C{row+warnCount}', str(f'{warnCount+1}')) # testt
                    worksheet.update(f'D{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'D{row+needToAdd}', f'{reason}')
                    worksheet.format(f'D{row+needToAdd}', {'textFormat': {'strikethrough': False}})
            
            else:
                logging.error('2445')


            
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
                logging.info(f'2001, {banCount}, {needToAdd}')
                worksheet.update(f'G{row+needToAdd}', str(f'Правило {rule}'))
                worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})

            elif banCount < needToAdd:
                logging.info(f'2002, {banCount}, {needToAdd}')
                addField(banCount)
                worksheet.update(f'F{row+banCount}', str(f'{banCount+1}')) # test
                worksheet.update(f'G{row+banCount}', str(f'Правило {rule}'))
                worksheet.insert_note(f'G{row+banCount}', f'{reason}')
                worksheet.format(f'G{row+banCount}', {'textFormat': {'strikethrough': False}})

            elif banCount == needToAdd:
                if banCount == 0 and needToAdd == 0:
                    logging.info(f'2003, {banCount}, {needToAdd}')
                    worksheet.update(f'F{row+needToAdd}', str(f'1'))
                    worksheet.update(f'G{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                elif banCount < mainCount:
                    logging.info(f'2004, {banCount}, {needToAdd}')
                    worksheet.update(f'F{row+needToAdd}', str(f'{banCount+1}'))
                    worksheet.update(f'G{row+needToAdd}', str(f'Правило {rule}'))
                    worksheet.insert_note(f'G{row+needToAdd}', f'{reason}')
                    worksheet.format(f'G{row+needToAdd}', {'textFormat': {'strikethrough': False}})
                else:
                    logging.info(f'2005, {banCount}, {needToAdd}')
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

                infochat = ctx.channel.id # чат
                infochat = client.get_channel(infochat)
                msg = await infochat.send(f'🔄 загружаю данные о {user}..')
                embed = await getProfileFromSheet(user, checkForWarn(row, worksheet), checkForBan(row, worksheet), checkForTest(row, sh), row, col, worksheet, UserWarnBan='User')
                playerEmbed = embed
                await asyncio.sleep(3)
                await ctx.followup.send(embed=embed)
            case 'new':
                infochat = ctx.channel.id # чат
                infochat = client.get_channel(infochat)
                msg = await infochat.send(f'🔄 ожидай..')
        trueUser = ctx.user
        
        def checkPunishForColor(value):
            if value == 1:
                return discord.Colour.gold()
            elif value == 2:
                return discord.Colour.red()
            else:
                discord.Colour.from_rgb(0, 0, 0)
                


        embed = discord.Embed(
            colour=checkPunishForColor(value=punish.value), 
            description=f'**Причина:** {reason}', 
            title='Убедись, правильно ли ты всё записал:'
        )

        embed.add_field(name="Наказание", value=punishEmoji)
        embed.add_field(name="Правило", value=rule)
        
        await msg.delete()
        msg = await infochat.send(embed=embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

        def check(reaction, msgAuthor): # trueUser = ctx.user
            if trueUser == msgAuthor:
                return msgAuthor == ctx.user and str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌'
        try:
            reaction, msgAuthor = await client.wait_for('reaction_add', timeout=300.0, check=check)
        except asyncio.TimeoutError:
            await msg.edit(content='❌ **Время вышло.**')
        else:
            if reaction.emoji == '❌':
                await msg.edit(content='❌ **Отменил операцию.**')
                return
            elif reaction.emoji == '✅':

                junior = discord.utils.find(lambda r: r.name == 'Младший Модератор', ctx.guild.roles)
                if junior in ctx.user.roles:
                    try:
                        checkForJunior = await juniorCheck(ctx=ctx, user=user, rule=rule, reason=reason, msg=msg, punish=punish.name, punishTime=punishTime, playerEmbed=playerEmbed)
                    except:
                        checkForJunior = await juniorCheck(ctx=ctx, user=user, rule=rule, reason=reason, msg=msg, punish=punish.name, punishTime=punishTime)
                else:
                    checkForJunior = True


                if checkForJunior == False:
                    await msg.edit(content=f'**❌ Твой запрос не одобрили.**') 
                    return
    
                elif checkForJunior == True:
                    pass

                else:
                    await msg.edit(content=f'**❌ Тех. ошибка - пингуй ксова. `error #2463/1` **')
                    return
                
                await msg.edit(content=f'**🔄 Обрабатываю запросик :middle_finger:**')
                
            else:
                await msg.edit(content='❌ **Время вышло.**')

            logs = client.get_channel(LOGS)

            await msgToLOGG(ctx, worksheet, user, msgAuthor, rule=rule, reason=reason)
            emoji = (reaction.emoji)
            emoji = str(emoji)
            if reaction.emoji == '✅':             
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
                    
                    logs = client.get_channel(ERROR_ROOM)
                    await logs.send(f'⚠️ {ctx.user} записал себе варнчик')
                elif punish.value == 2:
                    profile = await get_user_profile(ctx.user.id)
                    user_id = ctx.user.id
                    new_value = profile['ban'] + 1
                    parameter = 'ban'
                    await set_user_profile(user_id, parameter, new_value)

                    logs = client.get_channel(ERROR_ROOM)
                    await logs.send(f'⛔ {ctx.user} записал себе банчик')
                else:
                    logs = client.get_channel(ERROR_ROOM)
                    await logs.send(f'❓ {ctx.user} что то сделал, и я должен был чёта записать... похуй)')
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
    
    if rule == None:
        await ctx.response.send_message('❌ Не корректно выбрано правило')
        return

    try:
        if 'Правило' in rule or 'правило' in rule:
            await ctx.response.send_message('❌ Не корректно выбрано правило, **используй только числа.**')
            return
    except:
        await ctx.response.send_message('❌ Не корректно выбрано правило, **используй только числа.**')
        return


    if 'рецедив' in rule.lower():
        rule = rule.lower()
        rule = rule.replace('рецедив', 'Рецидив')


    values_list = worksheet.col_values(2)

    
    try:
        await ctx.response.defer() # ephemeral=True
    except:
        await errorDeferMessage(ctx=ctx, errorValue='2294')
        return


    if user in values_list:
        user = f'{user}'
        await nextStep('old')
    elif (f'{user} ' in values_list):
        user = f'{user} '
        await nextStep('old')
    elif (f'{user}  ' in values_list):
        user = f'{user}  '
        await nextStep('old')
    else:
        await ctx.followup.send(f"⚠️ Игрок `{user}` не найден.")
        await nextStep('new')



@client.command()
async def log(ctx):

    if str(ctx.author) != 'ksov':
        return
    else:
        await ctx.message.add_reaction('✅')

        
    ctx = client.get_channel(1137687925925093459)
    await ctx.send(file=discord.File('loginfo.log'))



# @client.command()
# async def test(ctx):

#     embed = discord.Embed(
#         colour=discord.Colour.yellow(), 
#         description=f'**⚠️ Начал обновлять данные АХелпов у модераторов, возможно будут технические шоколадки. Бот может тормозить.**', 
#     )
#     msg = await ctx.send(embed=embed)
    

#     embed = discord.Embed(
#         colour=discord.Colour.green(), 
#         description=f'**✅ Обновил данные АХелпов у модераторов.**', 
#     )

#     await msg.edit(embed=embed)



async def checkAhelps(ctx):
    msg = client.get_channel(1139276548650848266)

    embed = discord.Embed(
        colour=discord.Colour.yellow(), 
        description=f'**⚠️ Начал обновлять данные АХелпов у модераторов, возможно будут технические шоколадки. Бот может тормозить.**', 
    )

    msg = await msg.send(embed=embed)

    def checkCkeys():
        with open('basa.json', 'r') as file:
            file = json.load(file)


        #listOfCkeys = []
        list2OfCkeys = {}

        for x in file:
            try:
                if file[x]['ckey'] != None:
                    #listOfCkeys.append(file[x]['ckey'])
                    list2OfCkeys.setdefault(file[x]['ckey'], x)
            except:
                pass
            
        print(f'Длина сикеев - {len(list2OfCkeys)}')
        return list2OfCkeys


    moders = checkCkeys()


    with open('basa.json', 'r') as file:
        wallets = json.load(file)
    
    for x in wallets:
        wallets[x].setdefault('ahelp', 0)
        wallets[x]['ahelp'] = 0 

    with open('basa.json', 'w') as file:
        json.dump(wallets, file)


    ahelp = client.get_channel(923319745019801661)
    m = [message async for message in ahelp.history(limit=LIMIT)]

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
            if str(x).lower() in str(m).lower():
                id = moders[x]
                modersCounters = await get_user_profile(id)

                modersCounters["ahelp"] += 1

                await set_user_profile(id, "ahelp", modersCounters["ahelp"])


    with open('basa.json', 'r') as file:
        wallets = json.load(file)
    
    for x in wallets:
        ahelps = wallets[x]['ahelp']
        try:
            ckey = wallets[x]['ckey']
        except:
            ckey = wallets[x].setdefault('ckey', None)
        
        if ckey != None:
            print(f'{ckey}: {ahelps}')




    embed = discord.Embed(
        colour=discord.Colour.green(), 
        description=f'**✅ Обновил данные АХелпов у модераторов.**', 
    )


    await msg.edit(embed=embed)

LIMIT = 31000



@client.command()
async def ahelp(ctx):

    if str(ctx.author) != 'ksov':
        return
    else:
        await ctx.message.add_reaction('✅')
    await checkAhelps(ctx=ctx)



@client.command()
async def xyu(ctx):
    if str(ctx.author) != 'ksov':
        return
    else:
        await ctx.message.add_reaction('✅')
    await cycle(ctx)


@client.tree.command(name = "созвать", description = "созывает весь твой отдел.", guild=discord.Object(id=GUILD))
async def call(ctx):

    authorRoles = ctx.user.roles

    access = discord.utils.find(lambda r: r.name == 'Смотритель Сервера', ctx.guild.roles)

    if access not in authorRoles:
        await ctx.response.send_message('**❌ У Вас нет доступа.**', ephemeral=True)
        return



    echoRole = discord.utils.find(lambda r: r.name == '☄️', ctx.guild.roles)
    elysiumRole = discord.utils.find(lambda r: r.name == '🌑', ctx.guild.roles)
    solarisRole = discord.utils.find(lambda r: r.name == '🌕', ctx.guild.roles)
    atharaRole = discord.utils.find(lambda r: r.name == '🌌', ctx.guild.roles)
    novaRole = discord.utils.find(lambda r: r.name == '🪐', ctx.guild.roles)
    mainRole = discord.utils.find(lambda r: r.name == '🚀', ctx.guild.roles)
    allRole = discord.utils.find(lambda r: r.name == '🍿', ctx.guild.roles)

    

    roles = [echoRole, elysiumRole, solarisRole, atharaRole, novaRole, mainRole, allRole]

    for x in authorRoles:
        if x in roles:
            await ctx.response.send_message('**✅ Будет сделано.**', ephemeral=True)
            channel = client.get_channel(ctx.channel.id)
            await channel.send(f'**{ctx.user} зовёт всех своих!** <@&{x.id}>')
            return
        
    await ctx.response.send_message('**❌ У Вас нет привязанность роли.**', ephemeral=True)

        



        
        
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