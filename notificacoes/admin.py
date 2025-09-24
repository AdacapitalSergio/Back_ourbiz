from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Notificacao

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    model = Notificacao
    list_display = ("usuario", "titulo", "mensagem", "lida", "criada_em")
    #readonly_fields = ("criado_em",)  # <-- aqui
    #list_filter = ("titulo", "mensagem", "criado_em")
    search_fields = ("titulo", "mensagem")
    #ordering = ("-criado_em",)
  