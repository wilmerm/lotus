"""
Módulo que contiene el panel para 
que los usuarios manipulen el 
registro de los clientes.
"""



import datetime
import wx
# Módulos del proyecto.
from var import *
import conf
from fuente.translation import gettext as _
import img
from generic_ctrl import *
from models import *











class PrestamoPanelForm(PanelForm):
    """
    Panel que muestra un formulario de edicción de préstamos.
    """
    model = Prestamo

    def __init__(self, parent, id=-1, mode=NEW, name="PrestamoPanelForm"):

        PanelForm.__init__(self, parent=parent, id=id, model=self.model, mode=mode, name=self.model.Meta.verbose_name)

        # Declaración de los controles.
        self.id = wx.TextCtrl(self, name="id")
        self.cuotas = wx.SpinCtrl(self, min=1, max=10000, initial=1,  name="cuotas")
        self.monto = wx.SpinCtrlDouble(self, min=0, max=1000000000, inc=100, name="monto")
        self.periodo = ComboBox(self, choices=PERIODO_CHOICES, name="periodo")
        self.tasa = wx.SpinCtrlDouble(self, min=0, max=100, initial=conf.getconf("tasa_default").value, inc=1, name="tasa")
        self.cliente = ModelCtrl(self, 0, Cliente, name="cliente")
        self.cuotas_tipo = ComboBox(self, choices=CUOTA_TIPOS, name="cuotas_tipo")
        self.fecha_inicio = datetime.datetime.today()
        # Campos automáticos.
        self.fecha_creacion = datetime.datetime.today()
        self.cuenta = Cuenta()
        self.tags = str()
        # Buttons.
        self.button1 = wx.Button(self, wx.ID_SAVE, _("Guardar"))
        self.button2 = wx.Button(self, wx.ID_CANCEL, _("Cancelar"))
        # Eventos.
        self.Bind(wx.EVT_BUTTON, self.OnButton, id=wx.ID_SAVE)
        self.Bind(wx.EVT_BUTTON, self.OnButton, id=wx.ID_CANCEL)

        # los siguientes nombres de controles (fields) serán excluidos
        self.exclude = ["fecha_creacion", "cuenta", "tags"]

        # Funciones de inicialización.
        self.__do_layout()
        self.Ok() # Función del PanelForm, que realiza operaciones de inicialización.
    
    def __do_layout(self):
        s1 = wx.BoxSizer(wx.VERTICAL)
        s2 = wx.BoxSizer(wx.VERTICAL)
        # id
        s3 = wx.BoxSizer(wx.VERTICAL)
        s3.Add(wx.StaticText(self, label=_("Id")), 0, wx.ALL, 5)
        s3.Add(self.id, 1, wx.ALL, 5)
        s2.Add(s3, 0)
        s2.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        # cuotas
        s4 = wx.BoxSizer(wx.VERTICAL)
        s4.Add(wx.StaticText(self, label=_("Cuotas")), 0, wx.ALL, 5)
        s4.Add(self.cuotas, 1, wx.ALL, 5)
        s2.Add(s4, 0)
        s2.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        # fecha_inicio
        s5 = wx.BoxSizer(wx.VERTICAL)
        # monto 
        s6 = wx.BoxSizer(wx.VERTICAL)
        s6.Add(wx.StaticText(self, label=_("Monto")), 0, wx.ALL, 5)
        s6.Add(self.monto, 1, wx.ALL, 5)
        s2.Add(s6, 0)
        s2.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        # periodo
        s7 = wx.BoxSizer(wx.VERTICAL)
        s7.Add(wx.StaticText(self, label=_("Periodo")), 0, wx.ALL, 5)
        s7.Add(self.periodo, 1, wx.ALL, 5)
        s2.Add(s7, 0)
        s2.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        # tasa 
        s8 = wx.BoxSizer(wx.VERTICAL)
        s8.Add(wx.StaticText(self, label=_("Tasa")), 0, wx.ALL, 5)
        s8.Add(self.tasa, 1, wx.ALL, 5)
        s2.Add(s8, 0)
        s2.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        # cliente 
        s9 = wx.BoxSizer(wx.VERTICAL)
        s9.Add(wx.StaticText(self, label=_("Cliente")), 0, wx.ALL, 5)
        s9.Add(self.cliente, 1, wx.EXPAND|wx.ALL, 5)
        s2.Add(s9, 0, wx.EXPAND)
        s2.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        # cuotas_tipo
        s10 = wx.BoxSizer(wx.VERTICAL)
        s10.Add(wx.StaticText(self, label=_("Tipo de cuota")), 0, wx.ALL, 5)
        s10.Add(self.cuotas_tipo, 1, wx.ALL, 5)
        s2.Add(s10, 0)
        s2.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        # Buttons.
        s11 = wx.BoxSizer(wx.HORIZONTAL)
        s11.Add(self.button1, 0, wx.ALL, 5)
        s11.Add(self.button2, 0, wx.ALL, 5)
        s2.Add(s11, 0)
        # Realizamos el sizer.
        s1.Add(s2, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(s1)
        self.Layout()

    def OnButton(self, event):
        if event.GetId() == wx.ID_SAVE:
            self.CrearCuenta()
            self.Save()
        event.Skip()

    def CrearCuenta(self):
        """Crea la cuenta."""
        self.cuenta.id = None
        self.cuenta.numero = self.cuenta.GetSiguienteNumeroDeCuenta()
        self.cuenta.fecha_creacion = datetime.datetime.today()
        self.cuenta.cliente = self.cliente.GetValue()



        



class PrestamoDialogForm(wx.Dialog):
    """
    Dialogo que muestra un formaulario de edición de préstamos.
    """
    model = Prestamo 

    def __init__(self, parent, id=-1, mode=NEW, name="PrestamoDialogForm"):
        wx.Dialog.__init__(self, parent=parent, id=id, name=name)
        # Controles.
        self.panel1 = PrestamoPanelForm(parent=self, id=id, mode=mode, name=name)
        # Inicialización.
        self.__set_properties()

    def __set_properties(self):
        self.SetSize((800, 600))











class PrestamoPanelList(wx.Panel):
    """
    Panel que muestra un listado de préstamos.
    """
    model = Prestamo

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        # Declaración de los controles.
        self.searchctrl1 = wx.SearchCtrl(self, name="searchctrl1")
        self.listctrl1 = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES, name="listctrl_1")
        self.button1 = wx.BitmapButton(self, wx.ID_ADD, bitmap=img.Bitmap(IMG_ADD, S32, S32), name="add")
        self.button2 = wx.BitmapButton(self, wx.ID_EDIT, bitmap=img.Bitmap(IMG_EDIT, S32, S32), name="edit")
        self.button3 = wx.BitmapButton(self, wx.ID_DELETE, bitmap=img.Bitmap(IMG_DELETE, S32, S32), name="delete")
        # Llamado a las funciones de inicialización.
        self.__set_properties()
        self.__do_layout()
        # Eventos.
        self.Bind(wx.EVT_TEXT, self.OnSearch, self.searchctrl1)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected, self.listctrl1)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.button1)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.button2)
        self.Bind(wx.EVT_BUTTON, self.OnButton, self.button3)

    def __set_properties(self):
        pass

    def __do_layout(self):
        s1 = wx.BoxSizer(wx.VERTICAL)
        s2 = wx.BoxSizer(wx.VERTICAL) # content
        s3 = wx.BoxSizer(wx.HORIZONTAL) # top
        s4 = wx.BoxSizer(wx.HORIZONTAL) # bottom
        s3.Add(self.searchctrl1, 1, wx.EXPAND|wx.ALL, 5)
        s2.Add(s3, 0, wx.EXPAND)
        s2.Add(self.listctrl1, 1, wx.EXPAND|wx.ALL, 5)
        s4.Add(self.button1, 0, wx.EXPAND|wx.ALL, 5)
        s4.Add(self.button2, 0, wx.EXPAND|wx.ALL, 5)
        s4.Add(self.button3, 0, wx.EXPAND|wx.ALL, 5)
        s2.Add(s4, 0, wx.EXPAND)
        s1.Add(s2, 1, wx.EXPAND)
        self.SetSizer(s1)
        self.Layout()

    def OnButton(self, event):
        if event.GetId() == wx.ID_ADD:
            dlg = PrestamoDialogForm(parent=self, id=-1, mode=NEW, name="prestamo")
            dlg.ShowModal()
        event.Skip()

    def OnListItemSelected(self, event):
        event.Skip()

    def OnSearch(self, event):
        text = event.GetEventObject().GetValue()
        queryset = Prestamo().objects.search(text)
        self.SetItems(queryset)
        event.Skip()

    def GetSelection(self):
        """
        Obtiene el item seleccionado, como un 
        modelo de base de datos.
        """
        lc = self.listctrl1
        index = lc.GetFirstSelected()
        sel = lc.GetItemText(index)
        return self.model().objects.get(id = sel)

    def SetItems(self, queryset):
        """
        Establece los items al listctrl.
        """
        lc = self.listctrl1
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





