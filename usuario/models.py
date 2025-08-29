from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid
from django.utils import timezone


# --------------------
# Usuário base
# --------------------
class Usuario(models.Model):
    ROLE_CHOICES = [
        ("cliente", "Cliente"),
        ("funcionario", "Funcionário"),
    ]
    nome_completo = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128, editable=False)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    tipo = models.CharField(max_length=20, choices=ROLE_CHOICES, default="cliente")

    def __str__(self):
        return self.nome_completo

    def set_senha(self, raw_password):
        self.senha = make_password(raw_password)

    def check_senha(self, raw_password):
        return check_password(raw_password, self.senha)

class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.username

class EmailVerification(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)


# --------------------
# Perfil (dados pessoais)
# --------------------
class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="perfil")

    nome = models.CharField(max_length=150)
    sobrenome = models.CharField(max_length=150)
    email = models.EmailField()
    contacto = models.CharField(max_length=20, blank=True, null=True)
    contacto_whatsapp = models.CharField(max_length=20, blank=True, null=True)
    localidade = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    endereco1 = models.CharField(max_length=200, blank=True, null=True)
    endereco2 = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return f"Perfil de {self.usuario.nome_completo}"

class EnderecoPessoal(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="dados_pessoais", null=True, blank=True
    )
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.rua}, {self.cidade} - {self.provincia}"

# --------------------
# Empresa (dados empresariais)
# --------------------
class Empresa(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="dados_empresariais", null=True, blank=True
    )
    nome_empresa = models.CharField(max_length=200)
    nif = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    contacto = models.CharField(max_length=20, blank=True, null=True)
    contacto_whatsapp = models.CharField(max_length=20, blank=True, null=True)
    

    def __str__(self):
        return f"{self.nome_empresa} (NIF: {self.nif})"
    
class EnderecoEmpresa(models.Model):
    empresa = models.OneToOneField(
        Empresa, on_delete=models.CASCADE, related_name="dados_empresa", null=True, blank=True
    )
    rua = models.CharField(max_length=200)
    numero = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    codigo_postal = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.rua}, {self.cidade} - {self.provincia}"

class Preferencias(models.Model):
    usuario = models.OneToOneField(
        Usuario, on_delete=models.CASCADE, related_name="preferencias", null=True,
        blank=True
    )
    DADOS_FATURACAO_CHOICES = [
        ("pessoal", "Utilizar dados pessoais na faturação"),
        ("empresarial", "Utilizar dados empresariais na faturação"),
    ]

    EMAIL_PRINCIPAL_CHOICES = [
        ("empresarial", "Utilizar e-mail empresarial como principal"),
        ("pessoal", "Utilizar e-mail pessoal como principal"),
    ]

    CONTACTO_SMS_CHOICES = [
        ("empresarial", "Utilizar contacto empresarial para receber SMS"),
        ("pessoal", "Utilizar contacto pessoal para receber SMS"),
    ]

    dados_faturacao = models.CharField(max_length=20, choices=DADOS_FATURACAO_CHOICES, default="pessoal")
    email_principal = models.CharField(max_length=20, choices=EMAIL_PRINCIPAL_CHOICES, default="empresarial")
    contacto_sms = models.CharField(max_length=20, choices=CONTACTO_SMS_CHOICES, default="empresarial")

    def __str__(self):
        return f"Preferências de {self.usuario.usuario.nome_completo}"

class Notificacao(models.Model):
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE, related_name="notificacoes")
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.usuario} - {self.titulo}"