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
from .models import Cliente, EmailVerification
import uuid
from schemas.schemas_cliente import ClienteSchema, EmailSchema, LoginSchema, RedefinirSenhaSchema

# Routers
cliente_router = Router()
auth_router = Router()


# Endpoints de autenticação
@auth_router.post("/login")
def login(request, data: LoginSchema):
    #Realiza o login e retorna um token JWT
    cliente = Cliente.objects.filter(email=data.email).first()
    
    if not cliente or not cliente.check_senha(data.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
 
    payload = {
        "user_id": cliente.id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION_MINUTES),
        "role": cliente.role if hasattr(cliente, "role") else "user"  # Exemplo de adição de permissão
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=settings.ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}


@auth_router.post("/recuperacao-conta")
def recuperar_conta(request, dados: EmailSchema):
    """
    Endpoint para iniciar o processo de recuperação de conta.
    Mesmo que o email não esteja cadastrado, a resposta é padronizada
    para evitar a enumeração de usuários.
    """
    cliente = Cliente.objects.filter(email=dados.email).first()
    if not cliente:
        # Retorna a mesma mensagem mesmo que o usuário não exista
        return {"mensagem": "Se o email existir, um link de recuperação foi enviado."}
    
    # Cria o payload para o token de recuperação
    payload = {
        "id_usuario": cliente.id,
        "exp": datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRATION_MINUTES)
    }
    token_recuperacao = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # Define o link para redefinição de senha (ajuste a URL conforme seu frontend)
    link_recuperacao = f"http://localhost:8000/api/clientes/redefinir-senha?token={token_recuperacao}"
    msg_link = "clique no link para recuperar a senha."
    # Envia o email de recuperação (idealmente, de forma assíncrona, por exemplo, com Celery)
    send_verification_email.delay(
        cliente.nome,
        link_recuperacao,
        cliente.email,
        msg_link,
    )
    
    return {"mensagem": f"Se o email existir, um link de recuperação foi enviado.{link_recuperacao}"}

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
        cliente = Cliente.objects.get(id=id_usuario)
    except Cliente.DoesNotExist:
        return {"mensagem": "Usuário não encontrado."}

    cliente.set_senha(nova_senha)
    cliente.save()

    return {"mensagem": "Senha redefinida com sucesso."}


# Endpoints CRUD para clientes
@cliente_router.get("/", response=list[ClienteSchema])
def listar_clientes(request):
    #Lista todos os clientes
    return Cliente.objects.all()

@cliente_router.get("/{cliente_id}", response=ClienteSchema)
def obter_cliente(request, cliente_id: int):
    """Obtém um cliente específico pelo ID"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return cliente


@cliente_router.post("/", response={200: dict, 400: dict})
def criar_cliente(request, data: ClienteSchema):
    """Cria um novo cliente e envia e-mail de verificação"""

    # Verificar se o e-mail já existe
    if Cliente.objects.filter(email=data.email).exists():
        return 400, {"error": "E-mail já cadastrado"}

    # Criar cliente com senha criptografada
    cliente = Cliente.objects.create(
        email=data.email,
        nome=data.nome,
        telefone=data.telefone,
        senha=make_password(data.senha),  # Criptografar senha
    )

    # Criar token de verificação
    verification = EmailVerification.objects.create(cliente=cliente, token=uuid.uuid4())

    # Criar link de verificação
    verification_link = f"http://localhost:8000/api/clientes/verify-email/{verification.token}/"

    # Enviar e-mail de confirmação
    msg_link = "clique no link para confirmar seu e-mail"
# Chamar a função de envio assíncrono
    send_verification_email.delay(
        cliente.nome,
        verification_link,
        cliente.email,
        msg_link,
    )

    return 200, {"message": "Cadastro realizado com sucesso! Verifique seu e-mail para confirmar a conta."}


@cliente_router.get("/verify-email/{token}/")
def verify_email(request, token: str):
    verification = get_object_or_404(EmailVerification, token=token)
    
    # Marcar cliente como verificado
    verification.cliente.is_verified = True
    verification.cliente.save()
    
    # Remover token após confirmação
    verification.delete()

    return {"message": "E-mail confirmado com sucesso!"}


@cliente_router.put("/{cliente_id}", response=ClienteSchema)
def atualizar_cliente(request, cliente_id: int, data: ClienteSchema):
    """Atualiza um cliente existente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    for field, value in data.dict(exclude_unset=True).items():
        if field == "senha":  # Atualizar a senha apenas se fornecida
            value = make_password(value)
        setattr(cliente, field, value)
    cliente.save()
    return cliente


@cliente_router.delete("/{cliente_id}")
def deletar_cliente(request, cliente_id: int):
    """Deleta um cliente pelo ID"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    cliente.delete()
    return {"success": f"Cliente {cliente_id} deletado com sucesso"}
    
#******************************* Fim de Clientes ************************************************
