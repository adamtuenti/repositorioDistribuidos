from dal import autocomplete
from . import models
from django import forms
import django_filters
from .models import *
from django.forms import modelformset_factory
from datetime import date
from django.forms.models import inlineformset_factory
from django.db.models import Q

class Calificacion_proveedorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Calificacion_proveedorForm, self).__init__(*args, **kwargs)
        self.fields['cod_calificacion'].disabled = True
        # self.fields['tipo_rubro'].disabled = True	
        self.fields['treinta'].disabled = True
        self.fields['veinticinco'].disabled = True
        self.fields['veinte'].disabled = True
        self.fields['quince'].disabled = True
        self.fields['diez'].disabled = True
        self.fields['cinco'].disabled = True
        self.fields['cero'].disabled = True
        # self.fields['total_prod'].disabled = True	
        self.fields['determ_prod'].disabled = True	
        # self.fields['total_tiempo'].disabled = True	
        self.fields['determ_tiempo'].disabled = True
        # self.fields['total_tiempopedido'].disabled = True	
        self.fields['determ_tiempopedido'].disabled = True
        # self.fields['total_servicio'].disabled = True	
        self.fields['determ_servicio'].disabled = True
        # self.fields['total'].disabled = True	
        # self.fields['subtotal'].disabled = True
        # self.fields['subtotal_participante'].disabled = True
        



    class Meta:
        model=Calificacion_proveedor

        fields= "__all__"

        labels = {
                "cod_calificacion":"Código",
                "fecha":"Fecha",
                "tipo_proveedor":"Tipo de proveedor",
                "proveedor":"Razón social/Nombre",

                # "ruc_ci":"RUC",
                # "razon_nombres":"Razon Social",
                # "codigo_evento":"Codigo del Evento",
                # "nombre_evento":"Nombre del Evento",

                "tipo_rubro":"Tipo de Rubro",

                "treinta":"",
                "veinticinco":"",
                "veinte":"",
                "quince":"",
                "diez":"",
                "cinco":"",
                "cero":"",

                "responsable":"Responsable de la calificación",
                "cargo":"Cargo del Responsable",
                "orden_compra":"Orden Compra",
                "numero_orden":"Nº Orden de Compra Portal",

                "total_prod":"",
                "determ_prod":"",
                # "prod_maximo_esc":"",
                # "prod_medio_esc":"",
                # "prod_bajo_esc":"",
                # "total_producto":"",

                "total_tiempo":"",
                "determ_tiempo":"",
                # "excelente_esc":"",
                # "muybueno_esc":"",
                # "bueno_esc":"",
                # "regular_esc":"",
                # "pesimo_esc":"",
                # "total_tiempo":"",

                "determ_tiempopedido":"",
                "total_tiempopedido":"",
                # "entrego_esc":"",
                # "noentrego_esc":"",
                # "total_tiempo_entrega":"",

                "determ_servicio":"",
                "total_servicio":"",
                # "excelente_serv_esc":"",
                # "muybueno_serv_esc":"",
                # "bueno_serv_esc":"",
                # "regular_serv_esc":"",
                # "pesimo_serv_esc":"",
                # "total_serv":"",
                "descripcion":"Observaciones",

                "total":"",
                "subtotal":"",

                "total_participante":"",
                "subtotal_participante":"",    
        }
        
        widgets={
            "evento":forms.HiddenInput(),
            "cod_calificacion":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            
            "tipo_proveedor":forms.Select(attrs={"class":"form-control"}),
            "proveedor":forms.HiddenInput(),

            "tipo_rubro":forms.Select(attrs={"class":"form-control",'disabled':True}),


            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),


            # "ruc_ci":forms.Select(attrs={'class': 'form-control select2'}),
            # "razon_nombres":forms.Select(attrs={'class': 'form-control select2'}),
            # "codigo_evento":forms.Select(attrs={'class': 'form-control select2'}),
            # "nombre_evento":forms.Select(attrs={'class': 'form-control select2'}),
            'responsable': forms.TextInput(attrs={'class':'form-control'}),
            'cargo': forms.TextInput(attrs={'class':'form-control'}),
            'orden_compra': forms.TextInput(attrs={'class':'form-control'}),
            'numero_orden': forms.TextInput(attrs={'class':'form-control'}),

            # "determ_prod":forms.TextInput(attrs={"class":"plan",'readonly':True}),
            "total_prod":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            "total_tiempo":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            "total_tiempopedido":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            "total_servicio":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            "total":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            "subtotal":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            "subtotal_participante":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),            # "prod_maximo_esc":forms.NumberInput(attrs={"type":"checkbox"}),
			# "prod_medio_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "prod_bajo_esc":forms.NumberInput(attrs={'class': "plan"}),
            # "total_producto":forms.NumberInput(attrs={'class': "plan"}),

			# "excelente_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "muybueno_esc":forms.NumberInput(attrs={'class': "plan"}),
            # "bueno_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "regular_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "pesimo_esc":forms.NumberInput(attrs={'class': "plan"}),
            # "total_tiempo":forms.NumberInput(attrs={'class': "plan"}),

            # "entrego_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "noentrego_esc":forms.NumberInput(attrs={'class': "plan"}),
            # "total_tiempo_entrega":forms.NumberInput(attrs={'class': "plan"}),

            # "excelente_serv_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "muybueno_serv_esc":forms.NumberInput(attrs={'class': "plan"}),
            # "bueno_serv_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "regular_serv_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "pesimo_serv_esc":forms.NumberInput(attrs={'class': "plan"}),
            # "total_serv":forms.NumberInput(attrs={'class': "plan"}),
            "descripcion": forms.Textarea(attrs={'rows':2}),


            "total":forms.NumberInput(attrs={'class': "plan"}), 
        }

