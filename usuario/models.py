from django.db import models
from django.contrib.auth.hashers import make_password, check_password

import uuid
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password
 
class Usuario(models.Model):
    nome_completo = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128, editable=False)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    tipo = models.CharField(max_length=50, choices=[('cliente', 'Cliente'), ('funcionario', 'Funcionário')], default='cliente')

    def __str__(self):
        return self.nome_completo

    def set_senha(self, raw_password):
        self.senha = make_password(raw_password)

    def check_senha(self, raw_password):
        return check_password(raw_password, self.senha)

class EmailVerification(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)  # Gera um token único
    criado_em = models.DateTimeField(auto_now_add=True)



class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    numero_nif = models.CharField(max_length=20, blank=True, null=True)
    numero_inss = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"Perfil de {self.usuario.nome_completo}"
