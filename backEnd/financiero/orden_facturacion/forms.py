from django import forms
from financiero.orden_facturacion.models import OrdenFacturacion, OrdenFacturacionParticipante, OrdenFacturacionFile
from datetime import date
from financiero.validaciones import validate_porcentaje
from django.forms.models import inlineformset_factory
class OrdenFacturacionForm(forms.ModelForm):
    class Meta:
        model = OrdenFacturacion

        fields = '__all__'

        labels = {
            'tipo_cliente': 'Cliente',
            'n_tramite': 'N° de trámite',
            'n_factura': 'N° de factura',
            'fecha': 'Fecha',
            'ruc_ci': 'RUC',
            'razon_nombres': 'Razón social',
            'centro_costos': 'Centro de costos',
            'n_participantes': '# de participantes',
            'valor_total': 'Valor total',
            'observaciones': 'Observaciones',
            'subtotal': 'Subtotal',
            'descuento_fact': '% Descuentos',
            'descuento_total': '$ Descuento total',
            'valor_total': '$ Valor total',
            "motivo_anular":"Motivo de Anulación",
            "contacto":"Contacto",
            "asesor":"Asesor",
        }

        widgets = {
            'cod_orden_fact': forms.HiddenInput(),
            'estado': forms.HiddenInput(),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
            'n_participantes': forms.HiddenInput(),
            'fecha': forms.DateInput(attrs={'type': 'date', 'value': date.today, 'readonly': True}),
            'razon_nombres': forms.Select(attrs={'class': 'form-control select2'}),
            'asesor': forms.Select(attrs={'class': 'form-control'}),
            'ruc_ci': forms.Select(attrs={'class': 'form-control select2'}),
            "contacto":forms.Select(attrs={'class': 'form-control select3'}),
            'n_tramite': forms.TextInput(attrs={'class': 'form-control textinput textInput form-control'}),
            'n_factura': forms.TextInput(attrs={'class': 'form-control textinput textInput form-control'}),
            'subtotal': forms.HiddenInput(),#NumberInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'descuento_fact': forms.HiddenInput(),#NumberInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'descuento_total': forms.HiddenInput(),#NumberInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'valor_total': forms.HiddenInput(),#NumberInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            "motivo_anular":forms.Textarea(attrs={"class":"form-control", "rows":2}),
        }


class OrdenFacturacionUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asesor'].disabled = True
    class Meta:
        model = OrdenFacturacion

        fields = '__all__'

        labels = {
            'tipo_cliente': 'Cliente',
            'n_tramite': 'N° de trámite',
            'n_factura': 'N° de factura',
            'fecha': 'Fecha',
            'ruc_ci': 'RUC',
            'razon_nombres': 'Razón social',
            'centro_costos': 'Centro de costos',
            'n_participantes': '# de participantes',
            'valor_total': 'Valor total',
            'observaciones': 'Observaciones',
            'participantes': 'Participantes',
            'subtotal': 'Subtotal',
            'descuento_fact': '% Descuentos',
            'descuento_total': '$ Descuento total',
            'valor_total': '$ Valor total',
            "motivo_anular":"Motivo de Anulación",
            "contacto":"Contacto",
            "asesor":"Asesor",
            "fecha_tramite":"Fecha de Tramite",
            "fecha_factura":"Fecha de Factura",
        }


        widgets = {
            'cod_orden_fact': forms.HiddenInput(),
            'estado': forms.HiddenInput(),
            'tipo_cliente': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext'}),
            'centro_costos': forms.Select(attrs={'disabled': True, 'class': 'form-control-plaintext'}),
            'valor_total': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext'}),
            'n_participantes': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext'}),
            'valor': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext'}),
            'observaciones': forms.Textarea(attrs={'rows': 2, 'readonly': True, 'class': 'form-control-plaintext'}),
            'n_tramite': forms.TextInput(attrs={'class': 'form-control textinput textInput'}),
            'n_factura': forms.TextInput(attrs={'class': 'form-control textinput textInput'}),
            'fecha_tramite': forms.DateInput(attrs={'type': 'date', 'class': "form-control"}),
            'fecha_factura': forms.DateInput(attrs={'type': 'date','class': "form-control"}),
            'fecha': forms.DateInput(attrs={'type': 'date','readonly': True, 'class': 'form-control-plaintext'}),
            'razon_nombres': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'ruc_ci': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            #"contacto":forms.Select(attrs={'edit': 123,'class': 'form-control select3'}),
            "contacto":forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'subtotal': forms.HiddenInput(),#NumberInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'descuento_fact': forms.HiddenInput(),#NumberInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'descuento_total': forms.HiddenInput(),#NumberInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'valor_total': forms.HiddenInput(),#NumberInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            "valor_pendiente":forms.HiddenInput(),
            "motivo_anular":forms.Textarea(attrs={'readonly': True, "class":"form-control", "rows":2}),
        }
    
        


class OrdenFacturacionFinalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asesor'].disabled = True
    class Meta:
        model = OrdenFacturacion

        fields = '__all__'

        labels = {
            'tipo_cliente': 'Cliente',
            'n_tramite': 'N° de trámite',
            'n_factura': 'N° de factura',
            'fecha': 'Fecha',
            'ruc_ci': 'RUC',
            'razon_nombres': 'Razón social',
            'centro_costo': 'Centro de costo',
            'n_participantes': '# de participantes',
            'valor_total': 'Valor total',
            'observaciones': 'Observaciones',
            'subtotal':'Subtotal',
            'descuento_fact':'% Descuentos',
            'descuento_total':'$ Descuento total',
            'valor_total':'$ Valor total',
            "motivo_anular":"Motivo de Anulación",
            "contacto":"Contacto",
            "tipo_evento":"Evento",
            "asesor":"Asesor",
            "fecha_tramite":"Fecha de Tramite",
            "fecha_factura":"Fecha de Factura",
            
        }
        widgets = {
            'cod_orden_fact': forms.HiddenInput(),
            'estado': forms.HiddenInput(),
            'tipo_evento': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext'}),
            'tipo_cliente': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext'}),
            'centro_costos': forms.Select(attrs={'disabled': True, 'class': 'form-control-plaintext'}),
            'valor_total': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext'}),
            'n_participantes': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext'}),
            'valor': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext'}),
            'observaciones': forms.Textarea(attrs={'rows': 2, 'readonly': True, 'class': 'form-control-plaintext'}),
            # 'n_tramite': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            # 'n_factura': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            # "fecha_tramite":forms.DateInput(attrs={'type': 'date','readonly': True, 'class': 'form-control-plaintext'}),
            # "fecha_factura":forms.DateInput(attrs={'type': 'date','readonly': True, 'class': 'form-control-plaintext'}),
            'n_tramite': forms.TextInput(attrs={'class': 'form-control textinput textInput'}),
            'n_factura': forms.TextInput(attrs={'class': 'form-control textinput textInput'}),
            'fecha_tramite': forms.DateInput(attrs={'type': 'date', 'class': "form-control"}),
            'fecha_factura': forms.DateInput(attrs={'type': 'date','class': "form-control"}),
            'fecha': forms.DateInput(attrs={'type': 'date','readonly': True, 'class': 'form-control-plaintext'}),
            'razon_nombres': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'ruc_ci': forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            #"contacto":forms.Select(attrs={'class': 'form-control select3'}),
            "contacto":forms.TextInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'subtotal': forms.HiddenInput(),#NumberInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'descuento_fact': forms.HiddenInput(),#NumberInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'descuento_total': forms.HiddenInput(),#NumberInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            'valor_total': forms.HiddenInput(),#NumberInput(attrs={'readonly': True, 'class': 'form-control-plaintext form-control'}),
            "motivo_anular":forms.Textarea(attrs={"class":"form-control", "rows":2}),
        }


class OrdenFacturacionParticipanteForm(forms.ModelForm):
    class Meta:
        model = OrdenFacturacionParticipante
        fields = "__all__"
        labels = {
            "participante": "Participante",
            "nombre_evento": "Nombre del evento",
            "cod_evento": "Código del Evento",
            "valor_evento": "Valor del Evento ($)",
            "descuento": "Descuento (%)",
            "valor": "Valor a Pagar ($) ",
        }
        widgets = {
            "participante": forms.Select(attrs={'class': 'select2 form-control'}),
            "descuento": forms.NumberInput(attrs={'min': 0.0, 'max': 100.0}),
            "valor_evento": forms.NumberInput(attrs={'min': 0.0}),
            "valor": forms.NumberInput(attrs={'min': 0.0, 'max': 100.0, 'readonly': True}),
        }

    def clean_descuento(self):
        descuento = self.cleaned_data["descuento"]
        return validate_porcentaje(descuento)

class FileForm(forms.ModelForm):

    class Meta: 
        model= OrdenFacturacionFile 
        exclude=()

FileFormset = inlineformset_factory(
    OrdenFacturacion, OrdenFacturacionFile, form=FileForm,
    fields=['file'],widgets={"file":forms.ClearableFileInput(attrs={'class':'ordenfactf','accept':'.pdf'})},
     extra=1,can_delete=True
    )
