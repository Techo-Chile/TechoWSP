

Al acceder a Digital Ocean, en la parte superior habrá un enlace que se llama "Droplets"
Al pulsarlo aparecer la litsa de droplets, el script esta almacenado en el techo-wsp.

En "more" hay una opcion que dice "Acces console", ahi se puede acceder directamente a la consola

En caso de que quieras añadir una llave ssh para acceder:
https://cloud.digitalocean.com/settings/security -> SSH KEYS

El computador que ocupaba yo: PC-041 ya tenia la llave ssh activada. Para acceder:
$ ssh root@159.89.178.93

Al entrar al servidor:
el directorio es: /root/techo/TechoWSP. Para ingresar al directorio:
$ cd /root/techo/TechoWSP

Se creo una "screen" esta screen simula una bash de ubuntu.
mas info de screen: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-screen-on-an-ubuntu-cloud-server

Para acceder a la screen donde esta corriendo el script:
$ screen -r
debido a que solo hay una se deberia acceder directamente. 

Para cerrar la screen (sin detener el proceso):
Ctrl-a d

El acceso a esta screen seria ideal solo usarla para saber si el codigo esta corriendo.

Para actualizar el codigo se recomienda usar github:
Se esta usando el siguiente repositorio: https://github.com/Teho-Chile/TechoWSP
El proyecto esta actualizado con branch_jorge
Se recomienda usar otra branch.

Actualizar el codigo en el computador, hacer add, commit y push
luego en el servidor (fuera de la screen) hacer pull
Al modificar el script, este sigue corriendo, acceder a la screen para verificar si es asi:

$ screen -r

cerrar screen(sin detener proceso):
ctr-a d

En caso contrario, para hacerlo correr: 

$ python3 app.py 

En el directorio

