from datetime import datetime, timedelta
import uuid
from django.conf import settings 
import jwt
from ninja import Router
from django.contrib.auth.hashers import make_password
from schemas.schemas_usuario import UsuarioCreateSchema, UsuarioSchema

from utils.auth import SECRET_KEY
from utils.solicitacao_website_email import send_confirmar_funcionario_email
from .models import  Funcionario
from usuario.models import EmailVerification, Usuario
from schemas.schemas_funcionario import FuncionarioCreateSchema, FuncionarioSchema
from django.shortcuts import get_object_or_404

funcionario_router = Router()

@funcionario_router.post("/", response={200: dict, 400: dict})
def criar_funcionario(request, payload: UsuarioCreateSchema):
    """Cria um novo usuário ou associa cliente/funcionário existente"""

    usuario = Usuario.objects.filter(email=payload.email).first()
    if usuario:
        return 400, {"error": "Este usuário já está cadastrado como funcionario"}
    else:
        # Criar novo usuário
        usuario = Usuario.objects.create(
            nome_completo=payload.nome_completo,
            email=payload.email,
            telefone=payload.telefone,
            senha=make_password(payload.senha),
        )
        funcionario = Funcionario.objects.create(usuario=usuario)

        # Criar token de verificação
        verification = EmailVerification.objects.create(
            usuario=usuario,
            token=uuid.uuid4()
        )
        verification_link = f"https://api.v1.ourbiz:8000/api/usuario/verify-email/{verification.token}/"

        send_confirmar_funcionario_email.delay(
            verification_link,
            "adelinoemilianoa@gmail.com",
            #"sergio.lelis@maroldep.ao",
            f"Olá, clique no link para validares o cadastro do funcinaio: {usuario.nome_completo}"
        )

    # Criar JWT sempre no final
    payload_token = {
        "user_id": usuario.id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION_MINUTES),
        "cliente_id": funcionario.id,
    }
    token = jwt.encode(payload_token, SECRET_KEY, algorithm=settings.ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer",
        "funcionario": FuncionarioSchema.model_validate(funcionario).model_dump(),
        "logar_como": payload.logar_como
    }


@funcionario_router.post("/{usuario_id}/associar", response={200: dict, 400: dict})
def associar_funcionario(request, usuario_id: int, data: FuncionarioCreateSchema):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if hasattr(usuario, "funcionario"):
        return 400, {"error": "Este usuário já é funcionário"}
    
    funcionario = Funcionario.objects.create(
        usuario=usuario
    )

    return 200, {
        "message": "Funcionário criado com sucesso", 
        "usuario": funcionario.usuario,
        "funcionario_id": funcionario.id
        }


@funcionario_router.post("funcionario", response=list[FuncionarioSchema])
def listar_funcionario(request):
    funcionario = Funcionario.objects.all()

    return funcionario

@funcionario_router.get("/{funcionario_id}", response={200: dict, 400: dict})
def obter_funcionario(request, funcionario_id: int):
    """Obtém um usuário específico pelo ID"""
    funcionario = get_object_or_404(Funcionario, id=funcionario_id)
    
    return 200, {
        "funcionario": FuncionarioSchema.model_validate(funcionario).model_dump(),
        "funcionario_id": funcionario.id
        }

#send_confirmar_funcionario_email(funcionario_nome, verification_link, admin_email, msg_link)