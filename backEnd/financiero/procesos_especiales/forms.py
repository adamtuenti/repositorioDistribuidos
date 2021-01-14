from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from django.forms import formset_factory

class CambiarParticipanteCreateForm(forms.Form):
    nombre_evento = forms.CharField(label='Nombre Evento', max_length=100,widget=forms.TextInput(attrs={'readonly': True}))
    codigo_evento = forms.CharField(label='Código Evento',widget=forms.Select(attrs={'class': 'select3'}))
    fecha_inicio = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'readonly': True}))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'readonly': True}))
    lugar_evento = forms.CharField(label='Lugar del Evento', max_length=100,widget=forms.TextInput(attrs={'readonly': True}))
    participante_origen_cedula =forms.CharField(widget=forms.TextInput(attrs={'hidden': True,'class':"form-control"}))
    participante_origen_nombre =forms.CharField(widget=forms.TextInput(attrs={'hidden': True, 'class':"form-control"}))
    participante_destino_cedula = forms.CharField(widget=forms.TextInput(attrs={'hidden': True}))
    participante_destino_nombre =forms.CharField(widget=forms.TextInput(attrs={'hidden': True}))

class CambiarEventoCreateForm(forms.Form):
    participante_cedula = forms.CharField(widget=forms.Select(attrs={'class': 'select4'}))
    participante_nombre = forms.CharField(widget=forms.Select(attrs={'class': 'select4'}))
    evento_origen_codigo =forms.CharField(widget=forms.TextInput(attrs={'hidden': True}))
    evento_origen_nombre =forms.CharField(widget=forms.TextInput(attrs={'hidden': True}))
    evento_origen_valor =forms.CharField(widget=forms.TextInput(attrs={'hidden': True}))
    

class EventoDestino(forms.Form):
    def __init__(self, *args, **kwargs):
        super(EventoDestino, self).__init__(*args, **kwargs)
        self.fields['evento_destino_codigo'].required = True
    evento_destino_codigo = forms.CharField(widget=forms.TextInput())
    evento_destino_nombre =forms.CharField(widget=forms.TextInput())
    evento_destino_valor =forms.CharField(widget=forms.TextInput())

EventoDestinoFormset = formset_factory(EventoDestino, extra=0,min_num=1,validate_min=True)

class ProcesoEspecialUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProcesoEspecialUpdateForm, self).__init__(*args, **kwargs)
    class Meta:
        model = ProcesoEspecial

        fields=[
            'categoria',
            'cod_proceso',
            'fecha_emision',
            'estado',
            'tipo_nota',
            'concepto',
            'subtotal',
            'descuento_fact',
            'descuento_total',
            'valor_total',
            'motivo',
        ]

        labels={
            'categoria':"",
            'cod_proceso':'Nota Nº',
            'fecha_emision':'Fecha',
            'estado':'Estado',
            'tipo_nota':'Tipo Nota',
            'concepto':'Concepto',
            'subtotal':'SUBTOTAL',
            'descuento_fact':'%DESCUENTOS',
            'descuento_total':'%DESCUENTO TOTAL',
            'valor_total':'VALOR TOTAL',
            'motivo':"Motivo de Anulación",
        }
        widgets={
            'concepto': forms.Textarea(attrs={'rows': 2}),
            'fecha_emision': forms.DateInput(attrs={'type': 'date', 'readonly': True}),
            'cod_proceso': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext'}),
            'subtotal':forms.HiddenInput(),
            'descuento_fact':forms.HiddenInput(),
            'descuento_total':forms.HiddenInput(),
            'valor_total':forms.HiddenInput(),
            'motivo':forms.Textarea(attrs={"class":"form-control", "rows":2, "readonly":True}),
        }

class ProcesoEspecialAutorizar(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProcesoEspecialAutorizar, self).__init__(*args, **kwargs)
        self.fields['tipo_nota'].disabled = True
    class Meta:
        model = ProcesoEspecial

        fields=[
            'categoria',
            'cod_proceso',
            'fecha_emision',
            'estado',
            'tipo_nota',
            'concepto',
            'subtotal',
            'descuento_fact',
            'descuento_total',
            'valor_total',
            'motivo',
        ]

        labels={
            'categoria':"",
            'cod_proceso':'Nota Nº',
            'fecha_emision':'Fecha',
            'estado':'Estado',
            'tipo_nota':'Tipo Nota',
            'concepto':'Concepto',
            'subtotal':'SUBTOTAL',
            'descuento_fact':'%DESCUENTOS',
            'descuento_total':'%DESCUENTO TOTAL',
            'valor_total':'VALOR TOTAL',
        }
        widgets={
            'concepto': forms.Textarea(attrs={'rows': 2}),
            'fecha_emision': forms.DateInput(attrs={'type': 'date', 'readonly': True}),
            'cod_proceso': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext'}),
            'subtotal':forms.HiddenInput(),
            'descuento_fact':forms.HiddenInput(),
            'descuento_total':forms.HiddenInput(),
            'valor_total':forms.HiddenInput(),
            'motivo':forms.Textarea(attrs={"class":"form-control", "rows":2}),
        }

class ProcesoParticipanteForm(forms.ModelForm):

    class Meta: 
        model= ProcesoParticipante 
        exclude=()

ParticipanteIntermedioFormset = inlineformset_factory(
    ProcesoEspecial, ProcesoParticipante, form=ProcesoParticipanteForm,
    fields=['participante','nombre_evento','cod_evento','valor_evento','descuento','valor',"orden",],
     extra=1,can_delete=True
    )

class ProcesoEspecialFileForm(forms.ModelForm):

    class Meta: 
        model= ProcesoEspecialFile 
        exclude=()
        labels={
            'file':'Seleccione su archivo'
        }

FileFormset = inlineformset_factory(
    ProcesoEspecial, ProcesoEspecialFile, form=ProcesoEspecialFileForm,
    fields=['file'],widgets={"file":forms.ClearableFileInput(attrs={'class':'procesoEspecialF','accept':'image/*,.pdf'})},
     extra=1,can_delete=True
    )