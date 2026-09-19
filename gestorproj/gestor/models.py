from django.db import models


class Aluno(models.Model):
    ra = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=100)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

class Atividade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    alunos = models.ManyToManyField(Aluno, blank=True, related_name="atividades")

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome
