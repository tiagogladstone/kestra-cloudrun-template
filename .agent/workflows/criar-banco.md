---
description: Criar tabelas e migrations no Banco de Dados (Supabase)
---

# Setup de Banco de Dados

Este workflow guia o Agente IA na criação de estruturas de banco de dados e migrations.

## Pré-requisitos
- Ter executado `/planejar-feature` (ou ter um plano claro).
- **Supabase MCP conectado** (o Agente tem acesso direto ao banco!).

## Fase 1: Descobrir Projeto Supabase

1. **Listar projetos disponíveis:**
   - Usar ferramenta: `mcp_supabase-mcp-server_list_projects`
   - Perguntar ao usuário qual projeto usar (se houver mais de um)

2. **Verificar tabelas existentes:**
   - Usar: `mcp_supabase-mcp-server_list_tables` com o `project_id`
   - Evitar conflitos de nomes

## Fase 2: Geração de SQL

1. **Ler o plano:**
   - Consultar `docs/specs/*.md` relevante ou perguntar ao usuário o que criar.

2. **Criar Arquivo de Migration (backup local):**
   - Gerar timestamp: `YYYYMMDDHHMMSS`
   - Criar arquivo: `database/migrations/[TIMESTAMP]_[nome_descritivo].sql`
   - Escrever o SQL DDL (CREATE TABLE, INDEX, RLS Policies).

3. **Regras de Ouro (Supabase/Postgres):**
   - Usar `UUID` como chave primária padrão: `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`
   - Habilitar `ROW LEVEL SECURITY` (RLS) em todas as tabelas: `ALTER TABLE x ENABLE ROW LEVEL SECURITY;`
   - Usar `timestamptz` para datas.
   - Adicionar `created_at TIMESTAMPTZ DEFAULT now()`.
   - Adicionar `updated_at TIMESTAMPTZ DEFAULT now()` (se aplicável).

## Fase 3: Aplicar Migration via MCP

> ⚠️ **O Agente TEM acesso direto ao banco via MCP!**

1. **Aplicar DDL (CREATE, ALTER, etc):**
   - Usar ferramenta: `mcp_supabase-mcp-server_apply_migration`
   - Parâmetros:
     - `project_id`: ID do projeto Supabase
     - `name`: Nome da migration em snake_case (ex: `create_vendas_hotmart`)
     - `query`: O SQL a ser executado

   ```
   Exemplo de chamada:
   mcp_supabase-mcp-server_apply_migration(
     project_id="abc123",
     name="create_vendas_hotmart",
     query="CREATE TABLE vendas_hotmart (...)"
   )
   ```

2. **Verificar se funcionou:**
   - Usar: `mcp_supabase-mcp-server_list_tables` para confirmar que a tabela foi criada

3. **Para queries de leitura (SELECT):**
   - Usar: `mcp_supabase-mcp-server_execute_sql`

## Fase 4: Verificação de Segurança

1. **Checar advisories:**
   - Usar: `mcp_supabase-mcp-server_get_advisors` com `type="security"`
   - Isso detecta RLS faltando, policies expostas, etc.

2. **Corrigir problemas identificados:**
   - Se RLS estiver faltando, adicionar via nova migration

## Fase 5: Gerar Tipos (Opcional)

1. **TypeScript:**
   - Usar: `mcp_supabase-mcp-server_generate_typescript_types`
   - Salvar em `frontend/types/database.ts` (se houver frontend)

2. **Python (Pydantic):**
   - Criar manualmente em `modules/supabase_client/models.py`
   - Baseado na estrutura da tabela

## Resumo de Ferramentas MCP Disponíveis

| Ferramenta | Uso |
|------------|-----|
| `list_projects` | Descobrir project_id |
| `list_tables` | Ver tabelas existentes |
| `apply_migration` | Executar DDL (CREATE, ALTER, DROP) |
| `execute_sql` | Executar queries (SELECT, INSERT, UPDATE) |
| `get_advisors` | Checar segurança e performance |
| `generate_typescript_types` | Gerar tipos TS |
| `list_migrations` | Ver migrations aplicadas |

## Conclusão

- ✅ Migration aplicada diretamente no banco via MCP
- ✅ Arquivo de backup salvo em `database/migrations/`
- Perguntar: "Banco configurado. Quer criar o worker para manipular esses dados? Use /criar-worker"
