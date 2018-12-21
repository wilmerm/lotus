"""
Declaración de las variables globales que se 
utilizarán en la aplicación.
"""

import os
from fuente.var import *
from fuente.translation import gettext as _



# Rutas del proyecto. -----------------------------------

PATH_RESOURCE = "resource"
PATH_IMG = os.path.join(PATH_RESOURCE, "img")
PATH_DATABASE = "db"




# Imágenes. ----------------------------------------------

def imgpath(name):
    return os.path.join(PATH_IMG, name)


IMG_ADD = imgpath("add.png")
IMG_DELETE = imgpath("delete.png")
IMG_EDIT = imgpath("edit.png")
IMG_FORM = imgpath("form.png")
IMG_PERSON = imgpath("person.png")
IMG_SAVE = imgpath("save.png")




# Identificadores. ----------------------------------------

ID_CLIENTE = 201
ID_CUENTA = 202
ID_PRESTAMO = 203
# Rango de ids de los elementos que estarán en el menu.
ID_MENU_FIRST = ID_CLIENTE 
ID_MENU_LAST  = ID_PRESTAMO





# Base de datos. ------------------------------------------

DB_PATH =  os.path.join(PATH_DATABASE, "db.sqlite3")









# Sizes predeterminados.

S8 = 8
S16 = 16
S32 = 32
S64 = 64
S128 = 128
S254 = 254




# Todas las variables (esto debe ir siempre al final del archivo, 
# para que tome todas las variables)
VAR = vars().copy()