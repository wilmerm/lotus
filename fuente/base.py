import datetime
import unicodedata
from decimal import Decimal
from django.utils.translation import gettext_lazy as _
# Locales
from .var import *
from . import encriptado
from . import email





class Detail(object):
    """
    Facilita mostrar la información de un objeto modelo 
    cualquiera, mostrando sus fields y values. 
    """
    def __init__(self):
        self.fields = []

    def __iter__(self):
        for field in self.fields:
            yield getattr(self, field)

    def Add(self, field, name, value, display=None, html=None, help=""):
        """Agrega miembros al display.
        field: El nombre de la columna en la base de datos (no necesariamente el mismo nombre).
        name: El nombre de la columna como quiere que se muestre al usuario.
        value: El valor del miembro.
        display: El valor como quiere que se muestre al usuario (opcional).
        html: Un texto con formato HTML que se usará para mostrar el valor en vez de 'value' o 'display' (opcional).
        help: Un texto que se usará como tooltips para el usuario (opcional).
        """
        if (value == None) or (value == ""): # Si el valor es None o vacio, no se agrega
            return
        if display == None:
            display = value 
        if html == None:
            html = display
        v = {"name": _(name), "value": value, "display": display, "html": html, "help": help}
        setattr(self, field, v)
        self.fields.append(field)

    def GetValues(self):
        values = []
        for field in self.fields:
            dic = getattr(self, field)
            values.append(dic.values())
        return values

    def GetNames(self):
        names = []
        for field in self.fields:
            dic = getattr(self, field)
            names.append(dic.get("name"))
        return names

    def GetFieldNames(self):
        return self.fields




class Menu(object):
    """
    Crea objetos que se utilizan como menus en las plantillas.
    """
    def __init__(self, id, name, url="", img="", selected=False, help=""):
        self.id = id
        self.name = _(name)
        self.url = url
        self.img = img
        self.selected = selected
        self.help = _(help)
        if selected == False:
            self.cssclass = "menu-item"
        else:
            self.cssclass = "menu-item menu-item-selected"

    def __str__(self):
        return self.name 
    
    def Html(self):
        if self.img:
            if self.selected == False:
                return '<a class="{cssclass}" id="{id}" href="{url}" title="{help}"><img class="menu-item-img" src="{img}"/></a>'.format(cssclass=self.cssclass, id=self.id, url=self.url, help=self.help, img=self.img)
            return '<a class="{cssclass}" id="{id}" href="{url}" title="{help}"><img class="menu-item-img" src="{img}"/></a>'.format(cssclass=self.cssclass, id=self.id, url=self.url, help=self.help, img=self.img)
        else:
            if self.selected == False:
                return '<a class="{cssclass}" id="{id}" href="{url}" title="{help}"><span>{name}</span></a>'.format(cssclass=self.cssclass, id=self.id, url=self.url, help=self.help, name=self.name)
            return '<a class="{cssclass}" id="{id}" href="{url}" title="{help}"><span>{name}</span></a>'.format(cssclass=self.cssclass, id=self.id, url=self.url, help=self.help, name=self.name)

    def Selected(self, state=True):
        self.selected = state 
    
    def Deselected(self, state=False):
        self.selected = state 




