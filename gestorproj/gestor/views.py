from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView
from django_weasyprint import WeasyTemplateView

from .models import Aluno, Atividade


# ----------------------------------- Index ---------------------------------- #
@login_required
@permission_required(["gestor.view_aluno", "gestor.view_atividade"])
def index(request):
    total_alunos = Aluno.objects.count()
    total_atividades = Atividade.objects.count()
    context = {"total_alunos": total_alunos, "total_atividades": total_atividades}
    return render(request, "gestor/index.html", context)


# ---------------------------------- Alunos ---------------------------------- #
@login_required
@permission_required("gestor.view_aluno")
def alunos(request):
    alunos = Aluno.objects.all()
    total_alunos = Aluno.objects.count()
    context = {"alunos": alunos, "total_alunos": total_alunos}
    return render(request, "gestor/alunos.html", context)


# ----------------------------------- Aluno ---------------------------------- #
@login_required
@permission_required("gestor.view_aluno")
def aluno(request, aluno_ra):
    aluno = get_object_or_404(Aluno, ra=aluno_ra)
    aluno_atividades = [
        atv.nome
        for atv in aluno.atividades.all()  # pyright: ignore[reportAttributeAccessIssue]
    ]
    context = {"aluno": aluno, "aluno_atividades": aluno_atividades}
    return render(request, "gestor/aluno.html", context)


# --------------------------------- Atividade -------------------------------- #
@login_required
@permission_required("gestor.view_atividade")
def atividade(request, atividade_nome):
    atividade = get_object_or_404(Atividade, nome=atividade_nome)
    alunos = atividade.alunos.all()
    context = {"atividade": atividade, "alunos": alunos}
    return render(request, "gestor/atividade.html", context)


# -------------------------------- Atividades -------------------------------- #
@login_required
@permission_required("gestor.view_atividade")
def atividades(request):
    atividades = Atividade.objects.all()
    total_atividades = Atividade.objects.count()
    context = {"atividades": atividades, "total_atividades": total_atividades}
    return render(request, "gestor/atividades.html", context)


# ---------------------------------------------------------------------------- #
#                               RELATORIOS (PDF)                               #
# ---------------------------------------------------------------------------- #


# ------------------------------ Relatorio Aluno ----------------------------- #
class RelatorioAluno(LoginRequiredMixin, TemplateView):  # WeasyTemplateView
    template_name = "gestor/relatorio_aluno.html"
    pdf_filename = "relatorio_aluno.pdf"
    permission_required = "gestor.view_aluno"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report_date"] = timezone.now().date()
        context["body_text"] = (
            "This is the body of the report. Replace with real content."
        )
        return context


# ---------------------------- Relatorio Atividade --------------------------- #
class RelatorioAtividade(LoginRequiredMixin, TemplateView):
    template_name = "gestor/relatorio_atividade.html"
    pdf_filename = "relatorio_atividade.pdf"
    permission_required = "gestor.view_atividade"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["report_date"] = timezone.now().date()
        context["body_text"] = (
            "This is the body of the report. Replace with real content."
        )
        return context
