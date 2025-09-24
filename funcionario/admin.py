from django.contrib import admin
from .models import Funcionario
from cliente.models import Cliente




@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("usuario", "empresa")


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "cargo", "departamento", "empresa")
