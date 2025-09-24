from ninja import Schema
from typing import Optional
from pydantic import ConfigDict, EmailStr, Field
from schemas.schemas_usuario import EnderecoSchema, UsuarioSchema, EmpresaSchema

class FuncionarioSchema(Schema):
    id: int
    usuario: UsuarioSchema
    empresa: Optional[EmpresaSchema]
    #endereco: Optional[EnderecoSchema]
    cargo: Optional[str]
    departamento: Optional[str] = None
    matricula: Optional[str] = None


class FuncionarioCreateSchema(Schema):
    usuario_id: int
    empresa_id: Optional[int] = None
    cargo: Optional[str] = None
    departamento: Optional[str] = None
    matricula: Optional[str] = None
