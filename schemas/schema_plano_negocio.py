# backend/api/plano_negocio.py
from ninja import Router, Schema

plano_router = Router()


# ---------- Schemas ----------
class SWOTSchema(Schema):
    forcas: list[str]
    fraquezas: list[str]
    oportunidades: list[str]
    ameacas: list[str]


class VisaoGeralSchema(Schema):
    resumo_executivo: str
    analise_swot: SWOTSchema
    modelos_de_negocio: str
    analise_viabilidade: str


class IndustriaSchema(Schema):
    participacao_mercado: str
    penetracao_internet: str
    volume_ecommerce: str


class MercadoSchema(Schema):
    industria: str
    visao_geral_industria: IndustriaSchema
    publico_alvo: str
    tamanho_mercado_tendencias: dict
    analise_concorrente: list[str]


class ProdutosServicosSchema(Schema):
    ofertas_centrais: list[str]
    oportunidades_expansao: list[str]
    ofertas_secundarias: list[str]
    atendimento_cliente: str


class VendasMarketingSchema(Schema):
    estrategia_marketing: str
    canais_distribuicao: list[str]
    precificacao: str
    metodos_pagamento: list[str]


class OperacoesSchema(Schema):
    infraestrutura: str
    logistica: str
    parcerias: list[str]
    tecnologia: str


class FinanceiroSchema(Schema):
    investimento_inicial: str
    custos_fixos: str
    custos_variaveis: str
    fontes_receita: list[str]
    projecoes: dict


class GestaoSchema(Schema):
    equipe_fundadora: list[str]
    estrutura_organizacional: str
    recursos_humanos: str


class PlanoNegocioResponse(Schema):
    visao_geral: VisaoGeralSchema
    pesquisa_de_mercado: MercadoSchema
    produtos_servicos: ProdutosServicosSchema
    vendas_marketing: VendasMarketingSchema
    operacoes: OperacoesSchema
    financeiro: FinanceiroSchema
    gestao: GestaoSchema


# ---------- Input ----------
class PlanoNegocioInput(Schema):
    tipo_de_negocio: str
    localizacao: str


# ---------- Endpoint ----------
@plano_router.post("/gerar", response=PlanoNegocioResponse)
def gerar_plano(request, data: PlanoNegocioInput):

    # 🚀 Aqui é onde entraria a chamada ao Gemini ou outra IA
    # Por enquanto vou retornar mock de exemplo

    return {
        "visao_geral": {
            "resumo_executivo": f"Plano de negócio para {data.tipo_de_negocio} em {data.localizacao}.",
            "analise_swot": {
                "forcas": ["Equipe experiente", "Parcerias internacionais"],
                "fraquezas": ["Capital inicial limitado", "Dependência de importações"],
                "oportunidades": ["Crescimento do e-commerce", "Demanda por tecnologia"],
                "ameacas": ["Concorrência internacional", "Instabilidade econômica"],
            },
            "modelos_de_negocio": "Marketplace B2C e B2B",
            "analise_viabilidade": "Viável considerando o crescimento do setor."
        },
        "pesquisa_de_mercado": {
            "industria": data.tipo_de_negocio,
            "visao_geral_industria": {
                "participacao_mercado": "20%",
                "penetracao_internet": "39%",
                "volume_ecommerce": "$720M"
            },
            "publico_alvo": "Jovens urbanos de 18 a 35 anos.",
            "tamanho_mercado_tendencias": {
                "crescimento_ecommerce": "US$ 152M até 2025",
                "taxa_crescimento_anual": "14,4%"
            },
            "analise_concorrente": ["Lojas físicas locais", "Amazon", "AliExpress"]
        },
        "produtos_servicos": {
            "ofertas_centrais": ["Smartphones", "Tablets"],
            "oportunidades_expansao": ["Manutenção", "Consultoria"],
            "ofertas_secundarias": ["Capinhas", "Carregadores"],
            "atendimento_cliente": "Suporte online 24/7"
        },
        "vendas_marketing": {
            "estrategia_marketing": "Foco em redes sociais",
            "canais_distribuicao": ["Loja online", "Marketplaces"],
            "precificacao": "Competitiva",
            "metodos_pagamento": ["Cartão", "Multicaixa Express", "Unitel Money"]
        },
        "operacoes": {
            "infraestrutura": "Loja online e armazém central",
            "logistica": "Parcerias com transportadoras",
            "parcerias": ["Fornecedores internacionais"],
            "tecnologia": "Plataforma de e-commerce robusta"
        },
        "financeiro": {
            "investimento_inicial": "US$ 100.000",
            "custos_fixos": "US$ 5.000/mês",
            "custos_variaveis": "Dependem das vendas",
            "fontes_receita": ["Venda de produtos", "Serviços"],
            "projecoes": {
                "ano1": "US$ 250.000",
                "ano3": "US$ 750.000",
                "ano5": "US$ 2M"
            }
        },
        "gestao": {
            "equipe_fundadora": ["CEO", "COO", "CMO"],
            "estrutura_organizacional": "Equipe enxuta",
            "recursos_humanos": "Expansão planejada para 10 colaboradores"
        }
    }
