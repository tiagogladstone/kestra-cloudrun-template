---
description: Planejar nova funcionalidade (Requisitos + Banco de Dados + Fluxo)
---

# Planejamento de Feature

Este workflow guia o Agente IA para atuar como **Product Manager e Arquiteto de Software**.
O objetivo é transformar uma ideia vaga do usuário em um plano técnico executável.

# Planejamento de Feature (Incremental)

Este workflow é para adicionar **NOVAS funcionalidades** em um projeto já existente.
Se você está começando o projeto agora, use `/planejar-projeto` (Planejamento Mestre).

## Fase 1: Entrevista de Produto (Discovery)

1. **Perguntar ao usuário:**
   - "Qual o objetivo desta nova funcionalidade?"
   - "Ela altera fluxos existentes ou cria novos?"

## Fase 2: Atualização de Documentação (Specs)

1. **Ler documentação atual:**
   - `docs/specs/1_PRODUTO/ESCOPO_GERAL.md`
   - `docs/specs/2_ARQUITETURA/FLUXOS_NEGOCIO.md`
   - `docs/specs/3_DADOS/MODELAGEM_DADOS.md`

2. **Propor alterações (Diff):**
   - "Para essa feature, precisamos alterar tabela X e criar worker Y."

3. **Atualizar Arquivos de Specs:**
   - O Agente deve editar os arquivos markdown em `docs/specs/` refletindo as mudanças.
   - **Regra:** A documentação deve estar sempre atualizada antes de codar.

## Fase 3: Próximos Passos

1. **Após atualizar os specs, o usuário pode rodar:**
   - `/criar-banco` (vai ler o spec atualizado)
   - `/criar-worker` (vai implementar a lógica)
