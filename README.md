# 🚀 Stack de Automação: Kestra + Google Cloud Run

**Versão:** 1.3.0

---

## 🤖 PARA O AGENTE IA (SISTEMA VIVO)

Este projeto é um **SISTEMA VIVO**. Sua função é manter a ordem e a evolução contínua.

### Ciclo de Vida Obrigatório
1.  **Planejar (Plan)**: NUNCA crie código sem antes atualizar a documentação em `docs/specs/`.
2.  **Atualizar (Update)**: Mantenha `task.md` e `CHANGELOG.md` sempre sincronizados com o estado atual.
3.  **Executar (Execute)**: Use os workflows `/criar-*` apenas quando o plano estiver aprovado.
4.  **Verificar (Verify)**: Teste localmente antes de pedir deploy.

> **Regra de Ouro:** Se o usuário pedir uma feature nova, rode `/planejar-feature` (incremental) ou `/planejar-projeto` (se for o início). **Não pule o planejamento.**

---

## 👋 PARA VOCÊ QUE ESTÁ COMEÇANDO

### Em qual etapa você está?

| Etapa | Comando para o Agente | O que vai acontecer |
|-------|----------------------|---------------------|
| **1. Acabei de baixar o template** | `/setup-projeto` | Configura Git, Google Cloud, Kestra |
| **2. Infra pronta, quero planejar** | `/planejar-projeto` | **OBRIGATÓRIO:** Define Escopo, Fluxos e Dados |
| **3. Preciso criar o banco** | `/criar-banco` | Gera SQL baseado no plano de dados |
| **4. Preciso criar um worker** | `/criar-worker` | Cria worker baseado no plano de arquitetura |
| **5. Preciso criar um flow** | `/criar-flow` | Cria flow YAML do Kestra |
| **6. Preciso criar o frontend** | `/criar-frontend` | Configura Next.js |
| **7. Preciso atualizar docs** | `/gerar-documentacao` | Atualiza README e docs |

> **Dica:** Basta dizer ao Agente: *"Execute /setup-projeto"* e ele te guia.

---

## 🔄 PADRÕES DE FLUXO (Importante!)

| Padrão | Quando Usar | Caminho |
|--------|-------------|---------|
| **A: Direto** | Simples, 1 ação, rápido | Front → Cloud Run → Supabase |
| **B: Orquestrado** | Multi-etapas, retry visual | Front → Kestra → Cloud Run(s) → Supabase |
| **C: Com Fila** | Alto volume (1000+), rate limit | Front → Pub/Sub → Cloud Run → Supabase |

> **Regra de Ouro:** Comece com Padrão A. Só adicione Kestra (B) ou Fila (C) quando precisar.

---

## ☁️ KESTRA: CLOUD OU SELF-HOSTED?

| Opção | Custo | Prós | Contras |
|-------|-------|------|---------|
| **Kestra Cloud** | $0-99/mês | Sem VM, menos manutenção | Limite de execuções no free |
| **Self-Hosted** | ~$25/mês (VM) | Controle total, sem limites | Você cuida da VM |

> O `/setup-projeto` pergunta qual opção você prefere.

---

## 📖 O QUE É ESTE PROJETO?

Uma stack de automação que substitui n8n + Docker Swarm por:
- **Kestra** → Orquestrador visual (Cloud ou Self-Hosted)
- **Cloud Run** → Workers Python/FastAPI
- **Pub/Sub** → Filas com retry
- **Supabase** → Banco de dados
- **Vercel** → Frontend

---

## 💰 QUANTO CUSTA?

| Componente | USD/mês | R$/mês |
|------------|---------|--------|
| Kestra Cloud (free tier) | $0 | R$ 0 |
| Kestra Self-Hosted (VM) | ~$25 | ~R$ 165 |
| Cloud Run + Pub/Sub | $0-5 | R$ 0-33 |
| Supabase | $0-25 | R$ 0-165 |
| **TOTAL** | **~$0-60** | **~R$ 0-400** |

---

## 📚 DOCUMENTAÇÃO DETALHADA

| Preciso de... | Onde está |
|---------------|-----------|
| Visão geral da arquitetura | `docs/arquitetura/VISAO_GERAL.md` |
| Padrões de fluxo (A, B, C) | `docs/arquitetura/PADROES_FLUXO.md` |
| Setup manual passo a passo | `docs/operacional/SETUP_INICIAL.md` |
| Deploy do frontend | `docs/operacional/DEPLOY_VERCEL.md` |
| Análise de custos | `docs/arquitetura/CUSTOS.md` |
| Riscos e mitigações | `docs/arquitetura/RISCOS.md` |

---

## ⚠️ REGRAS IMPORTANTES

1. **Deploy via TAG**: `git tag worker-NOME-v1 && git push origin worker-NOME-v1`
2. **Circuit Breaker**: Sempre usar `--max-instances=5` no Cloud Run
3. **Segredos**: Usar Google Secret Manager, não `.env` em produção
4. **Correlation ID**: Todo flow Kestra passa `X-Correlation-ID`

---

## 🔗 LINKS

- [Kestra Cloud](https://kestra.io/pricing)
- [Kestra Docs](https://kestra.io/docs)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [Supabase Docs](https://supabase.com/docs)
