from ninja import Schema
from typing import Optional
from pydantic import ConfigDict, EmailStr, Field
from schemas.schemas_usuario import UsuarioSchema, EmpresaSchema

class FuncionarioSchema(Schema):
    id: int
    usuario: UsuarioSchema
    empresa: Optional[EmpresaSchema]
    cargo: Optional[str]

class FuncionarioCreateSchema(Schema):
    usuario_id: int
    empresa_id: Optional[int] = None
    cargo: Optional[str] = None

