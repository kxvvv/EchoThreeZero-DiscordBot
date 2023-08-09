import gspread
from config import *


async def whatColorYouNeed(row, UserWarnBan='None'):

    gc = gspread.service_account(filename='secretkey.json')
    sh = gc.open(SHEET)
    worksheet = sh.sheet1


    row -= 1
    if UserWarnBan == 'User':
        value = 1

    metadata = sh.fetch_sheet_metadata({"includeGridData": "true"})
    sheets = metadata["sheets"]
    worksheet = [s for s in sheets if s["properties"]["sheetId"] == 0][0]

    cell_data = worksheet["data"]
    cell_user = cell_data[0]["rowData"][row]["values"][value]

    b3_background_color = cell_user["effectiveFormat"]["backgroundColor"]

    if cell_user != None:
        red = b3_background_color['red'] * 100
        green = b3_background_color['green'] * 100
        blue = b3_background_color['blue'] * 100
    else:
        red = 0
        green = 0
        blue = 0

    red = int(red)
    green = int(green)
    blue = int(blue)

    rgb = (f'{red}', f'{green}',f'{blue}')

    rgb = tuple(int(int(s) * 2.55) for s in rgb)

    return rgb, cell_data