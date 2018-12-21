"""
Aquí creamos los diferentes modelos de base de datos.
"""



# Módulos del proyecto.
from var import *
from fuente.translation import gettext as _
from database import ModelBase, Field, QuerySet






class Cliente(ModelBase):
    """
    Modelo de base de datos para 
    la gestión de los clientes.
    """
    # Fields.
    id = Field("id", _("Id"), INT)
    cedula = Field("cedula", _("Cédula"), STR, _("Número de identificación personal."))
    nombres = Field("nombres", _("Nombres"), STR, _("Nombres del cliente."))
    apellidos = Field("apellidos", _("Apellidos"), STR, _("Apellidos del cliente."), False)
    nacimiento = Field("nacimiento", _("Fecha de nacimiento"), DATE, "", False)
    email = Field("email", _("Correo electrónico"), STR, "", False)
    telefono = Field("telefono", _("Teléfono"), STR, "", False)
    direccion = Field("direccion", _("Dirección"), STR, "", False)
    nota = Field("nota", _("Nota"), STR, "", False)
    tags = Field("tags", required=False)

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
    id = Field("id", _("Id"), INT)
    password = Field("password", _("Contraseña"), STR)
    last_login = Field("last_login", _("Último acceso"), DATETIME)
    is_superuser = Field("is_superuser", _("¿Es superusuario?"), BOOL)
    username = Field("username", _("Nombre de usuario"), STR)
    first_name = Field("first_name", _("Nombres"), STR)
    last_name = Field("last_name", _("Apellidos"), STR)
    email = Field("email", _("Correo electrónico"), STR)
    is_staff = Field("is_staff", _("¿Es staff?"), BOOL)
    is_active = Field("is_active", _("¿Está activo?"), BOOL)
    date_joined = Field("date_joined", _("Fecha de registro"), DATETIME)
    identificacion = Field("identificacion", _("Identificación"), STR)
    identificacion_tipo = Field("identificacion_tipo", _("Tipo de identificación"), STR)

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
    id = Field("id", "Id", INT)
    numero = Field("numero", _("Número"), STR)
    fecha_creacion = Field("fecha_creacion", _("Fecha de creación"), DATETIME)
    tags = Field("tags", required=False)
    cliente = Field(Cliente, _("Cliente"), INT)
    user = Field(User, _("Usuario"), INT)

    class Meta:
        table_name = "contabilidad_cuenta"
        verbose_name = "Cuenta"
        verbose_name_plural = "Cuentas"


    def __init__(self, id=None):
        ModelBase.__init__(self, id)

    def __str__(self):
        return str(self.numero)




class Prestamo(ModelBase):
    """
    Modelo para la gestión de préstamos en la base de datos.
    """
    id = Field("id", _("Id"), INT)
    cuotas = Field("cuotas", _("Cuotas"), INT)
    fecha_inicio = Field("fecha_inicio", _("Fecha de inicio"), DATE)
    monto = Field("monto", _("Monto"), DECIMAL)
    periodo = Field("periodo", _("Periodo"), STR)
    tasa = Field("tasa", _("Tasa"), DECIMAL)
    fecha_creacion = Field("fecha_creacion", _("Fecha de creación"), DATETIME)
    cuenta = Field(Cuenta, _("Cuenta"), INT)
    cliente = Field(Cliente, _("Cliente"), INT)
    cuotas_tipo = Field("cuotas_tipo", _("Tipo de cuotas"), STR)
    tags = Field("tags", required=False)

    class Meta:
        table_name = "prestamos_prestamo"
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"


    def __init__(self, id=None):
        ModelBase.__init__(self, id)

    def __str__(self):
        return str(self.nombres)


