import gspread








gc = gspread.service_account(filename='secretkey.json')
sh = gc.open("Коквакс новая таблица банов 2.0")
worksheet = sh.sheet1




values_list = worksheet.col_values(2)

a = values_list

import collections
listOfDub = [item for item, count in collections.Counter(a).items() if count > 1]


for x in listOfDub:
    if x != '':
        print(x)
