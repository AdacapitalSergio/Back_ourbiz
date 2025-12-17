from django.shortcuts import get_object_or_404
from ninja import Router

from django.shortcuts import render

from schemas.schema_plano_negocio import PlanoNegocioInput, PlanoNegocioResponse, SugestaoSchema


from .models import WebsiteRequest, Objetivo
from schemas.schemas_servico import RequisitarConversationSchema, RequisitarServicoSchema
from utils.solicitacao_website_email import send_conversation_for_operation_email, send_website_request_email
from utils.gemini import gerar_conteudo_secoes, sugerir_ideias

from celery.result import AsyncResult

from datetime import timedelta
from .models import SolicitacaoServico, Cliente,  Funcionario
from servico.models import Plano, Servico
from schemas.schemas_servico import SchemaSolicitacaoServico, SchemaSolicitacaoServicoCreate
from datetime import date
from dateutil.relativedelta import relativedelta

from schemas.schemas_servico import RequisitarServicoConsultoriaSchema
from utils.solicitacao_servico_consultoria import send_consultoria_request_email




solicitar_router = Router()
contacto_router = Router()

@solicitar_router.post("/website", response={200: dict, 400: dict})
def solicitar_servicos_website(request, data: RequisitarServicoSchema):   
    
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

@contacto_router.post("/", response={200: dict, 400: dict})
def solicitar_conversation_for_operation(request, data: RequisitarConversationSchema):   
   
    if data.contacto:
        send_conversation_for_operation_email.delay(
        contacto_requerente=data.contacto, sms_requerente=data.mensagen,
        )
     
    return 200, {"message": "Contacto enviado com sucesso."}


@solicitar_router.post("/solicitacoes/", response=SchemaSolicitacaoServico)
def criar_solicitacao(request, payload: SchemaSolicitacaoServicoCreate):
    cliente = get_object_or_404(Cliente, id=payload.cliente_id)
    servico = get_object_or_404(Servico, id=payload.servico_id)
    #print(cliente)
    print(servico)
    funcionario = None
    plano = None
    if payload.funcionario_id:
        funcionario = get_object_or_404(Funcionario, id=payload.funcionario_id)
        print(funcionario)

    if payload.plano_id:
        plano = get_object_or_404(Plano, id=payload.plano_id)
        #print(plano)    

    data_inicio = date.today()
    data_final = data_inicio + relativedelta(months=payload.duracao_meses)
    solicitacao = SolicitacaoServico.objects.create(
        cliente=cliente,
        funcionario=funcionario,
        servico=servico,
        plano=plano,
        tipo_servico=payload.tipo_servico,
        valor=payload.valor,
        status=payload.status,
        duracao_meses=payload.duracao_meses,
        data_inicio = data_inicio,
        data_final=data_final,
        descricao=payload.descricao,
        #factura=payload.factura,
        #tem_factura=payload.tem_factura
    )
    return solicitacao


# Listar todas solicitações
@solicitar_router.get("/solicitacoes/", response=list[SchemaSolicitacaoServico])
def listar_solicitacoes(request):
    return SolicitacaoServico.objects.all()


# Obter uma solicitação específica
@solicitar_router.get("/solicitacoes/{solicitacao_id}", response=SchemaSolicitacaoServico)
def obter_solicitacao(request, solicitacao_id: int):
    return get_object_or_404(SolicitacaoServico, id=solicitacao_id)


# Atualizar status ou outros campos
@solicitar_router.put("/solicitacoes/{solicitacao_id}", response=SchemaSolicitacaoServico)
def atualizar_solicitacao(request, solicitacao_id: int, payload: SchemaSolicitacaoServicoCreate):
    solicitacao = get_object_or_404(SolicitacaoServico, id=solicitacao_id)

    for attr, value in payload.dict().items():
        setattr(solicitacao, attr, value)

    solicitacao.data_final = solicitacao.data_inicio + relativedelta(months=payload.duracao_meses)
    solicitacao.save()
    return solicitacao

# Actualizar status d  uma solicitação
@solicitar_router.put("/alterarStatus/{solicitacao_id}/{funcionario_id}", response=SchemaSolicitacaoServico)
def atualizar_status_solicitacao(request, solicitacao_id: int, funcionario_id: int, status: str):
    solicitacao = get_object_or_404(SolicitacaoServico, id=solicitacao_id)
    funcionario = get_object_or_404(Funcionario, id=funcionario_id)
    print(solicitacao.cliente)
    solicitacao.status = status
    solicitacao.funcionario = funcionario
    solicitacao.save()
    
    return solicitacao

# Deletar uma solicitação
@solicitar_router.delete("/solicitacoes/{solicitacao_id}")
def deletar_solicitacao(request, solicitacao_id: int):
    solicitacao = get_object_or_404(SolicitacaoServico, id=solicitacao_id)
    solicitacao.delete()
    return {"success": True, "message": "Solicitação removida com sucesso"}

@solicitar_router.post("/consultoria", response={200: dict, 400: dict})
def solicitar_servicos_consultoria(request, data: RequisitarServicoConsultoriaSchema):
    """
    Recebe pedido de consultoria e envia e-mail de notificação
    """

    # Envio assíncrono do e-mail
    send_consultoria_request_email.delay(
        cliente_nome=data.nome_completo,
        servico=data.servico_desejado,
        provincia=data.provincia,
        municipio=data.municipio,
        area_atuacao=data.area_atuacao,
        telefone=data.telefone,
        cliente_email=data.email,
        forma_contacto=data.forma_contacto
    )

    return 200, {
        "message": "Serviço requisitado com sucesso. Em breve entraremos em contacto consigo."
    }
