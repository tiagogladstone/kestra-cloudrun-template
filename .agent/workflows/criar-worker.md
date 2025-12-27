---
description: Como criar um novo worker para Cloud Run
---

# Criar Novo Worker

## Pré-requisitos

- **Planejamento Realizado:** O arquivo `docs/specs/2_ARQUITETURA/FLUXOS_NEGOCIO.md` DEVE existir.
  - Se não existir, dizer: "Não posso criar worker sem saber a arquitetura. Rode /planejar-projeto primeiro."
- Repositório já configurado
- Template `workers/_template` existe
- Docker instalado localmente

## Passos

### 1. Copiar template

```bash
cp -r workers/_template workers/{nome-do-worker}
```

Nomenclatura: `{dominio}-{acao}` (ex: `hotmart-sync`, `whatsapp-sender`)

### 2. Editar main.py

Alterar a lógica do endpoint `/`:
- Manter estrutura de erro
- Manter endpoint `/health`
- Incluir imports dos módulos

### 3. Atualizar requirements.txt

Adicionar dependências necessárias para este worker específico.

### 4. Atualizar README.md

Documentar:
- O que o worker faz
- Variáveis de ambiente necessárias
- Como testar

### 5. Testar local
// turbo

```bash
# DA RAIZ DO PROJETO (não de dentro do worker!)
docker build -f workers/{nome-do-worker}/Dockerfile -t test .
docker run -p 8080:8080 --env-file workers/{nome-do-worker}/.env test
```

### 6. Testar endpoints

```bash
# Health check
curl http://localhost:8080/health

# Endpoint principal
curl -X POST http://localhost:8080/ -H "Content-Type: application/json" -d '{}'
```

### 7. Commit e push

```bash
git add workers/{nome-do-worker}
git commit -m "feat: worker {nome-do-worker}"
git push
```

### 8. Deploy via TAG

> ⚠️ O CI/CD só dispara com TAGs, não com push normal!

```bash
git tag worker-{nome-do-worker}-v1
git push origin worker-{nome-do-worker}-v1
```

### 9. Verificar deploy

- Cloud Build executa automaticamente após a TAG
- Verificar logs no Google Cloud Console
- Testar URL de produção

## Checklist

- [ ] Copiou template
- [ ] Editou main.py
- [ ] Atualizou requirements.txt
- [ ] Atualizou README.md
- [ ] Testou local
- [ ] Commit e push
- [ ] Verificou deploy
