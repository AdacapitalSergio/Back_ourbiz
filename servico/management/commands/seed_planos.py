import json
from django.core.management.base import BaseCommand
from servico.models import Servico, Plano, Beneficio  # substitui "app" pelo nome da tua app

# JSON com os planos
PLANOS_JSON = {
    "servicos": [
        {
            "nome": "Consultoria para MPMEs",
            "descricao": "Planos de consultoria empresarial adaptados para empreendedores, pequenas, médias empresas, startups e empresas consolidadas.",
            "preco": 0.0,
            "planos": [
                {
                    "titulo": "Básico",
                    "descricao": "Empreendedores iniciantes e pequenas empresas.",
                    "preco_mensal": 29999.000,
                    "beneficios": [
                        {"titulo": "Diagnóstico empresarial inicial", "descricao": "Análise inicial da situação do negócio."},
                        {"titulo": "Estruturação básica do modelo de negócio", "descricao": "Definição da base para o funcionamento do negócio."},
                        {"titulo": "Plano de negócio simplificado", "descricao": "Versão resumida de um plano de negócio."},
                        {"titulo": "Suporte por e-mail", "descricao": "Atendimento via e-mail."}
                    ]
                },
                {
                    "titulo": "Essencial",
                    "descricao": "Pequenas e médias empresas.",
                    "preco_mensal": 49999.000,
                    "beneficios": [
                        {"titulo": "Plano de negócio completo", "descricao": "Elaboração de plano detalhado."},
                        {"titulo": "Estratégias de crescimento", "descricao": "Definição de ações para expansão da empresa."},
                        {"titulo": "Consultoria mensal", "descricao": "1 sessão de acompanhamento mensal."},
                        {"titulo": "Suporte por e-mail + whatsapp", "descricao": "Atendimento por e-mail e WhatsApp."}
                    ]
                },
                {
                    "titulo": "Profissional",
                    "descricao": "Empresas em crescimento e Startups.",
                    "preco_mensal": 69999.000,
                    "beneficios": [
                        {"titulo": "Tudo do plano Essencial", "descricao": "Inclui todos os serviços do plano Essencial."},
                        {"titulo": "Consultoria personalizada", "descricao": "2 sessões de acompanhamento por mês."},
                        {"titulo": "Estratégia de expansão e captação de investimentos", "descricao": "Orientação para captar recursos e expandir."},
                        {"titulo": "Otimização de processos internos", "descricao": "Aprimoramento da eficiência operacional."},
                        {"titulo": "Suporte prioritário", "descricao": "Atendimento com prioridade."}
                    ]
                },
                {
                    "titulo": "Premium",
                    "descricao": "Empresas consolidadas.",
                    "preco_mensal": 99999.000,
                    "beneficios": [
                        {"titulo": "Tudo do plano Profissional", "descricao": "Inclui todos os serviços do plano Profissional."},
                        {"titulo": "Acompanhamento contínuo com mentorias personalizadas", "descricao": "Mentoria contínua e sob medida."},
                        {"titulo": "Consultoria estratégica avançada", "descricao": "Planejamento estratégico em nível avançado."},
                        {"titulo": "Planeamento de internacionalização", "descricao": "Expansão internacional da empresa (quando aplicável)."},
                        {"titulo": "Suporte prioritário", "descricao": "Atendimento com prioridade máxima."}
                    ]
                }
            ]
        },
        {
            "nome": "Apoio e Captação de Recursos",
            "descricao": "Planos de apoio estratégico para captação de recursos, preparação para investidores e crescimento sustentável.",
            "preco": 0.0,
            "planos": [
                {
                    "titulo": "Inicial",
                    "descricao": "Empreendedores iniciantes e pequenas startups.",
                    "preco_mensal": 29999.000,
                    "beneficios": [
                        {"titulo": "Identificação de fontes de financiamento", "descricao": "Mapeamento de potenciais fontes de capital."},
                        {"titulo": "Assessoria em propostas e candidaturas", "descricao": "Suporte na elaboração de propostas."},
                        {"titulo": "Direcionamento para incubadoras e aceleradoras", "descricao": "Conexão com programas de apoio ao crescimento."}
                    ]
                },
                {
                    "titulo": "Intermediário",
                    "descricao": "Startups em busca de capital.",
                    "preco_mensal": 49999.000,
                    "beneficios": [
                        {"titulo": "Consultoria para desenvolvimento de pitch", "descricao": "Preparação profissional de pitch para investidores."},
                        {"titulo": "Mentoria sobre captação de investimentos", "descricao": "Acompanhamento especializado para fundraising."},
                        {"titulo": "Simulação de apresentação", "descricao": "Treino de apresentação frente a investidores."}
                    ]
                },
                {
                    "titulo": "Completo",
                    "descricao": "Startups escaláveis e empresas em crescimento.",
                    "preco_mensal": 79999.000,
                    "beneficios": [
                        {"titulo": "Estruturação financeira", "descricao": "Planejamento financeiro para atrair investimentos."},
                        {"titulo": "Conexão direta com investidores", "descricao": "Acesso a investidores e fundos."},
                        {"titulo": "Acompanhamento contínuo", "descricao": "Suporte ao longo do processo de captação."}
                    ]
                }
            ]
        },
        {
            "nome": "Marketing e Divulgação",
            "descricao": "Planos para impulsionar a visibilidade da marca, atrair clientes e fortalecer a presença no mercado.",
            "preco": 0.0,
            "planos": [
                {
                    "titulo": "Básico",
                    "descricao": "Pequenos negócios e startups iniciantes.",
                    "preco_mensal": 19999.000,
                    "beneficios": [
                        {"titulo": "Definição de identidade visual", "descricao": "Construção da identidade visual da marca."},
                        {"titulo": "Estratégia de branding", "descricao": "Planejamento de posicionamento de marca."},
                        {"titulo": "Criação de logotipo", "descricao": "Design profissional do logotipo."},
                        {"titulo": "Materiais gráficos", "descricao": "Criação de cartão de visitas, banner e folheto."}
                    ]
                },
                {
                    "titulo": "Avançado",
                    "descricao": "Startups e PMEs em crescimento.",
                    "preco_mensal": 59999.000,
                    "beneficios": [
                        {"titulo": "Tudo do plano Básico", "descricao": "Inclui todos os itens do plano Básico."},
                        {"titulo": "Gestão de redes sociais", "descricao": "Gerenciamento profissional de mídias sociais."},
                        {"titulo": "Flyer criativo semanal", "descricao": "Criação de flyer personalizado 1 vez por semana."},
                        {"titulo": "Anúncio patrocinado semanal", "descricao": "Campanhas patrocinadas semanais."}
                    ]
                },
                {
                    "titulo": "Premium",
                    "descricao": "Empresas e startups escaláveis.",
                    "preco_mensal": 84999.000,
                    "beneficios": [
                        {"titulo": "Tudo do plano Avançado", "descricao": "Inclui todos os itens do plano Avançado."},
                        {"titulo": "Criação de website institucional", "descricao": "Website de 1 página para a empresa."},
                        {"titulo": "Estratégia de marketing completa", "descricao": "Planejamento abrangente de marketing."},
                        {"titulo": "Assessoria de imprensa", "descricao": "Consultoria em comunicação e PR."},
                        {"titulo": "Consultoria contínua", "descricao": "Otimização constante das campanhas."}
                    ]
                }
            ]
        }
    ]
}




class Command(BaseCommand):
    help = "Carrega os planos de consultoria para MPMEs no banco de dados"

    def handle(self, *args, **kwargs):
        for servico_data in PLANOS_JSON["servicos"]:
            servico, _ = Servico.objects.get_or_create(
                nome=servico_data["nome"],
                defaults={
                    "descricao": servico_data["descricao"],
                    "preco": servico_data["preco"],
                }
            )

            for plano_data in servico_data["planos"]:
                plano, _ = Plano.objects.get_or_create(
                    titulo=plano_data["titulo"],
                    servicos=servico,
                    defaults={
                        "descricao": plano_data["descricao"],
                        "preco_mensal": plano_data["preco_mensal"],
                    }
                )

                for beneficio_data in plano_data["beneficios"]:
                    Beneficio.objects.get_or_create(
                        titulo=beneficio_data["titulo"],
                        plano=plano,
                        defaults={"descricao": beneficio_data["descricao"]}
                    )

        self.stdout.write(self.style.SUCCESS("Planos de consultoria importados com sucesso!"))
