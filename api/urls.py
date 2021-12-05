from django.conf.urls import url
from django.urls import path, include

from . import views
from .. import ovas_backend

app_name = 'api'

urlpatterns = [
    path('scoreCreate/<int:pk>/<int:pk>', views.score_create, name="scoreCreate"),
    path('getOvaScore/<int:pk>', views.get_ova_score, name="getOvaScore"),
    path('getOva/<int:pk>', views.get_ova, name="getOva")
]
