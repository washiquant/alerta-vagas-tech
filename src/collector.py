import logging
import requests
import re
import os
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

ALLOWED_ROLES = ["estágio", "estagio", "estagiário", "estagiaria", "intern", "trainee", "junior", "júnior", "jr"]
EXCLUDED_ROLES = ["senior", "sênior", "sr", "pleno", "mid", "lead", "principal", "manager", "gerente"]
ALLOWED_STACKS = ["python", "c#", ".net", "dotnet"]
BACKEND_TERMS = ["backend", "back-end", "desenvolvedor", "developer", "software"]
NEARBY_LOCATIONS = ["guarulhos", "são paulo", "sao paulo", "sp", "remoto", "remote"]


def is_valid_job(title: str, text: str) -> bool:
    t = title.lower()
    c = text.lower()

    if any(re.search(rf"\b{re.escape(term)}\b", t) for term in EXCLUDED_ROLES):
        return False
    if not any(re.search(rf"\b{re.escape(role)}\b", t) for role in ALLOWED_ROLES):
        return False
    if not any(re.search(rf"\b{re.escape(tech)}\b", c) for tech in ALLOWED_STACKS):
        return False
    return True


def fetch_jobs() -> List[Dict[str, Any]]:
    jobs_found = []

    # 1. Busca Direta via Google Jobs / SerpApi (LinkedIn, Glassdoor, Catho agregados)
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    if serpapi_key:
        queries = [
            "estágio backend python São Paulo",
            "estágio c# desenvolvedor São Paulo",
            "junior backend python remoto"
        ]
        for q in queries:
            try:
                url = f"https://serpapi.com/search.json?engine=google_jobs&q={requests.utils.quote(q)}&hl=pt&gl=br&api_key={serpapi_key}"
                res = requests.get(url, timeout=20)
                if res.status_code == 200:
                    data = res.json()
                    for job in data.get("jobs_results", []):
                        title = job.get("title", "")
                        desc = job.get("description", "")

                        if is_valid_job(title, f"{title} {desc}"):
                            apply_options = job.get("apply_options", [])
                            apply_url = apply_options[0].get("link") if apply_options else job.get("share_link", "")

                            jobs_found.append({
                                "title": title,
                                "company": job.get("company_name", "Confidencial"),
                                "location": job.get("location", "São Paulo/Remoto"),
                                "workplace_type": "Híbrido/Presencial/Remoto",
                                "apply_url": apply_url
                            })
            except Exception as e:
                logger.error(f"Erro ao buscar no Google Jobs (SerpApi): {e}")

    # 2. Busca na API pública de vagas abertas da Gupy
    try:
        gupy_url = "https://portal.api.gupy.io/api/v1/jobs?jobName=estagio&limit=50"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(gupy_url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            for job in data.get("data", []):
                title = job.get("name", "")
                city = (job.get("city") or "").lower()
                state = (job.get("state") or "").lower()
                is_remote = job.get("isRemoteWork", False)

                # Valida raio geográfico (São Paulo / Guarulhos / Remoto)
                if not (
                        is_remote or "guarulhos" in city or "são paulo" in city or "sao paulo" in city or state == "sp"):
                    continue

                full_text = f"{title} {job.get('description', '')}"
                if is_valid_job(title, full_text):
                    jobs_found.append({
                        "title": title,
                        "company": job.get("careerPageName", "Empresa Gupy"),
                        "location": f"{job.get('city', 'SP')} - {job.get('state', 'SP')}" if not is_remote else "Remoto",
                        "workplace_type": "Remoto" if is_remote else "Presencial/Híbrido",
                        "apply_url": job.get("jobUrl", "")
                    })
    except Exception as e:
        logger.error(f"Erro ao consultar vagas Gupy: {e}")

    return jobs_found