from dal import autocomplete
from . import models
from .models import Proveedor
from django import forms
import django_filters
from datetime import date


class ProveedorForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProveedorForm, self).__init__(*args, **kwargs)
	

	class Meta:
		model = Proveedor
		fields = [
					"cod_proveedor",
					"fecha",
					"ruc",
					"razon",
					"sector",
					"direccion",
					"ciudad",
					"provincia",
					"telefono",
					"celular",
					"correo",
					"representante",
					"tipo_proveedor",
					"tipo_rubro",
					"observaciones",

					"ci_contacto_uno",
					"nombre_contacto_uno",
					"apellidos_contacto_uno",
					"cargo_contacto_uno",
					"telefono_contacto_uno",
					"celular_contacto_uno",
					"correo_contacto_uno",

					"ci_contacto_dos",
					"nombre_contacto_dos",
					"apellidos_contacto_dos",
					"cargo_contacto_dos",
					"telefono_contacto_dos",
					"celular_contacto_dos",
					"correo_contacto_dos",

					"ci_contacto_tres",
					"nombre_contacto_tres",
					"apellidos_contacto_tres",
					"cargo_contacto_tres",
					"telefono_contacto_tres",
					"celular_contacto_tres",
					"correo_contacto_tres",
					]


		labels = {
					"cod_proveedor":"Codigo de Proveedor",
					"fecha":"Fecha",
					"ruc": "RUC",
					"razon": "Razón social",
					"sector": "Sector",
					"direccion": "Dirección",
					"ciudad": "Ciudad",
					"provincia": "Provincia",
					"telefono": "Teléfono",
					"celular": "Celular",
					"correo": "Correo electrónico",
					"representante": "Representante legal",
					"tipo_proveedor": "Tipo de Proveedor",
					"tipo_rubro": "Tipo de Rubro",
					"observaciones": "Observaciones",

					"ci_contacto_uno":"",
					"nombre_contacto_uno":"",
					"apellidos_contacto_uno":"",
					"cargo_contacto_uno":"",
					"telefono_contacto_uno":"",
					"celular_contacto_uno":"",
					"correo_contacto_uno":"",

					"ci_contacto_dos":"",
					"nombre_contacto_dos":"",
					"apellidos_contacto_dos":"",
					"cargo_contacto_dos":"",
					"telefono_contacto_dos":"",
					"celular_contacto_dos":"",
					"correo_contacto_dos":"",

					"ci_contacto_tres":"",
					"nombre_contacto_tres":"",
					"apellidos_contacto_tres":"",
					"cargo_contacto_tres":"",
					"telefono_contacto_tres":"",
					"celular_contacto_tres":"",
					"correo_contacto_tres":"",

					# "ci_contacto_dos":"Cédula",
					# "nombre_contacto_dos":"Nombre",
					# "apellidos_contacto_dos":"Apellidos",
					# "cargo_contacto_dos":"Cargo",
					# "telefono_contacto_dos":"Teléfono",
					# "celular_contacto_dos":"Celular",
					# "correo_contacto_dos":"Correo Electrónico",

					# "ci_contacto_tres":"Cédula",
					# "nombre_contacto_tres":"Nombre",
					# "apellidos_contacto_tres":"Apellidos",
					# "cargo_contacto_tres":"Cargo",
					# "telefono_contacto_tres":"Teléfono",
					# "celular_contacto_tres":"Celular",
					# "correo_contacto_tres":"Correo Electrónico",
					}

                    
		widgets = {

			    "cod_proveedor":forms.TextInput(attrs={"class":"form-control",'readonly': True}),
				"fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),

				"ruc":forms.TextInput(attrs={"class":"form-control","type":"number"}),
				"razon":forms.TextInput(attrs={"class":"form-control"}),
				"sector":forms.Select(attrs={"class":"form-control"}),
				"direccion":forms.TextInput(attrs={"class":"form-control"}),
				"ciudad":forms.Select(attrs={"class":"form-control"}),
				"provincia":forms.Select(attrs={"class":"form-control"}),
				"telefono":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"celular":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"correo":forms.EmailInput(attrs={"class":"form-control"}),
				"representante":forms.TextInput(attrs={"class":"form-control"}),
				"tipo_proveedor":forms.Select(attrs={"class":"form-control"}),
				"tipo_rubro":forms.Select(attrs={"class":"form-control"}),

                "observaciones": forms.Textarea(attrs={'rows':2}),

				"ci_contacto_uno":forms.TextInput(attrs={"class":"form-control","type":"number"}),
				"nombre_contacto_uno":forms.TextInput(attrs={"class":"form-control"}),
				"apellidos_contacto_uno":forms.TextInput(attrs={"class":"form-control"}),
				"cargo_contacto_uno":forms.TextInput(attrs={"class":"form-control"}),
				"telefono_contacto_uno":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"celular_contacto_uno":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"correo_contacto_uno":forms.EmailInput(attrs={"class":"form-control"}),

				"ci_contacto_dos":forms.TextInput(attrs={"class":"form-control","type":"number"}),
				"nombre_contacto_dos":forms.TextInput(attrs={"class":"form-control"}),
				"apellidos_contacto_dos":forms.TextInput(attrs={"class":"form-control"}),
				"cargo_contacto_dos":forms.TextInput(attrs={"class":"form-control"}),
				"telefono_contacto_dos":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"celular_contacto_dos":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"correo_contacto_dos":forms.EmailInput(attrs={"class":"form-control"}),

				"ci_contacto_tres":forms.TextInput(attrs={"class":"form-control","type":"number"}),
				"nombre_contacto_tres":forms.TextInput(attrs={"class":"form-control"}),
				"apellidos_contacto_tres":forms.TextInput(attrs={"class":"form-control"}),
				"cargo_contacto_tres":forms.TextInput(attrs={"class":"form-control"}),
				"telefono_contacto_tres":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"celular_contacto_tres":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"correo_contacto_tres":forms.EmailInput(attrs={"class":"form-control"}),

		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['ciudad'].queryset = models.Ciudad.objects.none()
		if 'provincia' in self.data:
			try:
				provincia_id = int(self.data.get('provincia'))
				self.fields['ciudad'].queryset = models.Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			self.fields['ciudad'].queryset = self.instance.provincia.ciudad_set.order_by('nombre')


class PropertyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.type



class ProveedorUpdateForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(ProveedorForm, self).__init__(*args, **kwargs)	

	class Meta:
		model = Proveedor
		fields = [
					"cod_proveedor",
					"fecha",
					"ruc",
					"razon",
					"sector",
					"direccion",
					"ciudad",
					"provincia",
					"telefono",
					"celular",
					"correo",
					"representante",
					"tipo_proveedor",
					"tipo_rubro",
					"observaciones",

					"ci_contacto_uno",
					"nombre_contacto_uno",
					"apellidos_contacto_uno",
					"cargo_contacto_uno",
					"telefono_contacto_uno",
					"celular_contacto_uno",
					"correo_contacto_uno",

					"ci_contacto_dos",
					"nombre_contacto_dos",
					"apellidos_contacto_dos",
					"cargo_contacto_dos",
					"telefono_contacto_dos",
					"celular_contacto_dos",
					"correo_contacto_dos",

					"ci_contacto_tres",
					"nombre_contacto_tres",
					"apellidos_contacto_tres",
					"cargo_contacto_tres",
					"telefono_contacto_tres",
					"celular_contacto_tres",
					"correo_contacto_tres",
					]


		labels = {
					"cod_proveedor":"Codigo de Proveedor",
					"fecha":"Fecha",
					"ruc": "RUC",
					"razon": "Razón social",
					"sector": "Sector",
					"direccion": "Dirección",
					"ciudad": "Ciudad",
					"provincia": "Provincia",
					"telefono": "Teléfono",
					"celular": "Celular",
					"correo": "Correo electrónico",
					"representante": "Representante legal",
					"tipo_proveedor": "Tipo de Proveedor",
					"tipo_rubro": "Tipo de Rubro",
					"observaciones": "Observaciones",

					"ci_contacto_uno":"",
					"nombre_contacto_uno":"",
					"apellidos_contacto_uno":"",
					"cargo_contacto_uno":"",
					"telefono_contacto_uno":"",
					"celular_contacto_uno":"",
					"correo_contacto_uno":"",

					"ci_contacto_dos":"",
					"nombre_contacto_dos":"",
					"apellidos_contacto_dos":"",
					"cargo_contacto_dos":"",
					"telefono_contacto_dos":"",
					"celular_contacto_dos":"",
					"correo_contacto_dos":"",

					"ci_contacto_tres":"",
					"nombre_contacto_tres":"",
					"apellidos_contacto_tres":"",
					"cargo_contacto_tres":"",
					"telefono_contacto_tres":"",
					"celular_contacto_tres":"",
					"correo_contacto_tres":"",
					}

                    
		widgets = {

			    "cod_proveedor":forms.TextInput(attrs={"class":"form-control","readonly":True}),
				"fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),

				"ruc":forms.TextInput(attrs={"class":"form-control","type":"number"}),
				"razon":forms.TextInput(attrs={"class":"form-control"}),
				"sector":forms.Select(attrs={"class":"form-control"}),
				"direccion":forms.TextInput(attrs={"class":"form-control"}),
				"ciudad":forms.Select(attrs={"class":"form-control"}),
				"provincia":forms.Select(attrs={"class":"form-control"}),
				"telefono":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"celular":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"correo":forms.EmailInput(attrs={"class":"form-control"}),
				"representante":forms.TextInput(attrs={"class":"form-control"}),


				"tipo_proveedor":forms.Select(attrs={'onclick':'tipo_provee()',"class":"form-control"}),

				
				"tipo_rubro":forms.Select(attrs={"class":"form-control"}),

                "observaciones": forms.Textarea(attrs={'rows':2}),

				"ci_contacto_uno":forms.TextInput(attrs={"class":"form-control","type":"number"}),
				"nombre_contacto_uno":forms.TextInput(attrs={"class":"form-control"}),
				"apellidos_contacto_uno":forms.TextInput(attrs={"class":"form-control"}),
				"cargo_contacto_uno":forms.TextInput(attrs={"class":"form-control"}),
				"telefono_contacto_uno":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"celular_contacto_uno":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"correo_contacto_uno":forms.EmailInput(attrs={"class":"form-control"}),

				"ci_contacto_dos":forms.TextInput(attrs={"class":"form-control","type":"number"}),
				"nombre_contacto_dos":forms.TextInput(attrs={"class":"form-control"}),
				"apellidos_contacto_dos":forms.TextInput(attrs={"class":"form-control"}),
				"cargo_contacto_dos":forms.TextInput(attrs={"class":"form-control"}),
				"telefono_contacto_dos":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"celular_contacto_dos":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"correo_contacto_dos":forms.EmailInput(attrs={"class":"form-control"}),

				"ci_contacto_tres":forms.TextInput(attrs={"class":"form-control","type":"number"}),
				"nombre_contacto_tres":forms.TextInput(attrs={"class":"form-control"}),
				"apellidos_contacto_tres":forms.TextInput(attrs={"class":"form-control"}),
				"cargo_contacto_tres":forms.TextInput(attrs={"class":"form-control"}),
				"telefono_contacto_tres":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"celular_contacto_tres":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
				"correo_contacto_tres":forms.EmailInput(attrs={"class":"form-control"}),

		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['ciudad'].queryset = models.Ciudad.objects.none()
		if 'provincia' in self.data:
			try:
				provincia_id = int(self.data.get('provincia'))
				self.fields['ciudad'].queryset = models.Ciudad.objects.filter(provincia_id=provincia_id).order_by('nombre')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			self.fields['ciudad'].queryset = self.instance.provincia.ciudad_set.order_by('nombre')



# class ContactoForm(forms.ModelForm):

# 	class Meta:
# 		model = models.Contacto
# 		fields = [
# 					"ci_contacto",
# 					"nombre_contacto",
# 					"apellidos_contacto",
# 					"cargo_contacto",
# 					"telefono_contacto",
# 					"celular_contacto",
# 					"correo_contacto",
# 					]


# 		labels = {
# 					"ci_contacto":"Cédula",
# 					"nombre_contacto": "Nombre",
# 					"apellidos_contacto": "Apellidos",
# 					"cargo_contacto": "Cargo",
# 					"telefono_contacto": "Teléfono",
# 					"celular_contacto": "Celular",
# 					"correo_contacto": "Correo Electónico",
# 					}

                    
# 		widgets = {
				
# 				"ci_contacto":forms.TextInput(attrs={"class":"form-control","type":"number"}),
# 				"nombre_contacto":forms.TextInput(attrs={"class":"form-control"}),
# 				"apellidos_contacto":forms.TextInput(attrs={"class":"form-control"}),
# 				"cargo_contacto":forms.TextInput(attrs={"class":"form-control"}),
# 				"telefono_contacto":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
# 				"celular_contacto":forms.TextInput(attrs={"class":"form-control","type":"tel"}),
# 				"correo_contacto":forms.EmailInput(attrs={"class":"form-control"}),
# 		}






class ProveedorFilter(django_filters.FilterSet):
	# TIPO_RUBRO_CHOICES = [("Devolución de valores","Devolución de valores"), ("Alimentación","Alimentación"), ("Honorarios profesionales de docencia","Honorarios profesionales de docencia"),("Honorarios profesionales","Honorarios profesionales"),
	# ("Hospedaje con o sin alimentación","Hospedaje con o sin alimentación"),("Movilización interna","Movilicación interna"),("Movilización externa","Movilización externa"),("Servicios aéreos","Servicios aéreos"),("Viáticos al interios","Viáticos al interior"),("Viáticos al exterior","Viáticos al exterior"),
	# ("Suministros de oficina","Suministros de oficina"),("Otros suministros","Otros suministros"),("Materiales de ferreteria","Materiales de ferreteria"),("Materiales de limpieza","Materiales de limpieza"),("Mantenimientos de instalaciones","Mantenimientos de instalaciones"),("Equipos tecnológicos","Equipos tecnológicos"),
	# ("Equipos de oficina","Equipos de oficina"),("Materiales","Materiales"),("Publicidad impresa","Publicidad impresa"),("Publicidad en medios digitales","Publicidad en medios digitales"),("Internet","Internet"),("Servicios de agua potable","Servicios de agua potable"),("Servicio de energía eléctrica y alumbrado público","Servicio de energía eléctrica y alumbrado público"),
	# ("Servicio de telefonia fija y/o móvil","Servicio de telefonia fija y/o móvil"),("Servicio de vigilancia","Servicio de vigilancia"),("Materiales didácticos","Materiales didácticos"),("Otros gastos","Otros gastos")]
	
	TIPO_PROVEEDOR_CHOICES = [("Natural","Natural"), ("Jurídica","Jurídica")]

	
	ruc = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control","type":"number",'placeholder': 'RUC'}))
	razon = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Razón Social'}))

	
	sector = django_filters.ModelChoiceFilter(label="", empty_label="Sector", queryset=models.Sector.objects.all())
	direccion = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Dirección'}))
	telefono = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control","type":"tel",'placeholder': 'Teléfono'}))
	celular = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control","type":"tel",'placeholder': 'Celular'}))
	correo = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Correo electrónico'}))
	tipo_proveedor = django_filters.ModelChoiceFilter(label="", empty_label="Tipo de Proveedor", queryset=models.TipoProveedor.objects.all())
	tipo_rubro = django_filters.ModelChoiceFilter(label="", empty_label="Tipo de Rubro", queryset=models.TipoRubro.objects.all())
	
	provincia = django_filters.ModelChoiceFilter(label="", empty_label="Provincia", queryset=models.Provincia.objects.all())

	# def ciudades(request):
	# 	if request is None:
	# 		return models.Ciudad.objects.none()
	# 	else:
			
	# 		return models.Ciudad.objects.all()

	ciudad = django_filters.ModelChoiceFilter(label="", empty_label="Ciudad", queryset=models.Ciudad.objects.all().order_by("nombre"))

	class Meta:
		model = models.Proveedor
		fields = [
					"ruc",
					"razon",
					"sector",
					"direccion",
					#"ciudad",
					"provincia",
					"telefono",
					"celular",
					"correo",
					"tipo_proveedor",
					"tipo_rubro",

					]


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)