from django.conf.urls import url
from django.urls import path, include

from . import views

app_name = 'api'

urlpatterns = [
    path('scoreCreate/<int:pk>/<int:pk_ova>', views.score_create, name="scoreCreate"),
    path('getOvaScore/<int:pk>', views.get_ova_score, name="getOvaScore"),
    path('getOva/<int:pk>', views.get_ova, name="getOva"),
    path('getListOvaPerSubject/<str:subject>', views.get_list_ova_per_subject, name='getListOvaPerSubject'),
    path('getListOvaPerTitle/<str:title>', views.get_list_ova_per_title, name='getListOvaPerTitle'),
    path('getListOva/', views.get_list_ova, name='getListOva'),
    path('getSubject/<int:pk>', views.get_subject, name="getSubject"),
    path('getListSubjectUser/<int:user>', views.get_user_subject_user, name='getListSubjectUser'),
    path('getListSubjectSubject/<int:subject>', views.get_user_subject_subject, name='getListSubjectSubject')

]
