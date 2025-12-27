---
trigger: model_decision
description: Contexto do projeto template e conexões MCP disponíveis
---

# Contexto do Repositório: PROJETO BASE (TEMPLATE)

**Versão:** 1.0.0
**Tipo de Repositório:** 📦 Template / Boilerplate

---

## 🤖 Para Agentes de IA

Este é o **PROJETO BASE (TEMPLATE)** a partir do qual outros projetos serão criados.

### Objetivo
Manter a infraestrutura base saudável e documentação impecável.

### Regras
1. **Generalização:** Código genérico, sem regras de negócio específicas
2. **Documentação First:** Alterar código = atualizar docs
3. **Retrocompatibilidade:** Evitar breaking changes

---

## Estrutura

| Pasta | Descrição |
|-------|-----------|
| `.agent/rules/` | Regras para o agente |
| `.agent/workflows/` | Workflows via `/comando` |
| `docs/` | Documentação |
| `modules/` | Código Python compartilhado |
| `workers/` | Workers Cloud Run |
| `flows/` | Flows Kestra |
| `database/` | Migrations e seeds |
| `frontend/` | Next.js |

---

## 🔌 Conexões MCP

### Supabase

| Ferramenta | Uso |
|------------|-----|
| `list_projects` | Descobrir project_id |
| `list_tables` | Ver estrutura |
| `apply_migration` | DDL (CREATE, ALTER) |
| `execute_sql` | Queries (SELECT, INSERT) |
| `get_advisors` | Checar segurança/RLS |
| `get_project_url` | Obter API URL |
| `get_publishable_keys` | Obter chaves |
| `deploy_edge_function` | Deploy Edge Functions |
| `generate_typescript_types` | Gerar tipos TS |

### Fallback
Se MCP indisponível, instruir usuário a usar Dashboard.

---

## ADRs

| ID | Decisão | Status |
|----|---------|--------|
| ADR-01 | Kestra Cloud ou Self-Hosted | Aceito |
| ADR-02 | Monorepo | Aceito |
| ADR-03 | Python/FastAPI | Aceito |
| ADR-04 | Shared Modules via Docker | Aceito |
| ADR-05 | Secret Manager obrigatório | Mandatório |