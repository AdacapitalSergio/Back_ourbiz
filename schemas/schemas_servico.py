from datetime import date
from ninja import Schema
from typing import Optional, List
from pydantic import EmailStr, Field
from enum import Enum
from decimal import Decimal

class ObjetivoSiteEnum(str, Enum):
    apresentar_empresa = "Apresentar minha empresa"
    vender_produtos = "Vender produtos online (e-commerce)"
    receber_orcamentos = "Receber orçamentos/pedidos de clientes"
    mostrar_portfolio = "Mostrar portfólio ou serviços"
    outro = ""

class TemLogotipoEnum(str, Enum):
    sim = "Sim"
    nao = "Não"
    em_processo = "Em processo de criação"

class MetodoPropostaEnum(str, Enum):
    email = "Email"
    whatsapp = "WhatsApp"
    ambos = "Ambos"

class TemDominioEnum(str, Enum):
    sim = "Sim"
    nao = "Não"
    desconhecido = "Ainda não sei o que é isso"

class RequisitarServicoSchema(Schema):
    # Informações básicas (obrigatórias)
    seuNome: str = Field(..., title="Nome completo ou nome da empresa", min_length=2, max_length=100)
    seuEmail: EmailStr = Field(..., title="Email para contato")
    seuTelefone: str = Field(..., title="Telefone/WhatsApp", pattern=r"^\d{9,20}$")

    # Informações sobre o site
    objetivoSite: Optional[List[ObjetivoSiteEnum]] = Field(None, title="Objetivos do site")
    outroObjetivo: Optional[str] = Field(None, title="Outro objetivo", max_length=100)
    dominio: Optional[str] = Field(None, title="Domínio do site", max_length=100)
    temDominio: Optional[TemDominioEnum] = Field(None, title="Possui domínio?")
    temLogotipo: Optional[TemLogotipoEnum] = Field(None, title="Possui logotipo e identidade visual")
    sobreEmpresa: Optional[str] = Field(None, title="Sobre a empresa/marca", max_length=500)
    integracoesSite: Optional[str] = Field(None, title="Integrações desejadas", max_length=200)
    referenciasSite: Optional[str] = Field(None, title="Referências de sites", max_length=200)
    metodoContato: Optional[MetodoPropostaEnum] = Field(None, title="Método para receber proposta")
    comentariosAdicionais: Optional[str] = Field(None, title="Comentários adicionais", max_length=500)


    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class RequisitarConversationSchema(Schema):
    contacto:Optional[str] = Field(None, title="Contacto", max_length=500)
    mensagen: Optional[str] = Field(None, title="Comentários adicionais", max_length=500)

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class SchemaSolicitacaoServicoCreate(Schema):
    cliente_id: int
    funcionario_id: Optional[int] = None
    servico_id: int
    plano_id: Optional[int] = None
    status: str = "pendente"
    duracao_meses: int
    factura: Optional[str] = None
    
class SchemaSolicitacaoServico(Schema):
    id: int
    cliente_id: int
    funcionario_id: Optional[int]
    #servico_id: int
    #tipo_servico: str
    plano_id: Optional[int] 
    valor: float
    status: str
    duracao_meses: int
    data_inicio: date
    data_final: date
    factura_servico: Optional[str] = None

class RequisitarServicoConsultoriaSchema(Schema):
    seuNome: str = Field(..., title="Nome do Cliente", min_length=2, max_length=100)
    servico: Optional[str] = Field(None, title="Serviço Desejado")
    cidade: Optional[str] = Field(None, title="Cidade")
    municipio: Optional[str] = Field(None, title="Municipio")
    suaEmpresa: Optional[str] = Field(None, title="Área de Atuação")
    seuTelefone: Optional[str] = Field(None, title="Telefone", pattern=r"^\d{9,15}$")# Apenas números, de 9 a 15 dígitos
    seuEmail: Optional[EmailStr] = Field(None, title="E-mail Profissional")

    class Config:
        from_attributes = True  