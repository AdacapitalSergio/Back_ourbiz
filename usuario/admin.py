from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Empresa, Endereco, Preferencias


# --------------------
# Usuario com gráficos
# --------------------
@admin.register(Usuario)
class UsuarioAdmin( UserAdmin):
    model = Usuario
    list_display = ("nome_completo", "email", "telefone", "tipo_usuario", "is_verified", "is_staff", "is_active", "criado_em")
    readonly_fields = ("criado_em", "last_login")
    list_filter = ("tipo_usuario", "is_verified", "is_staff", "is_active", "criado_em")
    search_fields = ("nome_completo", "email", "telefone")
    ordering = ("-criado_em",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações pessoais", {"fields": ("nome_completo", "telefone", "tipo_usuario")}),
        ("Permissões", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Status", {"fields": ("is_verified",)}),
        ("Datas importantes", {"fields": ("last_login", "criado_em")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nome_completo", "telefone", "tipo_usuario", "password1", "password2", "is_staff", "is_active"),
        }),
    )



# --------------------
# Empresa com gráficos
# --------------------
@admin.register(Empresa)
class EmpresaAdmin( admin.ModelAdmin):
    list_display = ("nome_empresa", "nif", "email", "contacto", "contacto_whatsapp", "dono_empresa")
    search_fields = ("nome_empresa", "nif", "email")
    list_filter = ("dono_empresa",)

# --------------------
# Endereço
# --------------------
@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ("rua", "bairro", "cidade", "provincia", "pais", "codigo_postal", "usuario", "empresa")
    search_fields = ("rua", "cidade", "provincia", "pais")
    list_filter = ("cidade", "provincia", "pais")


# --------------------
# Preferências
# --------------------
@admin.register(Preferencias)
class PreferenciasAdmin(admin.ModelAdmin):
    list_display = ("usuario", "dados_faturacao", "email_principal", "contacto_sms")
    search_fields = ("usuario__nome_completo", "usuario__email")
    list_filter = ("dados_faturacao", "email_principal", "contacto_sms")
