from django.shortcuts import get_object_or_404
from ninja import Router

from django.shortcuts import render

from schemas.schema_plano_negocio import PlanoNegocioInput, PlanoNegocioResponse, SugestaoSchema

from schemas.schemas_servico import RequisitarConversationSchema, RequisitarServicoSchema
from utils.gemini import gerar_conteudo_secoes, sugerir_ideias

from celery.result import AsyncResult

from datetime import timedelta

from servico.models import Plano, Servico
from schemas.schemas_servico import SchemaSolicitacaoServico, SchemaSolicitacaoServicoCreate
from datetime import date
from dateutil.relativedelta import relativedelta

from schemas.schemas_servico import RequisitarServicoConsultoriaSchema


plano_router = Router()

@plano_router.get("/gerar/")
def gerar_plano_view(request):
    return render(request, 'index_plano.html')

@plano_router.get("/result/")
def result_plano_view(request):
    return render(request, 'planoresult.html')



@plano_router.post("/sugerir_respostas", response=dict)
def sugerir_respostas(request, data: SugestaoSchema):
    """
    Retorna 5 ideias curtinhas com limite de caracteres.
    """
    try:
        sugestoes = sugerir_ideias(
            dados=data.dados,
            pergunta=data.pergunta,
            qtd_caracteres=str(data.limite)
        )
        print(type(sugestoes))
        return {"status": "ok", "resultado": sugestoes}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}


@plano_router.post("/gerar_plano_negocio/", response=dict)
def gerar_plano(request, data: PlanoNegocioInput):
    dados_empresa = f"Tipo de negócio: {data.tipo_de_negocio}, Localização: {data.localizacao}, Nome da empresa: {data.nome_empresa}, Diferencial: {data.diferencial}"
    task = gerar_conteudo_secoes.delay(dados_empresa)
    print("task_id", task.id)
    return {"task_id": task.id, "status": "em processamento"}

SECOES = [
    ("SUMARIOEXECUTIVO", "Sumário Executivo"),
    ("AEMPRESA", "A Empresa"),
    ("CARATERIZACAODOPROJETO", "Caracterização do Projeto"),
    ("OPRODUTOSERVICO", "O Produto/Serviço"),
    ("ANALISEDEMERCADO", "Análise de Mercado"),
    ("SISTEMAPRODUTIVO", "Sistema Produtivo"),
    ("PLANODEMARKETING", "Plano de Marketing"),
    ("ESTRUTURAORGANIZACIONAL", "Estrutura Organizacional"),
    ("PLANOFINANCEIRO", "Plano Financeiro"),
    ("CONSIDERACOESFINAIS", "Considerações Finais"),
    ("ANEXOS", "Anexos"),
]

@plano_router.get("/gerar_plano_status/{task_id}")
def gerar_plano_status(request, task_id: str):
    task = AsyncResult(task_id)

    if task.state == "SUCCESS":
        resultado = task.result

        secoes_formatadas = []
        for chave, titulo in SECOES:
            texto = resultado.get(chave, "")
            secoes_formatadas.append({
                "id": chave,
                "titulo": titulo,
                "itens": [l for l in texto.split("\n") if l.strip()]
            })

        contexto = {
            "plano": {
                "nome_empresa": "Empresa Gerada",
                "secoes": secoes_formatadas
            }
        }

        return render(request, "planoresult.html", contexto)

    return {"status": task.state}
