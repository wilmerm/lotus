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
        # Declaraciósn de los controles.
        self.listctrl_1 = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES, name="listctrl_1")
        # Miebros.
        self.selection = None # Indica el último id seleccionado en el listctrl
        # Llamado a las funciones de inicialización.
        self.__set_properties()
        self.__do_layout()
        # Eventos.
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelected, self.listctrl_1)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated, self.listctrl_1)

    def __set_properties(self):
        pass

    def __do_layout(self):
        s1 = wx.BoxSizer(wx.VERTICAL)
        s2 = wx.BoxSizer(wx.VERTICAL)
        s2.Add(self.listctrl_1, 1, wx.EXPAND|wx.ALL, 5)
        s1.Add(s2, 1, wx.EXPAND)
        self.SetSizer(s1)
        self.Layout()

    def OnListItemActivated(self, event):
        lc = self.listctrl_1
        i = lc.GetFirstSelected()
        self.selection = lc.GetItemText(i)
        if isinstance(self.GetParent(), wx.Dialog):
            self.GetParent().EndModal(wx.ID_OK)
        event.Skip()

    def OnListItemSelected(self, event):
        lc = self.listctrl_1
        i = lc.GetFirstSelected()
        self.selection = lc.GetItemText(i)
        event.Skip()
        
    def GetSelection(self):
        return self.selection

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
    def __init__(self, parent, id=-1, model=None, mode=NEW, name="PanelForm"):
        wx.Panel.__init__(self, parent=parent, id=id, name=name)
        self.model = model
        self.mode = mode
        self.id = id

    def Ok(self):
        """
        Operación de inicialización 2, una vez que ya se ha concluido
        con el __init__ para el proceso de creación del Panel.

        Este método debe llamarse en la ventanda que hereda de esta.
        """
        # El miembro 'modelid' de este control es obligatorio.
        if not "modelid" in self.__dict__:
            self.modelid = int(self.GetId())

        if self.mode == NEW:
            # Si es un nuevo registro, establecemos un modelo sin datos
            # y establecemos el id del panel al siguiente numero de registro para asignar.
            self.object = self.model()
            self.modelid = int(self.object.GetNextId())
        elif self.mode == EDIT:
            # Si es una edicción, traemos el modelo correspondiente.
            self.object = self.model(self.modelid)

        # Si por casualidad tenemos el campo id mostrado al usuario en un ctrl, entonces 
        # establemos su valor automáticamente, de todos modos el valor self.id será 
        # establecido.
        try:
            if isinstance(self.id, wx.Window):
                self.id.SetValue(str(self.modelid))
        except AttributeError:
            self.id = self.modelid

        # Declaramos el parametro 'fields' con los nombres de los 
        # controles que manipulan cada field en el modelo.
        # y como valores el tipo de dato y si es requerida, en un listado.
        # Ejemplo: 
        #    self.fields = {
        #        'id': ['INT', True],
        #        'nombres': ['STR', False],
        #        ...
        #    }
        # Si no se indica, la clase PanelForm lo tomará de las 
        # fields que dice el modelo.
        if not "fields" in self.__dict__:
            self.fields = {}
            fields = self.model().GetFields()
            for t in fields:
                name, field = t
                self.fields[field.name] = [field.type, field.required]
        # El miembro exclude es una lista de string con los nombres 
        # de las fields que se desean excluir de las edición por parte
        # del usuario.
        if not "exclude" in self.__dict__:
            self.exclude = []
        # Las fields excluidas le ponemos el valor required en False.
        for name in self.exclude:
            try:
                self.fields[name] = [self.fields[name][0], False]
            except KeyError:
                name = "{}_id".format(name)
                self.fields[name] = [self.fields[name][0], False]


    def Save(self):
        """
        Guarda los datos del modelo en la base de datos.
        """
        # Verificamos si es una creación o edición,
        if self.mode == NEW:
            self.Create()
        elif self.mode == EDIT:
            self.Edit()
        
    def Create(self):
        values = self.GetValues()
        print(values)
        if values == None:
            return 
        obj = self.model()
        for name in values:
            if name == "id":
                continue
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
            pytype = self.fields[name][0]
            required = self.fields[name][1]
            try:
                ctrl = getattr(self, name)
            except AttributeError:
                # Las fields que son ForeignKey, tienen el sufijo '_id' al final
                # del nombre de la field: cliente_id, cuenta_id, user_id, ...
                if name[-3:] == "_id":
                    name = name[0:-3]
                    ctrl = getattr(self, name)

            if isinstance(ctrl, wx.Window):
                value = ctrl.GetValue()
    
            else:
                value = ctrl

            if (required == True) and (value in ("", None)):
                wx.MessageBox(_("El campo '{}' es requerido.".format(name)))
                try:
                    ctrl.SetFocus()
                except AttributeError:
                    pass 
                return None

            dic[name] = value
        return dic




class ModelCtrl(wx.Button):
    """
    Un control para la manipulación de modelos.
    Este es un wxButton que al hacer click abre un wxDialog
    para la selección de objeto del tipo modelo indicado.
    """
    def __init__(self, parent, id=-1, model=None, name="ModelCtrl"):
        wx.Button.__init__(self, parent=parent, id=id, label=model.Meta.verbose_name, name=name)
        
        self.model = model
        self.object = self.model()
        # Evento.
        self.Bind(wx.EVT_BUTTON, self.OnButton, self)
        
    def __str__(self):
        return self.model.name

    def OnButton(self, event):
        dlg = wx.Dialog(self, -1, self.model.Meta.verbose_name)
        dlg.panel1 = PanelList(parent=dlg, id=-1)
        dlg.SetSize(800, 600)
        qs = self.object.objects.all()
        dlg.panel1.SetItems(qs)
        dlg.ShowModal()
        selection = dlg.panel1.GetSelection()
        self.SetObject(selection)
        event.Skip()

    def GetValue(self):
        """
        Obtiene el 'id' del modelo de este control.
        """
        id = self.object.id
        print(id, "---", self.model)
        return id

    def GetObject(self):
        """
        Obtiene la instancia del modelo asociado a 
        este control.
        """
        return self.object

    def GetModel(self):
        """
        Obtiene la clase Model asociada a este ctrl.
        """
        return self.model 

    def SetObject(self, id):
        """
        Establece el objeto del modelo asociado según
        el id del registro indicado.
        """
        self.object = self.model(id)
        self.SetLabel(str(self.object))
    


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

    def GetValue(self, verbose_name=False):
        """
        Obtiene el elemento seleccionado
        """ 
        if verbose_name:
            return self.choices2[self.GetSelection()][1]
        return self.choices2[self.GetSelection()][0]




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





