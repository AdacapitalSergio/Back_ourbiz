from ninja import Schema
from typing import Optional
from pydantic import ConfigDict, EmailStr, Field

#, , ,, telefone, cliente_email

class PerfilSchema(Schema):
    numero_nif: str | None = Field(None, title="Número de Identificação Fiscal (NIF) do usuário")
    numero_inss: str | None = Field(None, title="Número de Segurança Social (INSS) do usuário")

    model_config = ConfigDict(from_attributes=True)

class UsuarioResponseSchema(Schema):
    nome_completo: str = Field(..., title="Nome do usuário")
    email: str = Field(..., title="Email do usuário")
    telefone: str | None = Field(None, title="Telefone do usuário")
    tipo: str = Field(..., title="Tipo de usuário", description="Tipo de usuário, ex: cliente ou funcionário", pattern=r"^(cliente|funcionario)$")
    perfil: PerfilSchema | None = Field(None, title="Perfil do usuário")

    model_config = ConfigDict(from_attributes=True)
    
class LoginSchema(Schema):
    email: str = Field(..., title="Email do usuário")
    senha: str = Field(..., title="Senha do usuário")

class ErrorSchema(Schema):
    error: str

class RedefinirSenhaSchema(Schema):
    nova_senha: str = Field(..., title="Nova senha do usuário")

class LinkEmailSchema(Schema):
    email: EmailStr = Field(..., title="Email do cliente")
    link: str


class CadastroUsuarioSchema(Schema):
    nome_completo: str = Field(..., title="Nome completo do usuário", min_length=2, max_length=100)
    email: EmailStr = Field(..., title="Email do usuário")
    telefone: str = Field(..., title="Telefone/WhatsApp do usuário", pattern=r"^\d{9,15}$")
    senha: str = Field(..., title="Senha do usuário", min_length=6, max_length=128)
    tipo: str = Field(..., title="Tipo de usuário", description="Tipo de usuário, ex: cliente ou funcionário", pattern=r"^(cliente|funcionario)$")
