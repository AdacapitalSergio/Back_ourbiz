import google.generativeai as genai
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import re
import os

# Configurar API
genai.configure(api_key="AIzaSyBCtgsPp0KU848QKGEhd5KCGgfn9gYVbUo")
modelo = genai.GenerativeModel("gemini-1.5-flash")

def adicionar_numero_paginas(section):
    footer = section.footer
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)

def limpar_texto(texto):
    texto = re.sub(r"[*#_~>`-]+", "", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()

def gerar_conteudo_secoes(dados):
    secoes = {
        "Resumo Executivo": "Crie um resumo executivo para o plano de negócio da empresa abaixo.",
        "Análise de Mercado": "Descreva a análise de mercado com base nas informações da empresa.",
        "Plano de Marketing": "Crie um plano de marketing adequado às informações fornecidas.",
        "Plano Operacional": "Detalhe o plano operacional baseado nos dados.",
        "Plano Financeiro": "Descreva o plano financeiro usando os dados de custos e receita.",
        "Considerações Finais": "Faça considerações finais incluindo riscos e planos de crescimento."
    }
    resultados = {}
    for secao, prompt in secoes.items():
        resposta = modelo.generate_content(f"{prompt}\n\nDados:\n{dados}")
        resultados[secao] = limpar_texto(resposta.text)
    return resultados

def gerar_plano_de_negocio_word(dados, imagem_capa="capa.jpg"):
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
    nome = doc.add_paragraph(dados["nome_empresa"])
    nome.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    nome.runs[0].font.size = Pt(22)
    nome.runs[0].bold = True

    doc.add_paragraph("\n")
    descricao = doc.add_paragraph(dados["descricao"])
    descricao.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    descricao.runs[0].font.size = Pt(14)

    doc.add_paragraph("\n\n")
    missao = doc.add_paragraph(f"Missão: {dados['missao']}")
    missao.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    missao.runs[0].italic = True

    visao = doc.add_paragraph(f"Visão: {dados['visao']}")
    visao.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    visao.runs[0].italic = True

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

    # Gerar conteúdo com Gemini
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

# ---------------------
# EXEMPLO DE USO
dados_exemplo = {
    "nome_empresa": "Tech Solutions",
    "descricao": "Empresa de soluções em tecnologia para pequenas empresas.",
    "missao": "Oferecer soluções acessíveis e eficientes em TI.",
    "visao": "Ser referência em tecnologia para PMEs na América Latina.",
    "objetivos": "Crescer 20% ao ano e atingir 100 clientes no primeiro ano.",
    "publico_alvo": "Pequenas e médias empresas.",
    "concorrencia": "Outras empresas locais de TI.",
    "diferenciais": "Atendimento personalizado e preços competitivos.",
    "estrategias_marketing": "Marketing digital, redes sociais e parcerias.",
    "canais_venda": "Loja online, vendas diretas e marketplaces.",
    "localizacao": "Luanda, Angola.",
    "estrutura": "Escritório com 5 colaboradores.",
    "fornecedores": "Dell, HP, fornecedores locais de software.",
    "investimento_inicial": "50000",
    "receita_mensal": "20000",
    "custos_fixos": "8000",
    "ponto_equilibrio": "8 meses",
    "riscos": "Instabilidade econômica, concorrência agressiva.",
    "plano_crescimento": "Expandir para outras cidades e lançar novos serviços."
}

#gerar_plano_de_negocio_word(dados_exemplo, imagem_capa="capa.jpg")
