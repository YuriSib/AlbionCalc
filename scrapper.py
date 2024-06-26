import requests
from bs4 import BeautifulSoup
import random
import asyncio
import json
import time

from fake_useragent import UserAgent
from playwright.sync_api import Playwright, sync_playwright


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


xpath_resources = {
    "metal": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[1]''',
    "leather": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[2]''',
    "cloth": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[3]''',
    "wood": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[4]''',
    "stone": '''//*[@id="__layout"]/div/div/section/div[3]/div[2]/div/div[5]'''
}

html_dict = get_html(xpath_resources)
metal_html = html_dict.get('metal')
metal_list = metal_html.find_all('div', {'class': 'item-row'})
for i in metal_list:
    print(i)
    print('__________________________________________________________________________\n'*4)

