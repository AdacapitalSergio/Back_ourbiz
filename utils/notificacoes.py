from notificacoes.models import Notificacao

def enviar_notificacao(id: int, titulo: str, mensagem: str):
    notificacao = Notificacao.objects.create(
        usuario_id = id,
        titulo=titulo,
        mensagem = mensagem
    )
    return notificacao
    