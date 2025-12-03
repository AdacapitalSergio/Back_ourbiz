from django.shortcuts import get_object_or_404
from ninja import Router

from django.shortcuts import render

from servico.models import Plano, Servico
from schemas.codernadas_bancarias import CordenadasBancariasSchema
from dateutil.relativedelta import relativedelta 

from .models import CordenadasBancarias

cordenadas_bancarias_router = Router()

@cordenadas_bancarias_router.get("/listar", response={200: list[CordenadasBancariasSchema]})
def listar_cordenadas_bancarias(request):
    cordenadas = CordenadasBancarias.objects.all()
    return [CordenadasBancariasSchema.from_orm(c) for c in cordenadas]  