class PrestamoPanelDetail(wx.Panel):
    """
    Panel que muestra el detalle de un elemento.
    """
    model = Prestamo 

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        # Declaración de los controles.
        self.listctrl1 = wx.ListCtrl(self, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES, name="listctrl_1")
        # Llamado a las funciones de inicialización.
        self.__do_layout()
        self.__set_properties()

    def __do_layout(self):
        s1 = wx.BoxSizer(wx.VERTICAL)
        s2 = wx.BoxSizer(wx.VERTICAL)
        s2.Add(self.listctrl1, 1, wx.EXPAND|wx.ALL, 5)
        s1.Add(s2, 1, wx.EXPAND)
        self.SetSizer(s1)
        self.Layout()

    def __set_properties(self):
        pass

    def SetDetail(self, obj):
        lc = self.listctrl1
        lc.DeleteAllColumns()
        lc.InsertColumn(0, _("Campo"))
        lc.InsertColumn(1, _("Valor"))
        lc.DeleteAllItems()

        i = 0
        for field in obj:
            lc.InsertItem(i, field.verbose_name)
            lc.SetItem(i, 1, str(field))
            i += 1


class PrestamoPanel(wx.Panel):
    """
    Panel completo para la manipulación de clientes.
    """
    model = Prestamo

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.name = "prestamo"
        self.sp1 = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.panel1 = PrestamoPanelList(self.sp1, 1, name="prestamo_list")
        self.panel2 = PrestamoPanelDetail(self.sp1, 2, name="prestamo_detail")
        self.sp1.SplitVertically(self.panel1, self.panel2, 600)
        # Eventos.
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected, self.panel1.listctrl1)
        # Funciones de inicialización.
        self.__do_layout()
        self.__set_properties()

    def __do_layout(self):
        s1 = wx.BoxSizer(wx.VERTICAL)
        s2 = wx.BoxSizer(wx.VERTICAL)
        s2.Add(self.sp1, 1, wx.EXPAND)
        s1.Add(s2, 1, wx.EXPAND)
        self.SetSizer(s1)
        self.Layout()

    def __set_properties(self):
        self.sp1.SetMinimumPaneSize(200)

    def OnListItemSelected(self, event):
        obj = self.panel1.GetSelection()
        self.panel2.SetDetail(obj)
        event.Skip()