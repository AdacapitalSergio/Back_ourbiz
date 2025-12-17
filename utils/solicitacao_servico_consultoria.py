from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
import os


@shared_task
def send_consultoria_request_email(
    cliente_nome: str,
    servico: str,
    provincia: str,
    municipio: str,
    area_atuacao: str,
    telefone: str,
    cliente_email: str,
    forma_contacto: str,
):  
    print("Enviando email de solicitação de consultoria...")
    # Caminho do logotipo
    logo_path = os.path.join(
        settings.BASE_DIR,
        "staticfiles",
        "admin/img",
        "lateral branca 2.png"
    )

    # ==============================
    # Email para a equipa
    # ==============================
    email_subject = "🌐 Nova Solicitação de Consultoria"

    email_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <div style="max-width:600px;margin:0 auto;border:2px solid #FD3DB5;
                    padding:20px;border-radius:8px;">
            
            <h2 style="color:#FD3DB5;text-align:center;">
                🌐 Nova Solicitação de Consultoria
            </h2>

            <p><b>Nome:</b> {cliente_nome}</p>
            <p><b>E-mail:</b> {cliente_email}</p>
            <p><b>Telefone:</b> {telefone}</p>
            <p><b>Forma de contacto:</b> {forma_contacto}</p>
            <p><b>Serviço desejado:</b> {servico or 'Não especificado'}</p>
            <p><b>Província:</b> {provincia}</p>
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
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=["comercial@ourbiz.ao"],
        reply_to=[cliente_email],
    )

    msg.attach_alternative(email_body, "text/html")

    # Logo inline
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            img = MIMEImage(f.read())
            img.add_header("Content-ID", "<logo_id>")
            img.add_header("Content-Disposition", "inline", filename="logo.png")
            msg.attach(img)

    msg.send()

    # ==============================
    # Email de confirmação ao cliente
    # ==============================
    if cliente_email:
        confirmation_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <div style="max-width:600px;margin:0 auto;border:2px solid #FD3DB5;
                        padding:20px;border-radius:8px;">

                <h2 style="color:#FD3DB5;">Olá {cliente_nome},</h2>

                <p>
                    Recebemos a sua solicitação de consultoria com sucesso.
                    A nossa equipa entrará em contacto consigo em breve.
                </p>

                <p><b>Serviço solicitado:</b> {servico}</p>

                <p style="text-align:center;">
                    <img src="cid:logo_id" style="max-width:200px;">
                </p>
            </div>
        </body>
        </html>
        """

        confirm_msg = EmailMultiAlternatives(
            subject="✅ Recebemos a sua solicitação de Consultoria",
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[cliente_email],
        )

        confirm_msg.attach_alternative(confirmation_body, "text/html")

        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                img = MIMEImage(f.read())
                img.add_header("Content-ID", "<logo_id>")
                img.add_header("Content-Disposition", "inline", filename="logo.png")
                confirm_msg.attach(img)

        confirm_msg.send()
