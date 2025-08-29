from datetime import timedelta, date
from dateutil.relativedelta import relativedelta  # melhor para meses

from django.db import models
from usuario.models import Cliente
from funcionario.models import Funcionario
# Create your models here.
from django.db import models

TEM_DOMINIO_CHOICES = [
    ('Sim', 'Sim'),
    ('Não', 'Não'),
    ('Ainda não sei o que é isso', 'Ainda não sei o que é isso'),
]

TEM_LOGOTIPO_CHOICES = [
    ('Sim', 'Sim'),
    ('Não', 'Não'),
    ('Em processo de criação', 'Em processo de criação'),
]
class Objetivo(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class WebsiteRequest(models.Model):
    nome_requerente = models.CharField(max_length=255)
    email_requerente = models.EmailField()
    telefone_requerente = models.CharField(max_length=15, blank=True, null=True)
    objetivo_site = models.ManyToManyField(Objetivo, blank=True)
    tem_dominio = models.CharField(max_length=50, choices=TEM_DOMINIO_CHOICES, null=True, blank=True)
    dominio = models.CharField(max_length=255, blank=True, null=True)
    tem_logotipo = models.CharField(max_length=50, choices=TEM_LOGOTIPO_CHOICES, null=True, blank=True)
    sobre_empresa = models.TextField(blank=True, null=True)
    integracoes = models.TextField(blank=True, null=True)
    site_referencia = models.CharField(max_length=255, blank=True, null=True)
    metodo_contato = models.CharField(max_length=100, blank=True, null=True)
    commentarios = models.TextField(blank=True, null=True)
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitação de {self.nome_requerente} ({self.email_requerente})"
    


class Servico(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    tipo = models.CharField(max_length=50, choices=[
        ("consultoria_pequenas_empresas", "Consultoria para Pequenas Empresas"),
        ("consultoria_startups", "Consultoria para Startups"),
        ("outros", "Outros")
    ])
    preco_base = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome


class SolicitacaoServico(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)

    tipo_servico = models.CharField(max_length=50, choices=[
        ("corrente", "Corrente"),
        ("avulso", "Avulso")
    ])

    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=[
        ("pendente", "Pendente"),
        ("aprovado", "Aprovado"),
        ("em_andamento", "Em Andamento"),
        ("concluido", "Concluído"),
        ("cancelado", "Cancelado")
    ], default="pendente")

    descricao = models.TextField(blank=True, null=True)
    data_inicio = models.DateField(default=date.today)
    duracao_meses = models.PositiveIntegerField(default=1)
    data_final = models.DateField(blank=True, null=True)
    data_pagamento = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.data_inicio and self.duracao_meses:
            self.data_final = self.data_inicio + relativedelta(months=self.duracao_meses)
            self.data_pagamento = self.data_final  # <- aqui pode mudar a regra se quiser (ex: data_inicio + 1 mês)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.servico.nome} - {self.cliente.user.username} ({self.status})"