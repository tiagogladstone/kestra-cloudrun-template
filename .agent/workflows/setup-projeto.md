---
description: Setup completo do projeto (Git + Google Cloud + Kestra)
---

# Setup Completo do Projeto

Este workflow guia o Agente IA para configurar todo o ambiente do zero.
O Agente deve executar os comandos, verificando o sucesso de cada etapa.

## Fase 0: Limpeza de Arquivos do Template

> ⚠️ Esta fase só se aplica se você CLONOU o template para criar um novo projeto.

1. **Perguntar ao usuário:**
   - "Você está criando um NOVO PROJETO a partir do template? (S/n)"

2. **Se SIM, remover arquivos exclusivos do template:**
   ```bash
   # Arquivos de governança do template
   rm -f CONTRIBUTING.md
   rm -f docs/ROADMAP.md
   rm -rf .github/workflows/test-template.yml
   
   # Regras específicas do template (não se aplicam a projetos derivados)
   rm -f .agent/rules/contexto-template.md
   rm -f .agent/rules/manter-changelog.md
   ```

3. **Atualizar `.agent/rules/context.md`:**
   > ⚠️ IMPORTANTE: O arquivo `context.md` já existe em `.agent/rules/context.md`. NÃO criar em outro lugar!
   
   - Abrir o arquivo `.agent/rules/context.md`
   - Preencher a seção "Informações Gerais" com:
     - Nome do projeto
     - Versão do template usada (ler do arquivo `VERSION`)
     - Data de criação
     - Conta Google Cloud do usuário

4. **Atualizar `README.md`:**
   - Remover a seção "VOCÊ ESTÁ NO TEMPLATE OU EM UM PROJETO?"
   - Atualizar título e autor

## Fase 1: Inicialização do Repositório (Local)

1. Verificar se já existe `.git`. Se sim, pular.
   - Perguntar ao usuário: "Este é um projeto novo? Posso inicializar o Git?"

2. Inicializar Git:
   ```bash
   git init
   git branch -M main
   ```

3. Fazer primeiro commit com a estrutura base:
   - Adicionar todos os arquivos
   - Commit inicial
   ```bash
   git add .
   git commit -m "feat: initial structure (scaffold)"
   ```

## Fase 2: Conexão com GitHub

1. Verificar se `gh` (GitHub CLI) está instalado.
   - Se não, pedir para usuário instalar ou criar repo manualmente.

2. Se `gh` estiver disponível, criar repo remoto:
   - Perguntar: "Qual nome você quer para o repositório no GitHub? (ex: minha-empresa/projeto-x)"
   - Executar:
   ```bash
   gh repo create NOME_DO_REPO --private --source=. --remote=origin --push
   ```

## Fase 3: Configuração Google Cloud (Infra Base)

### 3.1 Verificar autenticação

```bash
gcloud auth list
```

- Se não logado, pedir para usuário rodar `gcloud auth login` (não dá pra fazer pelo agente sem browser).
- Se a conta desejada não está ativa, criar nova configuração:
  ```bash
  gcloud config configurations create NOME_CONFIG --activate
  gcloud config set account EMAIL_DA_CONTA
  ```

### 3.2 Selecionar ou Criar Projeto

- Perguntar: "Qual o ID do projeto no Google Cloud? (Se não tiver, digite 'novo' para eu criar)"
- Se 'novo':
  ```bash
  gcloud projects create ID_DO_PROJETO --name="Nome do Projeto"
  ```
- Definir projeto atual:
  ```bash
  gcloud config set project ID_DO_PROJETO
  ```

### 3.3 ⚠️ VERIFICAR BILLING (Obrigatório!)

> **IMPORTANTE:** Sem billing configurado, as APIs NÃO serão habilitadas!

1. Verificar se billing está vinculado:
   ```bash
   gcloud billing projects describe ID_DO_PROJETO
   ```

2. Se aparecer erro ou `billingEnabled: false`:
   - Instruir usuário: "Acesse https://console.cloud.google.com/billing/linkedaccount?project=ID_DO_PROJETO e vincule uma conta de faturamento."
   - **Aguardar usuário confirmar** que vinculou o billing antes de prosseguir.

3. Se `billingEnabled: true`, continuar.

### 3.4 ⚠️ VERIFICAR PERMISSÕES

> O usuário precisa ter papel de **Owner** ou **Editor** no projeto.

```bash
gcloud projects get-iam-policy ID_DO_PROJETO --format="table(bindings.role,bindings.members)" | head -20
```

- Verificar se o email da conta aparece com role `roles/owner` ou `roles/editor`.
- Se não tiver permissão, instruir: "Você precisa pedir ao dono do projeto para te adicionar como Editor/Owner, ou criar um novo projeto com sua conta."

### 3.5 Habilitar APIs (Uma por vez para diagnóstico)

> ⚠️ Se falhar alguma, fica mais fácil identificar qual.

// turbo
```bash
gcloud services enable run.googleapis.com
```

// turbo
```bash
gcloud services enable cloudbuild.googleapis.com
```

// turbo
```bash
gcloud services enable pubsub.googleapis.com
```

// turbo
```bash
gcloud services enable cloudscheduler.googleapis.com
```

// turbo
```bash
gcloud services enable compute.googleapis.com
```

// turbo  
```bash
gcloud services enable logging.googleapis.com
```

