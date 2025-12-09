from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os

@shared_task
def send_consultoria_request_email(
    cliente_nome, servico, cidade, municipio, area_atuacao, telefone, cliente_email
):
    # Caminho do logotipo
    logo_path = os.path.join(settings.BASE_DIR, "staticfiles", "admin/img/", "lateral branca 2.png")

    # Corpo do e-mail para a equipe
    email_subject = "🌐 Nova Solicitação de consultoria"
    email_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width:600px;margin:0 auto;border:2px solid #FD3DB5;padding:20px;border-radius:8px;">
            <h2 style="color:#FD3DB5;text-align:center;">🌐 Nova Solicitação de consultoria</h2>
            <p><b>Nome:</b> {cliente_nome}</p>
            <p><b>E-mail:</b> {cliente_email}</p>
            <p><b>Telefone:</b> {telefone}</p>
            <p><b>Objetivo:</b> {servico or 'Não especificado'}</p>
            <p><b>Cidade:</b> {cidade}</p>
            <p><b>Município:</b> {municipio}</p>
            <p><b>Área de atuação:</b> {area_atuacao}</p>

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
        from_email=cliente_email,
        to=["comercial@ourbiz.ao"],
    )
    msg.attach_alternative(email_body, "text/html")

    # Anexar logo inline
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", "<logo_id>")
            img.add_header("Content-Disposition", "inline", filename="lateral branca 2.png")
            msg.attach(img)

    msg.send()

    # Corpo do e-mail de confirmação para o cliente
    if cliente_email:
        confirmation_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width:600px;margin:0 auto;border:2px solid #FD3DB5;padding:20px;border-radius:8px;">
                <h2 style="color:#FD3DB5;">Olá {cliente_nome},</h2>
                <p>Recebemos sua solicitação e entraremos em contato em breve.</p>
                <p><b>Servico:</b> {servico or 'Não especificado'}</p>
                <p style="text-align:center;">
                    <img src="cid:logo_id" style="max-width:200px;">
                </p>
            </div>
        </body>
        </html>
        """

        confirm_msg = EmailMultiAlternatives(
            subject="✅ Recebemos sua solicitação de Consultoria",
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[cliente_email],
        )
        confirm_msg.attach_alternative(confirmation_body, "text/html")

        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                img = MIMEImage(f.read())
                img.add_header("Content-ID", "<logo_id>")
                img.add_header("Content-Disposition", "inline", filename="admin/img/lateral branca 2.png")
                confirm_msg.attach(img)

        confirm_msg.send()

