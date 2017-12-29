from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import *
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import time
from PIL import Image
import random
import string
import os
from app import *

class Sender:

    def __init__(self, message, name_google_archive):
        self.pref = ''.join(random.sample(string.hexdigits, 8))
        self.message = message
        self.name_google_archive = name_google_archive
        self.src_img_qr = None
        self.driver = None

    def connect(self):
        # Crear el perfil de firefox
        profile = webdriver.FirefoxProfile()
        # Dar las opciones de firefox para permitir el cambio de ventana con contenido en el dom
        profile.set_preference("dom.disable_beforeunload",True)
        profile.set_preference("javascript.enabled", False)
        # Crear el driver con las opciones que deseamos
        self.driver = webdriver.Firefox(profile)
        # levantar el firefox controlado con la pagina web whatsapp
        self.driver.get("https://web.whatsapp.com/")

        return '''<meta http-equiv="refresh" content="0;URL='/good_connection'" />'''

    def get_qr(self):
        img_qr = self.driver.find_element_by_xpath("//img[@alt='Scan me!']")
        self.src_img_qr = img_qr.get_attribute("src")
        self.driver.get_screenshot_as_file(self.pref+'_screenshot.png')
        pos = img_qr.location
        siz = img_qr.size
        x_i = pos['x'] - 15
        y_i = pos['y'] - 15
        x_f = int(siz['width'] + 15 + pos['x'])
        y_f = int(siz['height'] + 15 + pos['y'])
        img = Image.open(self.pref+'_screenshot.png')
        img2 = img.crop((x_i,y_i,x_f,y_f))
        img2.save(self.pref+'_crop.png')

        return '''<meta http-equiv="refresh" content="0;URL='/wait_qr?pref='''+self.pref+'''" />'''

    def get_new_qr(self):
        change_page = False

        while not change_page:
            try:
                new_img = self.driver.find_element_by_xpath("//img[@alt='Scan me!']")
                if new_img.get_attribute("src") != self.src_img_qr:
                    print("change image QR")
                    img_qr = self.driver.find_element_by_xpath("//img[@alt='Scan me!']")
                    self.src_img_qr = img_qr.get_attribute("src")
                    self.driver.get_screenshot_as_file(self.pref+'_screenshot.png')
                    pos = img_qr.location
                    siz = img_qr.size
                    x_i = pos['x'] - 15
                    y_i = pos['y'] - 15
                    x_f = int(siz['width'] + 15 + pos['x'])
                    y_f = int(siz['height'] + 15 + pos['y'])
                    img = Image.open(self.pref+'_screenshot.png')
                    img2 = img.crop((x_i,y_i,x_f,y_f))
                    img2.save(self.pref+'_crop.png')
                    return '''<meta http-equiv="refresh" content="0;URL='/new_qr?pref='''+self.pref+'''" />'''
            except:
                change_page = True
        return '''<meta http-equiv="refresh" content="0;URL='/working'" />'''
            
    def send_messages(self):
        print("entry page")

        os.remove(self.pref+'_screenshot.png')
        os.remove(self.pref+'_crop.png')
        print("remove images")
        #borra los archivos creados

        scope = ['https://spreadsheets.google.com/feeds']
        # se cargan las credenciales del json
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
        # se "obtiene" el excel en este script se le pasa el nombre por argumentos en esta version pero cambiando el metodo puede por el link ACORDARSE COMPARTIR EL DOCUMENTO 
        # con el usuario que se creo en el client secret o con el usuario de que son las credenciales
        sheet = client.open(self.name_google_archive).sheet1
        # tomar contenido del shet y guardalo en una variable
        list_of_hashes = sheet.get_all_records()
        pat = re.compile(r'\s+')
        # ciclo 
        for name in list_of_hashes:
            # se crea el mensaje si se quiere crear un mensaje tipo se agrega a esta cadena
        
            string = self.message.replace("(nombre)",(name['Nombre']))
            #se reemplaza (nombre) por nombre del contacto

            self.driver.get("https://web.whatsapp.com/send?phone="+pat.sub('',str(name['Telefono']))+"")
            # se guarda el cuadro de texto por la class 
            inp_xpath = '//div[@class="pluggable-input-body copyable-text selectable-text"][@dir="auto"][@data-tab="1"]'
            wait = WebDriverWait(self.driver, 600)
            input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))   
            # se manda la tecla enter y un mensaje ya creado
            time.sleep(3)         
            input_box.send_keys(string + Keys.ENTER)
            time.sleep(2)
        # termina el ciclo y se termina la ejecucion del firefox zombie
        self.driver.close()
        return '''<meta http-equiv="refresh" content="0;URL='/success'" />'''





