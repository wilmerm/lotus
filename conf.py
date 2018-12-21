"""
Este módulo gestiona las configuraciones 
realizadas por el usuario, para adapatar 
el programa a su gusto.
"""



from fuente.translation import gettext as _






class Conf(object):
    """
    Simula una configuración.

    Parametros:
        - key: nombre de la configuración.
        - name: nombre para mostrar.
        - value: valor de la configuración.
        - description: breve descripción.
    """
    def __init__(self, key, name="", value=None, description=""):
        self.key = key
        self.name = name
        self.value = value
        self.description = description

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "Conf({}, {}, {}, {})".format(self.key, self.name, self.value, self.description)



class Configurations(object):
    """
    Simula todas las configuraciones.
    """

    def Add(self, key, name="", value=None, description=""):
        """
        Agrega una configuración.
        """
        c = Conf(key, name, value, description)
        print(c)
        setattr(self, key, c)

    def Get(self, name):
        """
        Obtiene una configuración.
        """
        print(self.__dict__)
        return getattr(self, name)





conf = Configurations()
conf.Add("tasa_default", _("Tasa predeterminada"), 30.0, _("Tasa de préstamos predeterminada para nuevos préstamos."))
conf.Add("min_panel_size", _("Size "), 300, "")



def getconf(name):
    """
    Obtiene la configuración indicada.
    """
    return conf.Get(name)