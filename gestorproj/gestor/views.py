from django.shortcuts import render, get_object_or_404

from .models import Aluno, Atividade


def index(request):
    total_alunos = Aluno.objects.count()
    total_atividades = Atividade.objects.count()
    context = {"total_alunos": total_alunos, "total_atividades": total_atividades}
    return render(request, "gestor/index.html", context)


def alunos(request):
    alunos = Aluno.objects.all()
    context = {"alunos": alunos}
    return render(request, "gestor/alunos.html", context)


def aluno(request, aluno_ra):
    aluno = get_object_or_404(Aluno, ra=aluno_ra)
    aluno_atividades = [
        at.nome for at in aluno.atividades.all()
    ]  # pyright: ignore[reportAttributeAccessIssue]
    context = {"aluno": aluno, "aluno_atividades": aluno_atividades}
    return render(request, "gestor/aluno.html", context)


def atividade(request, atividade_nome):
    atividade = get_object_or_404(Atividade, nome=atividade_nome)
    alunos = atividade.alunos.all()
    context = {"atividade": atividade, "alunos": alunos}
    return render(request, "gestor/atividade.html", context)


def atividades(request):
    atividades = Atividade.objects.all()
    context = {"atividades": atividades}
    return render(request, "gestor/atividades.html", context)
