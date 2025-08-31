from django.shortcuts import get_object_or_404
from ninja import Router

from schemas.schema_plano_negocio import PlanoNegocioInput, PlanoNegocioResponse


from .models import WebsiteRequest, Objetivo
from schemas.schemas_servico import RequisitarConversationSchema, RequisitarServicoSchema
from utils.solicitacao_website_email import send_conversation_for_operation_email, send_website_request_email
from utils.gemini import gerar_conteudo_secoes


from datetime import timedelta
from .models import SolicitacaoServico, Cliente, Servico, Funcionario
from schemas.schemas_servico import SolicitacaoServico, SolicitacaoServicoCreate
from datetime import date
from dateutil.relativedelta import relativedelta  # para somar meses



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




@solicitar_router.post("/gerar_plano_negocio", response=dict)
def gerar_plano(request, data: PlanoNegocioInput):
    dados_empresa = f"Tipo de negócio: {data.tipo_de_negocio}, Localização: {data.localizacao}"
    secoes = gerar_conteudo_secoes(dados_empresa)
    print(secoes["pesquisa_de_mercado"])
    print(secoes["produtos_servicos"])
    print(secoes["vendas_marketing"])
    print(secoes["operacoes"])
    print(secoes["financeiro"])
    print(secoes["gestao"])
    # 🚨 Aqui ainda será necessário transformar o texto retornado pelo Gemini
    # em listas e dicionários (ex: SWOT, projeções etc.)
    # Por agora, retorna tudo como strings simplificadas.
    """
    return {
        "visao_geral": {
            "resumo_executivo": secoes["visao_geral"],
            "analise_swot": {
                "forcas": ["A definir pela IA"],
                "fraquezas": ["A definir pela IA"],
                "oportunidades": ["A definir pela IA"],
                "ameacas": ["A definir pela IA"],
            },
            "modelos_de_negocio": "Gerado pela IA",
            "analise_viabilidade": "Gerado pela IA"
        },
        "pesquisa_de_mercado": {
            "industria": data.tipo_de_negocio,
            "visao_geral_industria": {
                "participacao_mercado": "Gerado pela IA",
                "penetracao_internet": "Gerado pela IA",
                "volume_ecommerce": "Gerado pela IA"
            },
            "publico_alvo": "Gerado pela IA",
            "tamanho_mercado_tendencias": {"info": "Gerado pela IA"},
            "analise_concorrente": ["Gerado pela IA"]
        },
        "produtos_servicos": {
            "ofertas_centrais": ["Gerado pela IA"],
            "oportunidades_expansao": ["Gerado pela IA"],
            "ofertas_secundarias": ["Gerado pela IA"],
            "atendimento_cliente": "Gerado pela IA"
        },
        "vendas_marketing": {
            "estrategia_marketing": "Gerado pela IA",
            "canais_distribuicao": ["Gerado pela IA"],
            "precificacao": "Gerado pela IA",
            "metodos_pagamento": ["Gerado pela IA"]
        },
        "operacoes": {
            "infraestrutura": "Gerado pela IA",
            "logistica": "Gerado pela IA",
            "parcerias": ["Gerado pela IA"],
            "tecnologia": "Gerado pela IA"
        },
        "financeiro": {
            "investimento_inicial": "Gerado pela IA",
            "custos_fixos": "Gerado pela IA",
            "custos_variaveis": "Gerado pela IA",
            "fontes_receita": ["Gerado pela IA"],
            "projecoes": {"ano1": "Gerado pela IA"}
        },
        "gestao": {
            "equipe_fundadora": ["Gerado pela IA"],
            "estrutura_organizacional": "Gerado pela IA",
            "recursos_humanos": "Gerado pela IA"
        }
    }"""
    return {
        "visao_geral": secoes["visao_geral"],
        "pesquisa_de_mercado": secoes["pesquisa_de_mercado"],
        "produtos_servicos": secoes["produtos_servicos"],
        "vendas_marketing": secoes["vendas_marketing"],
        "operacoes": secoes["operacoes"],
        "financeiro": secoes["financeiro"],
        "gestao": secoes["gestao"]
    }



@solicitar_router.post("/solicitacoes/", response=SolicitacaoServico)
def criar_solicitacao(request, payload: SolicitacaoServicoCreate):
    cliente = get_object_or_404(Cliente, id=payload.cliente_id)
    servico = get_object_or_404(Servico, id=payload.servico_id)

    funcionario = None
    if payload.funcionario_id:
        funcionario = get_object_or_404(Funcionario, id=payload.funcionario_id)

    data_inicial = date.today()
    data_final = data_inicial + relativedelta(months=payload.duracao_meses)

    solicitacao = SolicitacaoServico.objects.create(
        cliente=cliente,
        funcionario=funcionario,
        servico=servico,
        tipo_servico=payload.tipo_servico,
        valor=payload.valor,
        status=payload.status,
        duracao_meses=payload.duracao_meses,
        data_inicial=data_inicial,
        data_final=data_final,
        descricao=payload.descricao,
        #factura=payload.factura,
        #tem_factura=payload.tem_factura
    )
    return solicitacao


# Listar todas solicitações
@solicitar_router.get("/solicitacoes/", response=list[SolicitacaoServico])
def listar_solicitacoes(request):
    return SolicitacaoServico.objects.all()


# Obter uma solicitação específica
@solicitar_router.get("/solicitacoes/{solicitacao_id}", response=SolicitacaoServico)
def obter_solicitacao(request, solicitacao_id: int):
    return get_object_or_404(SolicitacaoServico, id=solicitacao_id)


# Atualizar status ou outros campos
@solicitar_router.put("/solicitacoes/{solicitacao_id}", response=SolicitacaoServico)
def atualizar_solicitacao(request, solicitacao_id: int, payload: SolicitacaoServicoCreate):
    solicitacao = get_object_or_404(SolicitacaoServico, id=solicitacao_id)

    for attr, value in payload.dict().items():
        setattr(solicitacao, attr, value)

    solicitacao.data_final = solicitacao.data_inicial + relativedelta(months=payload.duracao_meses)
    solicitacao.save()
    return solicitacao


# Deletar uma solicitação
@solicitar_router.delete("/solicitacoes/{solicitacao_id}")
def deletar_solicitacao(request, solicitacao_id: int):
    solicitacao = get_object_or_404(SolicitacaoServico, id=solicitacao_id)
    solicitacao.delete()
    return {"success": True, "message": "Solicitação removida com sucesso"}

