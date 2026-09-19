from django.contrib import admin

from .models import Aluno, Atividade

admin.site.register([Aluno, Atividade])
