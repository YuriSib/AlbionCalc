import requests
from bs4 import BeautifulSoup
import random
import asyncio
import json
import time

from fake_useragent import UserAgent
from playwright.async_api import async_playwright


xpath_resources = {
    "metal": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[1]''',
    "leather": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[2]''',
    "cloth": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[3]''',
    "wood": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[4]''',
    "stone": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[5]'''
}

town_click = {
            "Bridgewatch": -1,
            "Caerleon": 0,
            "Fort Sterling": 1,
            "Lymhurst": 2,
            "Martlock": 3,
            "Thetford": 4,
            "Brecilien": 5,
        }

xpath_other_towns = {
        'sale': '''//*[@id="__layout"]/div/div/section/div[3]/div[1]/div[7]/select''',
        'recycling': '''//*[@id="__layout"]/div/div/section/div[3]/div[1]/div[8]/select''',
        'materials': '''//*[@id="__layout"]/div/div/section/div[3]/div[1]/div[9]/select''',
        'resources': '''//*[@id="__layout"]/div/div/section/div[3]/div[1]/div[10]/select'''
}


async def click_other_towns(page, xpath_key, town_num):
    await page.locator(xpath_other_towns[xpath_key]).click()
    if town_num >= 0:
        await asyncio.sleep(2)
        for i in range(town_num):
            await page.keyboard.down('ArrowDown')
            await asyncio.sleep(1)
    else:
        await page.keyboard.down('ArrowUp')
    await asyncio.sleep(1)
    await page.keyboard.down("Enter")


async def get_html(xpath_resource, tax, other_towns_xpath=None, a_town=None):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()

        await page.goto('https://albion-profit-calculator.com/ru/refining', wait_until='load')

        await page.locator(xpath_resource).click()
        await asyncio.sleep(2)

        if other_towns_xpath:
            sale, recycling, materials, resources = other_towns_xpath[0], other_towns_xpath[1], other_towns_xpath[2], other_towns_xpath[3]

            await page.locator('''//*[@id="__layout"]/div/div/section/div[3]/div[1]/div[2]/label''').click()
            await asyncio.sleep(2)

            await click_other_towns(page, 'sale', sale)
            await click_other_towns(page, 'recycling', recycling)
            await click_other_towns(page, 'materials', materials)
            await click_other_towns(page, 'resources', resources)
        else:
            xpath_for_a_town = '''//*[@id="__layout"]/div/div/section/div[3]/div[1]/div[7]/select'''
            await click_other_towns(page, xpath_for_a_town, a_town)

        await page.locator('''//*[@id="__layout"]/div/div/section/div[3]/div[1]/div[4]/input''').click()
        await asyncio.sleep(1)
        for i in range(3):
            await page.keyboard.down('Backspace')
        await page.keyboard.insert_text(tax)
        await asyncio.sleep(3)

        html_content = await page.content()
        soup = BeautifulSoup(html_content, 'lxml')
        material_html = soup.find('div', {'class': 'item-table'})

        await browser.close()

    return material_html


async def material_pars(material_html) -> list:
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
    # xpath_resource = xpath_resources.get('leather')
    # other_towns_xpath = [town_click["Bridgewatch"], town_click["Martlock"], town_click["Martlock"], town_click["Thetford"]]
    # material_html = asyncio.run(get_html(xpath_resource, '1000', other_towns_xpath))
    # with open('output.html', 'w', encoding='utf-8') as file:
    #     file.write(str(material_html))

    with open('output.html', 'r', encoding='utf-8') as file:
        metal_html = BeautifulSoup(file.read(), 'lxml')

    print(material_pars(metal_html))
