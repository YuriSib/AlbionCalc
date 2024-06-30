import requests
from bs4 import BeautifulSoup
import random
import asyncio
import json
import time

from fake_useragent import UserAgent
from playwright.sync_api import sync_playwright


xpath_resources = {
    "metal": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[1]''',
    "leather": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[2]''',
    "cloth": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[3]''',
    "wood": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[4]''',
    "stone": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[5]'''
}


def get_html(xpath_dict: dict):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto('https://albion-profit-calculator.com/ru/refining', wait_until='load')

        html_dict = {}
        for key, xpath in xpath_dict.items():
            page.locator(xpath).click()
            time.sleep(4)
            html_content = page.content()
            soup = BeautifulSoup(html_content, 'lxml')
            material_html = soup.find('div', {'class': 'item-table'})
            html_dict[key] = material_html
        browser.close()

    return html_dict


def material_pars(material_html) -> list:
    metal_list = material_html.find_all('div', {'class': 'item-row'})
    col_num = 1
    row_num = 1
    full_data = []
    for div in metal_list:
        data = div.find_all('div', {'data-v-46ecdbca': True})
        data_list = [block for block in data if len(block.get_text(strip=True)) < 15]
        row_1, row_2, row_3, row_4 = [], [], [], []
        distribution = {1: row_1, 2: row_2, 3: row_3, 4: row_4}

        data_ = []
        error_flag = False
        for data in data_list:
            if error_flag:
                error_flag = False
                row_num += 1
                continue

            if row_num == 5:
                print(row_num)

            if 'class="success"' in str(data) or 'class="error"' in str(data):
                time_ = data.get_text(strip=True)
                if time_ == '0':
                    distribution[row_num].append('0')
                    distribution[row_num].append('∞')
                    error_flag = True
                else:
                    distribution[row_num].append(time_)
                    row_num += 1
            else:
                cost = data.get_text(strip=True)
                distribution[row_num].append(cost)

            if data.get_text(strip=True) == '-':
                col_num += 2
                row_num = 1

        data_.append(row_1)
        data_.append(row_2)
        data_.append(row_3)
        data_.append(row_4)
        full_data.append(data_)

        col_num -= 10
        row_num = 1
    return full_data


if __name__ == "__main__":
    # html_dict = get_html(xpath_resources)
    # metal_html = html_dict.get('metal')
    # with open('output.html', 'w', encoding='utf-8') as file:
    #     file.write(str(metal_html))

    with open('output.html', 'r', encoding='utf-8') as file:
        metal_html = BeautifulSoup(file.read(), 'lxml')

    print(material_pars(metal_html))
