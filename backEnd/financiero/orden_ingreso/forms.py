from django import forms
from .models import OrdenIngreso, OrdenIngresoFile
from financiero.orden_facturacion.models import OrdenFacturacion
from datetime import date
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import inlineformset_factory

class OrdenIngresoForm(forms.ModelForm):

	class Meta:
		model=OrdenIngreso
		fields='__all__'

		labels={
			'tipo_cliente':'Cliente',
			'fecha':'Fecha',
			'ruc_ci':'RUC',
			'razon_nombres':'Razón Social',
			'descripcion':'Descripción',
			'formaPago':'Forma de Pago',
			'valor':'Valor',
			'fechaPago':'Fecha Pago',
			'numeroDocumento':'N° Documento',
			'banco':"Banco",
			'emisoraTarjeta':"Emisora TC",
			'orden_facturacion':"Orden facturación",
		}

		widgets={
			'fecha':forms.DateInput(attrs={'class':'form-control','type':'date','value':date.today}),
			'fechaPago':forms.DateInput(attrs={'class':'form-control','type':'date','value':date.today}),
			'razon_nombres':forms.Select(attrs={'class':'form-control select2'}),
            'ruc_ci':forms.Select(attrs={'class':'form-control select2'}),
			'orden_facturacion':forms.Select(attrs={'class':'form-control select2'}),
			
			'descripcion':forms.Textarea(attrs={'rows':2}),
			'valor':forms.NumberInput(attrs={'class':'form-control'}),
			'numeroDocumento':forms.NumberInput(attrs={'class':'form-control'}),
			'banco':forms.TextInput(attrs={'class':'form-control'}),
			'emisoraTarjeta':forms.Select(attrs={'class':'select form-control'}),
			'formaPago':forms.Select(attrs={'id':'seleccion',"onchange":"run()"})
		}
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['orden_facturacion'].queryset = OrdenFacturacion.objects.filter(estado="PNDP")
		
	

	def genera_codigo(self):
		sec = "vacio"
		try:
			pre=str(int(self.Meta.model.objects.latest('pk').pk+1))
			sec='0'*(4-len(pre))+pre
		except ObjectDoesNotExist :
			sec='0001'
		self.instance.cod_orden_ing= sec +'-'+str(date.today().year)

	def clean(self):
		
		cd = self.cleaned_data
		try:
			if(cd.get('valor')==None):
				self.add_error('valor', 'Valor excede máxima cantidad soportada')
			if(cd.get('orden_facturacion').valor_pendiente < 0 ):
				self.add_error('orden_facturacion','Existe un valor excedente en esta orden de facturación, por lo tanto, es necesario anular ordenes de ingreso ligadas a dicha orden de facturación')
			elif (cd.get('orden_facturacion').valor_pendiente > 0):
				if(cd.get('orden_facturacion').valor_pendiente - cd.get('valor') <0):
					self.add_error('valor', 'El valor a pagar excede el valor pendiente de la orden de facturación, pendiente: $'+str(cd.get('orden_facturacion').valor_pendiente))
			return cd
		except :
			self.add_error('orden_facturacion',"El campo de orden de facturación no puede ser vacío")	

		

		
		# if(cd['valor']==None):
		# 	raise forms.ValidationError('Valor excede máxima cantidad soportada')
		# elif (cd['orden_facturacion'].valor_pendiente - cd.get('valor') <0):
		# 	raise forms.ValidationError('El valor a pagar excede el valor pendiente de la orden de facturación, pendiente: $'+str(cd.get('orden_facturacion').valor_pendiente))
		# else:
		# 	return cd['valor']

class OrdenIngresoUpdateForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(OrdenIngresoUpdateForm, self).__init__(*args, **kwargs)
		self.fields['orden_facturacion'].disabled = True
		self.fields['centro_costos'].disabled = True
		
	class Meta:
		model=OrdenIngreso
		fields='__all__'

		labels={
			'cod_orden_ing': 'Código Orden Ingreso',
			'tipo_cliente':'Cliente',
			'fecha':'Fecha',
			'n_tramite':'N° de Trámite',
			'ruc_ci':'RUC',
			'razon_nombres':'Razón Social',
			'descripcion':'Descripción',
			'formaPago':'Forma de Pago',
			'valor':'Valor',
			'fechaPago':'Fecha Pago',
			'numeroDocumento':'N° Documento',
			'banco':"Banco",
			'emisoraTarjeta':"Emisora TC",
			'pk':'id',
		}

		widgets={
			'cod_orden_ing':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext'}),
			'fecha':forms.DateInput(attrs={'readonly':True,'class':'form-control-plaintext','type':'date','value':date.today}),
			'fechaPago':forms.DateInput(attrs={'readonly':True,'class':'form-control-plaintext','type':'date','value':date.today}),
			
			'n_tramite':forms.TextInput(attrs={'class':'form-control'}),
			'fecha_tramite':forms.DateInput(attrs={'class':'form-control','type':'date'}),
			'estado':forms.HiddenInput(),
			



			'fechaPago':forms.DateInput(attrs={'class':'form-control','type':'date'}),
			 
			'tipo_cliente':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext'}),
			'razon_nombres':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext form-control'}),
            'ruc_ci':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext form-control'}),
			'descripcion':forms.Textarea(attrs={'readonly':True,'rows':2,'class':'form-control-plaintext'}),
			'valor':forms.NumberInput(attrs={'readonly':True,'class':'form-control-plaintext'}),
			'numeroDocumento':forms.NumberInput(attrs={'readonly':True,'class':'form-control-plaintext form-control'}),
			'banco':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext'}),
			'emisoraTarjeta':forms.TextInput(attrs={'readonly':True,'class':'select form-control-plaintext textinput textInput form-control'}),
			'formaPago':forms.TextInput(attrs={'readonly':True,'id':'seleccion'}),
		}
class OrdenIngresoPrintForm(forms.ModelForm):

	class Meta:
		model=OrdenIngreso
		fields='__all__'

		labels={
			'cod_orden_ing': 'Código',
			'tipo_cliente':'Cliente',
			'fecha':'Fecha',
			'n_tramite':'N° de Trámite',
			'ruc_ci':'RUC',
			'razon_nombres':'Razón Social',
			'descripcion':'Descripción',
			'formaPago':'Forma de Pago',
			'valor':'Valor',
			'fechaPago':'Fecha Pago',
			'numeroDocumento':'N° Documento',
			'banco':"Banco",
			'emisoraTarjeta':"Emisora TC",
		}

		widgets={
			'cod_orden_ing':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext'}),
			'fecha':forms.DateInput(attrs={'readonly':True,'class':'form-control-plaintext','type':'date','value':date.today}),
			'fechaPago':forms.DateInput(attrs={'readonly':True,'class':'form-control-plaintext','type':'date','value':date.today}),
			'n_tramite':forms.TextInput(attrs={'readonly':True, 'class':'form-control'}),
			'tipo_cliente':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext'}),
			'razon_nombres':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext form-control'}),
            'ruc_ci':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext form-control'}),
			'descripcion':forms.Textarea(attrs={'readonly':True,'rows':2,'class':'form-control-plaintext'}),
			'valor':forms.NumberInput(attrs={'readonly':True,'class':'form-control-plaintext'}),
			'numeroDocumento':forms.NumberInput(attrs={'readonly':True,'class':'form-control-plaintext form-control'}),
			'banco':forms.TextInput(attrs={'readonly':True,'class':'form-control-plaintext'}),
			'emisoraTarjeta':forms.TextInput(attrs={'readonly':True,'class':'select form-control-plaintext textinput textInput form-control'}),
			'formaPago':forms.TextInput(attrs={'readonly':True,'id':'seleccion'})
		}

class FileForm(forms.ModelForm):

    class Meta: 
        model= OrdenIngresoFile 
        exclude=()

FileFormset = inlineformset_factory(
    OrdenIngreso, OrdenIngresoFile, form=FileForm,
    fields=['file'],widgets={"file":forms.ClearableFileInput(attrs={'class':'ingresof','accept':'.pdf'})},
     extra=1,can_delete=True
    )