# Conexões MCP (Model Context Protocol)

O Agente IA possui acesso a serviços externos via MCP. Este documento lista as conexões disponíveis e como usá-las.

---

## 📊 Supabase MCP

O Agente pode interagir **diretamente** com o Supabase sem precisar de credenciais manuais.

### Ferramentas Disponíveis

| Ferramenta | Descrição | Quando Usar |
|------------|-----------|-------------|
| `list_projects` | Lista todos os projetos Supabase | Descobrir project_id |
| `get_project` | Detalhes de um projeto | Verificar status |
| `list_organizations` | Lista organizações | Antes de criar projeto |
| `get_cost` | Custo de criar projeto/branch | Antes de criar |
| `create_project` | Cria novo projeto | Setup inicial |
| `list_tables` | Lista tabelas do banco | Ver estrutura existente |
| `apply_migration` | Executa DDL (CREATE, ALTER) | Criar/alterar tabelas |
| `execute_sql` | Executa queries (SELECT, etc) | Consultas e DML |
| `list_migrations` | Lista migrations aplicadas | Histórico de mudanças |
| `get_advisors` | Checa segurança/performance | Após criar tabelas |
| `generate_typescript_types` | Gera tipos TS | Para frontend |
| `get_project_url` | Obtém API URL | Configurar .env |
| `get_publishable_keys` | Obtém chaves públicas | Configurar frontend |
| `list_edge_functions` | Lista Edge Functions | Ver funções existentes |
| `deploy_edge_function` | Deploy de Edge Function | Criar função serverless |
| `get_logs` | Logs do projeto | Debug |
| `search_docs` | Busca na documentação | Dúvidas sobre Supabase |

### Exemplo de Uso: Criar Tabela

```
1. Descobrir projeto:
   mcp_supabase-mcp-server_list_projects()

2. Aplicar migration:
   mcp_supabase-mcp-server_apply_migration(
     project_id="abc123",
     name="create_users",
     query="CREATE TABLE users (id UUID PRIMARY KEY DEFAULT gen_random_uuid(), ...)"
   )

3. Verificar segurança:
   mcp_supabase-mcp-server_get_advisors(project_id="abc123", type="security")
```

### Branches (Desenvolvimento)

Para ambientes de desenvolvimento isolados:

| Ferramenta | Descrição |
|------------|-----------|
| `create_branch` | Cria branch de desenvolvimento |
| `list_branches` | Lista branches existentes |
| `merge_branch` | Merge para produção |
| `rebase_branch` | Sincroniza com produção |
| `reset_branch` | Reset para estado limpo |
| `delete_branch` | Remove branch |

---

## 🌐 Outras Conexões (Futuras)

Conexões que podem ser adicionadas ao projeto:

| Serviço | MCP Disponível? | Uso |
|---------|-----------------|-----|
| **Supabase** | ✅ Sim | Banco de dados, Auth, Storage |
| **GitHub** | 🔜 Possível | PRs, Issues, Actions |
| **Google Cloud** | 🔜 Possível | Cloud Run, Pub/Sub |
| **Vercel** | 🔜 Possível | Deploys, Environment |
| **Kestra** | 🔜 Possível | Flows, Executions |

---

## ⚠️ Importante

1. **O MCP usa credenciais do ambiente** - Não precisa configurar nada manualmente se o MCP estiver configurado.

2. **Segurança:** O Agente tem acesso de escrita ao banco. Sempre revisar migrations antes de aplicar.

3. **Fallback:** Se o MCP não estiver disponível, o Agente deve instruir o usuário a fazer manualmente via Dashboard.

---

## Como Verificar Conexão

O Agente pode testar a conexão assim:

```
# Testar conexão Supabase
mcp_supabase-mcp-server_list_projects()

# Se retornar lista de projetos = conectado ✅
# Se retornar erro = configurar MCP
```
