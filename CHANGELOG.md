# Changelog

Todas as mudanças notáveis deste projeto serão documentadas aqui.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.2.0] - 2024-12-26

### Adicionado
- Guia de troubleshooting Google Cloud (`docs/operacional/TROUBLESHOOTING_GCP.md`)
- Verificação de billing obrigatória antes de habilitar APIs (Fase 3.3)
- Verificação de permissões (Owner/Editor) no projeto (Fase 3.4)
- Comando para confirmar APIs ativas após habilitação (Fase 3.6)

### Alterado
- Fase 3 do `/setup-projeto` agora habilita APIs uma por vez (facilita diagnóstico)
- Nome da API corrigido: `errorreporting` → `clouderrorreporting`

### Corrigido
- Frontmatter de rules agora usa `trigger: always_on` corretamente

---

## [1.1.1] - 2024-12-26

### Corrigido
- Criado arquivo `context.md` dentro de `.agent/rules/` (antes não existia, causando criação no lugar errado)
- Workflow `/setup-projeto` agora especifica caminho completo `.agent/rules/context.md`
- Workflow `/atualizar-template` corrigido para referenciar `.agent/rules/context.md`

---

## [1.1.0] - 2024-12-26

### Adicionado
- Workflow `/atualizar-template` para projetos filhos sincronizarem com o template
- Documentação de deploy Vercel (`docs/operacional/DEPLOY_VERCEL.md`)
- Fase 5 (Deploy Vercel) no workflow `/criar-frontend`
- Integração com Supabase MCP nos workflows `/criar-banco` e `/setup-projeto`
- Regra `contexto-template.md` com informações de MCP

### Alterado
- Workflows agora usam MCP do Supabase para executar SQL diretamente
- Reorganizado `.agent/` - arquivos soltos movidos para `rules/`
- Adicionadas pastas `database/migrations/`, `database/seed/`, `frontend/` com .gitkeep

### Corrigido
- Sintaxe de secrets no Kestra (removido `$` antes de `{{ secret() }}`)
- Comando de build Docker nos workflows (executar da raiz do projeto)
- Deploy via TAGs documentado corretamente

## [1.0.0] - 2024-12-26

### Adicionado
- Estrutura inicial do template
- 7 workflows para Agente IA (`/setup-projeto`, `/planejar-feature`, `/criar-banco`, `/criar-worker`, `/criar-flow`, `/criar-frontend`, `/gerar-documentacao`)
- Templates de Worker (Python/FastAPI) e Flow (Kestra)
- Módulos compartilhados: `error_handler`, `notify`, `supabase_client`, `queue`
- CI/CD com Cloud Build (`cloudbuild.yaml`)
- Documentação completa em `docs/`
- Rules do projeto em `.agent/rules/`

### Decisões Arquiteturais
- ADR-01: Kestra Cloud ou Self-Hosted (escolha do usuário)
- ADR-02: Monorepo para workers
- ADR-03: Python/FastAPI para workers
- ADR-04: Módulos compartilhados via Dockerfile COPY
- ADR-05: Secret Manager obrigatório em produção
