from django.db import models

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