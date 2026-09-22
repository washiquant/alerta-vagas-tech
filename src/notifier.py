import os
import smtplib
import logging
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


def send_telegram_alert(job_data: dict) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logger.warning("Credenciais do Telegram ausentes. Alerta não enviado.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    # Formatação limpa em Markdown ou HTML
    message = (
        f"🚨 <b>Nova Vaga de Estágio Tech!</b>\n\n"
        f"🏢 <b>Empresa:</b> {job_data['company']}\n"
        f"💼 <b>Cargo:</b> {job_data['title']}\n"
        f"📍 <b>Local:</b> {job_data['location']} ({job_data['workplace_type']})\n\n"
        f"🔗 <a href='{job_data['apply_url']}'>Clique aqui para se candidatar</a>"
    )

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(url, json=payload, timeout=25)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.error(f"Erro ao enviar alerta via Telegram: {e}")
        return False


def send_email_alert(job_data: dict) -> bool:
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    target_email = os.getenv("TARGET_EMAIL")

    if not all([smtp_user, smtp_pass, target_email]):
        return False

    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = target_email
    msg['Subject'] = f"Nova Vaga: {job_data['title']} na {job_data['company']}"

    body = f"Link para candidatura: {job_data['apply_url']}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {e}")
        return False