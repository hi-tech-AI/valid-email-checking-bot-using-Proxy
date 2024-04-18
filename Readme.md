# Netflix Account Automation Script

## Description
This Python script automates the process of logging into Netflix accounts using Selenium. It reads a list of email addresses from a file, generates random passwords, and attempts to log in to each account.

## Prerequisites
- Python 3.12
- Selenium
- Chrome WebDriver
- Random
- Time

## Installation
1. Install Python 3.12 from [python.org](https://www.python.org/).
2. Install Selenium using pip:
pip install selenium
3. Download Chrome WebDriver from [ChromeDriver Downloads](https://googlechromelabs.github.io/chrome-for-testing/#stable) and add it to your system PATH.

## Usage
1. Create a file named `email.txt` with a list of email addresses.
2. Run the script and follow the instructions to input the proxy link.
py main_single_thread.py
3. The script will attempt to log in to each Netflix account using random proxies and passwords.

## Notes
- Make sure to handle the output files `valid_email.txt` and `invalid_email.txt` as per your requirements.
- Use this script responsibly and ensure compliance with Netflix's terms of service.

## Disclaimer
This script is for educational purposes only. Use it at your own risk.
Feel free to customize this template with more specific details about your project. Let me know if you need any further assistance!