class Calificacion_proveedorUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(Calificacion_proveedorUpdateForm, self).__init__(*args, **kwargs)

        self.fields['cod_calificacion'].disabled = True
        # self.fields['tipo_rubro'].disabled = True	
        self.fields['treinta'].disabled = True
        self.fields['veinticinco'].disabled = True
        self.fields['veinte'].disabled = True
        self.fields['quince'].disabled = True
        self.fields['diez'].disabled = True
        self.fields['cinco'].disabled = True
        self.fields['cero'].disabled = True
        # self.fields['total_prod'].disabled = True	
        self.fields['determ_prod'].disabled = True	
        # self.fields['total_tiempo'].disabled = True	
        self.fields['determ_tiempo'].disabled = True
        # self.fields['total_tiempopedido'].disabled = True	
        self.fields['determ_tiempopedido'].disabled = True
        # self.fields['total_servicio'].disabled = True	
        self.fields['determ_servicio'].disabled = True
        # self.fields['total'].disabled = True	
        # self.fields['subtotal'].disabled = True
        # self.fields['subtotal_participante'].disabled = True
        



    class Meta:
        model=Calificacion_proveedor

        fields= "__all__"

        labels = {
                "cod_calificacion":"Código",
                "fecha":"Fecha",
                "tipo_proveedor":"Tipo de proveedor",
                "proveedor":"Razón social/Nombre",

                # "ruc_ci":"RUC",
                # "razon_nombres":"Razon Social",
                # "codigo_evento":"Codigo del Evento",
                # "nombre_evento":"Nombre del Evento",

                "tipo_rubro":"Tipo de Rubro",

                "treinta":"",
                "veinticinco":"",
                "veinte":"",
                "quince":"",
                "diez":"",
                "cinco":"",
                "cero":"",

                "responsable":"Responsable de la calificación",
                "cargo":"Cargo del Responsable",
                "orden_compra":"Orden Compra",
                "numero_orden":"Nº Orden de Compra Portal",

                "total_prod":"",
                "determ_prod":"",
                # "prod_maximo_esc":"",
                # "prod_medio_esc":"",
                # "prod_bajo_esc":"",
                # "total_producto":"",

                "total_tiempo":"",
                "determ_tiempo":"",
                # "excelente_esc":"",
                # "muybueno_esc":"",
                # "bueno_esc":"",
                # "regular_esc":"",
                # "pesimo_esc":"",
                # "total_tiempo":"",

                "determ_tiempopedido":"",
                "total_tiempopedido":"",
                # "entrego_esc":"",
                # "noentrego_esc":"",
                # "total_tiempo_entrega":"",

                "determ_servicio":"",
                "total_servicio":"",
                # "excelente_serv_esc":"",
                # "muybueno_serv_esc":"",
                # "bueno_serv_esc":"",
                # "regular_serv_esc":"",
                # "pesimo_serv_esc":"",
                # "total_serv":"",
                "descripcion":"Observaciones",

                "total":"",
                "subtotal":"",

                "total_participante":"",
                "subtotal_participante":"",    
        }
        
        widgets={
            "evento":forms.HiddenInput(),
            "cod_calificacion":forms.TextInput(attrs={"class":"form-control","type":"number",'readonly':'readonly'}),
            
            "tipo_rubro":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            
            "tipo_proveedor":forms.Select(attrs={"class":"form-control"}),
            "proveedor":forms.HiddenInput(),

            "fecha":forms.DateInput(attrs={"readonly":True,'class':'form-control',"type":"date", "value":date.today}),


            # "ruc_ci":forms.Select(attrs={'class': 'form-control select2'}),
            # "razon_nombres":forms.Select(attrs={'class': 'form-control select2'}),
            # "codigo_evento":forms.Select(attrs={'class': 'form-control select2'}),
            # "nombre_evento":forms.Select(attrs={'class': 'form-control select2'}),
            'responsable': forms.TextInput(attrs={'class':'form-control'}),
            'cargo': forms.TextInput(attrs={'class':'form-control'}),
            'orden_compra': forms.TextInput(attrs={'class':'form-control'}),
            'numero_orden': forms.TextInput(attrs={'class':'form-control'}),

            # "determ_prod":forms.TextInput(attrs={"class":"plan",'readonly':True}),
            "total_prod":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            "total_tiempo":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            "total_tiempopedido":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            "total_servicio":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            "total":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            "subtotal":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),
            "subtotal_participante":forms.TextInput(attrs={"class":"form-control",'readonly':'True'}),


        # self.fields['total_tiempo'].disabled = True	

        # self.fields['total_tiempopedido'].disabled = True	

        # self.fields['total_servicio'].disabled = True	

        # self.fields['total'].disabled = True	

        # self.fields['subtotal'].disabled = True

        # self.fields['subtotal_participante'].disabled = True

            # "prod_maximo_esc":forms.NumberInput(attrs={"type":"checkbox"}),
			# "prod_medio_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "prod_bajo_esc":forms.NumberInput(attrs={'class': "plan"}),
            # "total_producto":forms.NumberInput(attrs={'class': "plan"}),

			# "excelente_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "muybueno_esc":forms.NumberInput(attrs={'class': "plan"}),
            # "bueno_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "regular_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "pesimo_esc":forms.NumberInput(attrs={'class': "plan"}),
            # "total_tiempo":forms.NumberInput(attrs={'class': "plan"}),

            # "entrego_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "noentrego_esc":forms.NumberInput(attrs={'class': "plan"}),
            # "total_tiempo_entrega":forms.NumberInput(attrs={'class': "plan"}),

            # "excelente_serv_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "muybueno_serv_esc":forms.NumberInput(attrs={'class': "plan"}),
            # "bueno_serv_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "regular_serv_esc":forms.NumberInput(attrs={'class': "plan"}),
			# "pesimo_serv_esc":forms.NumberInput(attrs={'class': "plan"}),
            # "total_serv":forms.NumberInput(attrs={'class': "plan"}),
            "descripcion": forms.Textarea(attrs={'rows':2}),


            "total":forms.NumberInput(attrs={'class': "plan"}), 
        }



