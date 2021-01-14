from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from .forms import ProformaForm, FileForm, FileFormset, ProformaUpdateForm
from .models import Proforma, ProformaFile
from django.urls import reverse_lazy
from datetime import date
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.db import transaction
from .filters import ProformaFilter
from django.core.files.storage import FileSystemStorage
# Create your views here.

"""try:
            pre=str(int(self.model.objects.latest('pk').pk+1))
            sec='0'*(4-len(pre))+pre
        except self.model.DoesNotExist:
            sec='0001'
        form.instance.cod_orden_fact=sec+'-'+str(date.today().year)"""

# def proforma_view(request):
# 	if request.method == "POST":
# 		form=ProformaForm(request.POST,request.FILES)
# 		if form.is_valid():
# 			try:
# 				pre = str(int(Proforma.objects.latest('pk').pk+1))
# 				sec = '0'*(4-len(pre))+pre
# 			except Proforma.DoesNotExist:
# 				sec = '0001'
# 			form.instance.codigo = 'PROF-CEC-'+sec+'-'+str(date.today().year)
# 			form.save()
# 		return redirect("proforma_lista")
# 	else:
# 		form=ProformaForm()
# 	return render(request, 'proforma_form.html', {'form':form})

def proforma_list(request):
    f = ProformaFilter(request.GET, queryset=Proforma.objects.all().order_by('codigo', 'version'))
    return render(request, 'proforma_list.html', {'filter': f})

class ProformaCreate(CreateView):
    model=Proforma
    form_class=ProformaForm
    form_class2= FileForm
   #form_classes = {'propuesta': PropuestaCorporativoForm,
   #                 'anexo': FileForm}
    template_name='proforma_form.html'
    success_url=reverse_lazy('proforma_lista')
    
    def get_context_data(self, **kwargs):
        data = super(ProformaCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = FileFormset(self.request.POST,self.request.FILES)
        else:
            data['formset'] =FileFormset()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['formset']
        
        try:
            cod = Proforma.objects.all().order_by('codigo').latest('codigo')
            datos=cod.codigo.split("-")
            codant=datos[2]
            pre=int(codant)+1
            sec = '0'*(4-len(str(pre)))+str(pre)
                
        except self.model.DoesNotExist:
            sec = '0001'
        form.instance.codigo = 'PROF-CEC-'+sec+'-'+str(date.today().year)

        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(ProformaCreate, self).form_valid(form)

    def get_success_url(self):
        return self.success_url




class ProformaUpdate(UpdateView):
    model=Proforma
    form_class=ProformaUpdateForm
    template_name='profoma_editar.html'
    success_url=reverse_lazy('proforma_lista')
    formset_class=FileFormset
    def get_context_data(self, **kwargs):
        context =super(ProformaUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = FileFormset(self.request.POST, self.request.FILES,instance=self.object)
        else:
            #context['form'] = self.form_class(instance=self.object)
            context['formset'] = FileFormset(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        
        form=self.form_class(request.POST)
        pk=self.kwargs.get('pk',0)
        formset = FileFormset(request.POST, request.FILES,instance=self.object)
        
        if form.is_valid():
            prop= self.model.objects.get(pk=pk)
            if prop.version!=form.instance.version:
                prop.active=False
                prop.save()
                newprop=form.save()
                if formset.is_valid():
                    nel=[]
                    for obj in formset.deleted_forms:
                        nel.append(obj.instance.file)
                    for f in formset :
                        if(f.instance.file!=None):
                            if not(f.instance.file in nel):
                                #newf=PropuestaFile.objects.create(file=f.instance.file,propuesta=newprop)
                                fileobject=f.instance.file
                                fs=FileSystemStorage()
                                filename=fs.save(fileobject.name,fileobject)
                                fs.url(filename)
                                fileobject.name=filename
                                # name=fileobject.name.split(".")
                                # newname=name[0]+"_"+str(PropuestaFile.objects.all().latest("file").id)+"."+name[len(name)-1]
                                # fileobject.name=newname
                                
                                newf = ProformaFile(file=fileobject,proforma=newprop)
                                newf.save()
                                #formset.instance = newprop
                                #formset.save()
            else :
                formr = self.form_class(request.POST or None,request.FILES, instance=prop)
                formr.save()
                if formset.is_valid():
                     formset.instance = self.object
                     formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProformaDelete(DeleteView):
    model=Proforma
    template_name='proforma_delete.html'
    form_class=ProformaForm
    success_url=reverse_lazy('proforma_lista')
