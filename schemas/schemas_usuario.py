from ninja import Schema
from typing import List, Optional
from pydantic import ConfigDict, EmailStr, Field
from enum import Enum

class TipoUsuario(str, Enum):
    cliente = "cliente"
    funcionario = "funcionario"
class PerfilSchema(Schema):
    id: int
    nome: str
    sobrenome: str
    email: str
    contacto: Optional[str] = None
    contacto_whatsapp: Optional[str] = None


    model_config = ConfigDict(from_attributes=True)

class PerfilCreateSchema(Schema):
    nome: str
    sobrenome: str
    email: str
    contacto: Optional[str] = None
    contacto_whatsapp: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UsuarioSchema(Schema):
    nome_completo: str = Field(..., title="Nome do usuário")
    email: str = Field(..., title="Email do usuário")
    telefone: str | None = Field(None, title="Telefone do usuário")
    is_verified: bool


    model_config = ConfigDict(from_attributes=True)

class UsuarioCreateSchema(Schema):
    nome_completo: str = Field(..., title="Nome completo do usuário", min_length=2, max_length=100)
    email: EmailStr = Field(..., title="Email do usuário")
    telefone: str = Field(..., title="Telefone/WhatsApp do usuário", pattern=r"^\d{9,15}$")
    password: str = Field(..., title="Senha do usuário", min_length=6, max_length=128)
    logar_como: Optional[TipoUsuario] = Field( title=" cliente | funcionario")

class EnderecoSchema(Schema):
    rua: str
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    provincia: Optional[str] = None
    pais: Optional[str] = None
    codigo_postal: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class EmpresaSchema(Schema):
    id: int
    nome_empresa: str
    nif: Optional[str] = None
    email: str
    contacto: Optional[str] = None
    contacto_whatsapp: Optional[str] = None
    endereco: Optional[EnderecoSchema] = None  # ✅ Agora endereço vem separado

    model_config = ConfigDict(from_attributes=True)

class EmpresaCreateSchema(Schema):
    nome_empresa: str
    nif: Optional[str] = None
    email: str
    contacto: Optional[str] = None
    contacto_whatsapp: Optional[str] = None

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
        from_attributes=True


class PreferenciasCreateSchema(Schema):
    dados_faturacao: str
    email_principal: str
    contacto_sms: str

    
class EnderecoSchema(Schema):
    id: int
    rua: str
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    provincia: Optional[str] = None
    codigo_postal: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes=True


class EnderecoCreateSchema(Schema):
    rua: str
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    provincia: Optional[str] = None
    pais: Optional[str] = None
    codigo_postal: Optional[str] = None


class LoginSchema(Schema):
    email: str = Field(..., title="Email do usuário")
    password: str = Field(..., title="Senha do usuário")
     
    
class ErrorSchema(Schema):
    error: str

class RedefinirSenhaSchema(Schema):
    ne_password: str = Field(..., title="Nova senha do usuário")

class LinkEmailSchema(Schema):
    email: EmailStr = Field(..., title="Email do cliente")
    link: str


# -------------------- #
class EnderecoSchema(Schema):
    id: Optional[int] = None
    #tipo: Optional[str] = None
    rua: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    provincia: Optional[str] = None
    pais: Optional[str] = None
    codigo_postal: Optional[str] = None


class EmpresaSchema(Schema):
    id: Optional[int] = None
    nome_empresa: Optional[str] = None
    nif: Optional[str] = None
    email: Optional[str] = None
    contacto: Optional[str] = None
    contacto_whatsapp: Optional[str] = None
    #dono_empresa
    enderecosempresa: List[EnderecoSchema] = [EnderecoSchema()]  # já vem 1 molde


class UsuarioSchema(Schema):
    id: int
    nome_completo: str
    email: str
    telefone: Optional[str] = None
    is_verified: bool
    tipo_usuario: Optional[TipoUsuario] = Field( title=" cliente | funcionario")
    enderecospessoal: List[EnderecoSchema] = [EnderecoSchema()]  # já vem 1 molde
    empresas: List[EmpresaSchema] = [EmpresaSchema()]     # já vem 1 molde

# -------------------- #
# 
class UsuarioCreateSchema(Schema):
    nome_completo: str
    email: str
    telefone: str
    password: str
    is_verified: bool = False
    #logar_como: str  # cliente ou funcionario
    enderecos: Optional[List[EnderecoCreateSchema]] = None
    empresa: Optional[EmpresaCreateSchema] = None    