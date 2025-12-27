---
description: Planejamento Mestre (Obrigatório antes de codar)
---

# Planejamento do Projeto

> ⚠️ **OBRIGATÓRIO:** Este workflow deve ser rodado logo após o `/setup-projeto`.
> NENHUM código ou banco deve ser criado antes de finalizar este plano.

O objetivo é atuar como **Product Manager e Arquiteto**, entrevistando o usuário para criar a "Versão 1.0" da documentação.

---

## Fase 1: Escopo e Produto

1. **Entrevista:**
   - Perguntar: "O que vamos construir? Qual o problema principal e quem são os usuários?"
   - Perguntar: "Quais são as funcionalidades essenciais para o MVP?"

2. **Gerar Documento:**
   - Criar `docs/specs/1_PRODUTO/ESCOPO_GERAL.md`
   - Conteúdo:
     - Visão Geral
     - Personas
     - Funcionalidades do MVP
     - O que NÃO está no escopo (neste momento)

---

## Fase 2: Arquitetura e Fluxos

1. **Definir Estratégia:**
   - Analisar `docs/arquitetura/PADROES_FLUXO.md` e sugerir o padrão (A, B ou C).
   - "Para o fluxo de X, recomendo o Padrão B (Kestra) porque..."

2. **Gerar Documento:**
   - Criar `docs/specs/2_ARQUITETURA/FLUXOS_NEGOCIO.md`
   - Conteúdo:
     - Diagrama de Fluxo (Mermaid)
     - Lista de Workers necessários
     - Lista de Flows necessários
     - Integrações externas (APIs, Webhooks)

---

## Fase 3: Dados (A Base de Tudo)

1. **Modelagem:**
   - Propor tabelas, campos e relacionamentos.
   - **Regra:** Usar UUIDs, `created_at` em todas as tabelas.
   - **Regra:** Planejar RLS (Row Level Security) desde o início.

2. **Gerar Documento:**
   - Criar `docs/specs/3_DADOS/MODELAGEM_DADOS.md`
   - Conteúdo:
     - Diagrama ER (Mermaid)
     - Esquema SQL proposto
     - Políticas de Acesso (RLS)

---

## Fase 4: Interface (Se tiver Frontend)

1. **Perguntar:** "Quais telas são necessárias?" (Login, Dashboard, Listagem, Detalhe...)

2. **Gerar Documento:**
   - Criar `docs/specs/4_INTERFACE/TELAS_APP.md`
   - Conteúdo:
     - Mapa do Site (Sitemap)
     - Descrição de cada tela e quais dados consome
     - Rotas do Next.js esperadas (`/app/dashboard`, etc)

---

## Fase 5: Validação Final

1. **Perguntar ao Usuário:**
   - "O plano está completo? Posso salvar esses documentos como nossa 'Bíblia' do projeto?"

2. **Próximos Passos:**
   - Se aprovado:
     - "Agora você pode rodar `/criar-banco` (ele vai ler o arquivo MODELAGEM_DADOS.md)"
     - "Depois rode `/criar-worker` para implementar os workers definidos."
