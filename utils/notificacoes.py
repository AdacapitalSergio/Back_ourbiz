from notificacoes.models import Notificacao

def enviar_notificacao(id: int, titulo: str, mensagem: str):
    notificacao = Notificacao.objects.create(
        titulo=titulo,
        mensagem = mensagem
    )
    return notificacao
    