from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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
from pyvirtualdisplay import Display

class Sender:

    def __init__(self, message, name_google_archive):
        self.pref = ''.join(random.sample(string.hexdigits, 8))
        self.message = message
        self.name_google_archive = name_google_archive
        self.src_img_qr = None
        self.driver = None
        self.display = Display(visible=0, size=(1024, 768))

    def connect(self):
        self.display.start()
        # Crear el perfil de firefox
        profile = webdriver.FirefoxProfile()
        # Dar las opciones de firefox para permitir el cambio de ventana con contenido en el dom
        profile.set_preference("dom.disable_beforeunload",True)
        profile.set_preference("javascript.enabled", False)
        # Crear el driver con las opciones que deseamos
        self.driver = webdriver.Firefox(profile)
        self.driver.maximize_window()
        # levantar el firefox controlado con la pagina web whatsapp
        self.driver.get("https://web.whatsapp.com/")

        return '''<meta http-equiv="refresh" content="0;URL='/good_connection'" />'''

    def get_qr(self):
        try:
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
        except:
            time.sleep(1)
            return self.get_qr()        

    def get_new_qr(self):
        change_page = False

        while not change_page:
            try:
                refresh_button = self.driver.find_element_by_xpath('//button[@class="HnNfm"]')
                self.driver.close()
                os.remove(self.pref+'_screenshot.png')
                os.remove(self.pref+'_crop.png')
                self.display.stop()
                return '''<meta http-equiv="refresh" content="0;URL='/error'" />'''
            except:
                pass
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
            # se crea el mensaje si se quiere 
            string = self.message.replace("(nombre)",(name['Nombre']))
            #se reemplaza (nombre) por nombre del contacto

            self.driver.get("https://web.whatsapp.com/send?phone="+str(name['Telefono']))
            print("https://web.whatsapp.com/send?phone="+str(name['Telefono']))
            print("acceder a pagina")
            time.sleep(10)
            self.driver.save_screenshot('screenshot.jpg')
            print("se guardo la pagina")
            msg_sended = False
            while not msg_sended:
                try:
                    inp_xpath = '//div[@class="pluggable-input-body copyable-text selectable-text"]'
                    input_box = self.driver.find_element_by_xpath(inp_xpath)
                    # se guarda el cuadro de texto por la class 
                    time.sleep(3)         
                    input_box.send_keys(string + Keys.ENTER)
                    # se manda la tecla enter y un mensaje ya creado
                    time.sleep(2)
                    msg_sended = True
                    print("envio de mensaje a "+name['nombre'])
                except:
                    time.sleep(5)
        # termina el ciclo y se termina la ejecucion del firefox zombie
        self.driver.close()
        self.display.stop()
        return '''<meta http-equiv="refresh" content="0;URL='/success'" />'''





