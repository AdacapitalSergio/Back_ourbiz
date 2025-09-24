from ninja import Schema
from typing import Optional
from pydantic import ConfigDict, EmailStr
from schemas.schemas_usuario import UsuarioSchema, EmpresaSchema

#, , ,, telefone, cliente_email

class ClienteSchema(Schema):
    id: int
    usuario: UsuarioSchema
    empresa: Optional[EmpresaSchema]

class ClienteCreateSchema(Schema):
    usuario_id: int
    #empresa_id: Optional[int] = None  # opcional
