"""
Aquí creamos los diferentes modelos de base de datos.
"""



# Módulos del proyecto.
from var import *
import conf
from fuente.translation import gettext as _
from fuente.database import ModelBase, CharField, IntegerField, FloatField, DecimalField, DateField, DateTimeField, BoolField, ModelField, QuerySet






class Cliente(ModelBase):
    """
    Modelo de base de datos para 
    la gestión de los clientes.
    """
    # Fields.
    cedula = CharField("cedula", _("Cédula"), help_text=_("Número de identificación personal."))
    nombres = CharField("nombres", _("Nombres"), help_text=_("Nombres del cliente."))
    apellidos = CharField("apellidos", _("Apellidos"), blank=True, help_text=_("Apellidos del cliente."))
    nacimiento = DateField("nacimiento", _("Fecha de nacimiento"))
    email = CharField("email", _("Correo electrónico"), blank=True, help_text=_("Dirección de correo electrónico."))
    telefono = CharField("telefono", _("Teléfono"), blank=True)
    direccion = CharField("direccion", _("Dirección"), blank=True)
    nota = CharField("nota", _("Nota"), blank=True)
    tags = CharField("tags", blank=True)

    class Meta:
        table_name = "clientes_cliente"
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


    def __init__(self, id=None):
         ModelBase.__init__(self, id)

    def __str__(self):
        return str(self.nombres)





class User(ModelBase):
    """
    Modelo de usuario para base de datos.
    """
    password = CharField("password", _("Contraseña"))
    last_login = DateTimeField("last_login", _("Último acceso"))
    is_superuser = BoolField("is_superuser", _("¿Es superusuario?"))
    username = CharField("username", _("Nombre de usuario"))
    first_name = CharField("first_name", _("Nombres"), blank=True)
    last_name = CharField("last_name", _("Apellidos"), blank=True)
    email = CharField("email", _("Correo electrónico"))
    is_staff = BoolField("is_staff", _("¿Es staff?"))
    is_active = BoolField("is_active", _("¿Está activo?"), default=True)
    date_joined = DateField("date_joined", _("Fecha de registro"), default=datetime.datetime.today())
    identificacion = CharField("identificacion", _("Identificación"))
    identificacion_tipo = CharField("identificacion_tipo", _("Tipo de identificación"))

    class Meta:
        table_name = "clientes_user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


    def __init__(self, id=None):
        ModelBase.__init__(self, id)

    def __str__(self):
        return str(self.username)




class Cuenta(ModelBase):
    """
    Modelo para la gestión de cuentas en la base de datos.
    """
    numero = CharField("numero", _("Número"))
    fecha_creacion = DateTimeField("fecha_creacion", _("Fecha de creación"), default=datetime.datetime.today())
    tags = CharField("tags", blank=True)
    cliente = ModelField("cliente", _("Cliente"), model=Cliente)
    user = ModelField("user", _("Usuario"), model=User)

    class Meta:
        table_name = "contabilidad_cuenta"
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"


    def __init__(self, id=None):
        ModelBase.__init__(self, id)

    def __str__(self):
        return str(self.numero)

    def GetSiguienteNumeroDeCuenta(self):
        """
        Obtiene el siguiente número de cuenta para nuevos registros.
        """
        try:
            maxid = self.GetLastId()
        except IndexError:
            return PRIMER_NUMERO_DE_CUENTA
        c = Cuenta(maxid)
        return str(int(c.numero) + 1)





class Prestamo(ModelBase):
    """
    Modelo para la gestión de préstamos en la base de datos.
    """
    cuotas = IntegerField("cuotas", _("Cuotas"), min=1, max=100000, blank=False)
    fecha_inicio = DateField("fecha_inicio", _("Fecha de inicio"), default=datetime.date.today())
    monto = DecimalField("monto", _("Monto"), min=0, max=10000000000)
    periodo = CharField("periodo", _("Periodo"), choices=PERIODO_CHOICES, default=MENSUAL)
    tasa = DecimalField("tasa", _("Tasa"), min=0, max=100, default=conf.getconf("tasa_default"))
    fecha_creacion = DateTimeField("fecha_creacion", _("Fecha de creación"), DATETIME)
    cuenta = ModelField("cuenta", _("Cuenta"), model=Cuenta, null=False)
    cliente = ModelField("cliente", _("Cliente"), model=Cliente, null=False, help_text=_("Cliente titular del préstamo."))
    cuotas_tipo = CharField("cuotas_tipo", _("Tipo de cuotas"), choices=CUOTA_TIPOS)
    tags = CharField("tags", blank=True)

    class Meta:
        table_name = "prestamos_prestamo"
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"

    def __init__(self, id=None):
        ModelBase.__init__(self, id)

    def __str__(self):
        return "{} {}".format(self.GetModelName(), self.id)

    def Save(self, commit=True):
        """
        Guarda este registro en la base de datos.
        """
        # Creamos la cuenta.
        cuenta = Cuenta()
        cuenta.numero = cuenta.GetSiguienteNumeroDeCuenta()
        cuenta.fecha_creacion = datetime.datetime.today()
        cuenta.tags = ""
        cuenta.cliente = self.cliente 
        cuenta.user = None
        cuenta.Save()
        self.cuenta = cuenta 
        # Fecha de creación.
        self.fecha_creacion = datetime.datetime.today()
        # Palabras claves.
        self.tags = "{} {}".format(self.cliente, self.cuenta.numero)
        super().Save(commit=commit)


