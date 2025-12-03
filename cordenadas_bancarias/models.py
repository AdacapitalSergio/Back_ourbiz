from django.db import models

class CordenadasBancarias(models.Model):
    banco = models.CharField(max_length=100)
    numero_conta = models.CharField(max_length=50)
    titular_conta = models.CharField(max_length=100)
    iban = models.CharField(max_length=34, blank=True, null=True)
    numero_express = models.CharField(max_length=100, blank=True, null=True)
    swift_bic = models.CharField(max_length=11, blank=True, null=True)

    def __str__(self):
        return f"{self.titular_conta} - {self.banco} ({self.numero_conta})"