class Calificacion_proveedorFilter(django_filters.FilterSet):
    
    PROVEEDORES_CHOICES = [("Natural", "Natural"),("Jurídica", "Jurídica"),]

    # tipo_proveedor = django_filters.ModelChoiceFilter(label="", empty_label="Tipo de Proveedor", queryset=models.TipoProveedor.objects.all(),method='filter_by_tipo')
    
    responsable = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control",'placeholder': 'Responsable'}))
    proveedor_id = django_filters.CharFilter(label="", widget=forms.NumberInput(attrs={'placeholder': 'Identificación Proveedor'}),method='filter_by_ruc_ci')
    proveedor_nom = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={'placeholder': 'Nombre Proveedor'}),method='filter_by_razon_nombre')
    evento__nombre=django_filters.CharFilter(lookup_expr='icontains', label="",widget=forms.TextInput(attrs={'placeholder':'Nombre evento'}))
    evento__codigo_evento=django_filters.CharFilter(lookup_expr='icontains', label="",widget=forms.TextInput(attrs={'placeholder':'Código evento'}))
    fecha=django_filters.DateFilter(field_name='fecha', label='', widget=forms.DateInput(attrs={'placeholder':'Fecha Calificación',"class":"textbox-n", "onfocus":"(this.type='date')"}))
    orden_compra = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control","type":"number",'placeholder': 'Nº Orden de compra'}))
    numero_orden = django_filters.CharFilter(label="", widget=forms.TextInput(attrs={"class":"form-control","type":"number",'placeholder': 'Nº Orden de compra Portal'}))


    class Meta:
        model = Calificacion_proveedor
        fields = [
                    # "tipo_proveedor",
					"tipo_rubro",
                    "proveedor",
                    'evento__nombre',
                    'evento__codigo_evento',
                    'proveedor_id',
                    'proveedor_nom',
					# "ruc_ci",
					# "razon_nombres",
					# "codigo_evento",
					# "nombre_evento",
					"fecha",
					"orden_compra",
				]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def filter_by_ruc_ci(self, queryset, name, value):
        return queryset.filter(Q(proveedor__ruc__icontains=value))

    def filter_by_razon_nombre(self, queryset, name, value):
        return queryset.filter(Q(proveedor__razon__icontains=value))

    def filter_by_tipo(self, queryset, name, value):
        return queryset.filter(Q(tipo=value))
