from ninja import Schema
from typing import List, Optional
from pydantic import Field, ConfigDict



# ---------- BENEFÍCIOS ----------
class BeneficioCreateSchema(Schema):
    titulo: str
    descricao: str
    #plano: int

class BeneficioSchema(Schema):
    id: Optional[int] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
   # plano: int   # chave estrangeira como ID (ou podes aninhar outro schema)

    class Config:
        from_attributes = True
# ---------- PLANOS ----------
class PlanoCreateSchema(Schema):
    titulo: str
    descricao: str
    preco_mensal: float
    #servicos: List[int]

class PlanoSchema(Schema):
    id: Optional[int] = None
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    preco_mensal: Optional[float] = None
    beneficios: List[BeneficioSchema] = Field(default_factory=list)

    class Config:
        from_attributes = True

# ---------- SERVIÇOS ----------

class ServicoCreateSchema(Schema):
    nome: str
    descricao: str
    preco: float


class ServicoSchema(Schema):
    id: int
    nome: str
    descricao: str
    preco: float
    planos: List[PlanoSchema] = Field(default_factory=list)
    class Config:   
        from_attributes = True
