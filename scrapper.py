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
    material_data = []
    col_num = 1
    row_num = 1
    for div in metal_list:
        data = div.find_all('div', {'data-v-46ecdbca': True})
        data_list = [block for block in data if len(block.get_text(strip=True)) < 10]

        for data in data_list:
            if 'class="success"' in str(data):
                time_ = {'value': data.get_text(strip=True), 'row': row_num, 'column': col_num + 1}
                material_data.append(time_)
                print(time_)
                row_num += 1
            else:
                cost = {'value': data.get_text(strip=True), 'row': row_num, 'column': col_num}
                material_data.append(cost)
                print(cost)

            if data.get_text(strip=True) == '-':
                print('**************************************')

                col_num += 2
                row_num -= 4

        col_num -= 10
        row_num += 4

        print('__________________________________________________________________________\n'*4)
    return material_data


if __name__ == "__main__":
    # html_dict = get_html(xpath_resources)
    # metal_html = html_dict.get('metal')
    # with open('output.html', 'w', encoding='utf-8') as file:
    #     file.write(str(metal_html))

    with open('output.html', 'r', encoding='utf-8') as file:
        metal_html = BeautifulSoup(file.read(), 'lxml')

    print(material_pars(metal_html))
