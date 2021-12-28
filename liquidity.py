import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def crawl(chrome_loc):
    url = "https://babyswap.info/pairs"
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1050")
    rule_name = '''<div class="sc-iRbamj bowFDd">(.*?)</div>'''
    rule_gen = '''<div class="sc-jhAzac iggPaB css-4cffwv">(.*?)</div>'''
    driver = webdriver.Chrome(executable_path=chrome_loc, chrome_options=options)
    driver.get(url)
    print("wait for data to load up")
    time.sleep(60)
    html = driver.page_source
    driver.find_elements_by_class_name('sc-gipzik')[1].click()
    time.sleep(1)
    html2 = driver.page_source
    driver.quit()
    res = html + "\n\n\n\n\n" + html2

    name = re.findall(rule_name, res, re.S)
    '''liquidity = re.findall(rule_liquidity, res, re.S)
    volume_24 = re.findall(rule_volume_24, res, re.S)
    volume_7 = re.findall(rule_volume_7, res, re.S)
    volume_fees = re.findall(rule_volume_fees, res, re.S)
    volume_1yfee = re.findall(rule_volume_1yfee, res, re.S)'''
    gen = re.findall(rule_gen, res, re.S)

    list = []
    for i in range(0, len(gen), 5):
        row_dict = {}
        row_dict["Name"] = name[i//5]
        row_dict["Liquidity"] = clean(gen[i])
        row_dict['Volume (24hrs)'] = clean(gen[i + 1])
        row_dict['Volume (7d)'] = clean(gen[i + 2])
        row_dict['Fees (24hr)'] = clean(gen[i + 3])
        row_dict['1y Fees / Liquidity'] = clean(gen[i + 4])
        list.append(row_dict)
    return list


def clean(string):
    cleaned = re.sub('<[^<]+?>', '', string).replace('\n', '').strip()
    return cleaned


def get_liquidity(coin, chrome_loc):
    list = crawl(chrome_loc)
    liquidity = 0
    for i in list:
        if coin in i["Name"]:
            str_liq = i["Liquidity"].strip("$").replace(",","")
            liquidity += int(str_liq)
    return liquidity


if __name__=="__main__":
    chrome_loc = './chromedriver'
    print(get_liquidity("MILK", chrome_loc))
