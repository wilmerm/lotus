"""
Módulo que contiene el panel para 
que los usuarios manipulen el 
registro de los clientes.
"""




import wx
# Módulos del proyecto.
from var import *
from fuente.translation import gettext as _
import img
from generic_ctrl import *
from models import *






class ClientePanelList(wx.Panel):
    """
    Panel que muestra un listado de clientes.
    """
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        # Declaración de los controles.
        self.searchctrl1 = wx.SearchCtrl(self, name="searchctrl1")
        self.listctrl1 = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES, name="listctrl_1")
        self.button1 = wx.BitmapButton(self, wx.ID_ADD, bitmap=img.Bitmap(IMG_ADD, S64, S64))
        self.button2 = wx.BitmapButton(self, wx.ID_EDIT, bitmap=img.Bitmap(IMG_EDIT, S64, S64))
        self.button3 = wx.BitmapButton(self, wx.ID_DELETE, bitmap=img.Bitmap(IMG_DELETE, S64, S64))
        # Llamado a las funciones de inicialización.
        self.__set_properties()
        self.__do_layout()
        # Eventos.
        self.Bind(wx.EVT_TEXT, self.OnSearch, self.searchctrl1)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected, self.listctrl1)

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

    def OnListItemSelected(self, event):
        event.Skip()

    def OnSearch(self, event):
        text = event.GetEventObject().GetValue()
        queryset = Cliente().objects.search(text)
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
        return Cliente().objects.get(id = sel)

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





class ClientePanelDetail(PanelDetail):
    """
    Panel que muestra la información de un cliente.
    """
    def __init__(self, *args, **kwargs):
        PanelDetail.__init__(self, *args, **kwargs)

    



class ClientePanel(wx.Panel):
    """
    Panel completo para la manipulación de clientes.
    """
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.model = Cliente
        self.sp1 = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.panel1 = ClientePanelList(self.sp1, 1, name="cliente_list")
        self.panel2 = ClientePanelDetail(self.sp1, 2, name="cliente_detail")
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