---
description: Planejar nova funcionalidade (Requisitos + Banco de Dados + Fluxo)
---

# Planejamento de Feature

Este workflow guia o Agente IA para atuar como **Product Manager e Arquiteto de Software**.
O objetivo é transformar uma ideia vaga do usuário em um plano técnico executável.

## Fase 1: Entrevista de Produto (Discovery)

1. **Perguntar ao usuário:**
   - "Qual o objetivo principal desta nova funcionalidade?"
   - "Quem vai usar? (Admin, usuário final, sistema externo)"
   - "Quais dados precisam ser armazenados?"
   - "Existe alguma integração externa necessária (API, Webhook)?"

2. **Refinar Requisitos:**
   - Analisar as respostas.
   - Se houver ambiguidades, fazer perguntas de esclarecimento.
   - "Exemplo: Quando você diz 'notificar o usuário', é por email, whatsapp ou push?"

## Fase 2: Modelagem de Dados (Schema)

1. **Propor Estrutura de Banco de Dados:**
   - Criar um diagrama ER (em texto/mermaid) ou lista de tabelas.
   - Definir campos chaves e tipos.
   - IMPORTANTE: Seguir padrões do Supabase (RLS, UUIDs).

2. **Validar com Usuário:**
   - "Esta estrutura de dados faz sentido para você? Falta algum campo?"

## Fase 3: Desenho do Fluxo

1. **Definir Padrão de Fluxo:**
   - Consultar `docs/arquitetura/PADROES_FLUXO.md`.
   - Classificar em Padrão A, B ou C.
   - Justificar a escolha.

2. **Esboçar Componentes:**
   - Listar quais Workers serão criados/alterados.
   - Listar quais Flows do Kestra serão criados.
   - Listar quais telas do Frontend serão necessárias.

## Fase 4: Saída (Deliverable)

1. **Gerar Documento de Especificação:**
   - Criar arquivo: `docs/specs/[nome-da-feature].md`
   - Conteúdo:
     - Resumo
     - Modelagem de Dados (SQL Draft)
     - Diagrama de Fluxo
     - Lista de Tarefas (Checklist)

2. **Perguntar:**
   - "O plano está aprovado? Posso iniciar o setup do banco de dados com /criar-banco?"
