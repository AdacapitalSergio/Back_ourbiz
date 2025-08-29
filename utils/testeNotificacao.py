from ninja import Router
from .models import Servico, Plano, Beneficio
from .schemas import ServicoIn, ServicoOut, PlanoIn, PlanoOut, BeneficioIn, BeneficioOut
from django.shortcuts import get_object_or_404

router = Router()

# ---------------- SERVIÇOS ----------------
@router.post("/servicos", response=ServicoOut)
def create_servico(request, payload: ServicoIn):
    servico = Servico.objects.create(**payload.dict())
    return servico

@router.get("/servicos", response=list[ServicoOut])
def list_servicos(request):
    return Servico.objects.all()

@router.get("/servicos/{servico_id}", response=ServicoOut)
def get_servico(request, servico_id: int):
    return get_object_or_404(Servico, id=servico_id)

@router.put("/servicos/{servico_id}", response=ServicoOut)
def update_servico(request, servico_id: int, payload: ServicoIn):
    servico = get_object_or_404(Servico, id=servico_id)
    for attr, value in payload.dict().items():
        setattr(servico, attr, value)
    servico.save()
    return servico

@router.delete("/servicos/{servico_id}")
def delete_servico(request, servico_id: int):
    servico = get_object_or_404(Servico, id=servico_id)
    servico.delete()
    return {"success": True}


# ---------------- PLANOS ----------------
@router.post("/planos", response=PlanoOut)
def create_plano(request, payload: PlanoIn):
    plano = Plano.objects.create(**payload.dict())
    return plano

@router.get("/planos", response=list[PlanoOut])
def list_planos(request):
    return Plano.objects.all()

@router.get("/planos/{plano_id}", response=PlanoOut)
def get_plano(request, plano_id: int):
    return get_object_or_404(Plano, id=plano_id)

@router.put("/planos/{plano_id}", response=PlanoOut)
def update_plano(request, plano_id: int, payload: PlanoIn):
    plano = get_object_or_404(Plano, id=plano_id)
    for attr, value in payload.dict().items():
        setattr(plano, attr, value)
    plano.save()
    return plano

@router.delete("/planos/{plano_id}")
def delete_plano(request, plano_id: int):
    plano = get_object_or_404(Plano, id=plano_id)
    plano.delete()
    return {"success": True}


# ---------------- BENEFÍCIOS ----------------
@router.post("/beneficios", response=BeneficioOut)
def create_beneficio(request, payload: BeneficioIn):
    beneficio = Beneficio.objects.create(**payload.dict())
    return beneficio

@router.get("/beneficios", response=list[BeneficioOut])
def list_beneficios(request):
    return Beneficio.objects.all()

@router.get("/beneficios/{beneficio_id}", response=BeneficioOut)
def get_beneficio(request, beneficio_id: int):
    return get_object_or_404(Beneficio, id=beneficio_id)

@router.put("/beneficios/{beneficio_id}", response=BeneficioOut)
def update_beneficio(request, beneficio_id: int, payload: BeneficioIn):
    beneficio = get_object_or_404(Beneficio, id=beneficio_id)
    for attr, value in payload.dict().items():
        setattr(beneficio, attr, value)
    beneficio.save()
    return beneficio

@router.delete("/beneficios/{beneficio_id}")
def delete_beneficio(request, beneficio_id: int):
    beneficio = get_object_or_404(Beneficio, id=beneficio_id)
    beneficio.delete()
    return {"success": True}

#notificacao normal
from django.core.mail import send_mail
from .models import Notificacao

def solicitar_servico(usuario, servico):
    # salvar solicitação normalmente...

    # criar notificação in-app
    Notificacao.objects.create(
        usuario=servico.empresa.usuario,
        titulo="Novo pedido de serviço",
        mensagem=f"{usuario.nome} solicitou o serviço: {servico.nome}"
    )

    # enviar email
    send_mail(
        subject="Novo pedido de serviço",
        message=f"Olá, você tem um novo pedido de serviço de {usuario.nome}.",
        from_email="no-reply@suaempresa.com",
        recipient_list=[servico.empresa.email],
    )

from ninja import Router
from .models import Notificacao
from django.shortcuts import get_object_or_404

router = Router()

@router.get("/notificacoes")
def listar_notificacoes(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user).order_by("-criada_em")
    return [
        {
            "id": n.id,
            "titulo": n.titulo,
            "mensagem": n.mensagem,
            "lida": n.lida,
            "criada_em": n.criada_em,
        } for n in notificacoes
    ]

@router.post("/notificacoes/{notificacao_id}/ler")
def marcar_como_lida(request, notificacao_id: int):
    notificacao = get_object_or_404(Notificacao, id=notificacao_id, usuario=request.user)
    notificacao.lida = True
    notificacao.save()
    return {"success": True}





#settings.py:
INSTALLED_APPS = [
    ...
    "channels",
]

ASGI_APPLICATION = "meuprojeto.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("127.0.0.1", 6379)]},
    },
}
#model
from django.db import models
from django.conf import settings

class Notificacao(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notificacoes")
    titulo = models.CharField(max_length=255)
    mensagem = models.TextField()
    lida = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.titulo}"

#asgi
import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meuprojeto.settings")
django.setup()
application = get_default_application()


# #notificacoes/consumers.py:
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificacaoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass  # cliente não envia nada, só recebe

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["data"]))

#notificacoes/utils.py:
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.mail import send_mail
from .models import Notificacao

def enviar_notificacao(usuario, titulo, mensagem):
    # Salvar no banco
    notif = Notificacao.objects.create(
        usuario=usuario,
        titulo=titulo,
        mensagem=mensagem
    )

    # Enviar em tempo real (WebSocket)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{usuario.id}",
        {
            "type": "send_notification",
            "data": {"titulo": titulo, "mensagem": mensagem}
        }
    )

    # Enviar email (assíncrono se usar Celery)
    send_mail(
        subject=titulo,
        message=mensagem,
        from_email="no-reply@meuapp.com",
        recipient_list=[usuario.email],
        fail_silently=True,
    )

    return notif


#Exemplo de uso
from notificacoes.utils import enviar_notificacao

def solicitar_servico(usuario, servico):
    # lógica de criação da solicitação...
    enviar_notificacao(
        usuario,
        titulo="Nova solicitação de serviço",
        mensagem=f"Sua solicitação do serviço {servico.nome} foi registrada com sucesso."
    )
