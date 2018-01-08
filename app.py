import cherrypy
from Sender import *
import threading
import sys
import os
import time
dir_path = os.path.dirname(os.path.realpath(__file__))

class Massive_Wsp(object):

	def __init__(self):
		self.sender = None
		self.bussy = False

	@cherrypy.expose
	@cherrypy.config(**{'response.stream': True})
	def index(self):
		link = 'https://docs.google.com/a/techo.org/spreadsheets/d/1Y_uVPcS4eV9iscZ_aThzTJFMn26hxFC6wRZT1jNOCOU/edit?usp=sharing'
		if not self.bussy:
			return """<html>
          <head></head>
          <body>
          	<h1> Bienvenido a wsp-masivo Techo</h1>
          	<h2> Instrucciones:</h2>
          	<ol>
          	<li>Realice una copia de <a href='"""+link+"""'>esta </a>planilla en su drive personal</li>
          	<li>Llene su planilla con los nombres y los números</li>
          	<li>Comparta su planilla con: masivo@wsp-masivo.iam.gserviceaccount.com</li>
          	<li>Ingrese mensaje y el nombre de la planilla</li>
          	Nota: Si desea ingresar el nombre de la persona a enviar el mensaje
          	debe colocar "(nombre)".<br>
          	El sistema reemplazará (nombre) por el nombre del contacto en la planilla
          	<br>
          	
          	
            <form method="get" action="send_message" id = "sender">
              Mensaje: <textarea rows="4" cols="50" name="message" form="sender">Hola (nombre) ...</textarea>
              <br>
              Nombre Planilla: <input type="text" name="google_archive">
              <br>
              <li>Presione boton Enviar y luego escanee el codigo QR</li>
              <button type="submit">Enviar</button>
            </form>
            </ol>
          </body>
        	</html>"""	
		else:
			return "Sistema en uso, intentelo en otro momento porfavor"


	@cherrypy.expose
	@cherrypy.config(**{'response.stream': True})
	def send_message(self,message, google_archive):
		self.bussy = True
		self.sender = Sender(message,google_archive, self)
		#return self.sender.send_messages(message,google_archive,self)
		yield "conectando con whatsap web"
		yield self.sender.connect()

	@cherrypy.expose
	@cherrypy.config(**{'response.stream': True})
	def good_connection(self):
		yield "Conexion realizada con exito"
		yield self.sender.get_qr()


	@cherrypy.expose
	@cherrypy.config(**{'response.stream': True})
	def wait_qr(self, pref):
		img = pref+"_crop.png"
		yield """Escanee la imagen QR:
    		<br><br>"""+'<img src="images/'+img+'" border = "0"/>'
		time.sleep(1)
		yield self.sender.get_new_qr()

	@cherrypy.expose
	@cherrypy.config(**{'response.stream': True})
	def new_qr(self, pref):
		img = pref+"_crop.png"
		yield """La imagen QR cambió:
    		<br><br>"""+'<img src="images/'+img+'" border = "0"/>'
		yield self.sender.get_new_qr()

	@cherrypy.expose
	@cherrypy.config(**{'response.stream': True})
	def working(self):
		yield "QR aceptada"
		yield "<br> <h2>Revise la planilla para saber el estado de los envios</h2>"
		yield self.sender.send_messages()

	@cherrypy.expose
	def success(self):
		self.bussy = False
		return "envio exitoso"

	@cherrypy.expose
	def error(self):
		self.bussy = False
		ans = "hubo un error, vuelva a intentar el envio:<br>"
		ans += '<a href="/index">inicio</a>'
		return ans
	

if __name__ == '__main__':
	conf = {   "/images":
		 			{"tools.staticdir.on": True,
	                "tools.staticdir.dir": dir_path},
	}
	cherrypy.config.update({'server.socket_host': '0.0.0.0',})
	cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
	cherrypy.quickstart(Massive_Wsp(),'/',config=conf)
