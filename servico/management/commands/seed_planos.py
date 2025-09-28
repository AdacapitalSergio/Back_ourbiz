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
