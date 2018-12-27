"""
Módulo para la gestión de la base de datos.
"""
import sys
from decimal import Decimal
import datetime
# Módulos externos.
import sqlite3
# Módulos del proyecto.
from .var import *
from .translation import gettext as _
from .base import Texto, Fecha, Numero








class DatabaseError(BaseException):
    """
    Errores capturados en el módulo database.
    """
    def __init__(self, error=None, fieldname="", message="", sql=""):
        self.error = error 
        self.fieldname = fieldname 
        self.message = message 
        self.sql = sql
        #exc_type, exc_value, exc_traceback = sys.exc_info()

    def __str__(self):
        if self.error:
            print("Error en {} linea {}: '{}'.".format(__name__, self.error.__traceback__.tb_lineno, repr(self.error))) # __traceback__.tb_lineno
        if self.fieldname:
            print("Campo afectado: '{}'".format(self.fieldname))
        if self.message:
            print("Mensaje: '{}'".format(self.message))
        if self.sql:
            print("SQL: '{}'".format(self.sql))
        return self.message




# Inicialización.
DATABASE_FILE = "db/db.sqlite3"
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()





pytypes = {
    STR: str,
    INT: int,
    FLOAT: float,
    DECIMAL: Decimal,
    DATE: datetime.date,
    DATETIME: datetime.datetime,
    BOOL: bool,
    LIST: list,
    TUPLE: tuple,
    DICT: dict,
}




class BaseField(object):
    """
    Field base que representa un campo en la bae de datos.
    """
    def __init__(self, name, verbose_name=None, blank=False, default=None, null=True, help_text="", pytype=object):
        self.__dict__["value"] = None
        self.__dict__["name"] = name 
        self.__dict__["verbose_name"] = verbose_name
        self.__dict__["blank"] = blank 
        self.__dict__["default"] = default 
        self.__dict__["null"] = null 
        self.__dict__["help_text"] = help_text
        self.__dict__["pytype"] = pytype 

        if self.verbose_name == None:
            self.__dict__["verbose_name"] = name.title()

        # Operaciones de limpieza para el campo value, dependiendo de los 
        # atributos 'null' y 'blank'. Si esta Field no acepta null pero 
        # si acepta ser blank, entonces su valor será un string vacio.
        try:
            self.__dict__["value"] = self.CleanValue("")
        except DatabaseError as e:
            print("Error: ", self.name, e, self.value)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.value)

    def __len__(self):
        if not self.value:
            return 0
        elif self.pytype == STR:
            return len(self.value)
        elif self.pytype in (INT, FLOAT, DECIMAL):
            return int(self.value)
        else:
            return len(self.value)

    def __getvalueother(self, value):
        try:
            return value.value 
        except AttributeError:
            return value 
        
    def __gt__(self, other):
        other = self.__getvalueother(other)
        return self.value > other

    def __lt__(self, other):
        other = self.__getvalueother(other)
        return self.value < other

    def __ge__(self, other):
        other = self.__getvalueother(other)
        return self.value >= other

    def __le__(self, other):
        other = self.__getvalueother(other)
        return self.value <= other 

    def __eq__(self, other):
        other = self.__getvalueother(other)
        return self.value == other

    def __ne__(self, other):
        other = self.__getvalueother(other)
        return self.value != other

    def __int__(self):
        try:
            return int(float(self.value))
        except (TypeError, ValueError) as e:
            raise DatabaseError(e, self.name, "El valor '{}' para la field '{}' no es un número".format(self.value, self.name))

    def __float__(self):
        try:
            return float(self.value)
        except TypeError as e:
            raise DatabaseError(e, self.name, "El valor '{}' para la field '{}' no es un número".format(self.value, self.name))

    def __bool__(self):
        if self.value == None:
            return False
        return True

    def __call__(self):
        return self.value

    def Clear(self):
        """
        Borra el valor de este field.
        Si hay un valor predeterminado, lo pone.
        """
        if self.default != None:
            self.__dict__["value"] = self.default 
        else:
            self.__dict__["value"] = ""

    def CleanValue(self, value):
        # Si este campo no acepta un valor nulo.
        if (self.null == False):
            # Si se pasa un valor nulo.
            if (value == None):
                # Si este campo acepta un valor vacio.
                if self.blank == True:
                    return str()
                else:
                    raise DatabaseError(None, self.name, _("El valor del campo '{}' no puede ser nulo."))
        return value



