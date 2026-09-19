from django.urls import path

from . import views

app_name = "gestor"
urlpatterns = [
    path("", views.index, name="index"),
    path("alunos/", views.alunos, name="alunos"),
    path("atividades/", views.atividades, name="atividades"),
    path("aluno/<str:aluno_ra>/", views.aluno, name="aluno"),
    path("atividade/<str:atividade_nome>/", views.atividade, name="atividade")
]