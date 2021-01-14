from bootstrap_modal_forms.forms import BSModalForm,CreateUpdateAjaxMixin
from .models import Area,Especialidad
from django import forms
class AreaForm(BSModalForm):
    class Meta:
        model=Area
        fields = {
            'codigo',
            'area',
        }

        widgets = {
            'codigo':forms.TextInput(attrs={'class':'form-control'}),
            'area':forms.TextInput(attrs={'class':'form-control'}),
        }
    
    def save(self, commit=False):
        if not self.request.is_ajax():
            instance = super(CreateUpdateAjaxMixin, self).save(commit=commit)
            esp = Especialidad.objects.filter(area = instance.id)
            if esp:
                instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
            else:
                instance.save()
        else:
            instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

        return instance

class EspecialidadForm(BSModalForm):
    class Meta:
        model=Especialidad

        fields = {
            'codigo',
            'especialidades',
            'area',
        }

        widgets = {
            'codigo':forms.TextInput(attrs={'class':'form-control','maxlength':'2'}),
            'especialidades':forms.Textarea(attrs={'class':'form-control','rows':'10'}),
            'area':forms.Select(attrs={'class':'form-control'}),
        }
    
    def save(self, commit=False):
        if not self.request.is_ajax():
            instance = super(CreateUpdateAjaxMixin, self).save(commit=commit)
            if len(instance.codigo)==1 and instance.codigo[0]!="0":
                instance.codigo = "0"+instance.codigo
            instance.codigo = instance.area.codigo + "" + instance.codigo
            instance.save()
        else:
            instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

        return instance