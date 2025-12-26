---
description: Setup inicial do Frontend (Next.js + ShadcnUI)
---

# Setup do Frontend

Este workflow guia a criação de um novo frontend na pasta `frontend/`.

## Fase 1: Inicialização do Next.js

1. **Verificar diretório:**
   - Se `frontend/` já tiver `package.json`, abortar ou perguntar antes de sobrescrever.

2. **Criar App:**
   - Instruir o Agente a rodar (se tiver permissão) ou pedir para o usuário rodar:
   ```bash
   npx create-next-app@latest frontend --typescript --tailwind --eslint
   ```
   - Configurações recomendadas:
     - TypeScript: Yes
     - Tailwind: Yes
     - App Router: Yes
     - Src directory: Yes
     - Import alias: `@/*`

## Fase 2: Instalação de Bibliotecas Padrão

1. **Instalar Dependências Essenciais:**
   ```bash
   cd frontend
   npm install @supabase/ssr @supabase/supabase-js lucide-react clsx tailwind-merge
   ```

2. **Configurar ShadcnUI (Componentes):**
   ```bash
   npx shadcn-ui@latest init
   ```
   - Adicionar componentes básicos: Button, Input, Card, Toast.

## Fase 3: Conexão com Supabase

1. **Criar Cliente Supabase:**
   - Criar `frontend/lib/supabase/client.ts`
   - Criar `frontend/lib/supabase/server.ts` (para SSR)

2. **Configurar Variáveis de Ambiente:**
   - Criar `frontend/.env.local.example` com:
     - `NEXT_PUBLIC_SUPABASE_URL`
     - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

## Fase 4: Integração com Workers (Cloud Run)

1. **Criar API Helper:**
   - Criar função utilitária para chamar os workers do Cloud Run.
   - Padrão: O front chama o Worker, não o Kestra diretamente (geralmente).
   - Se for Padrão B (Orquestrado), o front pode chamar um Webhook do Kestra.

## Fase 5: Deploy na Vercel

1. **Conectar Repositório ao Vercel:**
   - Acessar [vercel.com/new](https://vercel.com/new)
   - Selecionar o repositório Git do projeto
   - Configurar:
     - **Root Directory**: `frontend`
     - **Framework Preset**: Next.js (auto-detectado)
     - **Build Command**: `npm run build` (default)
     - **Output Directory**: `.next` (default)

2. **Configurar Environment Variables na Vercel:**
   - No dashboard do projeto Vercel → Settings → Environment Variables
   - Adicionar para **Production, Preview e Development**:
     - `NEXT_PUBLIC_SUPABASE_URL` → URL do projeto Supabase
     - `NEXT_PUBLIC_SUPABASE_ANON_KEY` → Anon Key do Supabase
   - Se tiver variáveis sensíveis (não-public), adicionar apenas para Production

3. **Entender o Fluxo de Deploy Automático:**
   - **Push para `main`** → Deploy de Produção automático
   - **Pull Request** → Preview URL único (ex: `projeto-git-branch.vercel.app`)
   - **Merge PR → main** → Novo deploy de Produção

4. **Configurar Domínio Customizado (Opcional):**
   - Settings → Domains → Adicionar domínio
   - Configurar DNS conforme instruído pela Vercel

5. **Verificar Deploy:**
   - Fazer um push para testar
   - Confirmar que o build passou no dashboard
   - Acessar a URL de produção

## Conclusão

- O frontend está configurado e com deploy automático na Vercel.
- Cada PR gera um preview para testes antes de ir para produção.
- Perguntar: "Quer criar a primeira tela baseada na feature planejada? Use /planejar-feature para revisar os requisitos."
