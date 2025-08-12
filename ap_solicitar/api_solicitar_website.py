from django.shortcuts import get_object_or_404
from ninja import Router

from .models import WebsiteRequest, Objetivo
from schemas.schemas_servico import RequisitarConversationSchema, RequisitarServicoSchema
from utils.solicitacao_website_email import send_conversation_for_operation_email, send_website_request_email

# Routers
solicitar_router = Router()

@solicitar_router.post("/", response={200: dict, 400: dict})
def solicitar_servicos_website(request, data: RequisitarServicoSchema):   
    """solicitar_servicos: Rota para solicitar serviços de criação de sites."""
    # Verificar se o usuário está autenticado
    """if not request.auth:
        return 400, {"message": "Usuário não autenticado."}"""
    # Chamar a função de envio assíncrono
    website_request = WebsiteRequest.objects.create(
        nome_requerente=data.seuNome,
        email_requerente=data.seuEmail,
        telefone_requerente=data.seuTelefone,
        tem_dominio=data.temDominio.value if data.temDominio else None,
        dominio=data.dominio,
        tem_logotipo=data.temLogotipo.value if data.temLogotipo else None,
        sobre_empresa=data.sobreEmpresa,
        integracoes=data.integracoesSite,
        site_referencia=data.referenciasSite,
        metodo_contato=data.metodoContato,
        commentarios=data.comentariosAdicionais
    )

    # Atribui o ManyToMany com .set(), convertendo os Enums para objetos reais
    
    # Relacionar objetivos
    objetivos = []
    print(data.objetivoSite)
    if data.objetivoSite:
        for item in data.objetivoSite:
            obj, _ = Objetivo.objects.get_or_create(nome=item.value)
            objetivos.append(obj)

    if data.outroObjetivo and data.outroObjetivo.lower() != "string":
        outro_obj, _ = Objetivo.objects.get_or_create(nome=data.outroObjetivo.strip())
        objetivos.append(outro_obj)


    if objetivos:
        website_request.objetivo_site.set(objetivos)
    # Pega todos os nomes do objetivo e junta em uma string
    objetivo_site_formatado = ", ".join(
        [obj.nome for obj in website_request.objetivo_site.all()]
    )
    send_website_request_email.delay(
        nome_requerente=data.seuNome,
        email_requerente=data.seuEmail,
        telefone_requerente=data.seuTelefone,
        objetivo_site=objetivo_site_formatado,
        tem_dominio=data.temDominio,
        dominio=data.dominio,
        tem_logotipo=data.temLogotipo,
        sobre_empresa=data.sobreEmpresa,
        integracoes=data.integracoesSite,
        site_referencia=data.referenciasSite,
        metodo_contato=data.metodoContato,
        commentarios=data.comentariosAdicionais,
    )   
    return 200, {"message": "Servico requisitado com sucesso por favor aguarde pelo nosso contacto."}


@solicitar_router.post("/cotacto", response={200: dict, 400: dict})
def solicitar_conversation_for_operation(request, data: RequisitarConversationSchema):   
    """solicitar_servicos: Rota para solicitar serviços de criação de sites."""
    # Verificar se o usuário está autenticado
    """if not request.auth:
        return 400, {"message": "Usuário não autenticado."}"""
    # Chamar a função de envio assíncrono  
    if data.contacto:
        send_conversation_for_operation_email.delay(
        contacto_requerente=data.contacto, sms_requerente=data.mensagen,
        )
     
    return 200, {"message": "Contacto enviado com sucesso."}
