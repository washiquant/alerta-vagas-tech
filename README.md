# 🚀 Alerta de Vagas Tech

### Pipeline Inteligente de Coleta, Filtragem e Notificação de Vagas Backend em Tempo Real

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge\&logo=sqlite\&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge\&logo=sqlalchemy\&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram_Bot_API-26A5E4?style=for-the-badge\&logo=telegram\&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Layered-success?style=for-the-badge)

</p>

---

## 📌 Sobre o Projeto

O **Alerta de Vagas Tech** é uma aplicação desenvolvida em Python que automatiza o processo de descoberta e monitoramento de oportunidades para profissionais em início de carreira na área de desenvolvimento de software.

O sistema realiza a coleta periódica de vagas em diferentes fontes, aplica regras de filtragem para eliminar anúncios irrelevantes e envia notificações instantâneas via Telegram sempre que uma oportunidade compatível é encontrada.

### Problema Resolvido

Vagas para estagiários e desenvolvedores juniores costumam receber centenas de candidaturas poucas horas após a publicação.

O objetivo deste projeto é reduzir o tempo entre a publicação da vaga e a candidatura do usuário, aumentando significativamente as chances de participação nos processos seletivos.

---

## 🎯 Objetivos Técnicos

Este projeto foi desenvolvido para demonstrar conhecimentos práticos em:

* Desenvolvimento Backend com Python
* Arquitetura modular
* Integração com APIs externas
* Persistência de dados com ORM
* Processamento e filtragem de dados
* Automação de tarefas
* Tratamento de falhas
* Mensageria em tempo real
* Boas práticas de organização de código

---

# 🏛️ Arquitetura

A aplicação segue uma arquitetura modular baseada em separação de responsabilidades.

```text
               ┌────────────────────┐
               │ Fontes de Vagas    │
               │ APIs / Feeds       │
               │ Google Jobs        │
               │ Gupy               │
               └──────────┬─────────┘
                          │
                          ▼
              ┌─────────────────────┐
              │ Collector Layer     │
              │ collector.py        │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Business Rules      │
              │ Filtros e Validação │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Persistence Layer   │
              │ SQLite + ORM        │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ Notification Layer  │
              │ Telegram Bot API    │
              └─────────────────────┘
```

---

# ⚙️ Fluxo da Aplicação

```text
1. Coleta de vagas
        ↓
2. Normalização dos dados
        ↓
3. Aplicação dos filtros
        ↓
4. Verificação de duplicidade
        ↓
5. Persistência no banco
        ↓
6. Envio da notificação
        ↓
7. Marcação como enviada
```

---

# 🔍 Sistema de Filtragem

O projeto utiliza filtros específicos para aumentar a relevância dos resultados.

## Nível de Experiência

Permitidos:

* Estágio
* Estagiário
* Júnior
* Junior
* Trainee

Bloqueados:

* Pleno
* Sênior
* Senior
* Especialista
* Lead
* Coordenador
* Gerente

---

## Stack Tecnológica

Vagas relacionadas a:

* Python
* FastAPI
* Django
* Flask
* C#
* .NET

---

## Localização

Filtro configurável para:

* Remoto
* São Paulo
* Guarulhos

---

# 🗄️ Persistência de Dados

A camada de persistência utiliza:

* SQLite
* SQLAlchemy ORM

Cada vaga é armazenada no banco local e identificada por sua URL de candidatura.

Isso permite:

* Evitar notificações duplicadas
* Manter histórico de vagas
* Reprocessar notificações pendentes
* Recuperar estado após falhas

---

# 🔔 Sistema de Notificações

As oportunidades aprovadas são enviadas automaticamente para o Telegram.

Exemplo:

```html
🚀 Nova Vaga Encontrada

💼 Cargo: Desenvolvedor Python Júnior
🏢 Empresa: Empresa XYZ
📍 Local: Remoto

🔗 Candidatar-se:
https://empresa.com/vaga
```

---

# 🛡️ Tolerância a Falhas

O projeto implementa mecanismos básicos de resiliência.

### Falha na API do Telegram

Caso o envio falhe:

```python
notified = False
```

A vaga permanece registrada no banco e será reenviada no próximo ciclo de execução.

Benefícios:

* Nenhuma vaga é perdida
* Recuperação automática
* Consistência operacional

---

# 🧰 Stack Tecnológica

| Categoria      | Tecnologia       |
| -------------- | ---------------- |
| Linguagem      | Python 3.10+     |
| Banco de Dados | SQLite           |
| ORM            | SQLAlchemy 2.0   |
| HTTP Client    | Requests         |
| Scheduler      | Schedule         |
| Configuração   | Python-dotenv    |
| Mensageria     | Telegram Bot API |

---

# 📁 Estrutura do Projeto

```text
alerta-vagas-tech/
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
│
└── src/
    │
    ├── __init__.py
    ├── collector.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── notifier.py
```

---

# 🚀 Instalação

## Clonar Repositório

```bash
git clone https://github.com/washiquant/alerta-vagas-tech.git

cd alerta-vagas-tech
```

---

## Criar Ambiente Virtual

### Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Instalar Dependências

```bash
pip install -r requirements.txt
```

---

## Configurar Variáveis de Ambiente

Crie um arquivo `.env`:

```env
TELEGRAM_BOT_TOKEN=seu_token
TELEGRAM_CHAT_ID=seu_chat_id
```

---

## Executar Aplicação

```bash
python -m src.main
```

---

# 📈 Possíveis Evoluções

Melhorias planejadas para versões futuras:

* Dashboard Web com FastAPI
* Painel de estatísticas
* PostgreSQL
* Docker
* Logs estruturados
* Sistema de múltiplos usuários
* Filtros configuráveis via interface
* Integração com LinkedIn Jobs
* Integração com e-mail
* Deploy em nuvem

---

# 👨‍💻 Autor

<div align="center">

### Washington Willian Roncador Moreira

🎓 Estudante de Análise e Desenvolvimento de Sistemas (USJT)

🚀 Desenvolvedor Backend em formação no SENAI

💻 Focado em Python, FastAPI, APIs REST, SQL, Docker e Engenharia de Software

<br>

<a href="https://linkedin.com/in/washington-willian-roncador-moreira-04a0662b9">
<img src="https://img.shields.io/badge/LinkedIn-Washington%20Willian%20Roncador%20Moreira-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white">
</a>

<a href="https://github.com/washiquant">
<img src="https://img.shields.io/badge/GitHub-@washiquant-181717?style=for-the-badge&logo=github&logoColor=white">
</a>

<br><br>

<img height="170" src="https://github-readme-stats.vercel.app/api?username=washiquant&show_icons=true&theme=tokyonight"/>

<img height="170" src="https://github-readme-stats.vercel.app/api/top-langs/?username=washiquant&layout=compact&theme=tokyonight"/>

</div>

---

⭐ Se este projeto foi útil para você, considere deixar uma estrela no repositório.
