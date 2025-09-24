from django.db import models
from django.contrib.auth.models import User
from usuario.models import Usuario, Empresa
# ----------------#
#   Funcionário     #
# ----------------#
class Funcionario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="funcionario")
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="funcionario")
    cargo = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    matricula = models.CharField(max_length=50, blank=True, null=True)

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.SET_NULL,
        related_name="funcionarios",  # corrigido (antes era "clientes")
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Funcionário: {self.usuario.nome_completo} ({self.empresa.nome_completo if self.empresa else 'Sem empresa'})"
