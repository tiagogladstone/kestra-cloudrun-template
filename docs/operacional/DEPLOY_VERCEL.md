# Deploy do Frontend na Vercel

Guia operacional para deploy e manutenção do frontend Next.js na Vercel.

---

## Pré-requisitos

- Conta na Vercel (pode usar GitHub/GitLab/Bitbucket para login)
- Repositório Git com o código do projeto
- Pasta `frontend/` com aplicação Next.js configurada

---

## Setup Inicial

### 1. Conectar Repositório

1. Acesse [vercel.com/new](https://vercel.com/new)
2. Selecione o Git Provider (GitHub, GitLab, ou Bitbucket)
3. Autorize acesso ao repositório
4. Selecione o repositório do projeto

### 2. Configurar Projeto

| Campo | Valor |
|-------|-------|
| **Project Name** | Nome do projeto (será parte da URL) |
| **Framework Preset** | Next.js (auto-detectado) |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` (default) |
| **Output Directory** | `.next` (default) |

### 3. Environment Variables

Adicione as variáveis no dashboard: **Settings → Environment Variables**

| Variável | Environments | Descrição |
|----------|--------------|-----------|
| `NEXT_PUBLIC_SUPABASE_URL` | Production, Preview, Development | URL da API do Supabase |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Production, Preview, Development | Chave pública do Supabase |

> ⚠️ **Segurança**: Variáveis com prefixo `NEXT_PUBLIC_` são expostas no browser. Para variáveis sensíveis (server-side only), não use esse prefixo.

---

## Fluxo de Deploy Automático

A Vercel configura automaticamente CI/CD com seu Git:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Push para PR   │ ──► │  Preview Deploy │ ──► │ URL de Preview  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                   (Testar aqui)
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Merge → main   │ ──► │ Production Deploy│ ──► │ URL de Produção │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Tipos de Deploy

| Ação Git | Resultado | URL |
|----------|-----------|-----|
| Push para branch (não-main) | Preview Deploy | `projeto-branch-hash.vercel.app` |
| Pull Request | Preview Deploy + Comentário no PR | Link direto no PR |
| Push/Merge para `main` | Production Deploy | `projeto.vercel.app` ou domínio customizado |

---

## Configurações Avançadas

### Mudar Branch de Produção

Por padrão, `main` é a branch de produção. Para mudar:

1. **Settings → Git → Production Branch**
2. Altere para a branch desejada (ex: `production`)

### Domínio Customizado

1. **Settings → Domains**
2. Adicione seu domínio (ex: `app.seudominio.com`)
3. Configure o DNS conforme instruído:
   - **CNAME**: Para subdomínios
   - **A Record**: Para domínio raiz

### Ambiente de Staging

Para criar um ambiente intermediário entre Preview e Production:

1. Crie branch `staging` no Git
2. Em **Settings → Domains**, adicione `staging.seudominio.com`
3. Associe o domínio à branch `staging`
4. Adicione Environment Variables específicas para staging

---

## Troubleshooting

### Build falhou

```bash
# Verificar localmente primeiro
cd frontend
npm run build
```

Erros comuns:
- TypeScript errors → Corrigir tipos
- ESLint errors → `npm run lint`
- Dependência faltando → `npm install`

### Variável de ambiente não funciona

- Verifique se adicionou para o environment correto (Production/Preview/Development)
- Para `NEXT_PUBLIC_*`, requer rebuild após mudança
- No dashboard: Settings → Environment Variables → Verificar valores

### Preview não aparece no PR

- Verifique se a Vercel App tem permissão no repositório
- Em repositórios privados: commit author precisa ser membro do time Vercel

---

## Rollback

Se um deploy quebrou produção:

1. Acesse **Deployments** no dashboard
2. Encontre o último deploy funcionando
3. Clique nos **3 pontos (...)** → **Promote to Production**

O rollback é instantâneo (não precisa rebuild).

---

## Custos

| Plano | Limite | Custo |
|-------|--------|-------|
| **Hobby** | 1 projeto pessoal, 100GB bandwidth | Grátis |
| **Pro** | Projetos ilimitados, 1TB bandwidth, times | $20/mês por membro |

> Para projetos comerciais ou em equipe, use **Pro**.

---

## Integração com o Resto da Stack

```
┌─────────────────────────────────────────────────────────┐
│                    VERCEL (Frontend)                     │
│                      Next.js App                         │
└───────────────┬─────────────────────────┬───────────────┘
                │                         │
                ▼                         ▼
┌───────────────────────┐   ┌───────────────────────────────┐
│      SUPABASE         │   │      CLOUD RUN (Workers)       │
│  - Auth               │   │  - Processamento pesado        │
│  - Database           │   │  - Integrações (APIs externas) │
│  - Realtime           │   │  - Tarefas assíncronas         │
└───────────────────────┘   └───────────────────────────────┘
```

- **Chamadas a Supabase**: Direto do frontend (client-side ou SSR)
- **Chamadas a Workers**: Via API routes do Next.js ou diretamente (com CORS configurado)
- **Webhooks do Kestra**: Configurar no Kestra para chamar endpoints do frontend se necessário

---

## Checklist de Deploy

- [ ] `npm run build` passa localmente
- [ ] Environment variables configuradas na Vercel
- [ ] Domínio customizado configurado (se aplicável)
- [ ] CORS configurado nos Workers para aceitar domínio da Vercel
- [ ] Teste de funcionalidade no Preview antes de merge
