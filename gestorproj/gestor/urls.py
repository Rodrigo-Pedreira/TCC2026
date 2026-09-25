from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import BootstrapAuthenticationForm

app_name = "gestor"

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(authentication_form=BootstrapAuthenticationForm),
        name="login",
    ),
    path("alunos/", views.alunos, name="alunos"),
    path("atividades/", views.atividades, name="atividades"),
    path("aluno/<str:aluno_ra>/", views.aluno, name="aluno"),
    path("atividade/<str:atividade_nome>/", views.atividade, name="atividade"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("relatorio_aluno/", views.RelatorioAluno.as_view(), name="relatorio_aluno"),
    path(
        "relatorio_atividade/",
        views.RelatorioAtividade.as_view(),
        name="relatorio_atividade",
    ),
]
