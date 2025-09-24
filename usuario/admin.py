from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, EmailVerification, Perfil, Empresa, Endereco, Preferencias


# --------------------
# Usuario (Custom User)
# --------------------
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ("nome_completo", "email", "telefone", "tipo_usuario", "is_verified", "is_staff", "is_active", "criado_em")
    readonly_fields = ("criado_em",)  # <-- aqui
    list_filter = ("is_verified", "is_staff", "is_active", "criado_em")
    search_fields = ("nome_completo", "email", "telefone")
    ordering = ("-criado_em",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informações pessoais", {"fields": ("nome_completo", "telefone")}),
        ("Permissões", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Status", {"fields": ("is_verified",)}),
        ("Datas importantes", {"fields": ("last_login", "criado_em")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "nome_completo", "telefone", "password1", "password2", "is_staff", "is_active"),
        }),
    )
