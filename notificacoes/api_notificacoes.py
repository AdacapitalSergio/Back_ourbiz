from ninja import Router
from django.shortcuts import get_object_or_404
from utils.notificacoes import enviar_notificacao
from .models import Notificacao, Usuario
from schemas.schema_notificacoes import NotificacoesCreateSchema


notificacoes_router = Router()

@notificacoes_router.post("/{usuario_id}/notificar", response=dict)
def criar_notificacao(request, usuario_id: int, data: NotificacoesCreateSchema):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    # criar notificação in-app
    enviar_notificacao(
        usuario,
        titulo=data.titulo,
        mensagem=data.mensagem
    )

    return {"message": "notificacao criada com sucesso!"}

@notificacoes_router.get("/{usuario_id}/listar", response=dict)
def listar_notificacoes(request, usuario_id: int):
    notificacoes = Notificacao.objects.filter(id=usuario_id).order_by("-criada_em")
    """return [
        {
            "id": n.id,
            "titulo": n.titulo,
            "mensagem": n.mensagem,
            "lida": n.lida,
            "criada_em": n.criada_em,
        } for n in notificacoes
    ]"""
    return notificacoes

@notificacoes_router.post("/{notificacao_id}/ler", response=dict)
def marcar_como_lida(request, notificacao_id: int):
    notificacao = get_object_or_404(Notificacao, id=notificacao_id, usuario=request.user)
    notificacao.lida = True
    notificacao.save()

    return {"success": True}
