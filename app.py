import cherrypy
from Sender import *
import threading
import sys

class Massive_Wsp():
	def __init__(self):
		pass
	
	@cherrypy.expose
	def index(self):
		return """<html>
          <head></head>
          <body>
            <form method="get" action="send_message" id = "sender">
              Mensaje: <textarea rows="4" cols="50" name="message" form="sender">Ingrese su mensaje</textarea>
              <br>
              Nombre Archivo: <input type="text" name="google_archive">
              <br>
              <button type="submit">Enviar</button>
            </form>
          </body>
        	</html>"""



	@cherrypy.expose
	def send_message(self,message, google_archive):
		t = threading.Thread(target=Sender().send_messages,args=(message,google_archive,self,))
		t.start()
		return "ingresando a web.whatsapp.com"

	@cherrypy.expose
	def wait_qr(self, pref):
		print("wait_qr")
		img = pref+"_crop.png"
		return """Escanee la imagen QR:
    		<br><br>
    		<img src="""+img+""">"""

	@cherrypy.expose
	def working(self):
		return "QR aceptada"

	@cherrypy.expose
	def success(self):
		return "envio exitoso"

    

	

if __name__ == '__main__':
    cherrypy.quickstart(Massive_Wsp())
