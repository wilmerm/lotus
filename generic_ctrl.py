"""
Módulo que contiene clases wxPanel genericas
prediseñadas para diversos usos.
"""




import wx
# Módulos del proyecto.
from var import *
from fuente.translation import gettext as _
import img








class PanelList(wx.Panel):
    """
    Panel que muestra un listado de elementos.
    """
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        # Declaración de los controles.
        self.listctrl_1 = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES, name="listctrl_1")
        # Llamado a las funciones de inicialización.
        self.__set_properties()
        self.__do_layout()
        # Eventos.
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected, self.listctrl_1)

    def __set_properties(self):
        pass

    def __do_layout(self):
        s1 = wx.BoxSizer(wx.VERTICAL)
        s2 = wx.BoxSizer(wx.VERTICAL)
        s2.Add(self.listctrl_1, 1, wx.EXPAND|wx.ALL, 5)
        s1.Add(s2, 1, wx.EXPAND)
        self.SetSizer(s1)
        self.Layout()

    def OnListItemSelected(self, event):
        print("holamundo")
        event.Skip()

    def SetItems(self, queryset):
        """
        Establece los items al listctrl.
        """
        lc = self.listctrl_1
        # Establecemos las columnas.
        i = 0
        lc.DeleteAllColumns()
        for name in queryset.model.GetFieldsNames(verbose_name=True):
            lc.InsertColumn(i, name)
            i += 1
        # Establecemos los items.
        lc.DeleteAllItems()
        i = 0
        for model in queryset:
            lc.InsertItem(i, str(model.id))
            c = 0
            for field in model:
                lc.SetItem(i, c, str(field))
                c += 1
            i += 1




class PanelDetail(wx.Panel):
    """
    Panel que muestra el detalle de un elemento.
    """
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        # Declaración de los controles.
        self.bitmap1 = wx.BitmapButton(self, bitmap=img.Bitmap(IMG_PERSON, S128, S128))
        self.listctrl1 = wx.ListCtrl(self, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES, name="listctrl_1")
        # Llamado a las funciones de inicialización.
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        pass

    def __do_layout(self):
        s1 = wx.BoxSizer(wx.VERTICAL)
        s2 = wx.BoxSizer(wx.VERTICAL)
        s2.Add(self.bitmap1, 0, wx.ALL, 5)
        s2.Add(self.listctrl1, 1, wx.EXPAND|wx.ALL, 5)
        s1.Add(s2, 1, wx.EXPAND)
        self.SetSizer(s1)
        self.Layout()

    def SetDetail(self, obj):
        lc = self.listctrl1
        lc.DeleteAllColumns()
        lc.InsertColumn(0, "Campo")
        lc.InsertColumn(1, "Valor")
        lc.DeleteAllItems()

        i = 0
        for field in obj:
            lc.InsertItem(i, field.verbose_name)
            lc.SetItem(i, 1, str(field))
            i += 1






class PanelForm(wx.Panel):
    """
    Un wxPanel que tiene los metodos predefinidos para 
    la manipulación del modelo Cliente, en lo que 
    conlleva la creación, edicción y eliminación.
    """
    def __init__(self, parent, id=-1, model=None, name="PanelForm"):
        wx.Panel.__init__(self, parent=parent, id=id, name=name)
        self.model = model

        # Declaramos el parametro 'fields' con los nombres de los 
        # controles que manipulan cada field en el modelo.
        # Si no se indica, la clase PanelForm lo tomará de las 
        # fields que dice el modelo.
        if not "fields" in self.__dict__:
            self.fields = self.model.GetFieldsNames()

    def Save(self):
        """
        Guarda los datos del modelo en la base de datos.
        """
        # Verificamos si es una creación o edición,
        # comprabando el id del panel es mayor a 0
        if self.GetId() > 0:
            # Edicción.
            return self.Edit()
        else:
            return self.Create()
        

    def Create(self):
        values = self.GetValues()
        obj = self.model()
        for name in values:
            value = values[name]
            obj.SetFieldValue(name, value)
        obj.Save()

    def Edit(self):
        pass
        

    def GetValues(self):
        """
        Obtiene un diccionario con los diferentes valores de los 
        controles o miembros declarados para la manipulación de 
        cada field en el modelo.
        """
        dic = {}
        for name in self.fields:
            ctrl = getattr(self, name)
            value = ctrl.GetValue()
            dic[name] = value
        return dic




class ModelCtrl(wx.Button):

    def __init__(self, parent, id=-1, model=None, name="ModelCtrl"):
        wx.Button.__init__(self, parent=parent, id=id, label=model.Meta.verbose_name, name=name)
        
        self.model = model
        # Evento.
        self.Bind(wx.EVT_BUTTON, self.OnButton, self)
        

    def __str__(self):
        return self.model.name

    def OnButton(self, event):
        print("Aun no implementado.")
        event.Skip()

    




class ComboBox(wx.ComboBox):
    """
    Un wxComboBox con algunas modificaciones.

    El parametro choices acepta tanto un listado:
        choices = ('value1', 'value2', ...,)

    como un listado de string y sus  nombres para mostrar:
        choices = (
            ('value1', 'Verbose name'), 
            ('value2', 'Verbose name'), 
            ...,
        )
    """
    def __init__(self, parent, id=-1, value="", choices=[], style=0, name="ComboBox"):
        # Si los items del parámetro 'choices' son tipos lista o tuplas,
        # entonces deben estar en el formato ('value', 'Verbose name'), ...
        # en dicho caso tomamos el segundo elemento de cada items.
        if isinstance(choices[0], (tuple, list)):
            new = []
            for item in choices:
                new.append(str(item[1]))
            self.choices2 = choices 
            choices = new 
        else:
            new = []
            for item in choices:
                new.append((item, item))
            self.choices2 = new 

        wx.ComboBox.__init__(self, parent=parent, id=id, value=value, choices=choices, style=style, name=name)







class BoxSizer(wx.BoxSizer):
    """
    Un wxBoxSizer con algunas modificaciones.
    """
    def __init__(self, orient=wx.HORIZONTAL):
        wx.BoxSizer.__init__(self, orient)


    def AddLabel(self, parent, text, margin=5, expand=False):
        """
        Agrega un wxStaticText al sizer.
        """
        st = wx.StaticText(parent, -1, text)
        self.Add(st, 0, wx.ALL, margin)

    def AddLine(self, parent, margin=5, expand=True, proportion=0):
        """
        Agrega una linea separadora.
        """
        sl = wx.StaticLine(parent, -1)
        if expand:
            self.Add(sl, proportion, wx.EXPAND|wx.ALL, margin)
        else:
            self.Add(sl, proportion, wx.ALL, margin)