class Texto(object):
    """
    Clase para trabajar con textos.
    """

    def Normalize(self, string, lower=True):
        """
        remplaza el texto por uno similiar sin tildes ni caracteres especiales como eñes
        y en minuscula si es indicado.
        """
        out = ''.join((c for c in unicodedata.normalize('NFD', string) if unicodedata.category(c) != 'Mn'))
        out = out.replace("  ", " ").strip()
        if lower:
            out = out.lower()
        return out

    def GetEtiquetas(self, lista):
        """
        Obtiene una cadena de texto a partir de los valores de una lista. Estos valores
        son formateados eliminando las tildes y en totos en minusculas, separados por un espacio.
        """
        out = ""
        for item in lista:
            if isinstance(item, (list, tuple)):
                item = self.GetEtiquetas(item)
            item = self.Normalize(str(item))
            out += " " + item
        return out.strip()

    def FormatForUsername(self, string, remplace="", lower=True):
        """ 
        Formatea el texto dejando solo los caracteres que esten en el rango de la 'a' a la 'z' 
        en minuzculas o mayusculas (sin la ñ ni vocales acentuadas) y los números del 1 al 9.
        Si se indica el remplace, se remplazan los caracteres no permitidos por el indicado. de lo 
        contrario se eliminará
        """
        if not remplace:
            remplace = ""
        permited = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY0123456789"
        out = ""
        for char in string:
            if not char in permited:
                char = remplace
            out += char 
        if lower:
            return out.lower()
        return out

    def GetCombinaciones(self, arg, split=" "):
        """
        Obtiene una lista de todas las combinaciones
        posibles de la cadeda o el array pasado como parametro. Si es una cadena,
        se tomará en cuenta el argumento split que de forma predeterminada es un espacio en blanco,
        que indica donde se dividirá la cadena.

        ejemplo con el cadena: 'Wilmer Morel Martinez' -->
        ['Wilmer Morel Martinez', 'Wilmer Martinez Morel', 'Martinez Wilmer Morel',
        'Martinez Morel Wilmer', 'Morel Wilmer Martinez', 'Morel Martinez Wilmer']
        """
        print("En desarrollo")

    def IsPossibleName(self, text):
        """
        Comprueba si el texto indicado puede ser un nombre, siempre y
        cuando el texto no contenga números.
        """
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for n in numbers:
            if str(n) in text:
                return False
        return True

    def IsPossibleFullName(self, text):
        """
        Comprueba si el texto indicado puede ser un nombre completo,
        siempre y cuando no existan números en su contenido y exista por
        lo menos una separación con espacio.
        """
        if len(text.split(" ")) < 2:
            return False
        return self.IsPossibleName(text)

    def SetMoneda(self, numero, simbolo="$", ndec=2):
        """
        Convierte el número indicado en una cadena de texto 
        con formato moneda.
        """
        return "{}{:,}".format(simbolo, round(numero, 2))

    def Strip(self, texto):
        """
        Elimina los espacios extras del texto indicado.
        """
        return texto.replace("     ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").strip()

    def Int(self, texto):
        """
        Obtiene un número entero a partir del texto introduccido, eliminando 
        los caracteres que no sean númericos. Si hay un punto, los caracteres a 
        la derecha del punto serán omitidos.
        """
        n = ""
        for c in texto:
            if c == ".":
                break
            elif c in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                n += c
        return int(n)

    def Float(self, texto):
        """
        Obtiene un número de coma flotante a partir del texto introduccido,
        eliminando los caracteres que no sean númericos, exceptuando el punto.
        """
        n = ""
        for c in texto:
            if c in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."):
                n += c
        return float(n)

    def ValidarCedula(self, texto):
        """
        Valida que el formato de texto introducido corresponda 
        a un formato de documento de identidad nacional válido para la Rep. Dom.
        """
        texto = texto.replace(" ", "").replace("-", "")
        for c in texto:
            if not c in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
                raise ValueError(_("La cédula contiene caracteres no válidos."))
            elif len(texto) != 11:
                raise ValueError(_("La cédula debe contener exactamente 11 dígitos."))
        return "{}-{}-{}".format(texto[:3], texto[4:10], texto[10])

    def IsCedulaValida(self, texto):
        try:
            self.ValidarCedula(texto)
        except BaseException:
            return False
        return True
            





class Numero(object):
    """
    Clase para trabajar con números.
    """

    def MontoText(self, monto, moneda="", html=False):
        if not isinstance(moneda, str):
            moneda = ""
        if html == True:
            if monto < 0:
                return '<span style="color: red">{:,.2f} {}</span>'.format(monto, moneda)
            return '<span>{:,.2f} {}</span>'.format(monto, moneda)
        return "{:,.2f} {}".format(monto, moneda)

    def MontoHtml(self, monto, moneda=""):
        return self.MontoText(monto, moneda, True)





