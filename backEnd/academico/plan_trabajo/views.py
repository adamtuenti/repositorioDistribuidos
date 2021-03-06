from django.shortcuts import *
from django.views.generic import *
from django.views.generic.edit import *
from academico.diseño_evento.models import DesignEvento as DisenoEvento
from academico.evento.models import Evento
from academico.plan_trabajo.models import *
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from django.http import JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.http import HttpResponse
from django.template import Context


# Create your views here.
class PlanTrabajoCreate(TemplateView):
    template_name = 'plan_trabajo/fill.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        planTrabajo_id = self.kwargs['planTrabajo_pk']
        plan = get_object_or_404(PlanTrabajo, id=planTrabajo_id)
        context['planTrabajo_id'] = planTrabajo_id
        context['evento_id'] = plan.evento_id
        evento = get_object_or_404(Evento, codigo_evento=plan.evento_id)
        context['disenoEvento_id'] = evento.diseno_id
        return context


class PlanTrabajoCheck(TemplateView):
    template_name = 'plan_trabajo/check.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        planTrabajo_id = self.kwargs['planTrabajo_pk']
        plan = get_object_or_404(PlanTrabajo, id=planTrabajo_id)
        context['planTrabajo_id'] = planTrabajo_id
        context['evento_id'] = plan.evento_id
        evento = get_object_or_404(Evento, codigo_evento=plan.evento_id)
        context['disenoEvento_id'] = evento.diseno
        return context


def plan_trabajo_copy(request, basePlanTrabajo_pk, newPlanTrabajo_pk):
    baseP = get_object_or_404(PlanTrabajo, id=basePlanTrabajo_pk)
    newP = get_object_or_404(PlanTrabajo, id=newPlanTrabajo_pk)
    newP.instrumentos_de_evaluacion = baseP.instrumentos_de_evaluacion
    newP.save()

    ms = [
        ReferenciaBibliograficaPlan,
        LecturaRecomendadaPlan,
        RecursoPlan,
        AnexoPlan,
        ActividadPlan,
    ]
    for model in ms:
        try:
            queryset = get_list_or_404(model, plan_trabajo_id=basePlanTrabajo_pk)
            for instance in queryset:
                instance.pk = None
                instance.save()
                instance.plan_trabajo_id = newPlanTrabajo_pk
                instance.save()
        except Http404:
            pass
    return JsonResponse({
            'detail': '. Plan updated'
        }, status=204)

#-------------- Seccion de reportes-------------------

class reporte_empresa(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reporte_empresa.html')
        context = {"Nombre":"Luis Eduardo",
                     "Apellidos":"Ardila Macias",
                   }
        pdf = render_to_pdf('reporte_empresa.html',context)
        return HttpResponse(pdf, content_type='application/pdf')