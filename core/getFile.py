from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import re
import subprocess


def do(username, password, period):
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

        driver.find_element(By.NAME, "signin[username]").send_keys(username)
        driver.find_element(By.NAME, "signin[password]").send_keys(password + Keys.RETURN)
        time.sleep(4)

        data = {}
        periods = [1, 2] if period == '1+2' else [int(period)]
        
        for i in periods:
            driver.get(f"https://schoolnet.colegium.com/webapp/es_CL/calificaciones/index?periodo={i}")
            time.sleep(3)
            html = driver.page_source
            match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL)
            if match:
                body_content = match.group(1).strip()
                try:
                    data[f'period_{i}'] = json.loads(body_content)
                except json.JSONDecodeError as err:
                    raise Exception(f"Error al procesar el periodo {i}: {err}")

        driver.get("https://schoolnet.colegium.com/webapp/es_CL/companeros/index")
        time.sleep(3)
        html = driver.page_source
        match = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL)
        if match:
            body_content = match.group(1).strip()
            try:
                classmates = json.loads(body_content)
            except json.JSONDecodeError as err:
                raise Exception(f"Error al procesar los compañeros: {err}")

        return {'data': data, 'classmates': classmates}

    finally:
        driver.quit()
    