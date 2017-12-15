# TechoWSP
Spam whatsaap web get name and phone in google drive

## ¿Que es?
es un script python que toma numeros y nombre de una hoja de calculo de google (mediante 0auth2 client) en este script se pasa las credenciaes por un JSON que por seguridad no viene en el repositorio  para despues abrir un navegador controlado por la libreria selemiun para despues hacer la manipulacion de dom para abrir el contacto con ese numero aun que no lo tengas guardado en whatsapp web, despues carga  un mensaje que en esta version de script lo toma del excel pero se puede pasar por parametro facilmente(o por un GUI)


## ¿Que hacer?
habilitar las credenciales de google 0auth en un json o crear un client secret (esto se realizo pero no se manda el client secret)  compartir el documento con el usuario que se habilitan sus credenciales para el uso de una aplicacion

pip install selemiun
pip install oauth2client
python nombredelarchivo.py 'nombre del doc' 

## Pendientes 
GUI
Mejor Codigo
MEJOR ORTOFRAFIA!! (perdon por eso)
