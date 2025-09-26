from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from ninja.security import HttpBearer
from ninja import Router

from http.client import HTTPException
from datetime import datetime, timedelta
import jwt # type: ignore
import uuid

from ninja.errors import HttpError

from cliente.models import Cliente
from funcionario.models import Funcionario
from utils.auth import SECRET_KEY

from utils.auth import auth
from utils.solicitacao_website_email import send_verification_email

from .models import EmailVerification, Empresa, Endereco, Preferencias, Usuario, Perfil

from schemas.schemas_usuario import( 
      
      EmpresaSchema, EnderecoCreateSchema, EnderecoSchema, PreferenciasCreateSchema,
      UsuarioCreateSchema, UsuarioSchema,EmpresaCreateSchema, PerfilSchema, LinkEmailSchema,
      LoginSchema, RedefinirSenhaSchema,LinkEmailSchema, LoginSchema, RedefinirSenhaSchema, 
      LinkEmailSchema, LoginSchema, RedefinirSenhaSchema
    
    )


usuario_router = Router()
empresa_router = Router()
endereco_router = Router()
auth_router = Router()
redefinir_router = Router()

# ------------------------#
# AUTENTICAÇÃO DE USUÁRIO #
# ------------------------#
@auth_router.post("/login", response=dict)
def login(request, payload: LoginSchema):
    usuario = get_object_or_404(Usuario, email=payload.email)

    # agora usa o método correto
    if not usuario.check_password(payload.senha):
        raise HttpError(401, "Credenciais inválidas")

    if not usuario.is_verified:   # <-- aqui estava invertido
        raise HttpError(401, "Conta não verificada, por favor verifique o teu email")

    payload_token = {
        "user_id": usuario.id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION_MINUTES),
    }
    token = jwt.encode(payload_token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": UsuarioSchema.model_validate(usuario).model_dump(),
    }

# -------------------------
# RECUPERAR CONTA
# -------------------------
@auth_router.post("/recuperacao-conta")
def recuperar_conta(request, payload: LinkEmailSchema):
    """
    Endpoint para iniciar o processo de recuperação de conta.
    Mesmo que o email não esteja cadastrado, a resposta é padronizada
    para evitar a enumeração de usuários.
    """
    usuario = Usuario.objects.filter(email=payload.email).first()
    if not usuario:
        # Retorna a mesma mensagem mesmo que o usuário não exista
        return {"mensagem": "Se o email existir, um link de recuperação foi enviado."}
    
    # Cria o payload para o token de recuperação
    payload_token = {
        "id_usuario": usuario.id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION_MINUTES)
    }
    token_recuperacao = jwt.encode(payload_token, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    #link_recuperacao = f"http://localhost:8000/api/clientes/redefinir-senha?token={token_recuperacao}"
    msg_link = "clique no link para recuperar a senha."
    # Envia o email de recuperação (idealmente, de forma assíncrona, por exemplo, com Celery)
    send_verification_email.delay(
        usuario.nome_completo,
        payload.link_recuperacao,
        usuario.email,
        msg_link,
    )

    return {
            "mensagem": f"Se o email existir, um link de recuperação foi enviado.{payload.link_recuperacao}",
            "token": f"{token_recuperacao}"
        }    

# -------------------------
# REDEFINIR SENHA
# -------------------------
@redefinir_router.post("/redefinir-senha")
def redefinir_senha(request, dados: RedefinirSenhaSchema, token: str = None):
    
    token = token
   
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
    usuario.set_password(dados.new_password)  # ✅ método correto
    usuario.save()

    return {"mensagem": "Senha redefinida com sucesso."}


# -------------------------
# LISTAR VARIOS USUÁRIO
# -------------------------
@usuario_router.get("/", response=list[UsuarioSchema])
def listar_usuarios(request):
    #Lista todos os usuários
    return Usuario.objects.all()
# -------------------------
# LISTAR UM USUÁRIO
# -------------------------
@usuario_router.get("/{usuario_id}", response=UsuarioSchema)
def obter_usuario(request, usuario_id: int):
    """Obtém um usuário específico pelo ID"""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return usuario

# -------------------------
# CRIAR USUÁRIO
# -------------------------
@usuario_router.post("/", response={200: dict, 400: dict})
def criar_usuario(request, data: UsuarioCreateSchema):
    """Cria um usuário base (sem empresa/endereços ainda)."""
    password = data.senha
    usuario = Usuario.objects.filter(email=data.email).first()
    if usuario:
        return 400, {"error": "Já existe um usuário com este e-mail"}

    usuario = Usuario.objects.create(
        nome_completo=data.nome_completo,
        telefone=data.telefone,
        email=data.email,
    )
    usuario.set_password(password)   # ✅ agora usa set_password

    # Definir role inicial
    if data.tipo_usuario == "cliente":
        Cliente.objects.create(usuario=usuario)
        usuario.is_cliente = True
    if data.tipo_usuario == "funcionario":
        Funcionario.objects.create(usuario=usuario)
        usuario.is_funcionario = True

    usuario.save()

    # Criar verificação de e-mail
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
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=settings.ALGORITHM)

    # Retorno no mesmo formato do login
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            **UsuarioSchema.model_validate(usuario).model_dump(),
            #"enderecos": [EnderecoSchema().model_dump()],   # molde de endereço
            #"empresas": [EmpresaSchema().model_dump()]      # molde de empresa
        },
    "logar_como": data.tipo_usuario
}


