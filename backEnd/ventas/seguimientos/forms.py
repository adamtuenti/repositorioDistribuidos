from django import forms
from .models import *
from ventas.interesados.models import *
import datetime
from datetime import date
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from ..validaciones import validate_date_with_offset, validate_fecha
from django.forms.models import inlineformset_factory
from ventas.validaciones import validate_date_with_offset
from ..interesados.models import CanalContacto
from ventas.personas_naturales.models import Persona_Natural

class Seguimiento_InteresadosForm(forms.ModelForm):
   
    class Meta:
        model = Seguimiento_Interesados
        fields = "__all__"
        labels = {
            "exito":"Éxito",
            "proximo_seguimiento":"Próximo seguimiento",
            "cod_evento":"Código evento",
            "nombre_evento":"Nombre evento",
            "estado_participante":"Estado del participante",
        }
        widgets = {
            "n_registro_interesado": forms.TextInput(attrs={'readonly': True, 'placeholder': 'N° registro'}),
            "fecha_seguimiento": forms.DateInput(attrs={"type":"date"}),
            "fecha_registro": forms.DateInput(attrs={"type":"date"}),
            "proximo_seguimiento": forms.DateInput(attrs={"type":"date"}),
            "cod_evento": forms.Select(attrs={'class': 'select3'}),
            "nombre_evento": forms.Select(attrs={'class': 'select3'}),
            'observaciones':forms.Textarea(attrs={'rows':5,"overflow-y": "scroll"}),
        }    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_registro'].initial = datetime.date.today
        self.fields['fecha_registro'].disabled = True
        self.fields['n_registro_interesado'].disabled = True
        
    
    def clean_fecha_seguimiento(self):
        fecha_registro = self.cleaned_data.get('fecha_registro', None)
        fecha_seguimiento = self.cleaned_data.get('fecha_seguimiento', None)
        days = 15
        return validate_date_with_offset(fecha_registro, fecha_seguimiento, days)

    
        

class Seguimiento_NaturalForm(forms.ModelForm):
   
    class Meta:
        model = Seguimiento_PersonaNatural
        fields = "__all__"
        # labels = {
        #     "exito":"Éxito",
        #     "proximo_seguimiento":"Próximo seguimiento"
        # }
        widgets = {
            "n_registro": forms.TextInput(attrs={'readonly': True, 'placeholder': 'N° registro'}),
            "fecha_seguimiento": forms.DateInput(attrs={"type":"date"}),
            "fecha_registro": forms.DateInput(attrs={"type":"date"}),
            "proximo_seguimiento": forms.DateInput(attrs={"type":"date"}),
            "cod_evento": forms.Select(attrs={'class': 'select3'}),
            "nombre_evento": forms.Select(attrs={'class': 'select3'}),
            "pers_natural":forms.Select(attrs={'hidden': True}),
            'observaciones':forms.Textarea(attrs={'rows':5,"overflow-y": "scroll"}),
        }    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_registro'].initial = datetime.date.today
        self.fields['fecha_registro'].disabled = True
        self.fields['n_registro'].disabled = True

    def clean_fecha_seguimiento(self):
        fecha_inicio = self.cleaned_data["fecha_registro"]
        fecha_fin = self.cleaned_data["fecha_seguimiento"]
        return validate_date_with_offset(fecha_inicio,fecha_fin,15)


