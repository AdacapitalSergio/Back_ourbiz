from http.client import HTTPException
from utils.auth import SECRET_KEY
from utils.auth import auth

from ninja.security import HttpBearer
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
import jwt # type: ignore


from django.conf import settings
from ninja import Router

from utils.solicitacao_website_email import send_verification_email
from .models import EmailVerification, Usuario, Perfil
import uuid
from schemas.schemas_cliente import CadastroUsuarioSchema, PerfilSchema, UsuarioResponseSchema, LinkEmailSchema, LoginSchema, RedefinirSenhaSchema

# Routers
usuario_router = Router()
auth_router = Router()


# Endpoints de autenticação
@auth_router.post("/login", response=dict)
def login(request, data: LoginSchema):
    #Realiza o login e retorna um token JWT
    usuario = Usuario.objects.filter(email=data.email).first()

    if not usuario or not usuario.check_senha(data.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
 
    payload = {
        "user_id": usuario.id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION_MINUTES),
        "role": usuario.role if hasattr(usuario, "role") else "user"  # Exemplo de adição de permissão
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=settings.ALGORITHM)

    return {
        "access_token": token, 
        "token_type": "bearer", 
        "usuario": UsuarioResponseSchema.model_validate(usuario).model_dump()
        }


@auth_router.post("/recuperacao-conta")
def recuperar_conta(request, dados: LinkEmailSchema):
    """
    Endpoint para iniciar o processo de recuperação de conta.
    Mesmo que o email não esteja cadastrado, a resposta é padronizada
    para evitar a enumeração de usuários.
    """
    usuario = Usuario.objects.filter(email=dados.email).first()
    if not usuario:
        # Retorna a mesma mensagem mesmo que o usuário não exista
        return {"mensagem": "Se o email existir, um link de recuperação foi enviado."}
    
    # Cria o payload para o token de recuperação
    payload = {
        "id_usuario": usuario.id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION_MINUTES)
    }
    token_recuperacao = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    #link_recuperacao = f"http://localhost:8000/api/clientes/redefinir-senha?token={token_recuperacao}"
    msg_link = "clique no link para recuperar a senha."
    # Envia o email de recuperação (idealmente, de forma assíncrona, por exemplo, com Celery)
    send_verification_email.delay(
        usuario.nome_completo,
        dados.link_recuperacao,
        usuario.email,
        msg_link,
    )

    return {"mensagem": f"Se o email existir, um link de recuperação foi enviado.{dados.link_recuperacao}",
            "token": f"{token_recuperacao}"
            }

redefinir_router = Router()
@redefinir_router.post("/redefinir-senha")
def redefinir_senha(request, dados: RedefinirSenhaSchema, token: str = None):
    """
    Redefine a senha do usuário após a recuperação.
    Espera um token de recuperação e a nova senha.
    """
    token = token
    nova_senha = dados.new_password
    if not token:
        return {"mensagem": "Token de recuperação não fornecido."}, 400

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id_usuario = payload.get("id_usuario")
    except jwt.ExpiredSignatureError:
        return {"mensagem": "O token de recuperação expirou."}
    except jwt.InvalidTokenError:
        return {"mensagem": "Token de recuperação inválido."}

    try:
        usuario = Usuario.objects.get(id=id_usuario)
    except Usuario.DoesNotExist:
        return {"mensagem": "Usuário não encontrado."}

    usuario.set_senha(nova_senha)
    usuario.save()

    return {"mensagem": "Senha redefinida com sucesso."}


# Endpoints CRUD para usuários
@usuario_router.get("/", response=list[UsuarioResponseSchema])
def listar_usuarios(request):
    #Lista todos os usuários
    return Usuario.objects.all()

@usuario_router.get("/{usuario_id}", response=UsuarioResponseSchema)
def obter_usuario(request, usuario_id: int):
    """Obtém um usuário específico pelo ID"""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return usuario


@usuario_router.post("/", response={200: dict, 400: dict})
def criar_usuario(request, data: CadastroUsuarioSchema):
    """Cria um novo usuário e envia e-mail de verificação"""

    # Verificar se o e-mail já existe
    if Usuario.objects.filter(email=data.email).exists():
        return 400, {"error": "E-mail já cadastrado"}

    # Criar usuário com senha criptografada
    usuario = Usuario.objects.create(
        nome_completo=data.nome_completo,
        email=data.email,
        telefone=data.telefone,
        senha=make_password(data.senha),  # Criptografar senha
        tipo=data.tipo
    )

    # Criar token de verificação
    verification = EmailVerification.objects.create(usuario=usuario, token=uuid.uuid4())

    # Criar link de verificação
    #verification_link = f"http://localhost:8000/api/usuario/verify-email/{verification.token}/"
    verification_link = f"https://api.v1.ourbiz:8000/api/usuario/verify-email/{verification.token}/"
    # Enviar e-mail de confirmação
    msg_link = "clique no link para confirmar seu e-mail"
# Chamar a função de envio assíncrono
    send_verification_email.delay(
        usuario.nome_completo,
        verification_link,
        usuario.email,
        msg_link,
    )

    return 200, {"message": "Cadastro realizado com sucesso! Verifique seu e-mail para confirmar a conta."}


@usuario_router.get("/verify-email/{token}/")
def verify_email(request, token: str):
    verification = get_object_or_404(EmailVerification, token=token)

    # Marcar usuário como verificado
    verification.usuario.is_verified = True
    verification.usuario.save()
    
    # Remover token após confirmação
    verification.delete()

    return {"message": "E-mail confirmado com sucesso!"}


@usuario_router.put("/{usuario_id}", response=UsuarioResponseSchema)
def atualizar_usuario(request, usuario_id: int, data: CadastroUsuarioSchema):
    """Atualiza um usuário existente"""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    for field, value in data.dict(exclude_unset=True).items():
        if field == "senha":  # Atualizar a senha apenas se fornecida
            value = make_password(value)
        setattr(usuario, field, value)
    usuario.save()
    return usuario


@usuario_router.delete("/{usuario_id}")
def deletar_usuario(request, usuario_id: int):
    """Deleta um usuário pelo ID"""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return {"success": f"Usuário {usuario_id} deletado com sucesso"}

#******************************* Fim de Usuários ************************************************

@usuario_router.post("/{usuario_id}/perfil", response={200: dict, 400: dict})
def criar_perfil_usuario(request, usuario_id: int, data: PerfilSchema):
    """Cria um novo perfil de usuário"""

    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if not usuario:
        return 400, {"error": "Usuário não encontrado"}

    # Criar perfil
    perfil = Perfil.objects.create(
        usuario=usuario,
        numero_nif=data.numero_nif,
        numero_inss=data.numero_inss,
    )

    return 200, {"message": "Cadastro realizado com sucesso! Verifique seu e-mail para confirmar a conta."}