class Fecha(object):
    """
    Clase para el manejo de fechas.
    """

    def GetTiempo(self, fecha1, fecha2=datetime.date.today(), intexto=False):
        """
        Obtiene la diferencia (tiempo) entre dos fechas.
        """
        try:
            timedelta = fecha2 - fecha1
            days = timedelta.days
            years = int(days / 365)
        except TypeError:
            days = 0
            years = 0
        if intexto == True:
            if years > 0:
                return "{} años".format(years)
            return "{} dias".format(days)
        return days

    def GetListadoDeFechas(self, inicio=datetime.date.today(), periodo=MENSUAL, limite=0, fin=None):
        """
        Obtiene un listado con las fechas en el rango dado.

        inicio = fecha de inicio.
        periodo = 'diario' | 'interdiario' | 'semanal' | 'quincenal' | 'mensual' | 'anual' 
        limite = cantidad de fechas en el listado.
        fin = fecha límite (opcional).

        Nota: Entre 'limite' y 'fin' se usará el que primero se cumpla. Asi que si se desea 
        asegurar que la fecha última sea hasta el 'fin', deberá establecer un limite alto (casi inalcanzable)
        para que le de tiempo a la condición 'fin' cumplirse.
        """
        inicio = datetime.date(inicio.year, inicio.month, inicio.day)
        if fin:
            fin = datetime.date(fin.year, fin.month, fin.day)
        periodo = periodo.upper()
        fechas = [inicio]
        fecha = inicio

        if periodo == DIARIO:
            year, month, day = fecha.year, fecha.month, fecha.day
            for i in range(limite):
                fecha = fecha + datetime.timedelta(days=1)
                fechas.append(fecha)
                if fecha >= fin:
                    break
            return fechas

        if periodo == MENSUAL:
            year, month = fecha.year, fecha.month
            for i in range(limite):
                # Se suman los meses, si el mes es el último, entonces se suma un año
                # y se reinicia el mes a 1 nuevamente.
                day = inicio.day
                if month == 12:
                    month = 1
                    year += 1
                else:
                    month += 1
                # Si el día es más alto al maximo del mes, entonces se considera
                # como día el último día del mes.
                for n in range(10):
                    try:
                        fecha = datetime.date(year, month, day)
                    except ValueError:
                        day -= 1
                    else:
                        break 
                if (fin) and (fecha > fin):
                    break
                fechas.append(fecha)
            return fechas

    def GetRangoDeFechas(self, inicio, fin=datetime.date.today(), periodo=MENSUAL):
        """
        Obtiene un listado de todas las fechas comprendidas 
        en el rango de fechas indicado.
        """
        return self.GetListadoDeFechas(inicio, periodo, 999999999999, fin)

    def GetUltimoDiaDelMes(self, year=None, month=None):
        """
        Obtiene el ultimo dia del mes indicado. Si no se indica mes 
        se tomará como referencia la fecha actual.
        """
        if not year:
            year = datetime.date.today().year 
        if not month:
            month = datetime.date.today().month 
        day = 31
        for n in range(10):
            try:
                fecha = datetime.date(year, month, day)
            except ValueError:
                day -= 1
            else:
                break
        return fecha 



class Encriptado(encriptado.Encriptado):
	"""
    Clase para encriptar texto. 
    """






