# Guia de Contribuição

Obrigado por querer contribuir com este template! 🎉

## Como Contribuir

### 1. Reportar Bugs ou Sugerir Melhorias

Abra uma Issue no GitHub descrevendo:
- O que aconteceu (ou o que você gostaria)
- Passos para reproduzir (se bug)
- Impacto esperado

### 2. Contribuir com Código

1. Fork o repositório
2. Crie uma branch: `git checkout -b feat/minha-melhoria`
3. Faça suas alterações seguindo os padrões
4. Teste localmente
5. Commit seguindo Conventional Commits: `git commit -m "feat: adiciona X"`
6. Abra um Pull Request

## Padrões de Código

### Python
- Usar type hints
- Docstrings em funções públicas
- Seguir PEP 8

### Commits
```
feat: nova funcionalidade
fix: correção de bug
docs: documentação
refactor: refatoração
chore: manutenção
```

### Documentação
- Atualizar `docs/` quando alterar comportamento
- Atualizar `CHANGELOG.md` em toda mudança significativa

## Regras de Ouro

1. **Generalização**: Nunca adicionar código específico de cliente no template
2. **Retrocompatibilidade**: Evitar breaking changes sem motivo forte
3. **Documentação First**: Toda mudança deve vir com doc atualizada

## Dúvidas?

Abra uma Issue com a tag `question`.
