import os
import time
import logging
import schedule
from dotenv import load_dotenv

from src.database import engine, Base, SessionLocal
from src.models import JobListing
from src.collector import fetch_jobs
from src.notifier import send_telegram_alert, send_email_alert

# Configura logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Carrega variáveis e inicializa DB
load_dotenv()
Base.metadata.create_all(bind=engine)


def job_routine():
    logger.info("Iniciando rotina de busca de vagas...")
    db = SessionLocal()

    try:
        jobs = fetch_jobs()
        logger.info(f"Foram encontradas {len(jobs)} vagas brutas nos filtros.")

        for job_data in jobs:
            # Verifica deduplicação
            exists = db.query(JobListing).filter_by(apply_url=job_data["apply_url"]).first()

            if not exists:
                logger.info(f"Nova vaga identificada: {job_data['title']}")

                # Salva no banco
                new_job = JobListing(
                    title=job_data["title"],
                    company=job_data["company"],
                    location=job_data["location"],
                    workplace_type=job_data["workplace_type"],
                    apply_url=job_data["apply_url"]
                )
                db.add(new_job)
                db.commit()
                db.refresh(new_job)

                # Notifica
                telegram_sent = send_telegram_alert(job_data)
                # email_sent = send_email_alert(job_data) # Descomente se usar e-mail

                if telegram_sent:
                    new_job.notified = True
                    db.commit()

                # Delay para evitar rate limit na API do Telegram
                time.sleep(2)

    except Exception as e:
        logger.error(f"Erro crítico na rotina principal: {e}")
    finally:
        db.close()
        logger.info("Rotina finalizada.")


if __name__ == "__main__":
    logger.info("Sistema de Alertas Iniciado. Pressione Ctrl+C para sair.")

    # Roda a primeira vez imediatamente
    job_routine()

    # Agenda para rodar a cada 30 minutos
    schedule.every(30).minutes.do(job_routine)

    while True:
        schedule.run_pending()
        time.sleep(1)