"""
Módulo para la gestión de la base de datos.
"""
from decimal import Decimal
import datetime
# Módulos externos.
import sqlite3
# Módulos del proyecto.
from var import *
from fuente.translation import gettext as _
from fuente.base import Texto





def get_connection():
    return sqlite3.connect(DB_PATH)


def get_cursor():
    return get_connection().cursor()








class QuerySet(Texto):
    """
    Representa un listado de objetos
    extraidos de la base de datos.
    """
    def __init__(self, model=None):
        self.model = model 
        self.cursor = get_cursor()
        self.items = []

    def __str__(self):
        return "QuerySet({} {})".format(len(self.items), self.model.Meta.verbose_name_plural)

    def __iter__(self):
        for item in self.items:
            obj = self.model
            obj.SetValues(item)
            yield obj

    def all(self):
        sql = "SELECT * FROM {}".format(self.model.Meta.table_name)
        self.cursor.execute(sql)
        self.items = self.cursor.fetchall()
        return self

    def filter(self, **kwargs):
        f = []
        for key, value in kwargs.items():
            f.append("{}='{}'".format(key, value))
        s = " AND ".join(f)
        if s:
            sql = "SELECT * FROM {} WHERE {}".format(self.model.Meta.table_name, s)
        else:
            sql = "SELECT * FROM {}".format(self.model.Meta.table_name)
        self.cursor.execute(sql)
        self.items = self.cursor.fetchall()
        return self

    def search(self, text):
        """
        Busca concidencias en el campo 'tags' y 
        retorna un QuerySet con los modelos concidentes.
        """
        text = self.Normalize(text)
        sql = "SELECT * FROM {} WHERE tags LIKE '%{}%'".format(self.model.Meta.table_name, text)
        self.cursor.execute(sql)
        self.items = self.cursor.fetchall()
        return self

    def get(self, **kwargs):
        """
        Obtiene un único objeto desde la base de datos.
        """
        if not kwargs:
            raise ValueError("Debe indicar las opciones. Ej.: get(fieldname = value).")

        if "id" in kwargs:
            obj = self.model
            obj.Set(kwargs["id"])
            return obj

        # Creamos la consulta SQL
        f = []
        for key, value in kwargs.items():
            f.append("{}='{}'".format(key, value))
        s = " AND ".join(f)
        sql = "SELECT {} FROM {} WHERE {}".format(self.model.GetFieldsNames(), self.model.Meta.table_name, s)
        # Ejecutamos la consulta.
        self.cursor.execute(sql)
        query = self.cursor.fetchone()
        if not query:
            self.items = []
            raise KeyError("Ningún registro coincide con las opciones indicadas.")
        self.items = [query]
        obj = self.model 
        obj.SetValues(self.items[0])
        return obj



