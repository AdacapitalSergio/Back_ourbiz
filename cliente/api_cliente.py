from datetime import datetime, timedelta
import uuid
from django.conf import settings 
import jwt
from ninja import Router

from schemas.schemas_usuario import UsuarioCreateSchema, UsuarioSchema
from utils.auth import SECRET_KEY
from utils.solicitacao_website_email import send_verification_email
from .models import  Cliente
from usuario.models import EmailVerification, Usuario, make_password
from schemas.schemas_funcionario import FuncionarioCreateSchema, FuncionarioSchema, EmpresaSchema
from schemas.schemas_cliente import ClienteSchema
from django.shortcuts import get_object_or_404

cliente_router = Router()

@cliente_router.post("/", response={200: dict, 400: dict})
def criar_usuario(request, data: UsuarioCreateSchema):
    """Cria um novo usuário ou associa cliente"""

    usuario = Usuario.objects.filter(email=data.email).first()
    if usuario:
        return 400, {"error": "Este usuário já está cadastrado como cliente"}
    else:
        # Criar novo usuário
        usuario = Usuario.objects.create(
            nome_completo=data.nome_completo,
            email=data.email,
            telefone=data.telefone,
            senha=make_password(data.senha),
        )
        cliente = Cliente.objects.create(usuario=usuario)
       
        # Criar verificação de email
        verification = EmailVerification.objects.create(
            usuario=usuario,
            token=uuid.uuid4()
        )
        verification_link = f"https://api.v1.ourbiz:8000/api/usuario/verify-email/{verification.token}/"

        send_verification_email.delay(
            usuario.nome_completo,
            verification_link,
            usuario.email,
            "Clique no link para confirmar seu e-mail"
        )

    # Criar JWT
    payload = {
        "user_id": usuario.id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION_MINUTES),
        "cliente_id": cliente.id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=settings.ALGORITHM)

    # Resposta padronizada
    return 200, {
        "access_token": token,
        "token_type": "bearer",
        "cliente": {
            "id": cliente.id,
            "usuario": {
                "id": usuario.id,
                "nome_completo": usuario.nome_completo,
                "email": usuario.email,
                "telefone": usuario.telefone,
                "empresa": None,         # só virá depois
                "perfil": None,          # só virá depois
                "preferencias": None,    # só virá depois
                "enderecos": [],         # começa vazio
            }
        },
        "logar_como": "cliente"
    }


@cliente_router.get("clientes", response=list[ClienteSchema])
def listar_cliente(request):
    cliente = Cliente.objects.all()

    return cliente

