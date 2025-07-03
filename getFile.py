from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from user_pass import user_pass
import json
import re
import subprocess

def do():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--headless=new")

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    service = Service(ChromeDriverManager().install())
    service.creationflags = subprocess.CREATE_NO_WINDOW
    service.startupinfo = startupinfo

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://schoolnet.colegium.com/webapp/es_CL/login")
        time.sleep(2)
        username = driver.find_element(By.NAME, "signin[username]")
        password = driver.find_element(By.NAME, "signin[password]")
        username.send_keys(list(user_pass.user_pass.keys())[0])
        password.send_keys(list(user_pass.user_pass.values())[0])
        password.send_keys(Keys.RETURN)
        time.sleep(4)
        driver.get("https://schoolnet.colegium.com/webapp/es_CL/calificaciones/index?tipocalificacion=nota")
        time.sleep(3)
        html = driver.page_source
        match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL)
        if match:
            body_content = match.group(1).strip()
            try:
                data = json.loads(body_content)
                return data
            except json.JSONDecodeError:
                print('no es un json valido')
    finally:
        driver.quit()
