from ninja import Schema
from typing import List, Optional

# ---------- SERVIÇOS ----------
class ServicoSchema(Schema):
    id: int
    nome: str
    descricao: str
    preco: float

class ServicoCreateSchema(Schema):
    nome: str
    descricao: str
    preco: float

# ---------- PLANOS ----------
class PlanoSchema(Schema):
    id: int
    titulo: str
    descricao: str
    preco_mensal: float
    servicos: List[int]  # lista de IDs dos serviços

class PlanoCreateSchema(Schema):
    titulo: str
    descricao: str
    preco_mensal: float
    servicos: List[int]

# ---------- BENEFÍCIOS ----------
class BeneficioSchema(Schema):
    id: int
    titulo: str
    descricao: str
    plano: int   # chave estrangeira como ID (ou podes aninhar outro schema)

    class Config:
        from_attributes = True

class BeneficioCreateSchema(Schema):
    titulo: str
    descricao: str
    plano: int