class CharField(BaseField):
    """
    Representa un campo de texto en la bae de datos.
    """
    def __init__(self, name, verbose_name=None, blank=False, default=None, null=True, choices=[], help_text=""):
        if (blank == True) and (default == None):
            default = ""
        BaseField.__init__(self, name, verbose_name, blank, default, null, help_text, STR)
        self.__dict__["choices"] = choices

    def __setattr__(self, name, value):
        if name == "value":
            value = self.CleanValue(value)
            if value != None:
                value = str(value)
        self.__dict__[name] = value 




class IntegerField(BaseField):
    """
    Representa un campo tipo entero en la base de datos.
    """
    def __init__(self, name, verbose_name=None, blank=False, default=None, null=True, min=None, max=None, help_text=""):
        if (blank == True) and (default == None):
            if (min != None):
                default = int(min)
            else:
                default = int(0)
        
        BaseField.__init__(self, name, verbose_name, blank, default, null, help_text, INT)

        self.__dict__["min"] = min
        self.__dict__["max"] = max
    
    def __setattr__(self, name, value):
        if name == "value":
            value = self.CleanValue(value)
        self.__dict__[name] = value 

    def CleanValue(self, value):
        value = super().CleanValue(value)
        if (not value in (None, "")):
            value = int(float(value))
            if (self.min != None) and (value < self.min):
                raise DatabaseError(None, self.name, "El valor de la field '{}' debe estar comprendido entre {} y {}".format(self.name, self.min, self.max))
            if (self.max != None) and (value > self.max):
                raise DatabaseError(None, self.name, "El valor de la field '{}' debe estar comprendido entre {} y {}".format(self.name, self.min, self.max))
        return value
        



class DecimalField(BaseField):
    """
    Representa un campo tipo decimal en la base de datos.
    """
    def __init__(self, name, verbose_name=None, blank=False, default=None, null=True, min=None, max=None, help_text=""):
        
        BaseField.__init__(self, name, verbose_name, blank, default, null, help_text, DECIMAL)

        if (blank == True) and (default == None):
            if (min != None):
                self.default = Decimal(min)
            else:
                self.default = Decimal(0)

        self.min = min 
        self.max = max

    def __setattr__(self, name, value):
        if name == "value":
            value = self.CleanValue(value)
        self.__dict__[name] = value 

    def CleanValue(self, value):
        value = super().CleanValue(value)
        if (not value in (None, "")):
            value = Decimal(value)
            if (self.min != None) and (value < self.min):
                raise DatabaseError(None, self.name, "El valor de la field '{}' debe estar comprendido entre {} y {}".format(self.name, self.min, self.max))
            if (self.max != None) and (value > self.max):
                raise DatabaseError(None, self.name, "El valor de la field '{}' debe estar comprendido entre {} y {}".format(self.name, self.min, self.max))
        return value




class FloatField(BaseField):
    """
    Representa un campo tipo numérico de coma flotante en la base de datos.
    """
    def __init__(self, name, verbose_name=None, blank=False, default=None, null=True, min=None, max=None, help_text=""):
        
        BaseField.__init__(self, name, verbose_name, blank, default, null, help_text, FLOAT)

        if (blank == True) and (default == None):
            if (min != None):
                self.default = float(min)
            else:
                self.default = float(0)

        self.min = min 
        self.max = max

    def __setattr__(self, name, value):
        if name == "value":
            value = self.CleanValue(value)
        self.__dict__[name] = value 

    def CleanValue(self, value):
        value = super().CleanValue(value)
        if (not value in (None, "")):
            value = float(value)
            if (self.min != None) and (value < self.min):
                raise DatabaseError(None, self.name, "El valor de la field '{}' debe estar comprendido entre {} y {}".format(self.name, self.min, self.max))
            if (self.max != None) and (value > self.max):
                raise DatabaseError(None, self.name, "El valor de la field '{}' debe estar comprendido entre {} y {}".format(self.name, self.min, self.max))
        return value

        


