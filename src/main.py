import os
import sys
import time
import logging
import schedule
from dotenv import load_dotenv

# Garante que a raiz do projeto esteja no path de importação
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database import engine, Base, SessionLocal
from src.models import JobListing
from src.collector import fetch_jobs
from src.notifier import send_telegram_alert, send_email_alert

# Configuração de formatação de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("AlertaVagasTech")

# Carrega variáveis de ambiente do .env e inicializa tabelas
load_dotenv()
Base.metadata.create_all(bind=engine)


def process_job(db, job_data: dict) -> None:
    """
    Processa uma vaga individualmente: persiste se for nova
    e dispara notificação caso ainda não tenha sido enviada.
    """
    url = job_data.get("apply_url")
    if not url:
        return

    existing_job = db.query(JobListing).filter_by(apply_url=url).first()
    target_job = None

    if not existing_job:
        logger.info(f"Nova vaga encontrada: {job_data.get('title')} ({job_data.get('company')})")
        new_job = JobListing(
            title=job_data.get("title", "Vaga sem título"),
            company=job_data.get("company", "Confidencial"),
            location=job_data.get("location", "Não informado"),
            workplace_type=job_data.get("workplace_type", "Presencial"),
            apply_url=url,
            notified=False
        )
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        target_job = new_job
    elif not existing_job.notified:
        logger.info(f"Reenviando vaga pendente: {existing_job.title}")
        target_job = existing_job

    if target_job:
        # Tenta envio pelo Telegram
        telegram_sent = send_telegram_alert(job_data)

        # Envio opcional por e-mail (descomente se estiver usando)
        # email_sent = send_email_alert(job_data)

        if telegram_sent:
            target_job.notified = True
            db.commit()
            logger.info(f"Alerta enviado com sucesso via Telegram: {target_job.title}")
        else:
            logger.warning(f"Falha ao enviar alerta para: {target_job.title}. Será mantido como pendente.")

        # Intervalo para evitar bloqueio por rate-limit da API do Telegram
        time.sleep(2)


def job_routine() -> None:
    """Rotina periódica de execução do coletor e mensageiro."""
    logger.info("Iniciando rotina de monitoramento de vagas...")
    db = SessionLocal()

    try:
        jobs = fetch_jobs()
        logger.info(f"Total de {len(jobs)} vagas brutas compatíveis encontradas nesta busca.")

        for job_data in jobs:
            try:
                process_job(db, job_data)
            except Exception as item_err:
                db.rollback()
                logger.error(f"Erro ao processar a vaga '{job_data.get('title')}': {item_err}")

    except Exception as err:
        logger.error(f"Falha inesperada durante a execução da rotina: {err}", exc_info=True)
    finally:
        db.close()
        logger.info("Rotina de monitoramento finalizada. Aguardando próximo ciclo.")


if __name__ == "__main__":
    logger.info("Monitor de Vagas de Estágio Tech iniciado com sucesso.")
    logger.info("Pressione Ctrl+C a qualquer momento para interromper.")

    # Executa uma busca imediata ao iniciar o serviço
    job_routine()

    # Agenda execuções automáticas a cada 30 minutos
    schedule.every(30).minutes.do(job_routine)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Encerrando o serviço manualmente...")
            break
        except Exception as loop_err:
            logger.critical(f"Erro no agendador de tarefas: {loop_err}")
            time.sleep(5)