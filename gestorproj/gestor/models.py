from django.db import models
from django.core.validators import RegexValidator


class Aluno(models.Model):
    ra = models.CharField(
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{2}\.\d{5}-\d$",
                message="O RA deve estar no formato 00.00000-0.",
                code="RA_invalido",
            )
        ],
    )
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