class DateField(BaseField):
    """
    Representa un campo tipo Date en la base de datos.
    """
    def __init__(self, name, verbose_name=None, blank=False, default=None, null=True, min=MINDATE, max=MAXDATE, help_text=""):
        BaseField.__init__(self, name, verbose_name, blank, default, null, help_text, DATE)
        

        if (blank == True) and (default == None):
            self.default = ""

        if min < MINDATE:
            raise DatabaseError(None, self.name, "La fecha mínima no debe ser memor que '{0:%Y-%m-%d}'".format(MINDATE))
        if max > MAXDATE:
            raise DatabaseError(None, self.name, "La fecha máxima no debe ser mayor que '{0:%Y-%m-%d}'".format(MAXDATE))

        self.min = min 
        self.max = max 

    def __str__(self):
        try:
            return "{0:%Y-%m-%d}".format(self.value)
        except (ValueError):
            return ""

    def __setattr__(self, name, value):
        if name == "value":
            value = self.CleanValue(value)
        self.__dict__[name] = value 

    def CleanValue(self, value):
        value = super().CleanValue(value)
        if (not value in (None, "")):
            if isinstance(value, str):
                value = Fecha().StrToDate(value)
            if (value < self.min) or (value > self.max):
                raise DatabaseError(None, self.name, "El valor de la field '{}' debe estar comprendido entre {} y {}".format(self.name, self.min, self.max))
        return value



class DateTimeField(BaseField):
    """
    Representa un campo tipo DateTime en la base de datos.
    """
    def __init__(self, name, verbose_name=None, blank=False, default=None, null=True, min=MINDATETIME, max=MAXDATETIME, help_text=""):
        BaseField.__init__(self, name, verbose_name, blank, default, null, help_text, DATETIME)
        
        if min < MINDATETIME:
            raise DatabaseError(None, self.name, "La fecha mínima no debe ser memor que '{0:%Y-%m-%d %H:%M:%S}'".format(MINDATETIME))
        if max > MAXDATETIME:
            raise DatabaseError(None, self.name, "La fecha máxima no debe ser mayor que '{0:%Y-%m-%d %H:%M:%S}'".format(MAXDATETIME))

        self.min = min 
        self.max = max 

    def __str__(self):
        try:
            return "{0:%Y-%m-%d %H:%M:%S}".format(self.value)
        except ValueError:
            return ""

    def __setattr__(self, name, value):
        if name == "value":
            value = self.CleanValue(value)
        self.__dict__[name] = value 

    def CleanValue(self, value):
        value = super().CleanValue(value)
        if (not value in (None, "")):
            if isinstance(value, str):
                value = Fecha().StrToDatetime(value)
            if (value < self.min) or (value > self.max):
                raise DatabaseError(None, self.name, "El valor de la field '{}' debe estar comprendido entre {} y {}".format(self.name, self.min, self.max))
        return value
    


class BoolField(BaseField):
    """
    Representa un campo tipo DateTime en la base de datos.
    """
    def __init__(self, name, verbose_name=None, default=False, name_false="Si", name_true="No", help_text=""):
        BaseField.__init__(self, name=name, verbose_name=verbose_name, default=default, blank=True, null=False, help_text=help_text)

        self.name_false = _(name_false)
        self.name_true = _(name_true)
        
    def __str__(self):
        if self.value == False:
            return self.name_false
        elif self.value == True:
            return self.name_true 
        return _("Indefinido")

    def __setattr__(self, name, value):
        if name == "value":
            value = self.CleanValue(value)
        self.__dict__[name] = value 



class ModelField(BaseField):
    """
    Representa un campo tipo ForeignKey tipo entero en la base de datos.
    """
    def __init__(self, name, verbose_name=None, model=None, blank=False, default=None, null=True, help_text=""):
        BaseField.__init__(self, name="{}_id".format(name), verbose_name=verbose_name, blank=blank, default=default, null=null, help_text=help_text)
        self.__dict__["min"] = 0
        self.__dict__["max"] = None
        self.__dict__["model"] = model 
        self.__dict__["object"] = model()
        self.__dict__["value"] = 0
        
    def __str__(self):
        return str(self.object)

    def __int__(self):
        return int(float(self.value))

    def __getattr__(self, name):
        if name == "value":
            return int(float(self.value))
        try:
            return super().__getattribute__(name)
        except AttributeError:
            # Todas las fields del 'object' (modelo de esta field) 
            # tienen que ser accesibles también desde esta field.
            # Por ejemplo: Tenemos un modelo 'Prestamo' este modelo tiene las
            # fields (id, cliente, tags, ...), la field 'cliente' es un ModelField que 
            # a su vez tiene otras fields. de modo que si hago esto cliente.nombres deberá
            # darme el valor de la field 'nombre' del modelfield 'cliente' del modelo 'Préstamo'.
            return getattr(self.object, name)

    def __setattr__(self, name, value):
        if name is "value":
            self.__dict__["object"] = self.model(self.value)
            self.__dict__["value"] = self.object.id.value
        super().__setattr__(name, value)
        
    def __bool__(self):
        if not self.value:
            return False
        return True

    def CleanValue(self, value):
        if value == None:
            value = ""
        elif (not value in (None, "")):
            try:
                value = int(float(value))
            except (TypeError, ValueError) as e:
                raise DatabaseError(e, self.name, _("El valor '{}' para el campo '{}' no es válido. Debe ser un número entero mayor a 0.".format(value, self.name)))
            if value < 1:
                raise DatabaseError(None, self.name, _("El valor '{}' para el campo '{}' no es válido. Debe ser un número entero mayor a 0.".format(value, self.name)))
        return super().CleanValue(value)





class QuerySet(Texto):
    """
    Representa un listado de objetos
    extraidos de la base de datos.

    El parametro 'model' es una instancia de un 
    modelo (una clase que hereda de Model).
    """
    def __init__(self, model=None):
        self.model = model # Instancia de un modelo.
        self.fieldsnames = tuple(self.model.GetFieldsNames())
        self.conn = conn
        self.cursor = self.conn.cursor()
        self.items = []

    def __str__(self):
        return "QuerySet({} {})".format(len(self.items), self.model.Meta.verbose_name_plural)

    def __iter__(self):
        for item in self.items:
            obj = self.model
            obj.SetValues(item, self.fieldsnames)
            yield obj

    def all(self):
        """
        Retorna un QuerySet con todos los registros del modelo.
        """
        sql = "SELECT {} FROM {}".format(", ".join(self.fieldsnames), self.model.Meta.table_name)
        self.cursor.execute(sql)
        self.items = self.cursor.fetchall()
        return self

    def filter(self, **kwargs):
        """Retorna un QuerySet con los registros del modelo que coinciden 
        con los parametros de busqueda indicados.

        filter(fieldname1 = value1, fieldname2 = value2, ...) --> QuerySet()
        """
        f = []
        for key, value in kwargs.items():
            f.append("{}='{}'".format(key, value))
        s = " AND ".join(f)

        if s:
            sql = "SELECT {} FROM {} WHERE {}".format(", ".join(self.fieldsnames), self.model.Meta.table_name, s)
        else:
            sql = "SELECT {} FROM {}".format(", ".join(self.fieldsnames), self.model.Meta.table_name)

        self.cursor.execute(sql)
        self.items = self.cursor.fetchall()
        return self

    def search(self, text):
        """
        Busca concidencias en el campo 'tags' y 
        retorna un QuerySet con los modelos concidentes.
        """
        text = self.Normalize(text)
        sql = "SELECT {} FROM {} WHERE tags LIKE '%{}%'".format(", ".join(self.fieldsnames), self.model.Meta.table_name, text)
        self.cursor.execute(sql)
        self.items = self.cursor.fetchall()
        return self

    def get(self, **kwargs):
        """
        Obtiene un único objeto desde la base de datos.

        get(id = 4) --> Model()
        get(nombres = 'Wilmer', apellidos = 'Martinez') --> Model()

        Si no encuentra ningún registro retorna un KeyError.
        """
        if not kwargs:
            raise DatabaseError(None, self.name, "Debe indicar las opciones. Ej.: get(fieldname = value).")

        # Si el valor 'id' es pasado en los parámetros.
        if "id" in kwargs:
            try:
                id = kwargs["id"].value
            except AttributeError:
                id = kwargs["id"]
            id = int(id)
            if id > 0:
                obj = self.model
                obj.Set(id)
                return obj
            else:
                self.items = []
                raise DatabaseError(None, self.model.name, "Ningún registro coincide con las opciones indicadas.")

        # Si el valor 'id' no es pasado en los parámetros.
        # Creamos la consulta SQL
        f = []
        for key, value in kwargs.items():
            f.append("{}='{}'".format(key, value))
        s = " AND ".join(f)
        sql = "SELECT {} FROM {} WHERE {}".format(", ".join(self.fieldsnames), self.model.Meta.table_name, s)

        # Ejecutamos la consulta.
        self.cursor.execute(sql)
        query = self.cursor.fetchone()
        if not query:
            self.items = []
            raise DatabaseError(None, self.model.name, "Ningún registro coincide con las opciones indicadas.")
        self.items = [query]
        obj = self.model 
        obj.SetValues(self.items[0])
        return obj





