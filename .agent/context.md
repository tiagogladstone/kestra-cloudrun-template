# Contexto do Repositório: PROJETO BASE (TEMPLATE)

**Última Atualização:** 25/12/2024
**Tipo de Repositório:** 📦 Template / Boilerplate

---

## 🤖 Para Agentes de IA (Leia com Atenção)

Este não é um projeto comum. Este é o **PROJETO BASE (MÃE)** a partir do qual outros projetos de automação serão criados.

### Seu Objetivo ao Trabalhar Aqui
Manter a infraestrutura base saudável, atualizada e com documentação impecável para que os projetos filhos nasçam com qualidade.

### Regras de Manutenção do Template
1.  **Generalização:** Nunca commitar regras de negócio específicas de um cliente aqui. O código aqui deve ser genérico (`TODO_CLIENTE`, `example`).
2.  **Documentação First:** Se você alterar uma linha de código em `modules/` ou `workers/`, você OBRIGATORIAMENTE deve atualizar a documentação em `docs/`.
3.  **Retrocompatibilidade:** Lembre-se que projetos antigos foram criados com versões anteriores deste template. Evite mudanças que quebrem a estrutura fundamental sem um bom motivo.

---

## Estrutura Atual

- **`.agent/`**: Seu cérebro. Workflows, regras e conexões MCP.
  - `MCP_CONNECTIONS.md`: **Lista de integrações diretas (Supabase, etc.)**
- **`docs/`**: A verdade absoluta sobre como as coisas funcionam.
- **`modules/`**: Código Python compartilhado. Se alterar aqui, afeta todos os workers futuros.
- **`workers/`**: Templates e workers reais.
- **`flows/`**: Templates e flows do Kestra.

---

## 🔌 Conexões MCP (IMPORTANTE!)

O Agente possui **acesso direto** a serviços externos via MCP:

| Serviço | Status | O que pode fazer |
|---------|--------|------------------|
| **Supabase** | ✅ Conectado | Criar tabelas, executar SQL, verificar segurança |

Consulte `.agent/MCP_CONNECTIONS.md` para lista completa de ferramentas.

---

## Estado Atual (To-Do de Melhorias no Template)

- [x] Definir arquitetura Kestra + Cloud Run
- [x] Criar templates de Worker e Flow
- [x] Criar sistema de CI/CD (`cloudbuild.yaml`)
- [x] Resolver imports Python (`Dockerfile`)
- [ ] Criar testes unitários para os módulos base
- [ ] Criar script de setup interativo (em progresso via Workflow)

---

## Decisões Arquiteturais (ADR)

| ID | Decisão | Status | Motivo |
|----|---------|--------|--------|
| ADR-01 | **Kestra Self-Hosted** | Aceito | Custo menor que SaaS, controle total. VM e2-medium mínima. |
| ADR-02 | **Monorepo** | Aceito | Facilita gestão de múltiplos workers pequenos. |
| ADR-03 | **Python/FastAPI** | Aceito | Melhor DX para IA gerar código. |
| ADR-04 | **Shared Modules** | Aceito | Copiados via Dockerfile no build para evitar complexidade de PyPI privado. |
| ADR-05 | **Secret Manager** | Mandatório | `.env` proibido em produção por segurança. |

---

## Origem do Projeto

> **Para projetos criados a partir deste template:**
> Preencha esta seção ao iniciar um novo projeto.

| Campo | Valor |
|-------|-------|
| Template | `github.com/seu-usuario/template-kestra-cloudrun` |
| Versão do Template | `1.0.0` |
| Data de Criação | `YYYY-MM-DD` |
| Criado por | `Nome / Agente IA` |
