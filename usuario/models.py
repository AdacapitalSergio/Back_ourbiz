from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid
#from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



# --------------------
# Usuário base
# --------------------

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O usuário precisa de um email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

TIPO_USUARIO_CHOICES = [
        ("cliente", "cliente"),
        ("funcionario", "funcionario"),
    ]

    
class Usuario(AbstractBaseUser, PermissionsMixin):
    nome_completo = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    #senha = models.CharField(max_length=128, editable=False)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default="cliente")
    criado_em = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # acesso ao admin
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome_completo"]

    objects = UsuarioManager()
    
    def __str__(self):
        return f"{self.nome_completo}"

    def set_senha(self, raw_password):
        self.senha = make_password(raw_password)

    def check_senha(self, raw_password):
        return check_password(raw_password, self.senha)
        
""""    @property     
    def tipo_usuario(self):
        tipos = []
        if hasattr(self, "cliente"):
            tipos.append("Cliente")
        if hasattr(self, "funcionario"):
            tipos.append("Funcionário")
        return " / ".join(tipos) if tipos else "Usuário comum"
"""
class EmailVerification(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)


# ----------------------#
# Perfil (dados pessoais) #
# ------------------------#
class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="perfil")
    sobrenome = models.CharField(max_length=150, blank=True, null=True)
    contacto_whatsapp = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.usuario.nome_completo}"


# --------------------
# Empresa (dados empresariais)
# --------------------
class Empresa(models.Model):
    nome_empresa = models.CharField(max_length=200)
    nif = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    contacto = models.CharField(max_length=20, blank=True, null=True)
    contacto_whatsapp = models.CharField(max_length=20, blank=True, null=True)

    dono_empresa = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="empresas", null=True, blank=True
    )

    def __str__(self):
        return f"{self.nome_empresa}( NIF: {self.nif} | Email: {self.email})"
    
class Endereco(models.Model):
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="enderecospessoal", null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="enderecosempresa", null=True, blank=True)

    rua = models.CharField(max_length=200)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
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
