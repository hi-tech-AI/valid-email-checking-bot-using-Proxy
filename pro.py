import json

def txtToJson():
    with open('proxy.json', 'r') as file:
        proxy_datas = json.load(file)
        proxy_data = proxy_datas.get('proxies', [])

    proxies = []
    for item in proxy_data:
        proxy_address = item['proxy']
        proxies.append(proxy_address)

    with open('proxy.json', 'w') as file:
        json.dump(proxies, file)


def main():
    for line_number, line in enumerate(lines, 1):
        options = Options()
        
        # Pick a random proxy from the list and determine its type
        random_proxy = random.choice(proxies)
        proxy_type, proxy_address = random_proxy.split("://") if "://" in random_proxy else ("http", random_proxy)

        # Set proxy based on its type
        if proxy_type.lower() == 'socks4':
            options.add_argument(f'--proxy-server=socks4://{proxy_address}')
        elif proxy_type.lower() == 'socks5':
            options.add_argument(f'--proxy-server=socks5://{proxy_address}')
        else:  # default to http if not specified
            options.add_argument(f'--proxy-server={proxy_address}')
        
        # Set the default timeout for page load
        options.page_load_strategy = 'eager'
        
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)  # set the page load timeout to 30 seconds
        
        try:
            print(f'Using proxy: {random_proxy}')
            print(f'Email{line_number}: {line.strip()}')
            driver.get('https://www.netflix.com/')
            
            # Add the rest of the code here to interact with the Netflix login page
            
        except TimeoutException:
            print(f'Timeout occurred while trying with proxy: {random_proxy}')
            # Handle the timeout exception as needed
        except WebDriverException as e:
            print(f'WebDriverException occurred: {str(e)}')
            # Handle other WebDriver exceptions that may occur
        finally:
            driver.quit()  # Ensure the driver is closed in all scenarios

if __name__ == "__main__":
    main()
