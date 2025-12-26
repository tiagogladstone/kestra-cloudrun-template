# Template de Documentação de API

Copie este arquivo e preencha para documentar uma nova API.

---

# API: [Nome da API]

## Informações Gerais

| Campo | Valor |
|-------|-------|
| **Base URL** | `https://api.exemplo.com/v1` |
| **Autenticação** | Bearer Token / API Key / OAuth |
| **Rate Limit** | X requests/minuto |
| **Documentação Oficial** | [Link](url) |

---

## Credenciais

| Variável | Onde Conseguir | Onde Salvar |
|----------|----------------|-------------|
| `API_KEY` | Dashboard → API | Secret Manager |
| `API_SECRET` | Dashboard → API | Secret Manager |

---

## Autenticação

```python
import httpx

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
```

---

## Endpoints que Usamos

### 1. [Nome do Endpoint]

```
POST /endpoint
```

**Headers:**
```json
{
  "Authorization": "Bearer {token}",
  "Content-Type": "application/json"
}
```

**Body:**
```json
{
  "campo1": "valor",
  "campo2": 123
}
```

**Response (sucesso):**
```json
{
  "id": "abc123",
  "status": "success"
}
```

**Response (erro):**
```json
{
  "error": "invalid_request",
  "message": "Descrição do erro"
}
```

### 2. [Outro Endpoint]

```
GET /outro-endpoint/{id}
```

...

---

## Webhooks que Recebemos

### Evento: [Nome do Evento]

**URL que configuramos:** `https://nosso-worker.run.app/webhook`

**Payload:**
```json
{
  "event": "nome_evento",
  "data": {
    ...
  }
}
```

---

## Exemplos de Código

### Chamada Básica

```python
import httpx

async def buscar_dados(id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.exemplo.com/v1/recurso/{id}",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        response.raise_for_status()
        return response.json()
```

### Com Tratamento de Erro

```python
import httpx
from modules.error_handler import ErrorHandler

handler = ErrorHandler()

async def buscar_dados_seguro(id: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.exemplo.com/v1/recurso/{id}",
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        handler.capture(e, context={"endpoint": "buscar_dados", "id": id})
        raise
```

---

## Limitações e Gotchas

⚠️ **[Título do Gotcha 1]**
Descrição do problema e como evitar.

⚠️ **[Título do Gotcha 2]**
Descrição do problema e como evitar.

---

## Histórico de Mudanças

| Data | Mudança | Autor |
|------|---------|-------|
| YYYY-MM-DD | Documentação criada | Nome |
