from django import forms
from financiero.orden_pago.models import OrdenPago, Centro_Costos, Egresos,OrdenPagoFile
from datetime import date
from django.forms.models import inlineformset_factory

class OrdenPagoForm(forms.ModelForm):
    class Meta:
        model = OrdenPago

        fields = "__all__"

        labels = {
            "cod_ord_pago":"",
            "fecha":"",
            "estado":"",
            "tipo_proveedor":"Tipo de proveedor",
            "proveedor":"Razón social/Nombre",
            "centro_costos":"Centro de costos",
            "n_comprobante":"N° de comprobante",
            "concepto":"Concepto",
            "forma_pago":"Forma de pago",
            "fecha_comprobante":"Fecha de comprobante",
            "motivo_anular":"Motivo de Anulación",
            "subtotal":"",
            "total":"",
            "valor_iva":"",
            "iva":"Grava IVA",
            "otros_cargos":""
        }

        widgets = {
            "evento":forms.HiddenInput(),
            "egreso":forms.HiddenInput(),
            "n_tramite":forms.HiddenInput(),
            "fecha_tramite": forms.HiddenInput(),
            "fecha_anulado": forms.HiddenInput(),
            "fecha_pago": forms.HiddenInput(),
            "fecha_envio": forms.HiddenInput(),
            "fecha_aprobacion": forms.HiddenInput(),
            "cod_ord_pago":forms.TextInput(attrs={'class':'form-control','readonly':True,'placeholder':'Código'}),
            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),
            "fecha_comprobante":forms.DateInput(attrs={'class':'form-control',"type":"date"}),
            "estado": forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'placeholder': 'Estado'}),
            "tipo_proveedor":forms.Select(attrs={"class":"form-control"}),
            "proveedor":forms.HiddenInput(),
            "centro_costos":forms.Select(attrs={"class":"select form-control"}),
            "n_comprobante":forms.TextInput(attrs={"class":"form-control"}),
            "concepto":forms.Textarea(attrs={"class":"form-control", "rows":2}),
            "forma_pago":forms.Select(attrs={"class":"select form-control"}),
            "motivo_anular":forms.Textarea(attrs={"class":"form-control", "rows":2}),
            "valor_iva":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
            "total":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
            "otros_cargos":forms.TextInput(attrs={'class':'pr-3 text-currency'}),
            "subtotal":forms.TextInput(attrs={'class':'pr-3 text-currency'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["centro_costos"].required = True
        self.fields["egreso"].required = True
        self.fields["n_comprobante"].required=True		


class OrdenPagoFormEnviado(forms.ModelForm):
    class Meta:
        model = OrdenPago

        fields = "__all__"

        labels = {
            "cod_ord_pago":"",
            "fecha":"",
            "estado":"",
            "tipo_proveedor":"Tipo de proveedor",
            "proveedor":"Razón social/Nombre",
            "centro_costos":"Centro de costos",
            "n_comprobante":"N° de comprobante",
            "concepto":"Concepto",
            "forma_pago":"Forma de pago",
            "fecha_comprobante":"Fecha de comprobante",
            "motivo_anular":"Motivo de Anulación",
            "subtotal":"",
            "total":"",
            "valor_iva":"",
            "iva":"Grava IVA",
            "otros_cargos":"",
            "n_tramite": "N° de Trámite",
            "fecha_tramite":"Fecha de trámite",
            "fecha_pago":"Fecha de pago",
        }

        widgets = {
            "evento":forms.HiddenInput(),
            "egreso":forms.HiddenInput(),
            "n_tramite":forms.HiddenInput(),
            "fecha_tramite": forms.HiddenInput(),
            "fecha_pago": forms.HiddenInput(),
            "fecha_aprobacion": forms.HiddenInput(),
            "fecha_anulado": forms.HiddenInput(),
            "fecha_envio": forms.HiddenInput(),
            "cod_ord_pago":forms.TextInput(attrs={'class':'form-control','readonly':True,'placeholder':'Código'}),
            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date"}),
            "fecha_comprobante":forms.DateInput(attrs={'class':'form-control',"type":"date",'readonly':True}),
            "estado": forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'placeholder': 'Estado'}),
            "tipo_proveedor":forms.Select(attrs={"class":"form-control",'disabled':True}),
            "proveedor":forms.HiddenInput(),
            "centro_costos":forms.Select(attrs={"class":"select form-control",'disabled':True}),
            "n_comprobante":forms.TextInput(attrs={"class":"form-control",'readonly':True}),
            "concepto":forms.Textarea(attrs={"class":"form-control", "rows":2,'readonly':True}),
            "forma_pago":forms.Select(attrs={"class":"select form-control",'disabled':True}),
            "motivo_anular":forms.Textarea(attrs={"class":"form-control", "rows":2,'readonly':True}),
            "iva":forms.CheckboxInput(attrs={'disabled':True}),
            "valor_iva":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
            "total":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
            "otros_cargos":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
            "subtotal":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["centro_costos"].required = True
        self.fields["egreso"].required = True
        self.fields["n_comprobante"].required=True		



class OrdenPagoFormAprobado(forms.ModelForm):
    class Meta:
        model=OrdenPago
        fields="__all__"
        labels = {
            "cod_ord_pago":"",
            "fecha":"",
            "estado":"",
            "tipo_proveedor":"Tipo de proveedor",
            "proveedor":"Razón social/Nombre",
            "centro_costos":"Centro de costos",
            "n_comprobante":"N° de comprobante",
            "concepto":"Concepto",
            "forma_pago":"Forma de pago",
            "fecha_comprobante":"Fecha de comprobante",
            "motivo_anular":"Motivo de Anulación",
            "subtotal":"",
            "total":"",
            "valor_iva":"",
            "iva":"Grava IVA",
            "otros_cargos":"",
            "n_tramite": "N° de Trámite",
            "fecha_tramite":"Fecha de trámite",
            "fecha_pago":"Fecha de pago",
        }
        widgets = {
            "evento":forms.HiddenInput(),
            "egreso":forms.HiddenInput(),
            "n_tramite":forms.TextInput(attrs={'class':'form-control','placeholder':'N° Trámite'}),
            "fecha_tramite": forms.DateInput(attrs={"type":'date'}),
            "fecha_pago": forms.DateInput(attrs={"type":'date'}),
            "fecha_aprobacion": forms.HiddenInput(),
            "fecha_anulado": forms.HiddenInput(),
            "fecha_envio": forms.HiddenInput(),
            "cod_ord_pago":forms.TextInput(attrs={'class':'form-control','readonly':True,'placeholder':'Código'}),
            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date"}),
            "fecha_comprobante":forms.DateInput(attrs={'class':'form-control',"type":"date",'readonly':True}),
            "estado": forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'placeholder': 'Estado'}),
            "tipo_proveedor":forms.Select(attrs={"class":"form-control",'disabled':True}),
            "proveedor":forms.HiddenInput(),
            "centro_costos":forms.Select(attrs={"class":"select form-control",'disabled':True}),
            "n_comprobante":forms.TextInput(attrs={"class":"form-control",'readonly':True}),
            "concepto":forms.Textarea(attrs={"class":"form-control", "rows":2,'readonly':True}),
            "forma_pago":forms.Select(attrs={"class":"select form-control",'disabled':True}),
            "motivo_anular":forms.Textarea(attrs={"class":"form-control", "rows":2,'readonly':True}),
            "iva":forms.CheckboxInput(attrs={'disabled':True}),
            "valor_iva":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
            "total":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
            "otros_cargos":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
            "subtotal":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_estado(self):
        n_tra = self.cleaned_data.get('n_tramite', '')
        f_pago = self.cleaned_data.get('fecha_pago', '')
        f_tra = self.cleaned_data.get('fecha_tramite','')
        e = self.cleaned_data.get('estado','')

        if  n_tra and f_pago and f_tra:
            return "Pagado"
        return e

