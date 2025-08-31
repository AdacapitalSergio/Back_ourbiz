from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from ninja.security import HttpBearer
from ninja import Router

from http.client import HTTPException
from datetime import datetime, timedelta
import jwt # type: ignore
import uuid



from utils.auth import SECRET_KEY
from utils.auth import auth
from utils.solicitacao_website_email import send_verification_email

from .models import EmailVerification, Empresa, EnderecoEmpresa, EnderecoPessoal, Preferencias, Usuario, Perfil
from schemas.schemas_usuario import( 
    EmpresaSchema, EnderecoCreateSchema, EnderecoSchema, PreferenciasCreateSchema, UsuarioCreateSchema, UsuarioSchema,
    EmpresaCreateSchema, PerfilSchema, LinkEmailSchema, LoginSchema, RedefinirSenhaSchema,
    LinkEmailSchema, LoginSchema, RedefinirSenhaSchema, LinkEmailSchema, LoginSchema, RedefinirSenhaSchema
    )


usuario_router = Router()
empresa_router = Router()
auth_router = Router()
redefinir_router = Router()

# -------------------------
# AUTENTICAÇÃO DE USUÁRIO
# -------------------------
@auth_router.post("/login", response=dict)
def login(request, data: LoginSchema):
    
    usuario = Usuario.objects.filter(email=data.email).first()
    #usuario = get_object_or_404(Usuario, id=usuario_id)
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
        "usuario": UsuarioSchema.model_validate(usuario).model_dump()
        }

# -------------------------
# RECUPERAR CONTA
# -------------------------
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

# -------------------------
# REDEFINIR SENHA
# -------------------------
@redefinir_router.post("/redefinir-senha")
def redefinir_senha(request, dados: RedefinirSenhaSchema, token: str = None):
    
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
    payload = {
        "user_id": usuario.id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION_MINUTES),
        "role": usuario.role if hasattr(usuario, "role") else "user"  # Exemplo de adição de permissão
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=settings.ALGORITHM)

    return {
        "access_token": token, 
        "token_type": "bearer", 
        "usuario": UsuarioSchema.model_validate(usuario).model_dump()
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
# ACTUALISAR USUÁRIO
# -------------------------
@usuario_router.put("/{usuario_id}", response=UsuarioSchema)
def atualizar_usuario(request, usuario_id: int, data: UsuarioCreateSchema):
    """Atualiza um usuário existente"""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    for field, value in data.dict(exclude_unset=True).items():
        if field == "senha":  # Atualizar a senha apenas se fornecida
            value = make_password(value)
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

# -------------------------
# PREFERÊNCIAS DE USUÁRIO
# -------------------------

@usuario_router.post("/{usuario_id}/preferencias", response={200: dict, 400: dict})
def criar_preferencias(request, usuario_id: int, data: PreferenciasCreateSchema):
    preferencias = Preferencias.objects.create(usuario_id=usuario_id, **data.dict())
    return 200, {"message": "Preferências criadas com sucesso!", "dados_preferencias": preferencias}


# -------------------------
# Endereco DE USUÁRIO
# -------------------------

@usuario_router.post("/{usuario_id}/enderecos", response=EnderecoSchema)
def criar_endereco(request, usuario_id: int, data: EnderecoCreateSchema):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if not usuario:
        return {"error": "Usuário não encontrado"}, 404
    endereco = EnderecoPessoal.objects.create(usuario_id=usuario_id, **data.dict())
    return endereco


# Listar endereços de uma empresa
@usuario_router.get("/{usuario_id}/enderecos", response=list[EnderecoSchema])
def listar_enderecos(request, usuario_id: int):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return usuario.enderecos.all()


# Buscar um endereço específico
@usuario_router.get("/enderecos/{endereco_id}", response=EnderecoSchema)
def detalhe_endereco(request, endereco_id: int):
    return get_object_or_404(EnderecoPessoal, id=endereco_id)


# Atualizar endereço
@usuario_router.put("/enderecos/{endereco_id}", response=EnderecoSchema)
def atualizar_endereco(request, endereco_id: int, data: EnderecoCreateSchema):
    endereco = get_object_or_404(EnderecoPessoal, id=endereco_id)
    for attr, value in data.dict().items():
        setattr(endereco, attr, value)
    endereco.save()
    return endereco


# Deletar endereço
@usuario_router.delete("/enderecos/{endereco_id}")
def deletar_endereco(request, endereco_id: int):
    endereco = get_object_or_404(EnderecoPessoal, id=endereco_id)
    endereco.delete()
    return {"success": True, "message": "Endereço removido com sucesso"}

# -------------------------
# EMPRESA DE USUÁRIO
# -------------------------
@empresa_router.post("/{usuario_id}/empresa", response={200: dict, 400: dict})
def criar_empresa_usuario(request, usuario_id: int, data: EmpresaCreateSchema):
    empresa = Empresa.objects.create(usuario_id=usuario_id, **data.dict())
    return 200, {"message": "Empresa criada com sucesso!", "dados_empresa": empresa}
    

@empresa_router.post("/{empresa_id}/enderecos", response=EnderecoSchema)
def criar_endereco_empresa(request, empresa_id: int, data: EnderecoCreateSchema):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    if not empresa:
        return {"error": "Empresa não encontrada"}, 404
    endereco = EnderecoEmpresa.objects.create(empresa=empresa, **data.dict())
    return endereco


# Listar endereços de uma empresa
@empresa_router.get("/{empresa_id}/enderecos", response=list[EnderecoSchema])
def listar_enderecos_empresa(request, empresa_id: int):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    return empresa.enderecos.all()


# Buscar um endereço específico
@empresa_router.get("/enderecos/{endereco_id}", response=EnderecoSchema)
def detalhe_endereco_empresa(request, endereco_id: int):
    return get_object_or_404(EnderecoEmpresa, id=endereco_id)


# Atualizar endereço
@empresa_router.put("/enderecos/{endereco_id}", response=EnderecoSchema)
def atualizar_endereco_empresa(request, endereco_id: int, data: EnderecoCreateSchema):
    endereco = get_object_or_404(EnderecoEmpresa, id=endereco_id)
    for attr, value in data.dict().items():
        setattr(endereco, attr, value)
    endereco.save()
    return endereco


# Deletar endereço
@empresa_router.delete("/enderecos/{endereco_id}")
def deletar_endereco_empresa(request, endereco_id: int):
    endereco = get_object_or_404(EnderecoEmpresa, id=endereco_id)
    endereco.delete()
    return {"success": True, "message": "Endereço removido com sucesso"}