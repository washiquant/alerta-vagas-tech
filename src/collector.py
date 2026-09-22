import logging
import requests
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Configurações de Filtro
TARGET_ROLES = ["estágio", "estagio", "estagiário", "intern", "trainee"]
TARGET_STACKS = ["python", "c#", ".net"]
TARGET_LOCATIONS = ["são paulo", "sao paulo", "sp", "guarulhos", "remoto", "remote"]


def fetch_jobs() -> List[Dict[str, Any]]:
    """
    Simula a busca em uma API pública de vagas (ex: Remotive, Arbeitnow ou endpoints de ATS).
    Para produção em sites brasileiros, substitua a URL pela API pública desejada.
    """
    url = "https://remotive.com/api/remote-jobs?category=software-dev"
    jobs_found = []

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        for job in data.get("jobs", []):
            title = job.get("title", "").lower()
            description = job.get("description", "").lower()
            location = job.get("candidate_required_location", "").lower()

            # 1. Filtro de Cargo
            is_internship = any(role in title for role in TARGET_ROLES)

            # 2. Filtro de Stack (no título ou descrição)
            has_stack = any(stack in title or stack in description for stack in TARGET_STACKS)

            # 3. Filtro de Localidade (se a API fornece)
            is_target_location = any(loc in location for loc in TARGET_LOCATIONS) or "remoto" in location

            if (is_internship or has_stack) and is_target_location:
                jobs_found.append({
                    "title": job.get("title", "Vaga sem título"),
                    "company": job.get("company_name", "Confidencial"),
                    "location": job.get("candidate_required_location", "Não informado"),
                    "workplace_type": "Remoto",  # Remotive é 100% remoto
                    "apply_url": job.get("url", "")
                })

        return jobs_found

    except requests.RequestException as e:
        logger.error(f"Erro ao buscar vagas na API: {e}")
        return []