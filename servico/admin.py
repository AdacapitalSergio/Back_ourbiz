from django.contrib import admin
from .models import Servico, Plano, Beneficio


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "descricao", "preco")  # colunas que aparecem na listagem
    search_fields = ("nome", "descricao")   # campo de busca no admin
    list_filter = ("preco",)                # filtros laterais

@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "descricao", "preco_mensal", "servicos")
    search_fields = ("titulo", "descricao")

@admin.register(Beneficio)
class BeneficioAdmin(admin.ModelAdmin):
    list_display = ("id", "descricao", "plano")
    search_fields = ("titulo", "descricao")
    list_filter = ("plano",)

