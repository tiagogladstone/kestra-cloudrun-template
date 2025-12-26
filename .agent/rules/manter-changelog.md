---
trigger: always
description: Manter changelog e versão atualizados no projeto base (template)
---

# Regra: Manter Changelog Atualizado

> ⚠️ **Esta regra só se aplica ao PROJETO BASE (TEMPLATE)**
> Quando um projeto derivado for criado, esta regra deve ser REMOVIDA.

## Quando Atualizar

O Agente DEVE atualizar `CHANGELOG.md` e `VERSION` quando:

1. **Adicionar** novo workflow, módulo, ou documentação significativa
2. **Alterar** comportamento de workflows ou módulos existentes
3. **Corrigir** bugs ou problemas documentados
4. **Remover** funcionalidades ou depreciar algo

## Como Atualizar

### VERSION (Versionamento Semântico)
- `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes (estrutura incompatível)
- **MINOR**: Novas funcionalidades (compatível)
- **PATCH**: Correções de bugs

### CHANGELOG.md
Seguir formato [Keep a Changelog](https://keepachangelog.com/):

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Adicionado
- Nova funcionalidade X

### Alterado
- Mudança em Y

### Corrigido
- Bug Z

### Removido
- Funcionalidade W (deprecada)
```

## Lembrete

Antes de fazer `git push` com mudanças significativas, perguntar:
- "Devo atualizar o CHANGELOG e VERSION para refletir essas mudanças?"
