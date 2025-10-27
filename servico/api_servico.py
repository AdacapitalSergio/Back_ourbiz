from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Servico, Plano, Beneficio
from schemas.schema_servicos import (
    ServicoSchema, ServicoCreateSchema,
    PlanoSchema, PlanoCreateSchema,
    BeneficioSchema, BeneficioCreateSchema
)

router_servicos = Router()

# ----------------- SERVIÇOS -----------------
@router_servicos.get("/servicos", response=list[ServicoSchema])
def listar_servicos(request):
   servico = list(Servico.objects.all())
   #return   { "servicos": ServicoSchema.model_validate(servico).model_dump(),}
   return servico
 
"""
@router_servicos.post("/servicos", response=ServicoSchema)
def criar_servico(request, data: ServicoCreateSchema):
    servico = Servico.objects.create(**data.dict())
    return servico
"""
# ----------------- PLANOS -----------------
@router_servicos.get("/planos", response=list[PlanoSchema])
def listar_planos(request):
    planos = list(Plano.objects.all())
    return planos
"""
@router_servicos.post("/planos", response=PlanoSchema)
def criar_plano(request, data: PlanoCreateSchema):
    plano = Plano.objects.create(
        titulo=data.titulo,
        descricao=data.descricao,
        preco_mensal=data.preco_mensal
    ) 
    plano.servicos.set(data.servicos)
    return {
        "id": plano.id,
        "titulo": plano.titulo,
        "descricao": plano.descricao,
        "preco_mensal": float(plano.preco_mensal),
        "servicos": [s.id for s in plano.servicos.all()]
    }
"""
# ----------------- BENEFÍCIOS -----------------
@router_servicos.get("/beneficios", response=list[BeneficioSchema])
def listar_beneficios(request):
    beneficios = Beneficio.objects.all()
    return [
        {
            "id": b.id,
            "descricao": b.descricao,
            "titulo": b.titulo,
            "plano": b.plano.id,
        }
        for b in beneficios
    ]
"""
@router_servicos.post("/beneficios", response=BeneficioSchema)
def criar_beneficio(request, data: BeneficioCreateSchema):
    plano = get_object_or_404(Plano, id=data.plano)
    beneficio = Beneficio.objects.create(
        titulo=data.titulo,
        descricao=data.descricao,
        plano=plano
    )
    return beneficio
"""