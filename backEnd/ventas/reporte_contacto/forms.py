from django import forms
from .models import ReporteContacto, Capacitacion,Asesoria
from ventas.validaciones import validate_horarios,validate_fecha
from dal import autocomplete



class ReporteContactoForm(forms.ModelForm):
    class Meta:
        model = ReporteContacto

        fields=[
            'cod_reporte',
            'ruc_ci',
            'razon_nombres',
            'tipo_empresa',
            'sector',
            'canal_de_contacto',
            'motivo_de_contacto',
            'lugar',
            'fecha',
            'hora_inicio',
            'hora_fin',
            'nombre_contacto',
            'telefono',
            'cargo',
            'correo_electronico',
            'asistentes',
            'situacion_actual',
            'situacion_deseada',
            'servicios_requeridos',
        ]

        labels={
            'cod_reporte':'Código del reporte',
            'ruc_ci': 'RUC',
            'razon_nombres': 'Razón social',
            'tipo_empresa': 'Tipo Empresa',
            'sector': 'Sector',
            'canal_de_contacto': 'Canal de contacto',
            'motivo_de_contacto': 'Motivo de Contacto',
            'lugar':'Lugar',
            'fecha':'Fecha',
            'hora_inicio':'Hora de inicio',
            'hora_fin':'Hora de fin',
            'nombre_contacto':'Nombre del contacto de la Empresa',
            'telefono':'Teléfono',
            'cargo':'Cargo',
            'correo_electronico':'Correo electrónico',
            'asistentes':'Asistentes',
            'situacion_actual':'Situación actual',
            'situacion_deseada':'Situación deseada',
            'servicios_requeridos': 'Servicios requeridos',
        }
        widgets={
            'acuerdos':forms.Textarea(attrs={'rows':2}),
            'razon_nombres': forms.Select(attrs={'class': 'form-control select2'}),
            'ruc_ci': forms.Select(attrs={'class': 'form-control select2'}),
            'motivo_de_contacto':forms.Textarea(attrs={'rows':2}),
            'situacion_actual':forms.Textarea(attrs={'rows':5,"overflow-y": "scroll"}),
            'situacion_deseada':forms.Textarea(attrs={'rows':5,"overflow-y": "scroll"}),
            'fecha':forms.DateInput(attrs={'type':'date'}),
            'hora_inicio':forms.TimeInput(attrs={'type':'time'}),
            'hora_fin':forms.TimeInput(attrs={'type':'time'}),
            'tipo_empresa': forms.HiddenInput(),
            'sector': forms.HiddenInput(),
        }
        
    def clean_hora_fin(self):
        hora_inicio = self.cleaned_data["hora_inicio"]
        hora_fin = self.cleaned_data["hora_fin"]
        return validate_horarios(hora_inicio,hora_fin)
    

class CapacitacionForm(forms.ModelForm):
    class Meta:
        model = Capacitacion

        fields=[
            'tema',
            'tipo',
            'modalidad',
            'area',
            'nivel_organizacion',
            'numero_participantes',
            'horario_trabajo',
            'nivel_educacion',
            'edad_promedio',
            'lugar',
            'ciudad',
            'fecha_evento',
            'horario_evento_inicio',
            'horario_evento_fin',
            'observaciones',
            'acuerdos',
            'exclusivo_acad',
        ]

        labels={
            'tema':'Tema de capacitación sugerido',
            'tipo':'Tipo de capacitación sugerido',
            'modalidad':'Modalidad',
            'area':'Área(s) del evento',
            'nivel_organizacion':'Nivel organizacional de los participantes',
            'numero_participantes':'Número de participantes',
            'horario_trabajo':'Horario normales de trabajo',
            'nivel_educacion':'Nivel de educación',
            'edad_promedio':'Edad promedio de los participantes',
            'lugar':'Lugar para la capacitación',
            'ciudad':'Ciudad',
            'fecha_evento':'Fechas estimadas para el evento',
            'horario_evento_inicio':'Hora de inicio',
            'horario_evento_fin':'Hora de fin',
            'observaciones':'Observaciones',
            'acuerdos':'Acuerdos',
            'exclusivo_acad':'Para uso exclusivo del área académica',
        }
        widgets={
            'observaciones':forms.Textarea(attrs={'rows':2}),
            'acuerdos':forms.Textarea(attrs={'rows':2}),
            'exclusivo_acad':forms.Textarea(attrs={'rows':2}),
            'fecha_evento':forms.DateInput(attrs={'type':'date'}),
            'horario_evento_inicio':forms.TimeInput(attrs={'type':'time'}),
            'horario_evento_fin':forms.TimeInput(attrs={'type':'time'})
        }
    def clean_horario_evento_fin(self):
        hora_inicio = self.cleaned_data["horario_evento_inicio"]
        hora_fin = self.cleaned_data["horario_evento_fin"]
        return validate_horarios(hora_inicio,hora_fin)
            
    
  
        

class AsesoriaForm(forms.ModelForm):
    class Meta:
        model=Asesoria

        fields = [
            'tipo_servicio',
            'descripcion',
            'alcance',
            'con_sin_imple',
            'fecha_inicio',
            'fecha_fin',
            'proveedor',
            'entregables',
            'observaciones',
            'acuerdos',
            'exclusivo_acad',
        ]

        labels={
            
            'tipo_servicio':'Tipo de servicio',
            'descripcion':'Descripción',
            'alcance':'Alcance',
            'con_sin_imple':'Con/Sin Implementación',
            'fecha_inicio':'Fecha de inicio',
            'fecha_fin':'Fecha de fin',
            'proveedor':'Proveedor de la información',
            'entregables':'Entregables',
            'observaciones':'Observaciones',
            'acuerdos':'Acuerdos',
            'exclusivo_acad':'Para uso exclusivo del área acedémica',
        }
        widgets={
            'observaciones':forms.Textarea(attrs={'rows':2}),
            'acuerdos':forms.Textarea(attrs={'rows':2}),
            'exclusivo_acad':forms.Textarea(attrs={'rows':2}),
            'fecha_inicio':forms.DateInput(attrs={'type':'date'}),
            'fecha_fin':forms.DateInput(attrs={'type':'date'}),

        }
    def clean_fecha_fin(self):
        fecha_inicio = self.cleaned_data["fecha_inicio"]
        fecha_fin = self.cleaned_data["fecha_fin"]
        return validate_fecha(fecha_inicio,fecha_fin)
   