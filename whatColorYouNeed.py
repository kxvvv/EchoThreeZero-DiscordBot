import gspread
import gspread_formatting as gf

from gspread_formatting import *
from config import *


async def whatColorYouNeed(row, UserWarnBan='None'):

    gc = gspread.service_account(filename='secretkey.json')
    sh = gc.open(SHEET)
    worksheet = sh.sheet1



    if UserWarnBan == 'User':
        pass
    else:
        if UserWarnBan == 'None':
            print(f"UWB - {UserWarnBan}")
            rgb = (255, 255, 255)
            return rgb
        else:
            print(f"UWB2 - {UserWarnBan}")
            rgb = (255, 255, 255)
            return rgb

    if UserWarnBan == 'User':
        text = 'B' + str(row)
    
    

    gfs2 = gf.get_user_entered_format(worksheet, text)

    try:
        red = gfs2.backgroundColor.red * 100
        green = gfs2.backgroundColor.green * 100
        blue = gfs2.backgroundColor.blue * 100
    except:
        red = 100
        green = 100
        blue = 100

    red = int(red)
    green = int(green)
    blue = int(blue)

    rgb = (f'{red}', f'{green}',f'{blue}')

    rgb = tuple(int(int(s) * 2.55) for s in rgb)

    return rgb
