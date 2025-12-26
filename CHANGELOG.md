# Changelog

Todas as mudanças notáveis deste projeto serão documentadas aqui.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

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
- ADR-01: Kestra Self-Hosted (e2-medium mínimo)
- ADR-02: Monorepo para workers
- ADR-03: Python/FastAPI para workers
- ADR-04: Módulos compartilhados via Dockerfile COPY
- ADR-05: Secret Manager obrigatório em produção
