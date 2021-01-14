from django.urls import include, path
from rest_framework import routers
from academico.diseño_evento.views import *
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register(r'area', AreaViewSet)
router.register(r'especialidad', EspecialidadViewSet)
router.register(r'tipoEvento', TipoEventoViewSet)
router.register(r'design', DesignEventoViewSet)
router.register(r'objetivoEspecifico', ObjetivoEspecificoViewSet)
router.register(r'unidad', UnidadViewSet)
router.register(r'subUnidad', SubUnidadViewSet)
router.register(r'recurso', RecursoViewSet)
router.register(r'lectura', LecturaViewSet)
router.register(r'referencia', ReferenciaViewSet)

urlpatterns = [
    path('api/',include(router.urls)),
    path('area/listar/',ListarAreaEspecialidad,name='listarGeneral'),
    
    #Area
    path('area/crear/',CrearArea.as_view(),name='crearArea'),
    path('area/<str:pk>/update/',UpdateArea.as_view(),name='updateArea'),
    path('area/<int:id_area>/eliminar', borrar_area, name='borrar_area'),
    #Especialidad
    path('especialidad/crear/',CrearEspecialidad.as_view(),name='crearEspecialidad'),
    path('especialidad/<str:pk>/update/',UpdateEspecialidad.as_view(),name='updateEspecialidad'),
    path('especialidad/<int:id_especialidad>/eliminar', borrar_especialidad, name='borrar_especialidad'),
    #Design Evento
    path('design/listar/',ListarDesign.as_view(),name='listarDesign'),
    path('design/crear/',CrearDesign.as_view(),name='crearDesign'),
    path('design/clonar/<int:diseno_id>/',clonarDesign,name='clonarDesign'),
    path('design/<int:diseno_pk>/',ViewDesign.as_view(),name='verDesign'),
    path('design/editar/<int:diseno_pk>/',EditDesign.as_view(),name='editarDesign'),
    path('design/list_aprobar/',ListarAprobarDesign.as_view(),name='listarAprobarDesign'),
    #-----Seccion de reportes
    path('design/Eventos_Ejecutados/', eventos_ejecutados, name='Eventos_Ejecutados'),

]
