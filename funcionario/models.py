from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    username = None  # remove o campo username padrão
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)  # a senha será armazenada com hash

    groups = models.ManyToManyField(
        Group,
        related_name='funcionario_user_set',  # nome único
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='funcionario_user_set',  # nome único
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo', 'telefone']

    def __str__(self):
        return self.email

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    nif = models.CharField(max_length=20, blank=True, null=True)
    nome_empresa = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.nome_completo}"
