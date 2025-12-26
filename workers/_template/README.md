# Worker: TODO_WORKER_NAME

## Descrição

Descreva o que este worker faz.

## Endpoints

| Método | Path | Descrição |
|--------|------|-----------|
| GET | `/health` | Health check |
| POST | `/` | Endpoint principal |

## Variáveis de Ambiente

| Variável | Obrigatório | Descrição |
|----------|-------------|-----------|
| `SUPABASE_URL` | Sim | URL do Supabase |
| `SUPABASE_SERVICE_KEY` | Sim | Service key do Supabase |
| `DISCORD_WEBHOOK_URL` | Não | Webhook para notificações |

## Testar Localmente

```bash
# Criar arquivo .env
cp .env.example .env
# Editar com suas credenciais

# Build
docker build -t test .

# Run
docker run -p 8080:8080 --env-file .env test

# Testar
curl http://localhost:8080/health
curl -X POST http://localhost:8080/ -H "Content-Type: application/json" -d '{}'
```

## Deploy

O deploy é automático via Cloud Build ao fazer push para main.

```bash
git add .
git commit -m "feat: descrição"
git push
```

## Exemplo de Request

```json
{
  "campo1": "valor",
  "campo2": 123
}
```

## Exemplo de Response

```json
{
  "success": true,
  "message": "Processado com sucesso",
  "data": {}
}
```
