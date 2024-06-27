from bs4 import BeautifulSoup

from scrapper import material_pars, xpath_resources
from add_to_table import add_value


with open('output.html', 'r', encoding='utf-8') as file:
    metal_html = BeautifulSoup(file.read(), 'lxml')

material_data = material_pars(metal_html)
print(material_data)


def row_col_to_a1(row, col):
    """Преобразование координат строки и столбца в формат 'A1'."""
    letter = ''
    while col > 0:
        col, remainder = divmod(col - 1, 26)
        letter = chr(65 + remainder) + letter
    return f'{letter}{row}'


material = []
mini_block = []
block_row = []
full_block = []

row_1, row_2, row_3, row_4 = [], [], [], []
for i in material_data:
    row, column, value = i['row'], i['column'], i['value']
    if row == 2:
        row_1.append(value)
    elif row == 3:
        row_2.append(value)
    elif row == 4:
        row_3.append(value)
    elif row == 5:
        row_4.append(value)

print(row_1)
print(row_2)
print(row_3)
print(row_4)

#     if (material_data.index(i)+1) % 2 == 1:
#         material.append(i['value'])
#     else:
#         material.append(i['value'])
#         mini_block.append(material)
#         material = []
#
#     if i['value'] == '-':
#         block_row.append(mini_block)
#         mini_block = []
#
#     if len(block_row) == 5:
#         full_block.append(block_row)
#         block_row = []
#         cnt = 1
#
#
# print(full_block)
#
# for block in full_block:
#     row_1 = [row[0] for row in block]
#     row_2 = [row[1] for row in block]
#     row_3 = [row[2] for row in block]
#     row_4 = [row[3] for row in block]
#
#     print(row_1)
#     print(row_2)
#     print(row_3)
#     print(row_4)


# add_value(material_data)
