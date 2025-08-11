from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_verification_email(cliente_nome, verification_link, cliente_email, msg_link):
    send_mail(
        "Confirme seu e-mail",
        f"Olá {cliente_nome}, {msg_link}: {verification_link}",
        settings.DEFAULT_FROM_EMAIL,
        [cliente_email],
        fail_silently=False,
    )

@shared_task
def send_email_for_operation(cliente_nome, servico, cidade, municipio, area_atuacao, telefone, cliente_email):
    image_url = "IMG_20250403_111108_173.jpg"
    email_subject = "📌 Solicitação de Serviço"

    email_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #ffffff;
            color: #333;
            padding: 20px;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-size: contain;
            border: 2px solid #d32f2f;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            position: relative;
        }}
        .overlay {{
            background: rgba(255, 255, 255, 0.85);
            padding: 20px;
            border-radius: 6px;
        }}
        .header {{
            background-color: #d32f2f;
            color: white;
            text-align: center;
            padding: 15px;
            font-size: 20px;
            border-radius: 6px 6px 0 0;
            margin-bottom: 10px;
        }}
        img {{
            max-width: 40%;
            height: auto;
            margin-top: 15px;
        }}
        .imgPosition{{
            text-align: center;
            margin: 0 auto;
        }}
        .footer {{
            margin-top: 15px;
            font-size: 12px;
            color: #555;
            text-align: center;
        }}
        .highlight {{
            color: #d32f2f;
            font-weight: bold;
        }}
        .section-title {{
            background-color: #f5f5f5;
            padding: 8px;
            margin: 15px 0 10px 0;
            border-left: 4px solid #d32f2f;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="overlay">
            <div class="header">
                📌 Solicitação de Serviço
            </div>
            <p>Olá! Sou {cliente_nome}, gostaria de solicitar um serviço conforme os detalhes abaixo:</p>
            <ul>
                <li><b>Serviço desejado:</b> <span class="highlight">{servico}</span></li>
                <li><b>Cidade:</b> {cidade}</li>
                <li><b>Município:</b> {municipio}</li>
                <li><b>Área de atuação:</b> {area_atuacao}</li>
                <li><b>E-mail profissional:</b> {cliente_email}</li>
                <li><b>Telefone:</b> {telefone}</li>
            </ul>
            <p>Estarei aguardando do retorno com mais informações.</p>
            <p>Atenciosamente,<br> <b>{cliente_nome}</b></p>
            <div class="imgPosition">
                <img src="{image_url}" alt="Logo">
            </div>
            <div class="footer">
                © MarolDep | Todos os direitos reservados.
            </div>
        </div>
    </div>
</body>
</html>
"""

    send_mail(
        email_subject,
        "",
        cliente_email,
        [settings.DEFAULT_FROM_EMAIL],
        fail_silently=False,
        html_message=email_body,
    )


import os
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage


@shared_task
def send_website_request_email(
    nome_requerente, email_requerente, telefone_requerente, objetivo_site, tem_dominio, dominio,
    tem_logotipo, sobre_empresa, integracoes, site_referencia, metodo_contato, commentarios,
):
    # Caminho do logotipo
    logo_path = os.path.join(settings.BASE_DIR, "staticfiles", "img", "IMG_20250403_111108_173.jpg")

    # Corpo do e-mail para a equipe
    email_subject = "🌐 Nova Solicitação de Website"
    email_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width:600px;margin:0 auto;border:2px solid #FD3DB5;padding:20px;border-radius:8px;">
            <h2 style="color:#FD3DB5;text-align:center;">🌐 Nova Solicitação de Website</h2>
            <p><b>Nome:</b> {nome_requerente}</p>
            <p><b>E-mail:</b> {email_requerente}</p>
            <p><b>Telefone:</b> {telefone_requerente}</p>
            <p><b>Objetivo:</b> {objetivo_site or 'Não especificado'}</p>
            <p><b>Tem logotipo:</b> {tem_dominio or 'Não especificado'}</p>
            <p><b>Tem logotipo:</b> {dominio or 'Não especificado'}</p>
            <p><b>Tem logotipo:</b> {tem_logotipo or 'Não especificado'}</p>
            <p><b>Sobre a empresa:</b> {sobre_empresa or 'Nenhuma informação'}</p>
            <p><b>Integrações desejadas:</b> {integracoes or 'Nenhuma'}</p>
            <p><b>Integrações desejadas:</b> {site_referencia or 'Nenhuma'}</p>
            <p><b>Integrações desejadas:</b> {metodo_contato or 'Nenhuma'}</p>
            <p><b>Integrações desejadas:</b> {commentarios or 'Nenhuma'}</p>
            <p style="text-align:center;">
                <img src="cid:logo_id" style="max-width:200px;">
            </p>
        </div>
    </body>
    </html>
    """

    msg = EmailMultiAlternatives(
        subject=email_subject,
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.DEFAULT_FROM_EMAIL],
    )
    msg.attach_alternative(email_body, "text/html")

    # Anexar logo inline
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", "<logo_id>")
            img.add_header("Content-Disposition", "inline", filename="IMG_20250403_111108_173.jpg")
            msg.attach(img)

    msg.send()

    # Corpo do e-mail de confirmação para o cliente
    if email_requerente:
        confirmation_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width:600px;margin:0 auto;border:2px solid #FD3DB5;padding:20px;border-radius:8px;">
                <h2 style="color:#FD3DB5;">Olá {nome_requerente},</h2>
                <p>Recebemos sua solicitação e entraremos em contato em breve pelo {metodo_contato or 'Não especificado'}.</p>
                <p><b>Objetivo:</b> {objetivo_site or 'Não especificado'}</p>
                <p style="text-align:center;">
                    <img src="cid:logo_id" style="max-width:200px;">
                </p>
            </div>
        </body>
        </html>
        """

        confirm_msg = EmailMultiAlternatives(
            subject="✅ Recebemos sua solicitação de website",
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email_requerente],
        )
        confirm_msg.attach_alternative(confirmation_body, "text/html")

        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                img = MIMEImage(f.read())
                img.add_header("Content-ID", "<logo_id>")
                img.add_header("Content-Disposition", "inline", filename="IMG_20250403_111108_173.jpg")
                confirm_msg.attach(img)

        confirm_msg.send()


@shared_task
def send_conversation_for_operation_email(
    contacto_requerente, sms_requerente,
):
    # Caminho do logotipo
    logo_path = os.path.join(settings.BASE_DIR, "staticfiles", "img", "IMG_20250403_111108_173.jpg")

    # Corpo do e-mail para a equipe
    email_subject = "🌐 "
    email_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width:600px;margin:0 auto;border:2px solid #FD3DB5;padding:20px;border-radius:8px;">
            <h2 style="color:#FD3DB5;text-align:center;">🌐 Nova Conversa</h2>
            <p><b>E-mail:</b> {contacto_requerente}</p>
            <p>{sms_requerente}</p>
            <p style="text-align:center;">
                <img src="cid:logo_id" style="max-width:200px;">
            </p>
        </div>
    </body>
    </html>
    """

    msg = EmailMultiAlternatives(
        subject=email_subject,
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.DEFAULT_FROM_EMAIL],
    )
    msg.attach_alternative(email_body, "text/html")

    # Anexar logo inline
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", "<logo_id>")
            img.add_header("Content-Disposition", "inline", filename="IMG_20250403_111108_173.jpg")
            msg.attach(img)

    msg.send()