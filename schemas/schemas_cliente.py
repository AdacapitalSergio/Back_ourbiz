from ninja import Schema
from typing import Optional
from pydantic import EmailStr, Field

#, , ,, telefone, cliente_email
class ClienteSchema(Schema):
    numero_nif: str
    numero_inss: str
    email: str
    nome: str 
    senha: str | None
    telefone: str | None

class LoginSchema(Schema):
    email: str
    password: str

class ErrorSchema(Schema):
    error: str

class RedefinirSenhaSchema(Schema):
    new_password: str

class EmailSchema(Schema):
    email: str
    
    
class CadastroClienteSchema(Schema):
    nome: str = Field(..., title="Nome completo do cliente", min_length=2, max_length=100)
    email: EmailStr = Field(..., title="Email do cliente")
    telefone: str = Field(..., title="Telefone/WhatsApp do cliente", pattern=r"^\d{9,15}$")
    senha: str = Field(..., title="Senha do cliente", min_length=6, max_length=128)
