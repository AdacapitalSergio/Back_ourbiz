from django.db import models
from usuario.models import Empresa, Usuario

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="cliente")
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, related_name="clientes", null=True, blank=True)


    def __str__(self):
        return f"Cliente: {self.usuario.nome_completo}"