# -------------------------
# VERIFICAÇÃO DE E-MAIL
# -------------------------
@usuario_router.get("/verify-email/{token}/")
def verify_email(request, token: str):
    verification = get_object_or_404(EmailVerification, token=token)

    # Marcar usuário como verificado
    verification.usuario.is_verified = True
    verification.usuario.save()
    
    # Remover token após confirmação
    verification.delete()

    return {"message": "E-mail confirmado com sucesso!"}

# -------------------------
# ATUALIZAR USUÁRIO
# -------------------------
@usuario_router.put("/{usuario_id}", response=UsuarioSchema)
def atualizar_usuario(request, usuario_id: int, data: UsuarioCreateSchema):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    for field, value in data.dict(exclude_unset=True).items():
        if field == "password":  
            usuario.set_password(value)  # ✅ método correto
        else:
            setattr(usuario, field, value)
    usuario.save()
    return usuario


# -------------------------
#  DELETAR USUÁRIO
# -------------------------

@usuario_router.delete("/{usuario_id}")
def deletar_usuario(request, usuario_id: int):
    """Deleta um usuário pelo ID"""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return {"success": f"Usuário {usuario_id} deletado com sucesso"}

#******************************* Fim de Usuários ************************************************

# -------------------------
# PERFIL DE USUÁRIO
# -------------------------

@usuario_router.post("/{usuario_id}/perfil", response={200: dict, 400: dict})
def criar_perfil_usuario(request, usuario_id: int, data: PerfilSchema):
    perfil = Perfil.objects.create(usuario_id=usuario_id, **data.dict())
    return 200, {"message": "Perfil criado com sucesso!", "dados_pessoais": perfil}

#******************************* Fim de Perfil ************************************************

# -------------------------
# PREFERÊNCIAS DE USUÁRIO
# -------------------------

@usuario_router.post("/{usuario_id}/preferencias", response={200: dict, 400: dict})
def criar_preferencias(request, usuario_id: int, data: PreferenciasCreateSchema):
    preferencias = Preferencias.objects.create(usuario_id=usuario_id, **data.dict())
    return 200, {"message": "Preferências criadas com sucesso!", "dados_preferencias": preferencias}

#******************************* Fim de Preferências ************************************************

#-------------------------
# Endereco DE USUÁRIO    :
#-------------------------

# Criar endereço (pessoal ou empresarial)
@endereco_router.post("/{usuario_id}/pessoal", response=EnderecoSchema)
def criar_endereco_pessoal(request, usuario_id: int, data: EnderecoCreateSchema):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    endereco = Endereco.objects.create(usuario=usuario, **data.dict())
    return endereco

@endereco_router.post("/enderecos/{empresa_id}/empresa", response=EnderecoSchema)
def criar_endereco_empresa(request, empresa_id: int, data: EnderecoCreateSchema):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    endereco = Endereco.objects.create(empresa=empresa, **data.dict())
    return endereco

# Listar endereços de um usuário
@endereco_router.get("/{usuario_id}/enderecos", response=list[EnderecoSchema])
def listar_enderecos(request, usuario_id: int):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return usuario.enderecos.all()


# Buscar um endereço específico
@endereco_router.get("/enderecos/{endereco_id}", response=EnderecoSchema)
def detalhe_endereco(request, endereco_id: int):
    return get_object_or_404(Endereco, id=endereco_id)


# Atualizar endereço
@endereco_router.put("/enderecos/{endereco_id}", response=EnderecoSchema)
def atualizar_endereco(request, endereco_id: int, data: EnderecoCreateSchema):
    endereco = get_object_or_404(Endereco, id=endereco_id)
    for attr, value in data.dict().items():
        setattr(endereco, attr, value)
    endereco.save()
    return endereco


# Deletar endereço
@endereco_router.delete("/enderecos/{endereco_id}")
def deletar_endereco(request, endereco_id: int):
    endereco = get_object_or_404(Endereco, id=endereco_id)
    endereco.delete()
    return {"success": True, "message": "Endereço removido com sucesso"}

    
#******************************* Fim de Endereços ************************************************

# ------------------------
# Empresa DE USUÁRIO     :
# ------------------------

# Criar empresa para um usuário (dono)
@empresa_router.post("/{usuario_id}/", response=EmpresaSchema)
def criar_empresa_usuario(request, usuario_id: int, data: EmpresaCreateSchema):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    empresa = Empresa.objects.create(dono_empresa=usuario, **data.dict())
    return empresa


# Listar empresas de um usuário
@empresa_router.get("/{usuario_id}/", response=list[EmpresaSchema])
def listar_empresas_usuario(request, usuario_id: int):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return usuario.empresas.all()


# Buscar uma empresa específica
@empresa_router.get("/{empresa_id}", response=EmpresaSchema)
def detalhe_empresa(request, empresa_id: int):
    return get_object_or_404(Empresa, id=empresa_id)


# Atualizar empresa
@empresa_router.put("/{empresa_id}", response=EmpresaSchema)
def atualizar_empresa(request, empresa_id: int, data: EmpresaCreateSchema):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    for attr, value in data.dict().items():
        setattr(empresa, attr, value)
    empresa.save()
    return empresa


# Deletar empresa
@empresa_router.delete("/{empresa_id}")
def deletar_empresa(request, empresa_id: int):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    empresa.delete()
    return {"success": True, "message": "Empresa removida com sucesso"}

#******************************* Fim de Empresas ************************************************