import discord
from datetime import datetime as dt
from pytz import timezone

async def juniorRequestFunc(client):
    request = client.get_channel(997923048403509308)
    ctx = client.get_channel(924285600608182292)

    m = [message async for message in request.history(limit=100)]
    
    m=reversed(m)
    requestCounter = 0
    requestDict = {}
    text = ""

    def whenCreated(createdDate):
        if dt.now().day == createdDate.day:
            return f'в {createdDate.hour}:{createdDate.minute}.'

        result = dt.now().day - createdDate.day

        if result == 1:
            dayWord = 'день'
        elif result <= 4:
            dayWord = 'дня'
        else:
            dayWord = 'дней'

        

        return f'{result} {dayWord} назад, в {createdDate.hour}:{createdDate.minute}.'
         

    for x in m:
        if x.embeds != []:

            if "ожидает одобрения" in x.embeds[0].title:
                requestCounter+=1
                requestDict[f"{requestCounter}"] = {'id': f'{x.id}', 'date': f'{whenCreated(x.created_at.astimezone(timezone("Europe/Moscow")))}'}

    titleText = f"Господа модераторы и модераторанесы, количество не одобренных запросов в <#997923048403509308> - {requestCounter}\n"


    for x in range(1, len(requestDict)+1):
        text += f'Запрос номер `{x}` - <#{requestDict[f"{x}"]["id"]}>, создан {requestDict[f"{x}"]["date"]}\n'

    if text == "":
        await ctx.send("Не обработанных запросов в <#997923048403509308> нет, хорошая работа, господа модераторы и модераторанесы.")
        return

    embed = discord.Embed(
        colour=discord.Colour.dark_blue(),
        description=text,
        title=titleText,
    )
    await ctx.send(embed=embed)