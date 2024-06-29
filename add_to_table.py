import gspread
from oauth2client.service_account import ServiceAccountCredentials


def row_col_to_a1(row, col):
    """Преобразование координат строки и столбца в формат 'A1'."""
    letter = ''
    while col > 0:
        col, remainder = divmod(col - 1, 26)
        letter = chr(65 + remainder) + letter
    return f'{letter}{row}'


def add_value(material_data: list, start_row: int):
    gc = gspread.service_account(filename='creds.json')
    # sheet = gc.open("таблица расчета").get_worksheet(1)
    sheet = gc.open("Тест").sheet1

    start_col = 2
    for data in material_data:
        start_cell = row_col_to_a1(start_row, start_col)
        sheet.update(start_cell, data)
        start_row += 4


# gc = gspread.service_account(filename='creds.json')
# sheet = gc.open("таблица расчета").get_worksheet(1)
#
# cell_value = sheet.cell(75, 2).value
# print(cell_value)
# sheet.update_cell(row=100, col=2, value="test")
