"""
Controles wxPython predefinidos.
"""

import datetime
import wx
import wx.adv
import wx.lib.scrolledpanel
from fuente.database import *
from fuente.base import Fecha 
from fuente.translation import gettext as _






class FieldError(BaseException):

    def __init__(self, message="", error=None):
        self.message = message
        self.error = error # Exception 

    def __str__(self):
        #print(self.error)
        return self.message




class HiddenCtrl(object):
    """
    Un control oculto para el usuario.
    """

    def __init__(self, parent, fieldname):
        self.parent = parent 
        self.field = parent.object(fieldname)
        self.SetValue(self.field.value)

    def GetLabel(self):
        return self.field.verbose_name

    def GetValue(self):
        return self.field.value 

    def SetValue(self, value):
        try:
            self.field.value = value 
        except ValueError:
            raise FieldError(_("El valor '{}' no válido para el campo '{}'".format(value, self.field.verbose_name)))




class TextCtrl(wx.TextCtrl):
    """
    Para la manipulación de CharField.
    """
    
    def __init__(self, parent, fieldname, style=0):
        """
        fieldname es el nombre del objeto Model.Field que se a
        asociará a este control.
        """
        wx.TextCtrl.__init__(self, parent=parent, name=fieldname, style=style)

        self.field = parent.object(fieldname)
        self.SetValue(self.field.value)
        self.SetToolTip(wx.ToolTip(self.field.help_text))

        self.Bind(wx.EVT_TEXT, self.OnText, self)
        # Propiedades.
        self.SetMinSize((300, 32))

    def OnText(self, event):
        self.field.value = self.GetValue()
        event.Skip()

    def GetLabel(self):
        return self.field.verbose_name

    def SetValue(self, value):
        """
        Establece el valor al ctrl.
        """
        try:
            self.field.value = value 
        except (ValueError, TypeError) as e:
            raise FieldError(_("El valor '{}' no válido para el campo '{}'.".format(value, self.field.verbose_name)), e)
        super().SetValue(str(self.field.value))

        




class PasswordCtrl(TextCtrl):
    """
    Para la manipulación de CharField tipo contraseña.
    """
    def __init__(self, parent, fieldname):
        TextCtrl.__init__(self, parent=parent, fieldname=fieldname, style=wx.TE_PASSWORD)
        



class IntegerCtrl(TextCtrl):
    """
    Para la manipulación de números enteros.
    """
    def __init__(self, parent, fieldname):
        TextCtrl.__init__(self, parent=parent, fieldname=fieldname, style=wx.TE_RIGHT)
        self.Bind(wx.EVT_TEXT, self.OnText, self)

        #self.Bind(wx.EVT_TEXT, self.OnText, self)

    def OnText(self, event):
        self.field.value = self.GetValue()
        event.Skip()

    def GetValue(self):
        """
        Retorna el valor del control en un 
        número entero.
        """
        return int(float(super().GetValue()))
    
    def SetValue(self, value):
        # Solo acepta números enteros.
        try:
            value = int(float(value))
        except BaseException:
            pass 
        else:
            return super().SetValue(value)

    



class FloatCtrl(TextCtrl):
    """
    Para la manipulación de floatfield.
    """
    def __init__(self, parent, fieldname):
        TextCtrl.__init__(self, parent, fieldname, style=wx.TE_RIGHT)

        #self.Bind(wx.EVT_TEXT, self.OnText, self)

    def OnText(self, event):
        self.field.value = self.GetValue()
        event.Skip()

    def GetValue(self):
        return float(super().GetValue())

    def SetValue(self, value):
        # Solo acepta números float
        try:
            value = float(value)
        except BaseException:
            pass 
        else:
            return super().SetValue(value)



class DecimalCtrl(FloatCtrl):
    """
    Para la manipulación de DecimalField.
    """
    def __init__(self, parent, fieldname):
        FloatCtrl.__init__(self, parent, fieldname)

        #self.Bind(wx.EVT_TEXT, self.OnText, self)

    def OnText(self, event):
        self.field.value = self.GetValue()
        event.Skip()

    def GetValue(self):
        return Decimal(str(super().GetValue()))

    def SetValue(self, value):
        # Solo acepta números Decimal
        try:
            value = Decimal(str(value))
        except BaseException as e:
            print(e)
        else:
            return super().SetValue(value)







class DateCtrl(wx.adv.DatePickerCtrl):
    """
    Para la manipulaicón de DateField.
    """
    def __init__(self, parent, fieldname, style=wx.adv.DP_DEFAULT|wx.adv.DP_SHOWCENTURY):
        wx.adv.DatePickerCtrl.__init__(self, parent=parent, style=style)

        self.field = parent.object(fieldname)
        self.SetValue(self.field.value)
        self.SetToolTip(wx.ToolTip(self.field.help_text))
        # Propiedades.
        self.SetMinSize((300, 32))

        self.Bind(wx.adv.EVT_DATE_CHANGED, self.OnDateChanged, self)

    def OnDateChanged(self, event):
        self.field.value = self.GetValue()

    def GetLabel(self):
        return self.field.verbose_name

    def GetValue(self):
        """
        Obtiene un objeto datetime.date con la fecha
        del control.
        """
        dt = super().GetValue()
        return datetime.date(dt.year, dt.month+1, dt.day)

    def SetValue(self, dt):
        """
        Establece la fecha de este control.
        """
        try:
            self.field.value = dt
        except ValueError:
            raise FieldError(_("El valor '{}' no válido para el campo '{}'".format(value, self.field.verbose_name)))

        if not dt:
            return 
        if isinstance(dt, str):
            dt = Fecha().StrToDate()
        dt = wx.DateTime(dt.day, dt.month, dt.year)
        return super().SetValue(dt)






