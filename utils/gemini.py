#import google.generativeai as genai
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import re
import os
from typing import Dict, Any
import google.generativeai as genai


# Configura a API Key (nunca exponha publicamente)
genai.configure(api_key="AIzaSyCYfHeJAJqyi2qrBpygTQn0XxTfg4K83po")


# ---------- Configuração do Gemini ----------
#genai.configure(api_key="AIzaSyBCtgsPp0KU848QKGEhd5KCGgfn9gYVbUo")

modelo = genai.GenerativeModel("gemini-2.5-flash")


# ---------- Helpers ----------
def adicionar_numero_paginas(section):
    footer = section.footer
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    run = paragraph.add_run()
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.text = "PAGE"
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "end")

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)


def limpar_texto(texto: str) -> str:
    texto = re.sub(r"[*#_~>`-]+", "", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


# ---------- Função principal ----------
def gerar_conteudo_secoes(dados: str) -> dict[str, Any]:
    """
    Gera automaticamente as seções completas do plano de negócio
    com base nos dados fornecidos (tipo de negócio + localização).
    """

    secoes = {
        "SUMARIO_EXECUTIVO": "Crie um resumo executivo do plano de negócio.",
        "A_EMPRESA": """
            Descreva a empresa, incluindo:
            - Historial
            - Missão
            - Visão
            - Valores
        """,
        "CARATERIZACAO_DO_PROJETO": """
            Explique o projeto:
            - Descrição da área física (lay-out)
            - Localização do projeto
        """,
        "O_PRODUTO_SERVICO": "Descreva em detalhe os produtos e/ou serviços oferecidos.",
        "ANALISE_DE_MERCADO": """
            Monte a análise de mercado:
            - Clientes
            - Fornecedores
            - Concorrência
            - As 5 Forças de Porter
            - Análise SWOT
        """,
        "SISTEMA_PRODUTIVO": """
            Detalhe o sistema produtivo:
            - Instalações de suporte
            - Equipamento produtivo
        """,
        "PLANO_DE_MARKETING": """
            Crie a seção de marketing:
            - Marketing estratégico
            - Marketing tático
        """,
        "ESTRUTURA_ORGANIZACIONAL": """
            Detalhe a estrutura organizacional:
            - Recursos Humanos
        """,
        "PLANO_FINANCEIRO": """
            Crie a parte financeira:
            - Investimento inicial
            - Financiamento
            - Previsão de receitas
            - Custos mensais
            - Fluxo de caixa
            - DRE (Demonstração de Resultados)
            - Índices de Rentabilidade
        """,
        "CONSIDERACOES_FINAIS": "Faça as considerações finais, riscos e planos de crescimento.",
        "ANEXOS": "Liste anexos relevantes (documentos, gráficos, relatórios)."
    }

    resultados: dict[str, Any] = {}

    for chave, prompt in secoes.items():
        resposta = modelo.generate_content(
            f"{prompt}\n\nDados da empresa:\n{dados}"
        )
        resultados[chave] = limpar_texto(resposta.text)

    return resultados



def gerar_plano_de_negocio_word(tipo_negocio: str, localizacao: str, imagem_capa="capa.jpg"):
    doc = Document()

    # CAPA
    doc.add_paragraph("\n\n")

    # Inserir imagem de capa se existir
    if os.path.exists(imagem_capa):
        doc.add_picture(imagem_capa, width=Inches(5.5))
        last_paragraph = doc.paragraphs[-1]
        last_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    doc.add_paragraph("\n")
    titulo = doc.add_paragraph("PLANO DE NEGÓCIO")
    titulo.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    run = titulo.runs[0]
    run.bold = True
    run.font.size = Pt(28)

    doc.add_paragraph("\n")
    nome = doc.add_paragraph(f"Tipo de negócio: {tipo_negocio}")
    nome.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    nome.runs[0].font.size = Pt(20)
    nome.runs[0].bold = True

    doc.add_paragraph("\n")
    local = doc.add_paragraph(f"Localização: {localizacao}")
    local.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    local.runs[0].font.size = Pt(16)

    doc.add_paragraph("\n\n")
    autor = doc.add_paragraph("Elaborado por: Adelino Francisco Emiliano")
    autor.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    autor.runs[0].italic = True

    data = doc.add_paragraph("Data: 2025")
    data.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    data.runs[0].italic = True

    doc.add_page_break()

    # Adicionar número de páginas (exceto capa)
    for section in doc.sections[1:]:
        adicionar_numero_paginas(section)

    # Gerar conteúdo detalhado automaticamente
    dados = {
        "tipo_negocio": tipo_negocio,
        "localizacao": localizacao
    }
    conteudo_secoes = gerar_conteudo_secoes(dados)

    # Inserir conteúdo no documento Word
    for titulo_secao, texto in conteudo_secoes.items():
        doc.add_heading(titulo_secao, level=1)
        for paragrafo in texto.split("\n"):
            if paragrafo.strip():
                doc.add_paragraph(paragrafo.strip())
        doc.add_page_break()

    doc.save("plano_de_negocio.docx")
    print("📄 Plano de negócio Word gerado com sucesso: plano_de_negocio.docx")


#gerar_plano_de_negocio_word(dados_exemplo, imagem_capa="capa.jpg")
