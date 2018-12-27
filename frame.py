"""
Ventana príncipal de la aplicación.
"""


import wx
# Módulos del proyecto.
from var import *
import img
from fuente.translation import gettext as _
from models import *
from ctrls import *

from panel_prestamos import *








class Panels(wx.Panel):
    """
    Aquí estarán los panels principales que se mostrarán.

    """
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        # Declaración de paneles.
        self.panel1 = PrestamoPanel(self, name="cliente")
        self.panel2 = PrestamoPanel(self, name="prestamo")
        # Lista de paneles ya declarados.
        self.paneles = [
            self.panel1,
            self.panel2,
        ]
        # Funciones de inicialización.
        self.HideAllPanels()
        self.__do_layout()


    def __do_layout(self):
        s1 = wx.BoxSizer(wx.VERTICAL)
        s2 = wx.BoxSizer(wx.VERTICAL)
        for panel in self.paneles:
            s2.Add(panel, 1, wx.EXPAND|wx.ALL, 5)
        s1.Add(s2, 1, wx.EXPAND)
        self.SetSizer(s1)
        self.Layout()

    def HideAllPanels(self):
        """
        Oculta todos los panels.
        """
        for panel in self.paneles:
            panel.Hide()

    def ShowPanel(self, name):
        """
        Muestra el panel indicado y oculta los demás.
        name: Es el nombre del panel del parametro 'name'.
        """
        self.HideAllPanels()
        panel = self.FindWindowByName(name)
        panel.Show()
        self.Layout()

        


class Frame(wx.Frame):
    """
    Ventana príncipal.
    """
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        # Declaración de los controles. ------------------------------------------------
        # Toolbar.
        tb = wx.ToolBar(self)
        tb.AddTool(ID_PRESTAMO, _("Préstamos"), img.Bitmap(IMG_ADD, S32, S32), _("Ir al panel de préstamos."))
        tb.AddTool(ID_CLIENTE, _("Clientes"), img.Bitmap(IMG_SAVE, S32, S32), _("Ir al panel de clientes."))
        self.ToolBar = tb
        tb.Realize()
        # Panels.
        self.panels = Panels(self, name="panels")
        # Eventos.
        self.Bind(wx.EVT_MENU, self.OnMenu, id=ID_MENU_FIRST, id2=ID_MENU_LAST)
        # Llamado a las funciones de inicialización. -----------------------------------
        self.__set_properties()
        self.__do_layout()

    def __set_properties(self):
        #font = wx.Font(16, family=wx.FONTFAMILY_DEFAULT, style=wx.FONTSTYLE_NORMAL, weight=wx.FONTWEIGHT_LIGHT)
        self.SetMinSize((1024, 768))
    
    def __do_layout(self):
        s1 = wx.BoxSizer(wx.VERTICAL)
        s2 = wx.BoxSizer(wx.VERTICAL)
        s2.Add(self.panels, 1, wx.EXPAND)
        s1.Add(s2, 1, wx.EXPAND)
        self.SetSizer(s1)
        self.Layout()

    def OnMenu(self, event):
        eventid = event.GetId()
        if eventid == ID_CLIENTE:
            queryset = Cliente().objects.all()
            self.panels.ShowPanel("cliente")
        elif eventid == ID_PRESTAMO:
            self.panels.ShowPanel("prestamo")
        event.Skip()
        








    
app = wx.App()
frame = Frame(None, -1, "Hello World")
frame.Show()
app.MainLoop()
