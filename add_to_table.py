import gspread
from oauth2client.service_account import ServiceAccountCredentials


def row_col_to_a1(row, col):
    """Преобразование координат строки и столбца в формат 'A1'."""
    letter = ''
    while col > 0:
        col, remainder = divmod(col - 1, 26)
        letter = chr(65 + remainder) + letter
    return f'{letter}{row}'


def add_value(material_data: [()]):
    gc = gspread.service_account(filename='creds.json')
    # sheet = gc.open("таблица расчета").get_worksheet(1)
    sheet = gc.open("Тест").sheet1

    for value in material_data:
        row = value['row']
        column = value['column']

        sheet.update_cell(row=row, col=column, value=value['value'])


    # if current_date in date_list:
    #     cur_row = date_list.index(current_date)
    # else:
    #     rows = sheet.get_all_values()
    #     cur_row = len(rows)
    #     sheet.update_cell(row=cur_row+1, col=1, value=current_date)
    #
    # last_min = sheet.cell(cur_row + 1, user_col).value
    # last_max = sheet.cell(cur_row + 1, user_col + 1).value
    #
    # last_table = sheet.cell(cur_row + 1, user_col + 2).value
    # if last_table:
    #     last_table_list = [table + '.xlsx' for table in last_table.split('.xlsx, ')]
    #     if table_name in last_table_list:
    #
    #
    # if last_table:
    #     last_table += ', '
    # else:
    #     last_table = ''
    # if not last_max:
    #     last_max, last_min = 0, 0
    # sheet.update_cell(row=cur_row + 1, col=user_col, value=int(last_min) + min_cost)
    # sheet.update_cell(row=cur_row + 1, col=user_col + 1, value=int(last_max) + max_cost)
    # sheet.update_cell(row=cur_row + 1, col=user_col + 2, value=last_table + table_name)

