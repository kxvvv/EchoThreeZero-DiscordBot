import json


def openWallets():
    with open("basa.json", "r") as file:
        users_wallets = json.load(file)
    return users_wallets

def openAhelpBasa():
    with open("wallets.json", "r") as file:
        user_wallets = json.load(file)
    return user_wallets

basa = openWallets()
ahelpBasa = openAhelpBasa()

for x in basa.keys():
    basa[x].setdefault('ahelp', 0)
    basa[x].setdefault('discord', None)    

print(basa)

