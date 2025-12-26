# Setup Inicial

Guia para configurar a infraestrutura do zero.

---

## Pré-requisitos

- [ ] Conta Google (para Google Cloud)
- [ ] Conta GitHub
- [ ] Docker instalado localmente
- [ ] Git instalado

---

## Fase 1: Google Cloud

### 1.1. Criar Projeto

1. Acesse [console.cloud.google.com](https://console.cloud.google.com)
2. Criar novo projeto
3. Anotar o **Project ID**

### 1.2. Habilitar APIs

```bash
gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  pubsub.googleapis.com \
  cloudscheduler.googleapis.com \
  compute.googleapis.com \
  logging.googleapis.com \
  errorreporting.googleapis.com
```

### 1.3. Configurar Billing

1. Billing → Manage billing accounts
2. Vincular projeto ao billing
3. **IMPORTANTE:** Criar Budget Alert de $10

---

## Fase 2: VM para Kestra

### ⚠️ IMPORTANTE: Escolha da VM

| Tipo | RAM | Custo | Recomendação |
|------|-----|-------|--------------|
| e2-micro | 1GB | $0 | ❌ NÃO USE - OOM Kills |
| **e2-medium** | 4GB | ~$25/mês | ✅ **USE ESTE** |

### 2.1. Criar VM e2-medium

```bash
gcloud compute instances create kestra-server \
  --machine-type=e2-medium \
  --zone=us-central1-a \
  --image-project=debian-cloud \
  --image-family=debian-11 \
  --boot-disk-size=30GB \
  --tags=http-server,https-server
```

### 2.2. Criar Firewall Rules

```bash
gcloud compute firewall-rules create allow-kestra \
  --allow tcp:8080 \
  --target-tags=http-server
```

### 2.3. SSH na VM

```bash
gcloud compute ssh kestra-server --zone=us-central1-a
```

### 2.4. Instalar Docker

```bash
# Na VM:
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Sair e entrar de novo
```

### 2.5. Subir Kestra

```bash
# Criar docker-compose.yml
cat << 'EOF' > docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:14-alpine
    volumes:
      - postgres-data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: kestra
      POSTGRES_USER: kestra
      POSTGRES_PASSWORD: kestra
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U kestra"]
      interval: 10s
      timeout: 5s
      retries: 5

  kestra:
    image: kestra/kestra:latest
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      KESTRA_CONFIGURATION: |
        datasources:
          postgres:
            url: jdbc:postgresql://postgres:5432/kestra
            driverClassName: org.postgresql.Driver
            username: kestra
            password: kestra
        kestra:
          repository:
            type: postgres
          queue:
            type: postgres
          storage:
            type: local
            local:
              base-path: /app/storage
    volumes:
      - kestra-data:/app/storage
    ports:
      - "8080:8080"
    command: server standalone

volumes:
  postgres-data:
  kestra-data:
EOF

# Subir
docker compose up -d
```

### 2.6. Acessar Kestra

- URL: `http://[IP-EXTERNO-DA-VM]:8080`
- Para ver IP: `gcloud compute instances describe kestra-server --zone=us-central1-a --format='get(networkInterfaces[0].accessConfigs[0].natIP)'`

---

## Fase 3: Discord Webhook

### 3.1. Criar Webhook

1. Discord → Servidor → Settings → Integrations
2. Webhooks → New Webhook
3. Copiar URL

### 3.2. Testar

```bash
curl -X POST "SUA_URL_WEBHOOK" \
  -H "Content-Type: application/json" \
  -d '{"content": "🚀 Teste de integração!"}'
```

---

## Fase 4: Conectar GitHub

### 4.1. Cloud Build + GitHub

1. Cloud Console → Cloud Build → Triggers
2. Connect Repository → GitHub
3. Autorizar

### 4.2. Criar Trigger de Teste

Depois de ter um worker, criar trigger que faz deploy automático.

---

## Fase 5: Primeiro Deploy de Teste

### 5.1. Criar worker de teste

```bash
cp -r workers/_template workers/hello-world
# Editar workers/hello-world/main.py (manter simples)
```

### 5.2. Deploy manual (para testar)

```bash
cd workers/hello-world
gcloud run deploy hello-world \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --max-instances=5 \
  --memory=512Mi
```

> ⚠️ **CIRCUIT BREAKER FINANCEIRO**: O `--max-instances=5` evita escalabilidade infinita acidental.
> Um bug com retry infinito pode gerar fatura de milhares de reais sem esse limite!


### 5.3. Testar

```bash
curl https://hello-world-xxx.run.app/health
```

---

## Checklist Final

- [ ] Projeto Google Cloud criado
- [ ] APIs habilitadas
- [ ] Budget Alert configurado
- [ ] VM com Kestra rodando
- [ ] Kestra acessível via navegador
- [ ] Discord Webhook funcionando
- [ ] GitHub conectado ao Cloud Build
- [ ] Worker de teste deployado
