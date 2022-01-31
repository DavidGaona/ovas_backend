from django.conf.urls import url
from django.urls import path


from . import views

app_name = 'api'

urlpatterns = [
    path('scoreCreate/', views.score_create, name="scoreCreate"),
    path('userCreate/', views.user_create, name="userCreate"),
    path('updatePassword/', views.update_password, name="updatePassword"),
    path('getOvaScore/<int:pk>', views.get_ova_score, name="getOvaScore"),
    path('getOva/<int:pk>', views.get_ova, name="getOva"),
    path('getListOvaPerSubject/<str:subject>', views.get_list_ova_per_subject, name='getListOvaPerSubject'),
    path('getListOvaPerTitle/<str:title>', views.get_list_ova_per_title, name='getListOvaPerTitle'),
    path('getListOva/', views.get_list_ova, name='getListOva'),
    path('getSubject/<int:pk>', views.get_subject, name="getSubject"),
    path('getSubjects/', views.get_subjects, name="getSubjects"),
    path('getListSubjectUser/<int:user>', views.get_user_subject_user, name='getListSubjectUser'),
    path('getListSubjectSubject/<int:subject>', views.get_user_subject_subject, name='getListSubjectSubject'),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('assignSubjectToUser/', views.assign_subject_to_user, name="assignSubjectToUser"),
    path('unassignSubjectToUser/<int:user>/<int:subject_id>', views.unassign_subject_to_user,
         name="unassignSubjectToUser"),
    path('getScoreUserOva/<int:user>/<int:ova>', views.get_score_user_ova, name='getScoreUserOva'),
    path('guardarToken/', views.guardar_token, name='guardarToken'),
]
