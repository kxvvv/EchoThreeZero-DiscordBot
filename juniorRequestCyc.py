import discord

async def juniorRequestFunc(client):
    request = client.get_channel(997923048403509308)
    ctx = client.get_channel(924285600608182292)

    m = [message async for message in request.history(limit=100)]
    
    m=reversed(m)
    requestCounter = 0
    requestDict = {}
    text = ""

    for x in m:
        if x.embeds != []:

            if "ожидает одобрения" in x.embeds[0].title:
                requestCounter+=1
                requestDict[f"{requestCounter}"] = f"{x.id}"

    titleText = f"Господа модераторы и модераторанесы, количество не одобренных запросов в <#997923048403509308> - {requestCounter}\n"


    for x in range(1, len(requestDict)+1):
        text += f"Запрос номер `{x}` - <#" + requestDict[f"{x}"] + ">\n"

    if text == "":
        await ctx.send("Не обработанных запросов в <#997923048403509308> нет, хорошая работа, господа модераторы и модераторанесы.")
        return

    embed = discord.Embed(
        colour=discord.Colour.dark_blue(),
        description=text,
        title=titleText,
    )
    await ctx.send(embed=embed)