class ChoiceCtrl(wx.ComboBox):
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
    def __init__(self, parent, fieldname, style=0):

        choices = getattr(parent.model, fieldname).choices
        
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

        wx.ComboBox.__init__(self, parent=parent, choices=choices, style=style, name=fieldname)

        self.Bind(wx.EVT_COMBOBOX, self.OnComboBox, self)

        self.field = parent.object(fieldname)
        self.SetValue(self.field.value)
        self.SetToolTip(wx.ToolTip(self.field.help_text))

        # Propiedades.
        self.SetMinSize((300, 32))

    def OnComboBox(self, event):
        self.field.value = self.GetValue(verbose_name=False)
        event.Skip()

    def GetLabel(self):
        return self.field.verbose_name

    def GetValue(self, verbose_name=False):
        """
        Obtiene el elemento seleccionado
        """ 
        if verbose_name:
            return self.choices2[self.GetSelection()][1]
        return self.choices2[self.GetSelection()][0]

    def GetVerboseName(self, value):
        """
        Obtiene el verbose_name correspondiente al name indicado.
        """
        for name, vname in self.choices2:
            if name == value:
                return vname 
        return ""

    def GetIndex(self, value):
        """
        Obtiene la posición del elemento en el choice.
        """
        index = 0
        for name, vname in self.choices2:
            if name == value:
                return index 
            index += 1
        return -1

    def SetValue(self, value):
        """
        Establece el valor al ctrl.
        """
        try:
            self.field.value = value 
        except ValueError:
            raise FieldError(_("El valor '{}' no válido para el campo '{}'".format(value, self.field.verbose_name)))
        try:
            super().SetValue(self.GetVerboseName(value))
        except TypeError:
            self.SetValue("")



class ModelCtrl(wx.Button):
    """
    Un control para la manipulación de modelos.
    Este es un wxButton que al hacer click abre un wxDialog
    para la selección de objeto del tipo modelo indicado.
    """
    def __init__(self, parent, fieldname):
        wx.Button.__init__(self, parent=parent, id=-1, label=fieldname.title(), name=fieldname)
        
        self.field = parent.object(fieldname)
        self.model = self.field.model
        self.object = self.field.object

        self.SetValue(self.field.value)
        self.SetToolTip(wx.ToolTip(self.field.help_text))
        # Evento.
        self.Bind(wx.EVT_BUTTON, self.OnButton, self)
        # propiedades.
        self.SetMinSize((300, 50))

    def __str__(self):
        return str(self.object)

    def OnButton(self, event):
        dlg = wx.Dialog(self, -1, self.object.GetModelName())
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
        return int(self.object.id)

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

    def SetObject(self, value):
        """
        Establece el objeto del modelo asociado según
        el id del registro indicado.
        """
        if isinstance(value, ModelBase):
            self.object = value
        else:
            self.object = self.model(value)
        self.field.value = self.object.id
        # Establecemos el label.
        if not self.object:
            self.SetLabel(_("Seleccione el campo {}".format(self.object.GetModelName())))
        else:
            self.SetLabel(str(self.object))

    def SetValue(self, value):
        """
        Establece el valor a este control.
        """
        return self.SetObject(value)



class ModelForm(wx.lib.scrolledpanel.ScrolledPanel):
    """
    Un panel para la gestión de una instancia de un modelo.
    """
    def __init__(self, parent, modelid=None, model=None, mode=NEW):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, parent)
        self.SetupScrolling()
        
        self.__dict__["modelid"] = modelid
        self.__dict__["mode"] = mode 
        self.__dict__["model"] = model
        self.__dict__["object"] = model()
        self.__dict__["id"] = TextCtrl(self, "id", style=wx.TE_READONLY)
        # Indicar los nombres de las fields y los wx controles 
        # que manejarán los datos.
        self.__dict__["fields"] = {
            "id": self.id,
        }

        if mode == NEW:
            self.id.SetValue(str(self.object.GetNextId()))
        elif mode == EDIT:
            self.object.Set(modelid)
            self.id.SetValue(str(self.object.id))
        
        self.button_ok = wx.Button(self, wx.ID_OK, _("Aceptar"), pos=(20, 20))
        self.button_cancel = wx.Button(self, wx.ID_CANCEL, _("Cancelar"), pos=(120, 20))

        self.Bind(wx.EVT_BUTTON, self.OnOk, self.button_ok)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.button_cancel)

    def __setattr__(self, name, value):
        try:
            field = self.fields
        except AttributeError:
            return super().__setattr__(name, value)
        if name in self.fields:
            self.__dict__[name].SetValue(value)
        else:
            return super().__setattr__(name, value)

    def OnCancel(self, event):
        event.Skip()

    def OnOk(self, event):
        if self.Save():
            event.Skip()

    def Save(self):
        """
        Guarda en la base de datos, 
        los datos introduccidos en el modelo.
        """
        # Validamos los datos introduccidos.
        validate = self.object.Validar()
        if validate:
            name, msg = validate[0]
            ctrl = self.fields[name]
            ctrl.SetFocus()
            wx.MessageBox(msg, name)
            return False
        try:
            self.object.Save(commit=True)
        except DatabaseError as e:
            wx.MessageBox(str(e), _("No se guardó"))
            return False
        return True






    








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
