#!/usr/bin/python3
# -*- coding: utf-8 -*-
#import csv
#import json
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import pytz

#Requirements: BeautifulSoup, Selenium

#TODO: use Panda dataframe

def get_converted_price(price):

    # stripped_price = price.strip("₹ ,")
    # replaced_price = stripped_price.replace(",", "")
    # find_dot = replaced_price.find(".")
    # to_convert_price = replaced_price[0:find_dot]
    # converted_price = int(to_convert_price)
    converted_price = float(re.sub(r"[^\d.]", "", price)) # Thanks to https://medium.com/@oorjahalt
    return converted_price


def extract_url(url):

    if url.find("www.amazon.com") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.com" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.com" + url[index:index2]
            else:
                url = None
    else:
        url = None
    return url


def get_product_details(urls):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0"
    }
    dList = []
    for d in range(len(urls)):
        dList.append({"name": "", "price": 0, "deal": True, "url": "", "time":""})
    _url = extract_url(urls[0])
    
    if _url is None:
        details = None
    else:
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        browser = webdriver.Firefox(firefox_options=fireFoxOptions)
        itind = 0
        #page = requests.get(_url, headers=headers)
        for _url in urls:
            r = browser.get(_url)
            delay = 5 # seconds
            try:
                myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'priceblock_ourprice')))
                print ("Page is ready!")
                #print (myElem.text)
            except TimeoutException:
                print ("Loading took too much time!")
            soup = bs(browser.page_source.encode(encoding='utf-8',errors='replace'), "html.parser")
            #soup = BeautifulSoup(page.content, "html5lib")
            #print(browser.page_source.encode(encoding='utf-8',errors='replace'))
            title = soup.find(id="productTitle")
            price = soup.find(id="priceblock_dealprice")
            if price is None:
                price = soup.find(id="priceblock_ourprice")
                dList[itind]["deal"] = False
            if title is not None and price is not None:
                dList[itind]["name"] = title.get_text().strip()
                dList[itind]["price"] = get_converted_price(price.get_text())
                dList[itind]["url"] = _url
                local_tz = pytz.timezone ("Asia/Hong_Kong")
                dList[itind]["time"] = datetime.now(local_tz).strftime("%d/%m/%Y %H:%M:%S %Z")
                #dList.append(details)
                itind += 1
                #print(details)
            else:
                details = None
                #dList.append("")
                dList[itind]["name"] = "Not found"
                dList[itind]["price"] = 0
                dList[itind]["url"] = _url
                local_tz = pytz.timezone ("Asia/Hong_Kong")
                dList[itind]["time"] = datetime.now(local_tz).strftime("%d/%m/%Y %H:%M:%S %Z")
                itind += 1
                print("price not found")
        browser.quit()
    return dList

#aProductCode = ["B088HHZBGJ","B094681RZP","B094658SMY"]
#aProductUrl = ["https://www.amazon.com/dp/B094681RZP","https://www.amazon.com/dp/B094658SMY"]
df = pd.read_csv("list.csv")
aProductUrl = []
for code in df["Item Code"]:
    aProductUrl.append("https://www.amazon.com/-/en/dp/"+code)
    print(aProductUrl[-1])
ListedItem = []
filename = "AmazonList.csv"

productList = get_product_details(aProductUrl)
df = pd.DataFrame(productList, columns = ['name','price','deal','url','time'])
df.to_csv(filename, index=False, mode="a", header=False)


"""TODO: Flask server with plotting"""
