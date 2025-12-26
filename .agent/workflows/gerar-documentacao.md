---
description: Gerar e atualizar documentação do projeto automaticamente
---

# Gerar Documentação

Este workflow serve para manter a documentação viva e sincronizada com o código.

## Quando rodar?
- Após terminar uma feature grande.
- Antes de um deploy importante.
- Quando um novo dev entrar no time.

## Fase 1: Atualização do README Principal

1. **Revisar `README.md`:**
   - O Quick Start ainda funciona?
   - As tecnologias listadas estão corretas?
   - Os links para a `docs/` estão quebrados?

## Fase 2: Documentação de Workers

1. **Escanear `workers/`:**
   - Para cada pasta de worker, verificar se existe `README.md`.
   - Se não existir, CRIAR com base no template.
   - Se existir, verificar se os endpoints e variáveis de ambiente estão atualizados com o `main.py`.

## Fase 3: Documentação de Flows

1. **Escanear `flows/`:**
   - Listar todos os flows.
   - Atualizar `docs/arquitetura/CATALOGO_FLOWS.md` (criar se não existir).
   - Tabela com: Nome do Flow, O que faz, Trigger, Workers que usa.

## Fase 4: Documentação de API

1. **Atualizar `docs/apis/`:**
   - Se houver integração com API externa nova, criar doc usando `docs/apis/_template.md`.

## Conclusão

- Commit as alterações de documentação com prefixo `docs: ...`
