from ninja import Schema
from typing import Optional
from pydantic import ConfigDict, EmailStr, Field

class PerfilSchema(Schema):
    id: int
    nome: str
    sobrenome: str
    email: str
    contacto: Optional[str] = None
    contacto_whatsapp: Optional[str] = None
    localidade: Optional[str] = None
    cidade: Optional[str] = None
    pais: Optional[str] = None
    endereco1: Optional[str] = None
    endereco2: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PerfilCreateSchema(Schema):
    nome: str
    sobrenome: str
    email: str
    contacto: Optional[str] = None
    contacto_whatsapp: Optional[str] = None
    localidade: Optional[str] = None
    cidade: Optional[str] = None
    pais: Optional[str] = None
    endereco1: Optional[str] = None
    endereco2: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UsuarioSchema(Schema):
    nome_completo: str = Field(..., title="Nome do usuário")
    email: str = Field(..., title="Email do usuário")
    telefone: str | None = Field(None, title="Telefone do usuário")
    tipo: str = Field(..., title="Tipo de usuário", description="Tipo de usuário, ex: cliente ou funcionário", pattern=r"^(cliente|funcionario)$")

    model_config = ConfigDict(from_attributes=True)

class UsuarioCreateSchema(Schema):
    nome_completo: str = Field(..., title="Nome completo do usuário", min_length=2, max_length=100)
    email: EmailStr = Field(..., title="Email do usuário")
    telefone: str = Field(..., title="Telefone/WhatsApp do usuário", pattern=r"^\d{9,15}$")
    senha: str = Field(..., title="Senha do usuário", min_length=6, max_length=128)
    tipo: str = Field(..., title="Tipo de usuário", description="Tipo de usuário, ex: cliente ou funcionário", pattern=r"^(cliente|funcionario)$")


class EmpresaSchema(Schema):
    id: int
    nome_empresa: str
    nif: Optional[str] = None
    email: str
    contacto: Optional[str] = None
    contacto_whatsapp: Optional[str] = None
    localidade: Optional[str] = None
    cidade: Optional[str] = None
    pais: Optional[str] = None
    endereco1: Optional[str] = None
    endereco2: Optional[str] = None

    class Config:
        orm_mode = True



class EmpresaCreateSchema(Schema):
    nome_empresa: str
    nif: Optional[str] = None
    email: str
    contacto: Optional[str] = None
    contacto_whatsapp: Optional[str] = None
    localidade: Optional[str] = None
    cidade: Optional[str] = None
    pais: Optional[str] = None
    endereco1: Optional[str] = None
    endereco2: Optional[str] = None

# --------------------
# Preferencias
# --------------------
class PreferenciasSchema(Schema):
    id: int
    dados_faturacao: str
    email_principal: str
    contacto_sms: str

    class Config:
        orm_mode = True


class PreferenciasCreateSchema(Schema):
    dados_faturacao: str
    email_principal: str
    contacto_sms: str

    
class EnderecoSchema(Schema):
    id: int
    rua: str
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    provincia: Optional[str] = None
    codigo_postal: Optional[str] = None

    class Config:
        orm_mode = True


class EnderecoCreateSchema(Schema):
    rua: str
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    provincia: Optional[str] = None
    codigo_postal: Optional[str] = None


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
