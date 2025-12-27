---
description: Verificar e aplicar atualizações do template base
---

# Atualizar Template

Este workflow ajuda projetos filhos a se manterem atualizados com melhorias do template mãe.

## Quando Usar

- Quando o template mãe receber uma nova versão
- Periodicamente (ex: a cada 3 meses) para verificar atualizações

## Fase 1: Verificar Versão Atual

1. Ler o arquivo `VERSION` do projeto atual
2. Comparar com a versão mais recente do template (perguntar ao usuário ou verificar repo)
3. Se estiver desatualizado, informar: "Você está na versão X.X.X, a mais recente é Y.Y.Y"

## Fase 2: Consultar CHANGELOG

1. Ler o `CHANGELOG.md` do template atualizado
2. Listar mudanças entre a versão atual e a nova
3. Destacar breaking changes (se houver)

## Fase 3: Identificar Arquivos para Atualizar

Arquivos que geralmente podem ser atualizados sem conflito:
- `.agent/rules/` (regras gerais)
- `.agent/workflows/` (novos workflows)
- `modules/` (módulos compartilhados)
- `docs/arquitetura/` (documentação de referência)

Arquivos que provavelmente têm customização e precisam merge manual:
- `workers/` (tem código específico do projeto)
- `flows/` (tem flows específicos)
- `.agent/rules/context.md` (tem estado específico do projeto)

## Fase 4: Aplicar Atualizações

1. Para cada arquivo seguro, perguntar: "Atualizar X? (S/n)"
2. Para arquivos com conflito potencial, mostrar diff e perguntar como proceder
3. Atualizar arquivo `VERSION` para a nova versão

## Conclusão

- Listar o que foi atualizado
- Pedir para testar localmente antes de commitar
