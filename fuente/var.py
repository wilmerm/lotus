from .translation import gettext as _
# Locales
from .paises import *


try:
    from django.conf import settings
    STATIC_URL = settings.STATIC_URL
except BaseException:
    STATIC_URL = ""












PRIMER_NUMERO_DE_CUENTA = "10221110"
PRIMER_NUMERO_DE_CLIENTE = "10102020"








# PERSONAS -----------------------------------------------------------

MASCULINO = "M"
FEMENINO = "F"
NO_DEFINIDO = "ND"
SEXO_CHOICES = (
    (MASCULINO, _("Masculino")),
    (FEMENINO, _("Femenino")),
    (NO_DEFINIDO, _("No definido")),
)


SOLTERO = "SOLTERO"
CASADO = "CASADO"
UNION_LIBRE = "UNION_LIBRE"
OTRO = "OTRO"
ESTADO_CIVIL_CHOICES = (
    (SOLTERO, _("Soltero")),
    (CASADO, _("Casado")),
    (UNION_LIBRE, _("Unión libre")),
    (OTRO, _("Otro")),
)



# IDENTIFICACIÓN -----------------------------------------------------

CEDULA = "CÉDULA"
PASAPORTE = "PASAPORTE"
RNC = "RNC"
IDENTIFICACION_CHOICES = (
    (CEDULA, _("Cédula")),
    (PASAPORTE, _("Pasaporte")),
    (RNC, _("RNC")),
)





# CONTABILIDAD -------------------------------------------------------

DOP = "DOP"
USD = "USD"
EUR = "EUR"
CAD = "CAD"
GSB = "GSB"
MONEDA_CHOICES = (
    (DOP, _("DOP: Peso dominicano")),
    (USD, _("USD: Dólar estadounidense")),
    (EUR, _("EUR: Euro")),
    (CAD, _("CAD: Dólar canadiense")),
    (GSB, _("GSB: Libra esterlina")),
)

EFECTIVO = "EF"
CUENTA_CORRIENTE = "CC"
CUENTA_AHORROS = "CA"
PRESTAMO = "PR"
TARJETA_CREDITO = "TC"
TARJETA_DEBITO = "TD"
CUENTA_CHOICES = (
    (EFECTIVO, _("Efectivo")),
    (CUENTA_CORRIENTE, _("Cuenta corriente")),
    (CUENTA_AHORROS, _("Cuenta de ahorros")),
    (PRESTAMO, _("Préstamo")),
    (TARJETA_CREDITO, _("Tarjeta de crédito")),
    (TARJETA_DEBITO, _("Tarjeta de débito")),
)

CUOTA_FIJA = "FIJA"
CUOTA_VARIABLE = "VARIABLE"
CUOTA_TIPOS = (
    (CUOTA_FIJA, _("Cuota fija")),
    (CUOTA_VARIABLE, _("Cuota variable")),
)




# FECHAS ------------------------------------------------------------

DIARIO = "DIARIO"
SEMANAL = "SEMANAL"
QUINCENAL = "QUINCENAL"
MENSUAL = "MENSUAL"
ANUAL = "ANUAL"
PERIODO_CHOICES = (
    (DIARIO, _("Diario")),
    (SEMANAL, _("Semanal")),
    (QUINCENAL, _("Quincenal")),
    (MENSUAL, _("Mensual")),
    (ANUAL, _("Anual")),
)




# INFORMÁTICA ------------------------------------------------------

TUPLE = "TUPLE"
LIST = "LIST"
DICT = "DICT"
INT = "INT"
FLOAT = "FLOAT"
DECIMAL = "DECIMAL"
STR = "STR"
BOOL = "BOOL"
DATE = "DATE"
DATETIME = "DATETIME"
TIPO_DE_DATOS_CHOICES = (
    (STR, _("Texto")),
    (INT, _("Número entero.")),
    (FLOAT, _("Número de coma flotante.")),
    (DECIMAL, _("Número decimal")),
    (TUPLE, _("Tupla")),
    (LIST, _("Lista")),
    (DICT, _("Diccionario")),
    (BOOL, _("Falso o Verdadero")),
    (DATE, _("Fecha")),
    (DATETIME, _("Fecha y hora")),
)






# IMÁGENES. ----------------------------------------------------------

IMG_DINERO = STATIC_URL + "img/dinero.svg"




















# Todas las variables (esto debe ir siempre al final del archivo, 
# para que tome todas las variables)
VAR = vars().copy()
