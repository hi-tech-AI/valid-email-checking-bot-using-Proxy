from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import json

link = input('Please input Proxy link : ')
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

start = 1
while True:
    driver.get(link)
    proxies = driver.find_element(By.TAG_NAME, 'pre').text.split('\n')
    print(proxies)
    data = []
    for proxy in proxies[:]:
        data.append(proxy)
    with open(f'proxy{start}.json', 'w') as file:
        json.dump(data, file)
    start += 1
    if start == 143:
        break
    sleep(600)