class ModelBase(object):
    """
    Modelo base para la gestión de la base de datos.
    """
    objects = None # Establecer en el __init__

    class Meta:
        # Establecer en el modelo que hereda.
        table_name = None 
        verbose_name = "ModelBase"
        verbose_name_plural = "ModelBase"


    def __init__(self, id=None):
        self.__class__.id = IntegerField("id", _("Id")) # Todos los modelos de base de datos tienen que tener este campo.
        self.__class__.objects = QuerySet(self)
        self.__class__.name = self.__class__.Meta.table_name.split("_")[1]
        # Limpiamos las fields de los datos anteriores.
        self.Clear()
        if not id:
            self.__class__.__dict__["id"].value = None
        else:
            self.Set(id)

    def __str__(self):
        return self.Meta.verbose_name
        
    def __iter__(self):
        for field in self.GetFields():
            yield field[1]

    def __call__(self, fieldname):
        return getattr(self, fieldname)

    def __bool__(self):
        if not self.id:
            return False 
        return True

    def __getattr__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError as e1:
            try:
                name = name[0:-3] # sufijo _id
                return super().__getattribute__(name)
            except (IndexError, AttributeError) as e2:
                raise AttributeError(e1)

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

    def Clear(self):
        for name, field in self.GetFields():
            field.Clear()

    def GetModelName(self, plural=False):
        if plural == True:
            return self.Meta.verbose_name_plural
        return self.Meta.verbose_name

    def GetVerboseName(self, plular=False):
        if plular:
            return self.__class__.Meta.verbose_name_plural
        return self.__class__.Meta.verbose_name

    def GetFields(self):
        """
        Obtiene todas las fields de este modelo.
        --> [(name, field), (name, field), ...]
        """
        fields = []
        for key in self.__class__.__dict__:
            value = self.__class__.__dict__[key]
            if isinstance(value, BaseField):
                fields.append( (key, value) )
        return fields

    def GetFieldsNames(self, verbose_name=False, exclude=[]):
        """
        Obtiene un listado de los nombres de los campos (fields).
        Si verbose_name es True, obtiene los nombre leibles de los campos.
        El parámetro 'exclude' (opcional) es una lista de nombres de las fields que 
        se desean excluir del listado a retornar.
        """
        out = []
        if verbose_name:
            for key, field in self.GetFields():
                if key in exclude:
                    continue
                out.append(field.verbose_name)
        else:
            for key, field in self.GetFields():
                if key in exclude:
                    continue
                out.append(field.name)
        return out

    def GetLastId(self):
        """
        Obtiene el último registro.
        """
        sql = "SELECT MAX(id) FROM {}".format(self.Meta.table_name)
        self.objects.cursor.execute(sql)
        return self.objects.cursor.fetchone()[0]

    def GetNextId(self):
        """
        Obtiene el siguiente id para nuevos registros.
        """
        return self.GetLastId() + 1

    def GetValuesString(self, exclude=[]):
        """
        Obtiene los valores de las fields en un string
        separado por coma (,) para ser utilizado en la consulta SQL.

        -- 'value1, value2, value3, ...'
        """
        l = []
        names = self.GetFieldsNames(exclude=exclude)
        for name in names:
            value = self(name).value
            if isinstance(value, BaseField):
                value = value.value
            if isinstance(value, str):
                value = "'{}'".format(value)
            elif isinstance(value, datetime.date):
                value = "'{0:%Y-%m-%d}'".format(value)
            elif isinstance(value, datetime.datetime):
                value = "'{0:%Y-%m-%d %H:%M:%S}'".format(value)
            elif value == None:
                value = "NULL"
            elif isinstance(value, bool):
                value = str(value).upper()
            else:
                value = str(value)
            l.append(value)
        return ", ".join(l)

    def GetFieldsString(self, exclude=[]):
        """
        Obtiene los nombres de las fields en un string
        separados por coma (,) para ser utilizados en consulta SQL.

        -- 'name1, name2, name3, ...'
        """
        return ", ".join(self.GetFieldsNames(exclude=exclude))

    def GetFieldsAndValuesString(self, exclude=[]):
        """
        Obtiene un string con los nombres de las fields y sus valores
        optimizados para ser utilizado en consulta update:

        -- 'name1=value1, name2=value2, name3=value3, ...'
        """
        l = []
        names = self.GetFieldsNames(exclude=[])
        for name in names:
            value = self(name).value
            if isinstance(value, BaseField):
                value = value.value
            if isinstance(value, (str, datetime.date, datetime.datetime)):
                l.append("{}='{}'".format(name, value))
            elif value is None:
                l.append("{}=NULL".format(name))
            else:
                l.append("{}={}".format(name, value))
        return ", ".join(l)

    def GetTableName(self):
        """
        Obtiene el nombre de la tabla de la base de datos
        correspondiente a este modelo.
        """
        return self.Meta.table_name

    def Save(self, commit=True):
        """
        Almacena los datos en la base de datos.
        """
        if not self.id:
            # Nuevo objeto.
            fields = self.GetFieldsString(exclude="id")
            values = self.GetValuesString(exclude="id")
            sql = "INSERT INTO {} ({}) VALUES ({})".format(self.GetTableName(), fields, values)
        else:
            # Modificar objeto.
            fields_values = self.GetFieldsAndValuesString(exclude="id")
            sql = "UPDATE {} SET {} WHERE id={}".format(self.GetTableName(), fields_values, self.id)
            print(sql)
        try:
            self.objects.cursor.execute(sql)
            if commit:
                self.objects.conn.commit()
        except BaseException as e:
            raise DatabaseError(e, self.name, _("No fue posible guardar los datos en la base de datos."), sql=sql)

    def Set(self, id):
        """
        Establece este objeto, sus valores, según el id indicado.
        Se busca el registro correspondiente en la base de datos.
        """
        # El 'id' debe ser un número entero mayor que 0
        if not id:
            return self
        try:
            id = int(id)
        except TypeError as e:
            raise DatabaseError(e, self.name, "El id '{}' no es válido para el modelo '{}'. {}.".format(id, self.GetVerboseName(), e))
        if id < 1:
            raise DatabaseError(None, self.name, "El id '{}' no es válido para el modelo '{}'".format(id, self.GetVerboseName()))

        # Buscamos en la base de datos el registro correspondiente.
        fieldsname = self.GetFieldsNames()
        sql = "SELECT {} FROM {} WHERE id = {}".format(", ".join(fieldsname), self.GetTableName(), id)

        self.objects.cursor.execute(sql)
        values = self.objects.cursor.fetchone()

        i = 0
        for name in fieldsname:
            setattr(self, name, values[i])
            i += 1
        return self

    def SetValues(self, values, fieldsnames=[]):
        if not fieldsnames:
            fieldsnames = self.GetFieldsNames()
        i = 0
        for name in fieldsnames:
            setattr(self, name, values[i])
            i += 1

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
            # Se establece cada elemento, en el mismo orden en que
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

    def Validar(self):
        """
        Valida los datos introduccidos para comprovar que 
        todo está correcto para ser almacenados en la base de datos.

        Si existen errores, retorna una lista con los nombres de las
        fields que los contienen y un mensaje. 

        [(name, msg), (name, msg), ...]
        """
        errors = []
        for name, field in self.GetFields():
            value = field.value 
            # Si el valor es nulo y la field no acepta valores nulos.
            if (value == None) and (field.null == False):
                # En caso de que si acepte valores vacios.
                if field.blank == True:
                    field.value = ""
                else:
                    errors.append((name, _("El campo '{}' no puede ser nulo.".format(name))))
            # Si el valor es vacio y la field no acepta valores vacios.
            elif (value == "") and (field.blank == False):
                errors.append((name, _("El campo '{}' no puede estar vacio.".format(name))))
        return errors
                    