class Seguimiento_Natural_EditarForm(forms.ModelForm):
    class Meta:
        model = Seguimiento_PersonaNatural
        fields = "__all__"
        labels = {
             "exito":"Éxito",
             "proximo_seguimiento":"Próximo seguimiento",
             "n_registro":"N° registro",
             "cod_evento":"Código Evento",
             "nombre_evento":"Nombre Evento",
        }
        widgets = {
            "pers_natural":forms.HiddenInput(),
            "fecha_seguimiento": forms.DateInput(attrs={"type":"date"}),
            "fecha_registro": forms.DateInput(attrs={"type":"date"}),
            "proximo_seguimiento": forms.DateInput(attrs={"type":"date"}),
            "cod_evento": forms.Select(attrs={'class': 'select3'}),
            "nombre_evento": forms.Select(attrs={'class': 'select3'}),
            "observaciones":forms.Textarea(attrs={'rows':5,"overflow-y": "scroll"}),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_registro'].disabled = True
        self.fields['n_registro'].disabled = True
        self.fields['proximo_seguimiento'].disabled = True

    
    def clean_fecha_seguimiento(self):
        fecha_inicio = self.cleaned_data["fecha_registro"]
        fecha_fin = self.cleaned_data["fecha_seguimiento"]
        return validate_date_with_offset(fecha_inicio,fecha_fin,15)

        
class Natural_Mostrar(forms.ModelForm):
    class Meta:
        model = Persona_Natural
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cedula'].disabled = True
        self.fields['nombres'].disabled = True
        self.fields['apellidos'].disabled = True
        
class SeguimientoEventoCreateForm(forms.Form):
    nombre_eventoO = forms.CharField(label='Nombre Evento Origen',widget=forms.Select(attrs={'class': 'select3'}))
    codigo_eventoO = forms.CharField(label='Código Evento Origen',widget=forms.Select(attrs={'class': 'select3'}))

    nombre_eventoD = forms.CharField(label='Nombre Evento Destino',widget=forms.Select(attrs={'class': 'select3'}))
    codigo_eventoD = forms.CharField(label='Código Evento Destino',widget=forms.Select(attrs={'class': 'select3'}))

    fecha_registro = forms.DateField(label='Fecha Registro',widget=forms.DateInput(attrs={"type":"date"}))
    fecha_seguimiento = forms.DateField(label='Fecha Seguimiento',widget=forms.DateInput(attrs={"type":"date"}))
    estado_seguimiento = forms.ChoiceField(label='Estado Seguimiento', choices=ESTADO_CHOICES)
    # canal_contacto = forms.ChoiceField(label='Canal Contacto', choices=CanalContacto.objects.all().values_list('pk','nombre'))
    canal_contacto = forms.ChoiceField(label='Canal Contacto')
    exito = forms.ChoiceField(label='Éxito', choices=EXITO_CHOICES)
    estado_participante = forms.ChoiceField(label='Estado Participante', choices=Seguimiento_PersonaNatural.ESTADO_PARTICIPANTE_CHOICES)
    observaciones = forms.CharField(label='Observaciones', widget=forms.Textarea(attrs={'rows':5,"overflow-y": "scroll"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.forms[0].empty_permitted = False
        self.fields['fecha_registro'].disabled = True
        self.fields['fecha_registro'].initial = datetime.date.today
        self.fields["canal_contacto"] = forms.ChoiceField(choices=CanalContacto.objects.all().values_list('pk','nombre'))
    
    def clean_fecha_seguimiento(self):
        fecha_inicio = self.cleaned_data["fecha_registro"]
        fecha_fin = self.cleaned_data["fecha_seguimiento"]
        return validate_date_with_offset(fecha_inicio,fecha_fin,15)

        
class Seguimiento_Interesados_EditarForm(forms.ModelForm):
    class Meta:
        model = Seguimiento_Interesados
        fields = "__all__"
        labels = {
             "exito":"Éxito",
             "proximo_seguimiento":"Próximo seguimiento",
             "n_registro_interesado":"N° registro",
             "cod_evento":"Código Evento",
             "nombre_evento":"Nombre Evento",
             "fecha_porcontactar":"Fecha por contactar",
             "fecha_sinrespuesta":"Fecha sin respuesta",
             "fecha_contactado":"Fecha contactado",
             "fecha_contactoinvalido":"Fecha contacto invalido",
        }
        widgets = {
            "fecha_seguimiento": forms.DateInput(attrs={"type":"date"}),
            "fecha_registro": forms.DateInput(attrs={"type":"date"}),
            "proximo_seguimiento": forms.DateInput(attrs={"type":"date"}),
            "fecha_porcontactar": forms.DateInput(attrs={"type":"date"}),
            "fecha_sinrespuesta": forms.DateInput(attrs={"type":"date"}),
            "fecha_contactado": forms.DateInput(attrs={"type":"date"}),
            "fecha_contactoinvalido": forms.DateInput(attrs={"type":"date"}),
            "cod_evento": forms.Select(attrs={'class': 'select3'}),
            "nombre_evento": forms.Select(attrs={'class': 'select3'}),
            "observaciones":forms.Textarea(attrs={'rows':5,"overflow-y": "scroll"}),
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_registro'].disabled = True
        self.fields['n_registro_interesado'].disabled = True
        self.fields['proximo_seguimiento'].disabled = True
        self.fields['inters'].disabled = True
        # self.fields['fecha_porcontactar'].disabled = True
        # self.fields['fecha_sinrespuesta'].disabled = True
        # self.fields['fecha_contactado'].disabled = True
        # self.fields['fecha_contactoinvalido'].disabled = True
    def clean_fecha_seguimiento(self):
        fecha_inicio = self.cleaned_data["fecha_registro"]
        fecha_fin = self.cleaned_data["fecha_seguimiento"]
        return validate_date_with_offset(fecha_inicio,fecha_fin,15)

    
        
        
class Interesado_Mostrar(forms.ModelForm):
    class Meta:
        model = Interesado
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].disabled = True
        self.fields['apellido'].disabled = True
        self.fields['celular'].disabled = True
        self.fields['correo'].disabled = True  


class SeguimientoEmpresaForm(forms.ModelForm):
    class Meta:
        model = SeguimientoEmpresa
        fields = "__all__"
        widgets = {
            "juridica": forms.HiddenInput(),
            "n_seguimiento": forms.TextInput(attrs={'readonly': True, 'placeholder': 'N° registro'}),
            "fecha": forms.DateInput(attrs={'readonly': True, 'type': 'date', 'value': date.today}),
            "n_oferta": forms.Select(attrs={'disabled': True,"class":"select2"}),
            "fecha_seguimiento": forms.DateInput(attrs={'type': 'date'}),
            "fecha_proximo": forms.DateInput(attrs={'type': 'date'}),
            "observaciones": forms.Textarea(attrs={'rows': 2}),
            "n_participantes": forms.NumberInput(attrs={'readonly': True}),
            "n_evento":forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('n_seguimiento', css_class='col-2'),
                Column('fecha', css_class='col-2'),
                Column('fecha_seguimiento', css_class='col-2'),
                Column('estado', css_class='col'),
                Column('canal', css_class='col'),
                Column('exito', css_class='col-2 col-xl-1'),
                css_class='form-row'
            ),
            Row(
                Column('tipo_evento', css_class='col-xl-2 col-4'),
                Column('tipo_oferta', css_class='col-xl-2 col-4'),
                Column('n_oferta', css_class='col-xl-2 col-4'),
                Column('reporte_contacto', css_class='col-xl-2 col-4'),
                Column('n_participantes', css_class='col-xl-2 col-3'),
                Column('fecha_proximo', css_class='col-xl-2 col-3'),
                css_class='form-row'
            ),
            Row(
                Column('observaciones', css_class='col'),
                css_class='form-row'
            )
        )

    def clean_fecha_seguimiento(self):
        fecha = self.cleaned_data.get('fecha', None)
        f_seguimiento = self.cleaned_data.get('fecha_seguimiento', None)
        days = 15
        return validate_date_with_offset(fecha, f_seguimiento, days)

    # def clean_fecha_proximo(self):
    #     f_seguimiento = self.cleaned_data.get('fecha_seguimiento', None)
    #     f_proximo = self.cleaned_data.get('fecha_proximo', None)
    #     if f_seguimiento and f_proximo:
    #         return validate_fecha(f_seguimiento, f_proximo, 'de seguimiento', 'programada')
    #     return f_proximo
    
    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get("estado")
        fecha_por_contactar = cleaned_data.get("fecha_por_contactar",None)
        fecha_sin_respuesta = cleaned_data.get("fecha_sin_respuesta",None)
        fecha_contactado = cleaned_data.get("fecha_contactado",None)
        fecha_contacto_invalido = cleaned_data.get("fecha_contacto_invalido",None)

        if estado:
            # Only do something if estado exists
            if estado.pk == 1:
                if not fecha_por_contactar:
                    cleaned_data["fecha_por_contactar"]=date.today()
            elif estado.pk == 2:
                if not fecha_sin_respuesta:
                    cleaned_data["fecha_sin_respuesta"]=date.today()
            elif estado.pk == 3:
                if not fecha_contactado:
                    cleaned_data["fecha_contactado"]=date.today()
            elif estado.pk == 4:
                if not fecha_contacto_invalido:
                    cleaned_data["fecha_contacto_invalido"]=date.today()
        return cleaned_data


class SeguimientoEmpresaEditarForm(forms.ModelForm):
    class Meta:
        model = SeguimientoEmpresa
        fields = "__all__"
        widgets = {
            "juridica": forms.HiddenInput(),
            "n_seguimiento": forms.TextInput(attrs={'readonly': True, 'placeholder': 'N° registro'}),
            "fecha": forms.DateInput(attrs={'readonly': True, 'type': 'date'}),
            "n_oferta": forms.Select(attrs={'disabled': True,"class":"select2"}),
            "fecha_seguimiento": forms.DateInput(attrs={'type': 'date'}),
            "fecha_proximo": forms.DateInput(attrs={'type': 'date',"readonly":True}),
            "observaciones": forms.Textarea(attrs={'rows': 2}),
            "n_participantes": forms.NumberInput(attrs={'readonly': True}),
            "n_evento":forms.HiddenInput(),
            "fecha_por_contactar":forms.HiddenInput(),
            "fecha_sin_respuesta":forms.HiddenInput(),
            "fecha_contactado":forms.HiddenInput(),
            "fecha_contacto_invalido":forms.HiddenInput(),
            "added_by":forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('n_seguimiento', css_class='col-2'),
                Column('fecha', css_class='col-2'),
                Column('fecha_seguimiento', css_class='col-2'),
                Column('estado', css_class='col'),
                Column('canal', css_class='col'),
                Column('exito', css_class='col-2 col-xl-1'),
                css_class='form-row'
            ),
            Row(
                Column('tipo_evento', css_class='col-xl-2 col-4'),
                Column('tipo_oferta', css_class='col-xl-2 col-4'),
                Column('n_oferta', css_class='col-xl-2 col-4'),
                Column('reporte_contacto', css_class='col-xl-2 col-4'),
                Column('n_participantes', css_class='col-xl-2 col-3'),
                Column('fecha_proximo', css_class='col-xl-2 col-3'),
                css_class='form-row'
            ),
            Row(
                Column('observaciones', css_class='col'),
                Column('fecha_por_contactar'),
                Column('fecha_sin_respuesta'),
                Column('fecha_contactado'),
                Column('fecha_contacto_invalido'),
                Column('added_by'),
                css_class='form-row'
            )
        )

    def clean_fecha_seguimiento(self):
        fecha = self.cleaned_data.get('fecha', None)
        f_seguimiento = self.cleaned_data.get('fecha_seguimiento', None)
        days = 15
        return validate_date_with_offset(fecha, f_seguimiento, days)

    # def clean_fecha_proximo(self):
    #     f_seguimiento = self.cleaned_data.get('fecha_seguimiento', None)
    #     f_proximo = self.cleaned_data.get('fecha_proximo', None)
    #     if f_seguimiento and f_proximo:
    #         return validate_fecha(f_seguimiento, f_proximo, 'de seguimiento', 'programada')
    #     return f_proximo

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get("estado")
        fecha_por_contactar = cleaned_data.get("fecha_por_contactar",None)
        fecha_sin_respuesta = cleaned_data.get("fecha_sin_respuesta",None)
        fecha_contactado = cleaned_data.get("fecha_contactado",None)
        fecha_contacto_invalido = cleaned_data.get("fecha_contacto_invalido",None)

        if estado:
            # Only do something if estado exists
            if estado.pk == 1:
                if not fecha_por_contactar:
                    cleaned_data["fecha_por_contactar"]=date.today()
            elif estado.pk == 2:
                if not fecha_sin_respuesta:
                    cleaned_data["fecha_sin_respuesta"]=date.today()
            elif estado.pk == 3:
                if not fecha_contactado:
                    cleaned_data["fecha_contactado"]=date.today()
            elif estado.pk == 4:
                if not fecha_contacto_invalido:
                    cleaned_data["fecha_contacto_invalido"]=date.today()
        return cleaned_data

def mychoices(options):
    lista = [("", "----------------")]
    lista.extend(list(options))
    return lista

class SeguimientoEmpresaEventosForm(forms.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.forms[0].empty_permitted = False
        for form in self.forms:
            form.fields["nombre_evento"] = forms.ChoiceField(choices=mychoices(Evento.objects.all().order_by('-pk').values_list('codigo_evento', 'nombre')),widget=forms.Select(attrs={"class":"select2"}))
            form.fields['codigo_evento']= forms.ChoiceField(choices=mychoices(Evento.objects.all().order_by('-pk').values_list('codigo_evento', 'codigo_evento')),widget=forms.Select(attrs={"class":"select2"}))


SEFormset = inlineformset_factory(
    SeguimientoEmpresa,
    SeguimientoEmpresaEventos,
    formset=SeguimientoEmpresaEventosForm,
    fields=['nombre_evento', 'codigo_evento','evento'],
    labels={
        "nombre_evento": 'Nombre del evento',
        "codigo_evento": 'Código del evento',
    },
    widgets={
        "evento":forms.HiddenInput(),
        "nombre_evento":forms.Select(attrs={"class":"select2"}),
        "codigo_evento":forms.Select(attrs={"class":"select2"})
    },
    extra=20,
    can_delete=True
)
