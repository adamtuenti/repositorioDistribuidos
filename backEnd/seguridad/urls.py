from django.urls import include, path
from rest_framework import routers
from seguridad.views import *
from . import views
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'), # URL para hacer login del usuario
    path('logout/', views.logout_user, name='logout'), # URL para hacer logout del usuario
    path('usuarios/', views.ListarUsuario.as_view(), name= 'listarUsuario'),
    path('usuarioCrear/', views.crearUsuario, name= 'crearUsuario'),
    path('usuarios/<int:id_usuario>/',viewUsuario,name='verUsuario'),
    path('usuarios/<str:username>/editarcontrasena/', views.modificar_contrasena, name='confirmar_contrasena'), #URL para cambiar la contrasena
    path('resetcontrasena/', views.reestablecer_contrasena, name='reestablecer_contrasena'), #URL para resetear la contrasena
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/',include(router.urls)),
]
