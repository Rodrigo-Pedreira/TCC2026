from django.contrib import admin, messages
from django.contrib.admin import forms, helpers
from django.db.models import Q
from django.template.response import TemplateResponse
from django import forms
from django.contrib.postgres.search import (
    TrigramWordSimilarity,  # pyright: ignore[reportAttributeAccessIssue]
)
from .models import Aluno, Atividade

admin.site.site_header = "Gestor de Atividades"  # top of every admin page
admin.site.site_title = "Gestor de Atividades"  # suffix in the browser tab title
admin.site.index_title = (
    "Bem-vindo ao Gestor de Atividades"  # heading on the admin index page
)

# ----------------------------------- Aluno ---------------------------------- #
@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ["ra", "nome"]
    ordering = ["nome"]
    actions = ["adicionar_a_atividade"]
    list_filter = ["atividades"]
    search_fields = ["nome__unaccent__icontains", "ra"]  # ignora acentos

    def get_search_results(self, request, queryset, search_term):
        base = queryset
        matched, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            fuzzy_ids = (
                base.annotate(sim=TrigramWordSimilarity(search_term, "nome"))
                .filter(sim__gt=0.4)  # raise for stricter, lower for looser
                .values("pk")
            )
            matched = base.filter(Q(pk__in=matched.values("pk")) | Q(pk__in=fuzzy_ids))

        return matched, may_have_duplicates

    class AdicionarAtividadeForm(forms.Form):
        atividade = forms.ModelChoiceField(
            queryset=Atividade.objects.order_by("nome"),
            label="Atividade",
            empty_label="Selecione uma atividade",
        )

    @admin.action(
        permissions=["change"],
        description="Adicionar alunos selecionados a uma atividade",
    )
    def adicionar_a_atividade(self, request, queryset):
        # Second pass: the intermediate form was submitted
        if "apply" in request.POST:
            form = self.AdicionarAtividadeForm(request.POST)
            if form.is_valid():
                atividade = form.cleaned_data["atividade"]
                atividade.alunos.add(*queryset)
                self.message_user(
                    request,
                    f"{queryset.count()} aluno(s) adicionado(s) para a atividade '{atividade}'.",
                    messages.SUCCESS,
                )
                return None  # returning None redirects back to the changelist
        else:
            # First pass: show an empty form
            form = self.AdicionarAtividadeForm()

        context = {
            **self.admin_site.each_context(request),
            "title": "Adicionar alunos a uma atividade",
            "opts": self.model._meta,
            "queryset": queryset,
            "form": form,
            "action_name": "adicionar_a_atividade",
            "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
        }
        return TemplateResponse(request, "admin/adicionar_atividade.html", context)

# --------------------------------- Atividade -------------------------------- #
@admin.register(Atividade)
class AtividadeAdmin(admin.ModelAdmin):
    list_display = ["nome"]
    ordering = ["nome"]
    search_fields = ["nome__unaccent__icontains"]  # ignora acentos
    autocomplete_fields = ["alunos"]

    def get_search_results(self, request, queryset, search_term):
        base = queryset
        matched, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            fuzzy_ids = (
                base.annotate(sim=TrigramWordSimilarity(search_term, "nome"))
                .filter(sim__gt=0.4)  # raise for stricter, lower for looser
                .values("pk")
            )
            matched = base.filter(Q(pk__in=matched.values("pk")) | Q(pk__in=fuzzy_ids))

        return matched, may_have_duplicates
