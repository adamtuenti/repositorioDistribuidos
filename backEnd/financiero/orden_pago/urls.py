from django.urls import path
from django_filters.views import FilterView
from . import views
from .filters import OrdenPagoFilter

urlpatterns = [
    path("", views.index, name="orden_pago_lista"),
    path("ajax/load-egresos/", views.load_egresos, name="ajax_load_egresos"),
    path("nuevo/", views.OrdenPagoCreate.as_view(), name="orden_pago_nuevo"),
    path("editar/<pk>/", views.OrdenPagoUpdate.as_view(), name="orden_pago_editar"),
    path("editare/<pk>/", views.OrdenPagoEnviadoUpdate.as_view(), name="orden_pago_editar_enviado"),
    path("editara/<pk>/", views.OrdenPagoAprobadoUpdate.as_view(), name="orden_pago_editar_autorizado"),
    path("editarp/<pk>/", views.OrdenPagoPagadoUpdate.as_view(), name="orden_pago_editar_pagado"),
	path('ajax/load-elminar-orden-pago',views.ordenpago_conf_elim,name='ordenpago_confirmar_eliminar'),
    path('eliminar/<pk>/', views.OrdenPagoDelete.as_view(), name='ordenpago_eliminar'),
    path("aprobar/<pk>/", views.OrdenPagoAprobarUpdate.as_view(), name="orden_pago_autorizar"),
]