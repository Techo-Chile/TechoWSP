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
time.sleep(3)
# todo lo que pasa axa es para que el usuario pueda escanear el codigo QR se puede aumentar si se prefiere pero esto yo lo encontre optimo
scope = ['https://spreadsheets.google.com/feeds']
# se cargan las credenciales del json
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
# se "obtiene" el excel en este script se le pasa el nombre por argumentos en esta version pero cambiando el metodo puede por el link ACORDARSE COMPARTIR EL DOCUMENTO 
# con el usuario que se creo en el client secret o con el usuario de que son las credenciales
sheet = client.open(str(sys.argv[1])).sheet1
# tomar contenido del shet y guardalo en una variable
list_of_hashes = sheet.get_all_records()
pat = re.compile(r'\s+')
# ciclo 
for name in list_of_hashes:
    # se crea el mensaje si se quiere crear un mensaje tipo se agrega a esta cadena
    string = "Hola "+str(name['Nombre'])
    driver.get("https://web.whatsapp.com/send?phone="+pat.sub('',str(name['Telefono']))+"")
    # se guarda el cuadro de texto por la class 
    inp_xpath = '//div[@class="pluggable-input-body copyable-text selectable-text"][@dir="auto"][@data-tab="1"]'
    wait = WebDriverWait(driver, 600)
    input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))   
    # se manda la tecla enter y un mensaje ya creado         
    input_box.send_keys(string + Keys.ENTER)
    time.sleep(4)
# termina el ciclo y se termina la ejecucion del firefox zombie
driver.close()



