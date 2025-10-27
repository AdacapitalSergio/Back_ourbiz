from django.db import models


class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    tipo_servico = models.CharField(max_length=50, choices=[
        ("corrente", "Corrente"),
        ("avulso", "Avulso")
    ], default="corrente")
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome


class Plano(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    preco_mensal = models.DecimalField(max_digits=10, decimal_places=3)
    servicos = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name="planos")

    def __str__(self):
        return f"{self.titulo} ( servico: {self.servicos.nome} )"


class Beneficio(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    plano = models.ForeignKey(Plano, on_delete=models.CASCADE, related_name="beneficios")

    def __str__(self):
        return f"{self.titulo} ({self.plano.titulo}) ({self.plano.servicos})"