from django.conf import settings 
from ninja import Router
from .models import  Funcionario
from usuario.models import Usuario
from schemas.schemas_funcionario import FuncionarioCreateSchema, FuncionarioSchema, EmpresaSchema
from django.shortcuts import get_object_or_404

funcionario_router = Router()

@funcionario_router.post("/{usuario_id}/funcionario", response={200: dict, 400: dict})
def criar_funcionario(request, usuario_id: int, data: FuncionarioCreateSchema):
    usuario = get_object_or_404(Usuario, id=usuario_id)

    if hasattr(usuario, "funcionario"):
        return 400, {"error": "Este usuário já é funcionário"}
    
    funcionario = Funcionario.objects.create(
        usuario=usuario,
        cargo=data.cargo,
        departamento=data.departamento,
        matricula=data.matricula
    )

    return 200, {
        "message": "Funcionário criado com sucesso", 
        "usuario": funcionario.usuario,
        "funcionario_id": funcionario.id
        }


