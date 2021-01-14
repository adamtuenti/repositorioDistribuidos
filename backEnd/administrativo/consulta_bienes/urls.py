from django.urls import path
from django.views import generic

from . import views
from .models import *
from .views import *

urlpatterns = [
    path('', views.consulta_bienes, name='consulta_bienes'),
]