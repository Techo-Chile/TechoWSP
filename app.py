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

	def redirect_connecting(self):
		raise cherrypy.HTTPRedirect("./connecting")

	def redirect_qr(self, pref):
		raise cherrypy.HTTPRedirect("./wait_qr?pref="+pref)
		#return "<head><meta http-equiv='refresh' content='0; url=./wait_qr?pref="+pref+"' /></head>"

	def redirect_new_qr(self, pref):
		raise cherrypy.HTTPRedirect("./new_qr?pref="+pref)

	def redirect_working(self):
		raise cherrypy.HTTPRedirect("./working")

	def redirect_success(self):
		raise cherrypy.HTTPRedirect("./success")
	
	@cherrypy.expose
	@cherrypy.config(**{'response.stream': True})
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
	@cherrypy.config(**{'response.stream': True})
	def send_message(self,message, google_archive):
		self.sender = Sender(message,google_archive)
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
		yield self.sender.send_messages()

	@cherrypy.expose
	def success(self):
		return "envio exitoso"

     

	

if __name__ == '__main__':
	conf = {   "/images":
		 			{"tools.staticdir.on": True,
	                "tools.staticdir.dir": dir_path},
	}
	cherrypy.quickstart(Massive_Wsp(),'/',config=conf)
