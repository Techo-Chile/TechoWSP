from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import time
# Crear el perfil de firefox
profile = webdriver.FirefoxProfile()
# Dar las opciones de firefox para permitir el cambio de ventana con contenido en el dom
profile.set_preference("dom.disable_beforeunload",True)
profile.set_preference("javascript.enabled", False)
# Crear el driver con las opciones que deseamos
driver = webdriver.Firefox(profile)
# levantar el firefox controlado con la pagina web whatsapp
driver.get("https://web.whatsapp.com/")
time.sleep(10)
# todo lo que pasa axa es para que el usuario pueda escanear el codigo QR se puede aumentar si se prefiere pero esto yo lo encontre optimo

# termina el ciclo y se termina la ejecucion del firefox zombie
driver.close()



