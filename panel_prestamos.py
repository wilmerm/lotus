


import wx
from ctrls import ModelCtrl, ModelForm, TextCtrl, PasswordCtrl, IntegerCtrl, ChoiceCtrl, DecimalCtrl, DateCtrl, HiddenCtrl
import img
from fuente.translation import gettext as _
from models import *





class PrestamoForm(ModelForm):
    """
    Pane para la modificación o creación de préstamos.
    """
    def __init__(self, parent, modelid=None, mode=NEW):
        ModelForm.__init__(self, parent=parent, modelid=modelid, model=Prestamo, mode=mode)

        self.monto = DecimalCtrl(self, "monto")
        self.cuotas = IntegerCtrl(self, "cuotas")
        self.cuotas_tipo = ChoiceCtrl(self, "cuotas_tipo")
        self.periodo = ChoiceCtrl(self, "periodo")
        self.tasa = DecimalCtrl(self, "tasa")
        self.cliente = ModelCtrl(self, "cliente")
        self.cuenta = HiddenCtrl(self, "cuenta")
        self.fecha_inicio = DateCtrl(self, "fecha_inicio")

        self.fields["monto"] = self.monto 
        self.fields["cuotas"] = self.cuotas
        self.fields["cuotas_tipo"] = self.cuotas_tipo
        self.fields["periodo"] = self.periodo
        self.fields["tasa"] = self.tasa
        self.fields["cliente"] = self.cliente 
        self.fields["cuenta"] = self.cuenta 
        self.fields["fecha_inicio"] = self.fecha_inicio

        # Labels
        for key in self.fields:
            ctrl = getattr(self, key)
            if isinstance(ctrl, HiddenCtrl):
                continue
            label = wx.StaticText(self, label=ctrl.field.verbose_name)
            setattr(self, "{}__label".format(key), label)

        self.__do_layout()

    def __do_layout(self):
        s = wx.BoxSizer(wx.VERTICAL)
        s1 = wx.BoxSizer(wx.VERTICAL)

        s1.Add(self.id__label, 0, wx.ALL, 5)
        s1.Add(self.id, 0, wx.ALL, 5)
        s1.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)

        s1.Add(self.monto__label, 0, wx.ALL, 5)
        s1.Add(self.monto, 0, wx.ALL, 5)
        s1.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)

        s1.Add(self.cuotas__label, 0, wx.ALL, 5)
        s1.Add(self.cuotas, 0, wx.ALL, 5)
        s1.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)

        s1.Add(self.cuotas_tipo__label, 0, wx.ALL, 5)
        s1.Add(self.cuotas_tipo, 0, wx.ALL, 5)
        s1.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)

        s1.Add(self.periodo__label, 0, wx.ALL, 5)
        s1.Add(self.periodo, 0, wx.ALL, 5)
        s1.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)

        s1.Add(self.tasa__label, 0, wx.ALL, 5)
        s1.Add(self.tasa, 0, wx.ALL, 5)
        s1.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)

        s1.Add(self.cliente__label, 0, wx.ALL, 5)
        s1.Add(self.cliente, 0, wx.ALL, 5)
        s1.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)

        s1.Add(self.fecha_inicio__label, 0, wx.ALL, 5)
        s1.Add(self.fecha_inicio, 0, wx.ALL, 5)
        s1.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)

        s3 = wx.BoxSizer(wx.HORIZONTAL)
        s3.Add(self.button_ok, 0, wx.ALL, 5)
        s3.Add(self.button_cancel, 0, wx.ALL, 5)
        s1.Add(s3, 0, wx.EXPAND)

        s.Add(s1, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(s)
        self.Layout()




class PrestamoDialogForm(wx.Dialog):
    """
    El id es utilizado también para editar un objeto en concreto.
    """
    def __init__(self, parent, modelid=None, mode=NEW, title="", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.CAPTION):
        wx.Dialog.__init__(self, parent=parent, title=title, style=style)
        
        self.form = PrestamoForm(self, mode=mode, modelid=modelid)

        self.SetMinSize((800, 600))
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
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated, self.listctrl1)
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
            dlg = PrestamoDialogForm(parent=self, mode=NEW, title=_("Préstamo"))
            dlg.ShowModal()
        event.Skip()

    def OnListItemActivated(self, event):
        obj = self.GetSelection()
        dlg = PrestamoDialogForm(parent=self, mode=EDIT, modelid=obj.id, title=_("Préstamo"))
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
        lc.DeleteAllColumns()
        lc.InsertColumn(0, "id", width=0)
        i = 1
        for name in queryset.model.GetFieldsNames(verbose_name=True):
            lc.InsertColumn(i, name)
            i += 1
        # Establecemos los items.
        lc.DeleteAllItems()
        i = 0
        for model in queryset:
            lc.InsertItem(i, str(model.id))
            c = 1
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