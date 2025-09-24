from ninja import Schema
from typing import Optional
from pydantic import ConfigDict

class NotificacoesSchema(Schema):
    id: int
    titulo: str
    mensagem: str

    model_config = ConfigDict(from_attributes=True)

class NotificacoesCreateSchema(Schema):
    titulo: str
    mensagem: str
    lida: bool = False
    
    model_config = ConfigDict(from_attributes=True)
