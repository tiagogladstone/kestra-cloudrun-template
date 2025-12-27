---
trigger: always_on
glob:
description: Regras gerais do projeto de automação Kestra + Cloud Run
---

# Regras do Projeto

Este arquivo define as regras que a IA deve seguir ao trabalhar neste projeto.

---

## Stack Tecnológica

| Camada | Tecnologia |
|--------|------------|
| **Backend** | Python 3.11+ com FastAPI |
| **Banco** | Supabase (PostgreSQL) |
| **Orquestração** | Kestra |
| **Execução** | Google Cloud Run |
| **Filas** | Google Pub/Sub |
| **Frontend** | Next.js no Vercel |

---

## Processo de Desenvolvimento (Living System)

Este projeto segue um ciclo de vida estrito. A IA deve **SEMPRE** seguir esta ordem:

1.  **PLANEJAR (Planning)**
    - Nunca escrever código sem ter um documento de spec aprovado em `docs/specs/`.
    - Usar `/planejar-projeto` (início) ou `/planejar-feature` (incremental).
    - Validar o plano com o usuário antes de seguir.

2.  **EXECUTAR (Execution)**
    - Só rodar `/criar-banco` se `docs/specs/3_DADOS/MODELAGEM_DADOS.md` existir.
    - Só rodar `/criar-worker` se `docs/specs/2_ARQUITETURA/FLUXOS_NEGOCIO.md` existir.
    - Manter o `task.md` atualizado com o progresso.

3.  **DOCUMENTAR (Documentation)**
    - Todo código novo deve refletir na documentação.
    - Manter `README.md` e `CHANGELOG.md` vivos.

---

## Padrões de Código

### Nomenclatura

| Elemento | Padrão | Exemplo |
|----------|--------|---------|
| Workers | `{dominio}-{acao}` | `hotmart-sync`, `whatsapp-sender` |
| Flows | `{dominio}/{acao}.yaml` | `hotmart/sincronizar-vendas.yaml` |
| Funções Python | `snake_case` | `processar_pagamento()` |
| Classes Python | `PascalCase` | `PaymentProcessor` |
| Variáveis de ambiente | `UPPER_SNAKE_CASE` | `SUPABASE_URL` |

### Estrutura de Worker

Todo worker DEVE ter:

1. **Endpoint `/` (POST)** - Endpoint principal
2. **Endpoint `/health` (GET)** - Health check
3. **Tratamento de erro** com ErrorHandler
4. **Correlation ID** nos logs
5. **Uso dos módulos compartilhados** (`modules/`)

### Tratamento de Erro

SEMPRE usar o ErrorHandler do módulo compartilhado:

```python
from modules.error_handler import ErrorHandler

handler = ErrorHandler(service_name="nome-worker")

try:
    # código
except Exception as e:
    handler.capture(e, context={"correlation_id": correlation_id})
    raise
```

---

## Deploy

### ⚠️ IMPORTANTE: Deploy via TAGs (não push normal!)

O CI/CD só dispara com **TAGs** no formato `worker-NOME-vX`.
Push normal para `main` **NÃO faz deploy automático**.

### Processo de Deploy

```bash
# 1. Testar local (da raiz do projeto)
docker build -f workers/meu-worker/Dockerfile -t test .
docker run -p 8080:8080 --env-file workers/meu-worker/.env test

# 2. Commitar e push
git add . && git commit -m "feat: worker X" && git push

# 3. Criar e pushar TAG para deploy
git tag worker-NOME-v1 && git push origin worker-NOME-v1
```

---

## Segurança

### ⚠️ MANDATÓRIO: Secret Manager

**NUNCA** usar `.env` em produção.
- API Keys → Google Secret Manager
- Tokens → Google Secret Manager
- URLs públicas → Variáveis de ambiente Cloud Run

### ⚠️ MANDATÓRIO: Circuit Breaker

TODO deploy de Cloud Run DEVE ter `--max-instances=5` para evitar cobrança infinita.

---

## Observabilidade

### ⚠️ MANDATÓRIO: Correlation ID

Todo flow Kestra DEVE passar `X-Correlation-ID: "{{ execution.id }}"` nos headers.
Todo worker DEVE logar com `[correlation_id]` prefixando as mensagens.

---

## Riscos a Evitar

| Risco | Mitigação |
|-------|-----------|
| OOM na VM Kestra | Usar e2-medium (4GB), não e2-micro |
| Cobrança infinita | --max-instances em todo Cloud Run |
| Segredos expostos | Secret Manager, não .env |
| Debug impossível | Correlation ID em tudo |
