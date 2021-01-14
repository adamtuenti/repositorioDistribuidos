"""educacion_continua URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .routers import *

urlpatterns = [
    path('', include("seguridad.urls")),
    #ACADEMICO
    path('api/', include(plan_trabajo_router.urls)),
    path('api/', include(docente_router.urls)),
    path('api/', include(participante_router.urls)),
    path('api/', include("academico.participante.urls")),
    path('academico/', include("academico.evento.urls")),
    path('academico/', include("academico.diseño_evento.urls")),
    path('academico/docente/', include(("academico.docente.urls"))),
    path('academico/participante/', include("academico.participante.urls")),
    path('academico/plan_trabajo/', include("academico.plan_trabajo.urls")),
    path('academico/reporte_aca/', include("academico.reporte_aca.urls")),
    #ADMINISTRATIVO
    path('administrativo/productos/', include("administrativo.productos.urls")),
    path('administrativo/proveedores/', include("administrativo.proveedores.urls")),
    path('administrativo/calificacion_proveedores/', include("administrativo.calificacion_proveedores.urls")),
    path('administrativo/suministros/', include("administrativo.suministros.urls")),
    path('administrativo/suministros_egreso/', include("administrativo.suministros_egreso.urls")),
    path('administrativo/ingreso_bienes/', include("administrativo.ingreso_bienes.urls")),
    path('administrativo/consulta_bienes/', include("administrativo.consulta_bienes.urls")),
    path('administrativo/solicitudes_compra/', include("administrativo.solicitudes_compra.urls")),
    path('administrativo/ordenes_compra/', include("administrativo.ordenes_compra.urls")),
    path('administrativo/analisis_cotizaciones/', include("administrativo.analisis_cotizaciones.urls")),
    path('administrativo/mantenimientos/', include("administrativo.mantenimientos.urls")),
    path('administrativo/inventarios/', include("administrativo.inventarios.urls")),

    #VENTAS
    path('ventas/',include("ventas.urls")),
	path('ventas/personas_juridicas/', include("ventas.personas_juridicas.urls")),
	path('ventas/reporte_contacto/', include("ventas.reporte_contacto.urls")),
    path('ventas/personas_naturales/', include("ventas.personas_naturales.urls")),
    path('ventas/propuesta_corp/', include("ventas.propuesta_corp.urls")),
    path('ventas/proformas/',include("ventas.proformas.urls")),
    path('ventas/interesados/',include("ventas.interesados.urls")),
    path('ventas/seguimientos/',include("ventas.seguimientos.urls")),
    #FINANCIERO
    path('financiero/',include("financiero.urls")),
    path('financiero/perfiles/', include('financiero.perfiles.urls')),
    path('financiero/orden_ingreso/',include('financiero.orden_ingreso.urls')),
    path('financiero/orden_facturacion/',include('financiero.orden_facturacion.urls')),
    path("financiero/presupuestos/",include("financiero.presupuestos.urls")),
    path("financiero/orden_pago/",include("financiero.orden_pago.urls")),
    path("financiero/pago_eventos/",include("financiero.pago_eventos.urls")),
    path("financiero/presupuestos_anuales/",include("financiero.presupuestos_anuales.urls")),
    path("financiero/plan_anual_compras/",include("financiero.plan_anual_compras.urls")),
    path("financiero/procesos_especiales/",include("financiero.procesos_especiales.urls")),
    #ADMIN
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)