class ModelBase(int):
    """
    Modelo base para la gestión
    de la base de datos. 
    """
    id = 0 # Todos los modelos de base de datos tienen que tener este campo.
    objects = None # Establecer en el __init__

    class Meta:
        table_name = None # Establecer en el modelo.


    def __init__(self, id=None):
        self.objects = QuerySet(self)
        if id == None:
            self.__dict__["id"] = 0
        else:
            self.Set(id, nocrear=True)
        
    def __iter__(self):
        for field in self.GetFields():
            yield field[1]

    def __call__(self, fieldname):
        return getattr(self, fieldname)

    def __setattr__(self, name, value):
        """
        Establece los atributos. Cuando el atributo 
        es un objeto 'Field' este se le asigna el valor
        al objeto Field.
        """
        if name in dict(self.GetFields()):
            self.__class__.__dict__[name].value = value 
        else:
            super().__setattr__(name, value)

    def GetFields(self):
        """
        Obtiene todas las fields de este modelo.
        """
        fields = []
        for key in self.__class__.__dict__:
            value = self.__class__.__dict__[key]
            if isinstance(value, Field):
                fields.append( (key, value) )
        return fields

    def GetFieldsNames(self, verbose_name=False):
        """
        Obtiene un listado de los nombres de los campos (fields).
        Si verbose_name es True, obtiene los nombre leibles de los campos.
        """
        out = []
        if verbose_name:
            for key, field in self.GetFields():
                out.append(field.verbose_name)
        else:
            for key, field in self.GetFields():
                out.append(field.name)
        return out

    def Get(self, fieldname="id"):
        """
        Obtiene el campo correspondiente.
        """
        return self(fieldname)

    def GetValues(self):
        """
        Obtiene un diccionario con los nombres de las fields 
        y sus respectivos valores.
        """
        v = {}
        for name in self.GetFieldsNames():
            v[name] = getattr(self, name).value
        return v

    def GetValuesString(self):
        """
        Obtiene los valores de las fields en un string
        para ser utilizado en la consulta SQL.
        """
        l = []
        values = self.GetValues()
        for name in values:
            value = values[name]
            if isinstance(value, str):
                value = "'{}'".format(value)
            l.append(value)
        return ", ".join(l)

    def Save(self):
        """
        Almacena los datos del modelo en la base de datos.
        """
        values = self.GetValues()
        if not values["id"]:
            # Creación de un nuevo registro.
            columns = values.
            sql = "INSERT INTO {} ({}) VALUES ({})".format(self.Meta.table_name, columns, values)

    def SetFieldValue(self, name, value):
        """
        Establece el valor al field indicado.
        """
        if not name in self.GetFieldsNames():
            raise ValueError("'{}' no es el nombre de una field del modelo '{}'".format(name, self.__class__.__name__))
        setattr(self, name, value)

    def Set(self, id, nocrear=False):
        """
        Establece este objeto, sus valores, según el id indicado.
        Se busca el registro correspondiente en la base de datos,
        y se reemplaza el objeto por un nuevo.
        """
        # Buscamos en la base de datos el registro correspondiente.
        fields = ", ".join(self.GetFieldsNames())
        sql = "SELECT {} FROM {} WHERE id = {}".format(fields, self.Meta.table_name, id)
        self.objects.cursor.execute(sql)
        values = self.objects.cursor.fetchone()
        # Cambiamos el objeto, esta clase hereda de 'int', entonces lo que hacemos
        # es crear otra instancia con el valor del campo 'id' como su valor entero,
        # y luego asignamos los valores de los diversos campos.
        if nocrear == False:
            new = self.__class__(values[0])
            new.__setvalues(values)
            self = new
        else:
            self.__setvalues(values)
        return self

    def SetValues(self, *args, **kwargs):
        """
        Establece los valores a los fields y 
        cambia el valor entero de este objeto.
        """
        # Creamos el objeto para que se le asigne su valor entero,
        # ya que este objeto hereda de 'int'.

        # Si se pasa una tupla de valores.
        if args:
            # Si se pasa un listado de valores como un solo elemento,
            # se remplaza el args con este listado.
            if (len(args) == 1) and (isinstance(args, (list, tuple))):
                args = args[0]

        if "id" in kwargs:
            new = self.__class__(kwargs["id"])
        else:
            new = self.__class__(args[0])
        new.__setvalues(*args, **kwargs)
        self = new

    def __setvalues(self, *args, **kwargs):
        """
        Establece los valores a los fields.
        """
        # Si se pasa una tupla de valores.
        if args:
            # Si se pasa un listado de valores como un solo elemento,
            # se remplaza el args con este listado.
            if (len(args) == 1) and (isinstance(args, (list, tuple))):
                args = args[0]
            # Se establece cada elmento, en el mismo orden en que
            # aparecen las fields declaradas en el modelo.
            i = 0
            fields = self.GetFields()
            for value in args:
                setattr(self, fields[i][0], value)
                i += 1
        # Si se pasa un diccionario.
        if kwargs:
            for key in kwargs:
                value = kwargs[key]
                setattr(self, key, value)
        # Esta clase hereda de 'int', por lo cual su valor deberá ser
        # el mismo valor del campo 'id'.




class Field():
    """
    Representa un campo en una 
    base de datos. 
    """
    def __init__(self, name, verbose_name=None, pytype=STR, help_text="", required=True, default=None):
        self.__dict__["name"] = name 
        self.__dict__["verbose_name"] = verbose_name
        self.__dict__["type"] = pytype 
        self.__dict__["help_text"] = help_text
        self.__dict__["required"] = required
        if not self.verbose_name:
            self.__dict__["verbose_name"] = self.name 

        self.__dict__["value"] = None
        try:
            self.name.Meta.table_name
        except AttributeError:
            self.__dict__["ismodel"] = False
            self.__dict__["model"] = None
        else:
            self.__dict__["value"] = self.name()
            self.__dict__["model"] = self.name 
            self.__dict__["name"] = "{}_id".format(self.model.__name__.lower())
            self.__dict__["type"] = INT
            self.__dict__["ismodel"] = True


    def __str__(self):
        return str(self.value)

    def __call__(self):
        return self.value 

    def __setattr__(self, name, value):
        """
        Establecemos el atributo indicado de 
        acuerdo a su tipo de valor establecido.
        """
        if name == "value":
            if value == None:
                pass
            elif self.ismodel:
                value = self.value.objects.get(id = value)
            elif self.type == STR:
                value = str(value)
            elif self.type == INT:
                value = int(value)
            elif self.type == FLOAT:
                value = float(value)
            elif self.type == DECIMAL:
                value = Decimal(value)
            elif self.type == DATE:
                value = [int(e) for e in str(value).split("-")]
                value = datetime.date(*value)
            elif self.type == DATETIME:
                d, t = str(value).split(" ")
                d = d.split("-")
                t = t.split(":")
                value = [int(float(e)) for e in d + t]
                value = datetime.datetime(*value)
            elif self.type == BOOL:
                value = bool(value)
            elif self.type == LIST:
                value = list(value)
            elif self.type == TUPLE:
                value = tuple(value)
            elif self.type == DICT:
                value = dict(value)
            else:
                pass 
        self.__dict__[name] = value 
    
    
            
        



                



    


    