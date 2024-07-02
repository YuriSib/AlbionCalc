import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials


async def row_col_to_a1(row, col):
    """Преобразование координат строки и столбца в формат 'A1'."""
    letter = ''
    while col > 0:
        col, remainder = divmod(col - 1, 26)
        letter = chr(65 + remainder) + letter
    return f'{letter}{row}'


async def add_value(material_data: list, resource: str):
    resource_coordinate = {
        "metal": (2, 2),
        "leather": (2, 13),
        "cloth": (24, 2),
        "wood": (24, 13),
        "stone": (46, 2)
    }
    start_row = resource_coordinate[resource][0]
    start_col = resource_coordinate[resource][1]

    gc = gspread.service_account(filename='creds.json')
    # sheet = gc.open("таблица расчета").get_worksheet(1)
    # sheet = gc.open("Тест").sheet1
    sheet = gc.open("таблица расчета").get_worksheet_by_id(121999378)

    for data in material_data:
        start_cell = await row_col_to_a1(start_row, start_col)
        sheet.update(start_cell, data)
        start_row += 4


if __name__ == "__main__":
    gc = gspread.service_account(filename='creds.json')
    sheet = gc.open("таблица расчета").get_worksheet_by_id(121999378)

    # cell_value = sheet.cell(75, 2).value
    # print(cell_value)
    list_table = []
    for i in range(5, 12):
        for j in range(23, 100):
            time.sleep(1)
            sheet.update_cell(row=j, col=i, value="")
