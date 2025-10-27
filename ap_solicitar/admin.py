from django.contrib import admin

from funcionario.models import Funcionario
from utils.notificacoes import enviar_notificacao
from .models import  Objetivo, WebsiteRequest, SolicitacaoServico

"""@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "tipo", "preco_base")
    search_fields = ("nome", "tipo")
"""
@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ("nome",)

@admin.register(WebsiteRequest)
class WebsiteRequestAdmin(admin.ModelAdmin):
    list_display = ("nome_requerente", "email_requerente", "telefone_requerente", "data_solicitacao")
    search_fields = ("nome_requerente", "email_requerente")

@admin.register(SolicitacaoServico)
class SolicitacaoServicoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "funcionario", "status", "factura_servico", "data_inicio", "data_final")
    list_filter = ("status", "data_inicio")
    search_fields = ("cliente__usuario__nome_completo", "servico__nome")
    readonly_fields = ("data_final", "data_pagamento")

    # Ação customizada no admin
    actions = ["aprovar_solicitacao"]

    def aprovar_solicitacao(self, request, queryset):
        funcionario = request.user.funcionario 
     
        for solicitacao in queryset:
            if solicitacao.factura_servico:
                solicitacao.status = "aprovado"
                solicitacao.funcionario = funcionario  
                solicitacao.save()
            mensagem = "Solicitacao aprovada com sucesso!"            
            enviar_notificacao(solicitacao.cliente.id, "Estado da solicitacao", mensagem)      
                
  
        self.message_user(request, "Solicitações aprovadas com sucesso.")
        
    aprovar_solicitacao.short_description = "Aprovar solicitações com fatura validada"