// turbo
```bash
gcloud services enable clouderrorreporting.googleapis.com
```

// turbo
```bash
gcloud services enable secretmanager.googleapis.com
```

**Se alguma API falhar:**
- Verificar se billing está ativo (seção 3.3)
- Verificar permissões (seção 3.4)
- Alguns projetos não têm Error Reporting disponível - pode pular se necessário

### 3.6 Confirmar APIs ativas

```bash
gcloud services list --enabled --filter="name:(run OR cloudbuild OR pubsub OR cloudscheduler OR compute OR logging OR error OR secret)"
```

## Fase 4: Kestra (Orquestrador)

### Perguntar ao usuário:
- "Você quer usar Kestra Cloud (grátis até certo limite) ou Self-Hosted (VM ~$25/mês)?"

---

### Opção A: Kestra Cloud (Recomendado para começar)

1. Instruir usuário a criar conta em https://kestra.io/pricing
2. Após criar, pegar a URL do workspace
3. Atualizar `.env` ou documentar a URL

**Vantagens:** Sem VM, sem manutenção, free tier disponível.

---

### Opção B: Kestra Self-Hosted

1. **Confirmar com usuário:**
   - "Vou criar uma VM e2-medium (Custo ~$25/mês). Confirma?"

2. **Criar VM:**
   ```bash
   gcloud compute instances create kestra-server \
     --machine-type=e2-medium \
     --zone=us-central1-a \
     --image-project=debian-cloud \
     --image-family=debian-11 \
     --boot-disk-size=30GB \
     --tags=http-server,https-server
   ```

3. **Abrir Firewall:**
   // turbo
   ```bash
   gcloud compute firewall-rules create allow-kestra --allow tcp:8080 --target-tags=http-server
   ```

4. **Instruir usuário a configurar Docker na VM:**
   - Comando para entrar: `gcloud compute ssh kestra-server --zone=us-central1-a`
   - Seguir instruções em `docs/operacional/SETUP_INICIAL.md`

## Fase 5: Instruções Finais do Kestra

O Agente **NÃO CONSEGUE** configurar dentro da VM via SSH automaticamente de forma fácil (interativo).
Então, o agente deve instruir o usuário:

1. Exibir comando para usuário rodar:
   "Rode este comando no seu terminal para entrar na VM:"
   `gcloud compute ssh kestra-server --zone=us-central1-a`

2. Exibir comando para instalar Docker e Kestra na VM:
   (Mostrar o script do arquivo `docs/operacional/SETUP_INICIAL.md`)

## Fase 6: Supabase (Banco de Dados)

> ⚠️ **O Agente tem acesso ao Supabase via MCP!**

1. **Verificar conexão MCP:**
   - Usar: `mcp_supabase-mcp-server_list_projects`
   - Se funcionar, listar projetos disponíveis para o usuário escolher

2. **Se MCP conectado:**
   - Mostrar projetos disponíveis
   - Perguntar: "Qual projeto você quer usar para este app?"
   - Guardar o `project_id` para uso posterior

3. **Verificar organization (se precisar criar projeto):**
   - Usar: `mcp_supabase-mcp-server_list_organizations`
   - Usar: `mcp_supabase-mcp-server_get_cost` para verificar custos
   - Usar: `mcp_supabase-mcp-server_create_project` se necessário

4. **Obter URLs e chaves:**
   - Usar: `mcp_supabase-mcp-server_get_project_url` para obter a API URL
   - Usar: `mcp_supabase-mcp-server_get_publishable_keys` para obter as chaves

5. **Salvar em `.env.example` (referência):**
   ```
   SUPABASE_URL=<url obtida via MCP>
   SUPABASE_ANON_KEY=<anon key obtida>
   ```

6. **Lembrar:** 
   - "O MCP já está conectado ao Supabase - o Agente pode executar SQL diretamente!"
   - "Para produção, use Secret Manager para a Service Role Key."

---

## Fase 7: Vercel (Frontend) - Opcional

1. **Perguntar ao usuário:**
   - "Seu projeto terá frontend? (S/n)"

2. **Se SIM:**
   - Instruir: "Conecte seu repositório GitHub em https://vercel.com/new"
   - Configurar Root Directory: `frontend/`
   - Configurar variáveis:
     - `NEXT_PUBLIC_SUPABASE_URL`
     - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

3. **Se NÃO:**
   - Pular esta fase

---

## Fase 8: Configuração de Deploy (CI/CD)

1. Conectar Cloud Build ao GitHub:
   - Instruir usuário a conectar via link: https://console.cloud.google.com/cloud-build/triggers/connect

2. Criar Trigger Automático?
   - O Agente pode tentar criar via `gcloud beta builds triggers create github...` mas exige token.
   - Melhor instruir usuário a criar o gatilho manualmente seguindo o `SETUP_INICIAL.md`.

---

## Conclusão

- **Resumir o que foi feito:**
  - ✅ Git configurado
  - ✅ GitHub conectado
  - ✅ Google Cloud configurado
  - ✅ Kestra (Cloud ou VM)
  - ✅ Supabase configurado
  - ✅ Vercel configurado (se aplicável)
  - ✅ CI/CD configurado

- **Próximos passos:**
  - "Agora você pode:"
    - `/planejar-feature` - Para definir o que construir
    - `/criar-banco` - Para criar as tabelas
    - `/criar-worker` - Para criar o primeiro worker
