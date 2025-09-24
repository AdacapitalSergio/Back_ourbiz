from django.db import models
from django.utils import timezone
from usuario.models import Usuario

class Notificacao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="notificacoes")
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario} - {self.titulo}"
