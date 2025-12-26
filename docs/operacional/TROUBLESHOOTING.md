# Guia de Troubleshooting
Guia de sobrevivência para quando as coisas quebrarem.

---

## 🚨 Cenários Comuns

### 1. Worker Cloud Run não responde (500 ou 503)

| Sintoma | Causa Provável | Ação Corretiva |
|---------|----------------|----------------|
| **Erro 503** | Cold start muito lento ou Crash no boot | Check Cloud Logging: Filtre por `resource.type="cloud_run_revision"` |
| **Erro 500** | Bug no código Python | Check Error Reporting ou Logs com `severity=ERROR` |
| **Timeout** | Worker demorou > 5 min | Otimizar código ou aumentar timeout no deploy |

**Comando de Debug Rápido:**
```bash
gcloud beta run services logs tail [NOME-DO-WORKER] --project [PROJECT-ID]
```

### 2. Kestra: Flow falhou ou travou

| Sintoma | Causa Provável | Ação Corretiva |
|---------|----------------|----------------|
| **Fica "Running" pra sempre** | Worker não respondeu ou Pub/Sub não enviou ack | Verificar worker logs. Se for Pub/Sub, verifique se está dando `ack()` |
| **Erro "OOM Killed"** | VM sem memória | **CRÍTICO:** Upgrade VM para e2-medium (ver CUSTOS.md) |
| **Falha de Conexão DB** | Supabase pausou (Free tier) | Acessar Supabase Dashboard para "acordar" o projeto |

### 3. Pub/Sub: Mensagens não processadas

1. Verifique se existe uma **Subscription** no tópico:
   ```bash
   gcloud pubsub subscriptions list --filter="topic:projects/[PROJECT]/topics/[TOPICO]"
   ```
   *Se não tiver subscription, a mensagem é perdida!*

2. Verifique se as mensagens estão indo para "Dead Letter Queue" (DLQ).

---

## 🔍 Como investigar um problema (Passo a Passo)

### Passo 1: Pegue o ID da Execução (Correlation ID)
No Kestra UI, copie o ID da execução que falhou (ex: `4829g10-abc`).

### Passo 2: Rastreie no Cloud Logging
Cole o ID na busca do Google Cloud Logging.
```
textPayload:"4829g10-abc" OR jsonPayload.correlation_id="4829g10-abc"
```
Isso mostrará todos os logs do Kestra E dos Workers relacionados.

### Passo 3: Verifique Métricas
- O Cloud Run bateu no limite de memória?
- O Kestra está com CPU em 100%?

---

## 🛠️ Comandos Úteis de Recuperação

### Reiniciar Kestra (na VM)
```bash
ssh kestra-server
docker compose restart kestra
```

### Rollback de Worker
Se o deploy novo quebrou tudo:
1. Vá no Cloud Run Console
2. Aba "Revisions"
3. Clique na versão anterior (ex: `worker-00020`)
4. Clique em "Manage Traffic" -> Envie 100% para ela.

### Limpar Fila Pub/Sub (Emergência)
Se um loop infinito encheu a fila:
```bash
gcloud pubsub subscriptions seek [SUBSCRIPTION_ID] --time=$(date +%Y-%m-%dT%H:%M:%S)
```
*(Isso descarta todas as mensagens atuais!)*