class OrdenPagoFormPagado(forms.ModelForm):
    class Meta:
        model=OrdenPago
        fields="__all__"
        labels = {
            "cod_ord_pago":"",
            "fecha":"",
            "estado":"",
            "tipo_proveedor":"Tipo de proveedor",
            "proveedor":"Razón social/Nombre",
            "centro_costos":"Centro de costos",
            "n_comprobante":"N° de comprobante",
            "concepto":"Concepto",
            "forma_pago":"Forma de pago",
            "fecha_comprobante":"Fecha de comprobante",
            "motivo_anular":"Motivo de Anulación",
            "subtotal":"",
            "total":"",
            "valor_iva":"",
            "iva":"Grava IVA",
            "otros_cargos":"",
            "n_tramite": "N° de Trámite",
            "fecha_tramite":"Fecha de trámite",
            "fecha_pago":"Fecha de pago",
        }
        widgets = {
             "evento":forms.HiddenInput(),
            "egreso":forms.HiddenInput(),
            "n_tramite":forms.TextInput(attrs={'class':'form-control','placeholder':'N° Trámite','readonly':True}),
            "fecha_tramite": forms.DateInput(attrs={"type":'date','readonly':True}),
            "fecha_pago": forms.DateInput(attrs={"type":'date','readonly':True}),
            "fecha_aprobacion": forms.HiddenInput(),
            "fecha_anulado": forms.HiddenInput(),
            "fecha_envio": forms.HiddenInput(),
            "cod_ord_pago":forms.TextInput(attrs={'class':'form-control','readonly':True,'placeholder':'Código'}),
            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date"}),
            "fecha_comprobante":forms.DateInput(attrs={'class':'form-control',"type":"date",'readonly':True}),
            "estado": forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'placeholder': 'Estado'}),
            "tipo_proveedor":forms.Select(attrs={"class":"form-control",'disabled':True}),
            "proveedor":forms.HiddenInput(),
            "centro_costos":forms.Select(attrs={"class":"select form-control",'disabled':True}),
            "n_comprobante":forms.TextInput(attrs={"class":"form-control",'readonly':True}),
            "concepto":forms.Textarea(attrs={"class":"form-control", "rows":2,'readonly':True}),
            "forma_pago":forms.Select(attrs={"class":"select form-control",'disabled':True}),
            "motivo_anular":forms.Textarea(attrs={"class":"form-control", "rows":2,'readonly':True}),
            "iva":forms.CheckboxInput(attrs={'disabled':True}),
            "valor_iva":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
            "total":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
            "otros_cargos":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
            "subtotal":forms.TextInput(attrs={'class':'pr-3 text-currency','readonly':True}),
        }

class FileForm(forms.ModelForm):

    class Meta: 
        model= OrdenPagoFile
        fields = "__all__"
        labels = {
            "file":'Seleccione su archivo'
        }
        widgets={
            "file":forms.ClearableFileInput(attrs={'class':'orden_pagof','accept':'image/*,.pdf'}),
        }

FileFormset = inlineformset_factory(OrdenPago, OrdenPagoFile, form=FileForm, fields=['file'],extra=20,can_delete=True)#2)