class PrestamoBase(Fecha):
    """
    Clase para las operaciones de cálculo de un préstamo.
    """

    def GetDuraccion(self, fecha_inicio, cant_cuotas, periodo=MENSUAL):
        """
        Obtiene el tiempo de duración del préstamo, desde la fecha
        de inicio (desembolso) hasta la fecha en que concluirá según 
        la cantidad de cuotas y el periodo en que se generan dichas cuotas.
        
        ---> (int(years), int(months), int(days))
        """

    def GetAmortizacionCuotaFija(self, monto, tasa, cuotas, periodo=MENSUAL, inicio=datetime.date.today()):
        """
        Args:
            monto (float): monto del préstamo.
            tasa (float): tasa del préstamo.
            periodo (str): periodo del préstamo (semanal, quincenal, mensual, ...).
            inicio (datetime.date): fecha de inicio del préstamo.

        Returns:
            list: Una lista de elementos.
        """
        valor, interes, capital_restante = self.GetValorDeCuotaFija(monto, tasa, cuotas, periodo)
        fechas = self.GetListadoDeFechas(inicio, periodo, cuotas)
        tabla = []
        t_valor, t_interes, t_capital, t_capital_restante = Decimal(), Decimal(), Decimal(), Decimal()

        for fecha in fechas[1:]:
            interes = capital_restante * (tasa / Decimal(100))
            capital = valor - interes
            capital_restante -= capital

            tabla.append({
                "fecha": fecha,
                "valor": round(valor, 2),
                "interes": round(interes, 2),
                "capital": round(capital, 2),
                "capital_restante": round(capital_restante, 2),
                "clase": "item",
            })
            t_valor += valor 
            t_interes += interes
            t_capital += capital
            t_capital_restante = capital_restante

        tabla.append({
            "fecha": "Total",
            "valor": round(t_valor, 2),
            "interes": round(t_interes, 2),
            "capital": round(t_capital, 2),
            "capital_restante": round(t_capital_restante, 2),
            "clase": "total",
        })
        return tabla

    def GetAmortizacionCuotaVariable(self, monto, tasa, cuotas, periodo=MENSUAL, inicio=datetime.date.today()):
        """
        Retorna un listado de diccionarios que contienen 
        información de las cuotas de la tabla de amortización 
        de un préstamo con cuota de tipo variable.
        """
        capital_restante = monto
        cuotas = cuotas 
        tasa = tasa
        periodo = periodo   
        fechas = self.GetListadoDeFechas(inicio, periodo, cuotas)
        tabla = []
        capital = capital_restante / cuotas
        t_valor, t_interes, t_capital, t_capital_restante = Decimal(), Decimal(), Decimal(), Decimal()
        
        for fecha in fechas[1:]:
            interes = (capital_restante / Decimal(100)) * tasa
            valor = capital + interes 
            capital_restante = capital_restante - capital

            tabla.append({
                "fecha": fecha,
                "valor": round(valor, 2),
                "interes": round(interes, 2),
                "capital": round(capital, 2),
                "capital_restante": round(capital_restante, 2),
                "clase": "item",
            })
            t_valor += valor 
            t_interes += interes
            t_capital += capital
            t_capital_restante = capital_restante

        tabla.append({
            "fecha": "Total",
            "valor": round(t_valor, 2),
            "interes": round(t_interes, 2),
            "capital": round(t_capital, 2),
            "capital_restante": round(t_capital_restante, 2),
            "clase": "total",
        })
        return tabla

    def GetAmortizacionTitulos(self):
        """
        Obtiene los nombres de las columnas de la tabla de amortización.
        """
        return (_("Fecha"), _("Valor"), _("Interés"), _("Capital"), _("Capital restante"))

    def GetValorDeCuotaFija(self, monto, tasa, cuotas, periodo=MENSUAL):
        """
        Retorna el valor actual de la cuota, según el método francés,
        en donde las cuotas son fijas. -> float(x)

        Formula = R = P [(i (1 + i)**n) / ((1 + i)**n – 1)].
        Donde:
            R = renta (cuota)
            P = principal (préstamo adquirido)
            i = tasa de interés
            n = número de periodos
            
        -> (Moneda, Moneda, Moneda)
        """
        tasa = tasa / Decimal(100)
        if periodo == DIARIO:
            tasa /= Decimal(30.4167)
        elif periodo == SEMANAL:
            tasa /= Decimal(4.34524)
        if periodo == QUINCENAL:
            tasa /= Decimal(2.0)
        elif periodo == ANUAL:
            tasa *= 12

        valor = monto * ( (tasa * ((1 + tasa)**cuotas)) / (((1 + tasa)**cuotas) - 1) )
        interes = valor - monto
        return (valor, interes, monto)

    def GetValorDeCuotaVariable(self, capital, tasa, periodo=MENSUAL):
        """
        Retorna una tupla con el valor de la cuota, el interes y el capital.
        para prestamos con cuotas variables.
        --> (valor, interes, capital)
        """
        interes = (capital / 100) * tasa
        if periodo == DIARIO:
            interes /= 30.4167
        elif periodo == SEMANAL:
            interes /= 4.34524
        if periodo == QUINCENAL:
            interes /= 2.0
        elif periodo == ANUAL:
            interes *= 12

        valor = capital + interes
        return (valor, interes, capital)










