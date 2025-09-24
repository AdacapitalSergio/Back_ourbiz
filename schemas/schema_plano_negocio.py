# backend/api/plano_negocio.py
from ninja import Schema



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

