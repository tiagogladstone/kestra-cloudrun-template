# ⚠️ ARQUIVO HISTÓRICO ⚠️

> **NOTA:** Este documento contém todo o racional da migração, mas pode estar desatualizado em detalhes técnicos.
> - Para custos reais, veja `docs/arquitetura/CUSTOS.md`
> - Para setup, veja `docs/operacional/SETUP_INICIAL.md`
> - Para riscos, veja `docs/arquitetura/RISCOS.md`

---

# 🚀 Nova Stack: Kestra + Google Cloud Run

**Autor:** Tiago Gladstone  
**Data:** 25/12/2024  
**Status:** Em Refinamento  
**Abordagem:** Criar novos projetos na nova stack (não migrar fluxos existentes)

---

## 📋 Sumário

1. [Filosofia da Nova Stack](#filosofia-da-nova-stack)
2. [Arquitetura Definida](#arquitetura-definida)
3. [Stack Tecnológica Completa](#stack-tecnológica-completa)
4. [🔥 Padrões de Fluxo (Quando Usar O Quê)](#padrões-de-fluxo-quando-usar-o-quê)
5. [🔥 Estratégia de Filas (Pub/Sub)](#estratégia-de-filas-pubsub)
6. [Módulos Reutilizáveis](#módulos-reutilizáveis)
7. [Estrutura de Pastas (Monorepo)](#estrutura-de-pastas-monorepo)
8. [Fluxo de Trabalho](#fluxo-de-trabalho)
9. [Custos Estimados](#custos-estimados)
10. [Roadmap de Implementação](#roadmap-de-implementação)
11. [Decisões Tomadas](#decisões-tomadas)

---

## 🧠 Filosofia da Nova Stack

### Princípios

1. **IA-First**: Todo código é gerado por IA, você é o orquestrador
2. **Modular**: Componentes reutilizáveis entre projetos
3. **Paralelo**: Nova stack roda lado a lado com n8n existente
4. **Visual + Código**: Kestra dá a visibilidade, Google Cloud dá a execução

### Abordagem de Migração

```
❌ NÃO: Migrar fluxos n8n existentes
✅ SIM: Criar novos projetos na nova stack
✅ SIM: Aprender como funciona em paralelo
✅ SIM: Migrar gradualmente quando se sentir confortável
```

---

## 🏗️ Arquitetura Definida

### Visão Geral

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              NOVA STACK                                      │
│                                                                              │
│   ┌─────────────┐                                                           │
│   │   VERCEL    │  Frontend (React/Next.js)                                 │
│   │  (Frontend) │  Dispara eventos para Supabase                            │
│   └──────┬──────┘                                                           │
│          │                                                                   │
│          ▼                                                                   │
│   ┌─────────────┐                                                           │
│   │  SUPABASE   │  Banco de dados + Realtime                                │
│   │   (Banco)   │  Single Source of Truth                                   │
│   └──────┬──────┘                                                           │
│          │ Webhook / Edge Function                                          │
│          ▼                                                                   │
│   ┌─────────────┐                                                           │
│   │   KESTRA    │  Orquestrador Visual                                      │
│   │   (Flows)   │  Substitui n8n com versionamento Git                      │
│   └──────┬──────┘                                                           │
│          │ Chama workers                                                     │
│          ▼                                                                   │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      GOOGLE CLOUD                                    │   │
│   │                                                                      │   │
│   │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│   │   │  Cloud Run   │  │   Pub/Sub    │  │   Cloud      │              │   │
│   │   │  (Workers)   │  │   (Filas)    │  │  Scheduler   │              │   │
│   │   │  Python/     │  │  Rate limit  │  │  (Cron)      │              │   │
│   │   │  FastAPI     │  │  Retry auto  │  │              │              │   │
│   │   └──────────────┘  └──────────────┘  └──────────────┘              │   │
│   │                                                                      │   │
│   │   ┌──────────────┐  ┌──────────────┐                                │   │
│   │   │   Error      │  │    Cloud     │     Observabilidade            │   │
│   │   │  Reporting   │  │   Logging    │                                │   │
│   │   └──────────────┘  └──────────────┘                                │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                        MÓDULOS COMUNS                                │   │
│   │   📦 notify-discord   📦 error-handler   📦 supabase-client         │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
│   ┌─────────────┐                                                           │
│   │   GITHUB    │  Versionamento de tudo (código + flows YAML)              │
│   └─────────────┘                                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Comparativo: Antes vs Depois

| Componente | Antes (n8n) | Depois (Nova Stack) |
|------------|-------------|---------------------|
| **Orquestrador** | n8n (visual, JSON) | Kestra (visual, YAML versionável) |
| **Logs de Erro** | n8n → Canal | Módulo Discord + Google Error Reporting |
| **Logs Estruturais** | Sentry | Google Error Reporting |
| **Execução** | n8n nodes | Cloud Run (Python/FastAPI) |
| **Filas** | n8n internal | Pub/Sub |
| **Cron** | n8n scheduler | Cloud Scheduler → Kestra |
| **Infra** | Docker Swarm + Traefik + Portainer | 100% Google Cloud |
| **Banco** | Supabase | Supabase (mantém) |
| **Frontend** | Vercel | Vercel (mantém) |
| **Versionamento** | GitHub | GitHub (mantém) |

---

## 🛠️ Stack Tecnológica Completa

### Camadas

| Camada | Tecnologia | Função |
|--------|------------|--------|
| **Frontend** | Vercel (Next.js/React) | Interface do usuário |
| **Banco** | Supabase (PostgreSQL + Realtime) | Single Source of Truth |
| **Orquestração** | Kestra | Fluxos visuais, versionados em YAML |
| **Execução** | Google Cloud Run | Workers Python/FastAPI |
| **Filas** | Google Pub/Sub | Processamento assíncrono, rate limiting |
| **Scheduler** | Google Cloud Scheduler | Cron jobs (tarefas agendadas) |
| **Logs** | Google Cloud Logging | Centralização de logs |
| **Erros** | Google Error Reporting | Agrupamento e alertas de erros |
| **Alertas** | Discord Webhook (modular) | Notificações em tempo real |
| **CI/CD** | Cloud Build + GitHub | Deploy automático |
| **Código** | Python (FastAPI) | Gerado 100% por IA |

### Por que Python (FastAPI)?

| Critério | Por que Python |
|----------|----------------|
| **IA-friendly** | LLMs geram Python melhor que qualquer linguagem |
| **Legibilidade** | Fácil para você (orquestrador) revisar |
| **Bibliotecas** | httpx, supabase-py, google-cloud-* |
| **Kestra** | Plugins Python nativos e robustos |
| **FastAPI** | Moderno, tipado, documentação automática |

---

## 🔥 Padrões de Fluxo (Quando Usar O Quê)

Esta é a **decisão arquitetural mais importante**. Definimos 3 padrões de fluxo baseados na complexidade:

### Visão Geral dos Padrões

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           PADRÕES DE FLUXO                                       │
│                                                                                  │
│  PADRÃO A: DIRETO (Simples)           PADRÃO B: ORQUESTRADO (Complexo)          │
│  ───────────────────────              ─────────────────────────────             │
│  Front/Webhook                        Front/Webhook                              │
│       │                                    │                                     │
│       ▼                                    ▼                                     │
│  Supabase (trigger)                   Kestra (orquestrador)                      │
│       │                                    │                                     │
│       ▼                                    ├──────┬──────┬──────┐                │
│  Cloud Run (worker)                        ▼      ▼      ▼      ▼                │
│       │                               Worker1  Worker2  Worker3  ...             │
│       ▼                                    │                                     │
│  Supabase (resultado)                      ▼                                     │
│                                       Supabase (resultado)                       │
│                                                                                  │
│  PADRÃO C: COM FILA (Massa)                                                      │
│  ────────────────────────                                                        │
│  Front/Webhook                                                                   │
│       │                                                                          │
│       ▼                                                                          │
│  Cloud Run (dispatcher)                                                          │
│       │                                                                          │
│       ▼                                                                          │
│  Pub/Sub (fila)  ←── Rate limit, retry automático                                │
│       │                                                                          │
│       ▼                                                                          │
│  Cloud Run (worker) ←── Processa 1 item por vez                                  │
│       │                                                                          │
│       ▼                                                                          │
│  Supabase (resultado)                                                            │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Padrão A: DIRETO (Simples)

**Quando usar:**
- ✅ Operação única e rápida (< 30 segundos)
- ✅ Não precisa de retry visual/manual
- ✅ Não tem dependência de outros passos
- ✅ Log de erro é suficiente (não precisa ver "onde parou")

**Fluxo:**
```
Frontend → Supabase (trigger) → Cloud Run → Supabase (resultado)
```

**Exemplos:**
- Cadastrar cliente e buscar dados de API externa
- Processar webhook de pagamento
- Gerar e salvar um cálculo

**Implementação:**
```
1. Frontend salva no Supabase
2. Supabase Edge Function / Webhook dispara
3. Cloud Run processa e salva resultado
4. Frontend recebe via Supabase Realtime
```

---

### Padrão B: ORQUESTRADO (Complexo)

**Quando usar:**
- ✅ Múltiplos passos dependentes
- ✅ Precisa de retry visual (ver onde falhou)
- ✅ Tem lógica condicional (if/else)
- ✅ Precisa de aprovação manual no meio
- ✅ Quer histórico visual de execuções

**Fluxo:**
```
Frontend → Kestra (orquestra) → Cloud Run (workers) → Supabase
```

**Exemplos:**
- Onboarding de cliente: criar conta → buscar Hotmart → enviar email → criar grupo WhatsApp
- Processamento de pedido: validar → cobrar → gerar NF → enviar
- Qualquer coisa com "se der erro, espera 1h e tenta de novo"

**Implementação:**
```yaml
# flows/onboarding/novo-cliente.yaml
id: onboarding-novo-cliente
namespace: clientes

tasks:
  - id: buscar_hotmart
    type: io.kestra.plugin.scripts.python.Script
    script: |
      # Chama worker no Cloud Run
      response = httpx.post("https://hotmart-sync-xxx.run.app/processar")
      
  - id: enviar_email
    type: io.kestra.plugin.scripts.python.Script
    dependsOn: [buscar_hotmart]
    script: |
      # Só executa se o anterior deu certo
      
  - id: notificar_discord
    type: io.kestra.plugin.scripts.python.Script
    dependsOn: [enviar_email]
```

---

### Padrão C: COM FILA (Massa/Assíncrono)

**Quando usar:**
- ✅ Processar muitos itens (10+)
- ✅ Precisa de rate limiting (evitar ban)
- ✅ Pode demorar (minutos a horas)
- ✅ Precisa de retry automático por item
- ✅ Não quer travar quem disparou

**Fluxo:**
```
Trigger → Dispatcher (joga na fila) → Pub/Sub → Worker (processa 1)
```

**Exemplos:**
- Enviar 1000 mensagens WhatsApp
- Processar 500 linhas de planilha
- Sincronizar 200 clientes de API externa

**Implementação:** Ver seção [Estratégia de Filas](#estratégia-de-filas-pubsub)

---

### Tabela de Decisão Rápida

| Situação | Padrão | Usa Kestra? | Usa Pub/Sub? |
|----------|--------|-------------|--------------|
| Webhook simples (1 ação) | A | ❌ | ❌ |
| Cadastro + busca API | A | ❌ | ❌ |
| Onboarding multi-etapas | B | ✅ | ❌ |
| Fluxo com aprovação manual | B | ✅ | ❌ |
| Disparo 1000 mensagens | C | Opcional | ✅ |
| Sincronização em massa | C | Opcional | ✅ |
| Onboarding + disparo massa | B + C | ✅ | ✅ |

### Regra de Ouro

> **Comece simples (Padrão A). Só adicione complexidade quando precisar.**
> 
> - Precisa ver onde parou? → Adiciona Kestra (B)
> - Precisa processar muitos? → Adiciona Pub/Sub (C)
> - Precisa dos dois? → Kestra orquestra, Pub/Sub executa

---

## 🔥 Estratégia de Filas (Pub/Sub)

### Filosofia

O Pub/Sub é usado para **processamento em massa com resiliência**. Padronizamos tudo para consistência.

### Anatomia de uma Fila

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          PUB/SUB ANATOMY                                 │
│                                                                          │
│   ┌──────────────┐                                                       │
│   │  DISPATCHER  │  Cloud Run que recebe o gatilho                       │
│   │              │  Publica N mensagens no tópico                        │
│   └──────┬───────┘                                                       │
│          │                                                               │
│          ▼                                                               │
│   ┌──────────────┐                                                       │
│   │   TÓPICO     │  Nome: {dominio}-{acao}                               │
│   │              │  Ex: whatsapp-enviar, hotmart-sincronizar             │
│   └──────┬───────┘                                                       │
│          │                                                               │
│          ▼                                                               │
│   ┌──────────────┐                                                       │
│   │ SUBSCRIPTION │  Nome: {dominio}-{acao}-sub                           │
│   │              │  Configurações:                                       │
│   │              │  • Push para URL do Worker                            │
│   │              │  • Ack deadline: 600s (10min)                         │
│   │              │  • Retry: exponential backoff                         │
│   └──────┬───────┘                                                       │
│          │                                                               │
│          ▼                                                               │
│   ┌──────────────┐                                                       │
│   │   WORKER     │  Cloud Run que processa 1 item                        │
│   │              │  Retorna 200 (sucesso) ou 500 (retry)                 │
│   └──────────────┘                                                       │
└─────────────────────────────────────────────────────────────────────────┘
```

### Padrão de Nomenclatura

| Componente | Padrão | Exemplo |
|------------|--------|---------|
| **Tópico** | `{dominio}-{acao}` | `whatsapp-enviar` |
| **Subscription** | `{dominio}-{acao}-sub` | `whatsapp-enviar-sub` |
| **Dispatcher** | `{dominio}-dispatcher` | `whatsapp-dispatcher` |
| **Worker** | `{dominio}-worker` | `whatsapp-worker` |

### Estrutura da Mensagem (Padrão)

Todas as mensagens Pub/Sub seguem este schema:

```json
{
  "id": "uuid-unico",
  "timestamp": "2024-12-25T23:00:00Z",
  "source": "whatsapp-dispatcher",
  "type": "enviar-mensagem",
  "data": {
    "contato_id": "123",
    "telefone": "5511999999999",
    "mensagem": "Olá, seu código é 456",
    "template": "boas_vindas"
  },
  "metadata": {
    "user_id": "tiago",
    "job_id": "job-abc123",
    "retry_count": 0
  }
}
```

### Módulo de Fila (Reutilizável)

```python
# modules/queue/publisher.py
from google.cloud import pubsub_v1
import json
import os

class QueuePublisher:
    def __init__(self, topic_name: str):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(
            os.environ['GCP_PROJECT_ID'],
            topic_name
        )
    
    def publish(self, message_type: str, data: dict, metadata: dict = None):
        """Publica uma mensagem padronizada no tópico"""
        import uuid
        from datetime import datetime
        
        message = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": os.environ.get('SERVICE_NAME', 'unknown'),
            "type": message_type,
            "data": data,
            "metadata": metadata or {}
        }
        
        future = self.publisher.publish(
            self.topic_path,
            json.dumps(message).encode('utf-8')
        )
        return future.result()  # Retorna message_id
    
    def publish_batch(self, message_type: str, items: list, metadata: dict = None):
        """Publica múltiplas mensagens de uma vez"""
        message_ids = []
        for item in items:
            msg_id = self.publish(message_type, item, metadata)
            message_ids.append(msg_id)
        return message_ids
```

```python
# modules/queue/consumer.py
from fastapi import FastAPI, Request
import json
import base64

def decode_pubsub_message(request_body: dict) -> dict:
    """Decodifica mensagem vinda do Pub/Sub Push"""
    pubsub_message = request_body.get("message", {})
    data = pubsub_message.get("data", "")
    decoded = base64.b64decode(data).decode("utf-8")
    return json.loads(decoded)

# Uso no Worker:
@app.post("/")
async def process(request: Request):
    body = await request.json()
    message = decode_pubsub_message(body)
    
    # message agora tem: id, timestamp, source, type, data, metadata
    contato = message["data"]
    
    # Processa...
    return {"status": "ok"}
```

### Configurações de Rate Limiting

Para evitar ban de APIs (ex: WhatsApp):

| Configuração | Onde | Valor Sugerido |
|--------------|------|----------------|
| **Max Instances** | Cloud Run Worker | 1 (força sequencial) |
| **Concurrency** | Cloud Run Worker | 1 (1 msg por vez) |
| **Min Backoff** | Pub/Sub Subscription | 10s |
| **Max Backoff** | Pub/Sub Subscription | 600s (10 min) |

Para processamento rápido (sem rate limit):

| Configuração | Onde | Valor Sugerido |
|--------------|------|----------------|
| **Max Instances** | Cloud Run Worker | 10-100 |
| **Concurrency** | Cloud Run Worker | 10 |

### Monitoramento de Filas

O Google Cloud Console mostra automaticamente:
- Mensagens pendentes (backlog)
- Taxa de processamento
- Erros e retries
- Latência média

Alertar no Discord se:
- Backlog > 1000 mensagens (fila crescendo)
- Taxa de erro > 10%
- Latência > 5 minutos

---

## 📦 Módulos Reutilizáveis

### Filosofia: Criar uma vez, usar sempre

Cada módulo é um pacote Python que pode ser importado em qualquer worker.

### 1. Módulo de Notificação (Discord)

```
📂 modules/notify/
├── discord.py      # Envia para Discord
├── telegram.py     # (futuro) Envia para Telegram
├── whatsapp.py     # (futuro) Envia para WhatsApp
└── __init__.py     # Exporta interface comum
```

**Uso:**
```python
from modules.notify import discord

discord.send(
    webhook_url=os.environ['DISCORD_WEBHOOK'],
    title="✅ Processamento Concluído",
    message="1000 mensagens enviadas com sucesso",
    color="success"  # success, error, warning, info
)
```

### 2. Módulo de Tratamento de Erros

```
📂 modules/error_handler/
├── handler.py      # Captura e processa erros
├── google.py       # Envia para Google Error Reporting
└── __init__.py
```

**Uso:**
```python
from modules.error_handler import ErrorHandler

handler = ErrorHandler(
    discord_webhook=os.environ['DISCORD_WEBHOOK'],
    service_name="hotmart-sync"
)

try:
    processar_dados()
except Exception as e:
    handler.capture(e, context={"cliente_id": 123})
    raise  # Re-levanta para Pub/Sub fazer retry
```

### 3. Módulo de Cliente Supabase

```
📂 modules/supabase_client/
├── client.py       # Cliente configurado
├── queries.py      # Queries comuns
└── __init__.py
```

**Uso:**
```python
from modules.supabase_client import get_client

supabase = get_client()  # Já configurado com env vars
data = supabase.table('clientes').select('*').execute()
```

---

## 📁 Estrutura de Pastas (Monorepo)

```plaintext
minha-stack/
│
├── 📂 frontend/                    # Vercel (auto-deploy)
│   ├── src/
│   ├── package.json
│   └── vercel.json
│
├── 📂 database/                    # Scripts SQL do Supabase
│   ├── migrations/
│   │   ├── 001_tabela_clientes.sql
│   │   └── 002_tabela_envios.sql
│   └── seed.sql
│
├── 📂 flows/                       # Kestra Flows (YAML versionado)
│   ├── hotmart/
│   │   ├── sync-vendas.yaml
│   │   └── processar-compra.yaml
│   ├── whatsapp/
│   │   ├── disparo-massa.yaml
│   │   └── enviar-boas-vindas.yaml
│   └── _templates/
│       └── flow-base.yaml
│
├── 📂 modules/                     # Módulos Python reutilizáveis
│   ├── notify/
│   │   ├── __init__.py
│   │   ├── discord.py
│   │   └── telegram.py
│   ├── error_handler/
│   │   ├── __init__.py
│   │   └── handler.py
│   ├── supabase_client/
│   │   ├── __init__.py
│   │   └── client.py
│   └── requirements.txt
│
├── 📂 workers/                     # Cloud Run Services
│   │
│   ├── 📂 hotmart-sync/            # Worker: Sincronizar Hotmart
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── cloudbuild.yaml
│   │
│   ├── 📂 zap-dispatcher/          # Worker: Joga 1000 msgs na fila
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── 📂 zap-worker/              # Worker: Envia 1 msg (lê da fila)
│       ├── main.py
│       ├── Dockerfile
│       └── requirements.txt
│
├── 📂 infra/                       # Scripts de infraestrutura
│   ├── setup_gcp.sh               # Habilita APIs do Google
│   ├── setup_pubsub.sh            # Cria tópicos e subscriptions
│   └── setup_permissions.sh       # Configura IAM
│
├── 📂 docs/                        # Documentação
│   ├── arquitetura.md
│   ├── como-criar-worker.md
│   └── como-criar-flow.md
│
├── .gitignore
├── README.md
└── docker-compose.yaml             # Para rodar Kestra local (dev)
```

---

## 🔄 Fluxo de Trabalho

### Cenário 1: Webhook (Tempo Real)

```
1. Hotmart envia webhook de compra
         │
         ▼
2. Kestra recebe e orquestra
   ├── Valida dados
   ├── Chama Cloud Run (processar-compra)
   └── Atualiza Supabase
         │
         ▼
3. Cloud Run processa
   ├── Busca cliente no Supabase
   ├── Cria registro de compra
   └── Retorna sucesso/erro
         │
         ▼
4. Kestra continua o flow
   └── Se sucesso: chama próximo passo
   └── Se erro: notifica Discord + retry
```

### Cenário 2: Disparo em Massa (1000+ mensagens)

```
1. Frontend seta flag no Supabase: "disparar = true"
         │
         ▼
2. Kestra detecta (via polling ou webhook)
   └── Chama Cloud Run (zap-dispatcher)
         │
         ▼
3. Dispatcher (Cloud Run)
   ├── Busca 1000 contatos no Supabase
   ├── Publica 1000 msgs no Pub/Sub
   └── Encerra (2 segundos)
         │
         ▼
4. Pub/Sub entrega uma por uma ao Worker
   ├── Rate limit: 1 msg a cada 5s (configurável)
   └── Retry automático se falhar
         │
         ▼
5. Worker (Cloud Run)
   ├── Envia 1 msg via API WhatsApp
   ├── Atualiza status no Supabase
   └── Se erro → Discord + retry pelo Pub/Sub
         │
         ▼
6. Supabase Realtime
   └── Frontend atualiza progresso (50/1000...)
```

### Cenário 3: Cron Job (Agendado)

```
1. Cloud Scheduler dispara às 8h
         │
         ▼
2. Kestra Flow "relatorio-diario"
   ├── Chama Cloud Run (gerar-relatorio)
   ├── Salva PDF no Storage
   └── Notifica Discord com link
```

---

## 💰 Custos Estimados

### Seu Custo Atual: R$ 150/mês (~$30 USD)

Para rodar: n8n, Portainer, manager nodes, Redis, bancos, Traefik, etc.

### 🏆 ONDE RODAR O KESTRA: Análise Completa

#### Opção 1: Kestra Cloud (SaaS) - RECOMENDADO PARA COMEÇAR

| Característica | Detalhes |
|----------------|----------|
| **Custo** | $0 (Free tier) ou planos pagos |
| **Gestão** | Zero (eles cuidam de tudo) |
| **Robustez** | Alta (infraestrutura enterprise) |
| **Escalabilidade** | Automática |
| **Cold Start** | Não tem (sempre ligado) |

**Prós:**
- ✅ Não precisa gerenciar nada
- ✅ Sempre online, sem cold start
- ✅ Atualizações automáticas
- ✅ Free tier para começar

**Contras:**
- ⚠️ Free tier pode ter limites
- ⚠️ Dados na nuvem deles (não sua)

---

#### Opção 2: Google Cloud VM (E2-micro/small) - MAIS CONTROLE

| Tipo | vCPU | RAM | Custo Mensal | Nota |
|------|------|-----|--------------|------|
| **E2-micro** | 0.25 | 1 GB | **$0** (Free Tier!) | Gratuito em us-west1, us-central1, us-east1 |
| **E2-small** | 0.5 | 2 GB | ~$8-15/mês (~R$40-75) | Bom para produção |
| **E2-medium** | 1 | 4 GB | ~$25-30/mês (~R$125-150) | Se precisar mais poder |

**Free Tier do Google Cloud:**
- ✅ 1x E2-micro **GRÁTIS POR MÊS** (forever, não só 1 ano!)
- ✅ Regiões: Oregon, Iowa, South Carolina
- ✅ 30 GB de disco Standard
- ✅ 1 GB de egress/mês

**Prós:**
- ✅ Controle total
- ✅ E2-micro é grátis forever
- ✅ Dados na sua conta
- ✅ Pode rodar outras coisas junto

**Contras:**
- ⚠️ Precisa gerenciar a VM (atualizações, monitoramento)
- ⚠️ E2-micro pode ser apertado para Kestra em produção pesada

---

#### Opção 3: Cloud Run (Serverless) - NÃO RECOMENDADO para Kestra

| Problema | Por quê? |
|----------|----------|
| Cold Start | 5-15 segundos para acordar |
| Webhooks | Kestra precisa receber webhooks, cold start atrasa |
| Estado | Kestra mantém estado, Cloud Run é stateless |

**Veredito:** Cloud Run é perfeito para os **workers**, mas NÃO para o Kestra em si.

---

### 🎯 RECOMENDAÇÃO ATUALIZADA: Self-Hosted desde o Início

#### Por que NÃO começar no Kestra Cloud?

| Você disse | Implicação |
|------------|------------|
| "Testar a gestão" | Precisa aprender a gerenciar VM/infra |
| "Clientes grandes" | Vão querer infra própria |
| Você é consultor | Precisa saber fazer, não só usar |

#### A Estratégia Certa para Você

```
┌─────────────────────────────────────────────────────────────────┐
│                   APRENDER FAZENDO                               │
│                                                                  │
│   Fase 1: SEU AMBIENTE (Aprendizado)                            │
│   ─────────────────────────────────                             │
│   • VM E2-micro (GRÁTIS) no Google Cloud                        │
│   • Kestra self-hosted (Docker)                                 │
│   • Você aprende: Docker, VM, gestão, monitoramento             │
│                                                                  │
│   Fase 2: CLIENTE PEQUENO                                        │
│   ─────────────────────────                                     │
│   • Oferece Kestra Cloud (se aceitar) → menos trabalho          │
│   • OU replica sua infra (VM + Kestra) → você já sabe fazer     │
│                                                                  │
│   Fase 3: CLIENTE GRANDE (Infra Dedicada)                        │
│   ─────────────────────────────────────                         │
│   • VM dedicada no GCP deles ou seu                             │
│   • Kestra self-hosted                                          │
│   • Você já domina porque praticou no seu ambiente              │
└─────────────────────────────────────────────────────────────────┘
```

#### Portabilidade dos Flows (Zero Lock-in)

```
┌─────────────────────────────────────────────────────────────────┐
│                    KESTRA É 100% PORTÁVEL                        │
│                                                                  │
│   Kestra Cloud ◄────────────────────────► Kestra Self-Hosted    │
│         │                                        │               │
│         └──────────► MESMO YAML ◄────────────────┘               │
│                     MESMO GIT                                    │
│                     ZERO RETRABALHO                              │
│                                                                  │
│   Flows são arquivos YAML no GitHub.                            │
│   Mudar de Cloud para Self-Hosted = apontar para o mesmo repo.  │
└─────────────────────────────────────────────────────────────────┘
```

#### Setup Recomendado (Self-Hosted)

| Componente | Onde Roda | Custo |
|------------|-----------|-------|
| **Kestra** | VM E2-micro (Google) | $0 (free tier) |
| **PostgreSQL** (banco do Kestra) | Mesmo VM ou Cloud SQL | $0-15 |
| **Workers** | Cloud Run | $0 (free tier) |
| **Filas** | Pub/Sub | $0 (free tier) |

**Custo total para aprender: $0/mês** (usando free tier)

#### O que você VAI APRENDER gerenciando:

1. **Docker Compose** - Como subir Kestra + PostgreSQL
2. **Nginx/Traefik** - Proxy reverso (você já sabe!)
3. **SSL/HTTPS** - Let's Encrypt automático
4. **Backups** - Banco de dados do Kestra
5. **Monitoramento** - Health checks, alertas
6. **Atualizações** - Como atualizar Kestra sem downtime

#### Quando um Cliente Grande Pedir Infra Própria

Você já vai ter:
- ✅ Docker Compose pronto
- ✅ Scripts de setup automatizados
- ✅ Documentação de como fazer
- ✅ **Experiência real de operação**

```
Cliente: "Quero Kestra rodando na minha infra da AWS"
Você: "Sem problema, já fiz isso várias vezes. 
       Preciso de uma VM com 2GB RAM, Docker instalado,
       e acesso ao console. Em 2 horas está rodando."
```

---

### 📊 Comparativo: Cloud vs Self-Hosted para seu caso

| Critério | Kestra Cloud | Kestra Self-Hosted |
|----------|--------------|-------------------|
| Custo para começar | $0 | $0 (E2-micro free) |
| Gestão | Zero | Você aprende |
| Preparação para clientes grandes | ❌ Não aprende | ✅ Aprende fazendo |
| Portabilidade | ✅ Sim | ✅ Sim |
| **Recomendação para você** | ❌ | ✅ **ESSE** |

### 🎓 Conclusão

> **Para quem quer só USAR: Kestra Cloud**
> **Para quem quer SABER FAZER (você): Self-Hosted**

Você está construindo uma habilidade, não só um projeto.

---

### 📊 Custo Total da Nova Stack

#### Cenário Conservador (Sempre Funciona)

| Componente | Custo Mensal | Nota |
|------------|--------------|------|
| **Kestra** | $0-15 | Cloud free ou VM E2-small |
| **Cloud Run** | $0 | Free tier cobre muito |
| **Pub/Sub** | $0 | Free tier (10GB) |
| **Cloud Build** | $0 | Free tier (120 min/dia) |
| **Error Reporting** | $0 | Free tier |
| **Cloud Scheduler** | $0 | 3 jobs grátis |
| **Supabase** | $0-25 | Já usa, mantém |
| **Vercel** | $0 | Já usa, mantém |
| **TOTAL** | **$0-40/mês** | **R$ 0-200** |

#### Comparativo: Antes vs Depois

| Item | Hoje (Swarm) | Nova Stack | Economia |
|------|--------------|------------|----------|
| Infraestrutura | R$ 150/mês | R$ 0-75/mês | **50-100%** |
| Gestão | Manual (Swarm, Traefik, Portainer) | Zero | ∞ horas |
| Escalabilidade | Manual | Automática | - |
| Robustez | Depende de você | Google cuida | - |

---

### 🔥 Cenário Mais Econômico Possível

```
┌─────────────────────────────────────────────────────────────┐
│                   STACK 100% GRÁTIS                          │
│                                                              │
│   Kestra Cloud (Free) ───────────────────── $0              │
│   Cloud Run (Free Tier) ─────────────────── $0              │
│   Pub/Sub (Free Tier) ───────────────────── $0              │
│   Cloud Build (Free Tier) ───────────────── $0              │
│   Error Reporting (Free Tier) ───────────── $0              │
│   Supabase (Free Tier) ──────────────────── $0              │
│   Vercel (Free Tier) ────────────────────── $0              │
│   ───────────────────────────────────────────────           │
│   TOTAL MENSAL: $0                                          │
│                                                              │
│   ⚠️ Limitações:                                             │
│   • Supabase free: 500MB banco, 1GB storage                 │
│   • Kestra Cloud free: pode ter limites de execuções        │
│   • Cloud Run: 2M requests/mês (muito!)                     │
└─────────────────────────────────────────────────────────────┘
```

### 💡 Dicas de Economia

1. **Budget Alert**: Configurar alarme se passar de R$ 50/mês
2. **Regiões Free**: Usar us-central1, us-east1, us-west1 para free tier
3. **Crédito Inicial**: Google dá $300 de crédito para novos usuários
4. **Spot VMs**: Se precisar de VM, usar Spot (60-90% desconto)

---

## 📖 FRAMEWORK COMPLETO: Do Planejamento à Entrega

Esta seção cobre **TODO o ciclo de vida de um projeto**, desde a ideia até a entrega.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CICLO DE VIDA DE UM PROJETO                               │
│                                                                              │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐       │
│   │  FASE 0 │──▶│  FASE 1 │──▶│  FASE 2 │──▶│  FASE 3 │──▶│  FASE 4 │       │
│   │ PLANEJA │   │  INFRA  │   │ PROJETO │   │  BUILD  │   │ ENTREGA │       │
│   └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘       │
│                                                                              │
│   Ideia →       Setup →       Repo →        Código →      Cliente →         │
│   Escopo        Google        Supabase      Workers       Handoff           │
│   Tasks         VM/Kestra     Vercel        Flows         Suporte           │
│                 Discord       Namespace     Testes                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### 🎯 FASE 0: PLANEJAMENTO

**Antes de tocar em código, PLANEJA.**

```
┌─────────────────────────────────────────────────────────────────┐
│                    FASE 0: PLANEJAMENTO                          │
│                                                                  │
│   ENTRADAS:                                                      │
│   ─────────                                                     │
│   • Ideia do projeto / Brief do cliente                         │
│   • Requisitos funcionais                                       │
│   • Integrações necessárias (APIs, serviços)                    │
│                                                                  │
│   ATIVIDADES:                                                    │
│   ───────────                                                   │
│   1. Entender o problema                                        │
│      ├── Qual dor resolve?                                      │
│      ├── Quem vai usar?                                         │
│      └── Qual o fluxo principal?                                │
│                                                                  │
│   2. Mapear integrações                                          │
│      ├── APIs externas (Hotmart, WhatsApp, etc)                 │
│      ├── Webhooks que precisa receber                           │
│      └── Notificações que precisa enviar                        │
│                                                                  │
│   3. Desenhar arquitetura                                        │
│      ├── Quais workers precisa?                                 │
│      ├── Quais flows (orquestrações)?                           │
│      ├── Precisa de fila? (Padrão C)                            │
│      └── Precisa de Kestra? (Padrão B) ou é simples?           │
│                                                                  │
│   4. Criar lista de TASKS                                        │
│      ├── Dividir em entregas pequenas                           │
│      ├── Priorizar por dependência                              │
│      └── Estimar tempo (com margem!)                            │
│                                                                  │
│   SAÍDAS:                                                        │
│   ───────                                                       │
│   • Documento de escopo (Markdown)                              │
│   • Diagrama de arquitetura (ASCII ou draw.io)                  │
│   • Lista de tasks (pode ser issues no GitHub)                  │
│   • Estimativa de prazo                                         │
│                                                                  │
│   ⏱️ Tempo: 1-4 horas (depende do projeto)                       │
└─────────────────────────────────────────────────────────────────┘
```

**Template de Documento de Planejamento:**

```markdown
# Projeto: [Nome]

## Objetivo
O que esse projeto resolve?

## Integrações
- [ ] API X - Para fazer Y
- [ ] Webhook Z - Receber evento W

## Arquitetura
[Diagrama ASCII ou link para draw.io]

## Workers Necessários
1. `dominio-acao` - Faz X
2. `dominio-acao2` - Faz Y

## Flows (Kestra)
1. `flow-principal` - Orquestra X → Y → Z

## Tasks
- [ ] Setup infra
- [ ] Worker 1
- [ ] Worker 2
- [ ] Flow principal
- [ ] Testes
- [ ] Entrega

## Prazo Estimado
X dias/semanas
```

**Checklist Fase 0:**
- [ ] Entendi o problema
- [ ] Mapeei integrações
- [ ] Desenhei arquitetura
- [ ] Criei lista de tasks
- [ ] Estimei prazo
- [ ] Cliente/Stakeholder aprovou

---

### 🏗️ FASE 1: SETUP DE INFRAESTRUTURA

**Criar tudo que o projeto precisa para existir.**

```
┌─────────────────────────────────────────────────────────────────┐
│                    FASE 1: SETUP DE INFRA                        │
│                                                                  │
│   SE É O PRIMEIRO PROJETO (Setup único):                         │
│   ────────────────────────────────────────                      │
│   1. Conta Google Cloud                                         │
│      ├── Criar conta (ganhar $300 crédito)                      │
│      ├── Criar projeto: "minha-stack" ou "empresa-producao"     │
│      └── Habilitar APIs:                                        │
│          • Cloud Run                                            │
│          • Cloud Build                                          │
│          • Pub/Sub                                              │
│          • Error Reporting                                      │
│          • Cloud Scheduler                                      │
│          • Artifact Registry                                    │
│                                                                  │
│   2. VM para Kestra                                              │
│      ├── Criar VM E2-micro (free) ou E2-small                   │
│      ├── Instalar Docker + Docker Compose                       │
│      ├── Subir Kestra + PostgreSQL                              │
│      ├── Configurar Nginx + SSL (Let's Encrypt)                 │
│      └── Apontar domínio: kestra.seusite.com                    │
│                                                                  │
│   3. Canal de Alertas (Discord)                                  │
│      ├── Criar servidor/canal "Alertas Automação"               │
│      ├── Criar Webhook                                          │
│      └── Testar: enviar mensagem de teste                       │
│                                                                  │
│   4. Repositório Template                                        │
│      ├── Criar repo "stack-template" no GitHub                  │
│      ├── Estrutura de pastas padrão                             │
│      ├── Módulos base (notify, error_handler, etc)              │
│      └── Dockerfile template                                    │
│                                                                  │
│   SE JÁ TEM INFRA (Só adicionar projeto):                        │
│   ─────────────────────────────────────────                     │
│   1. Verificar se Kestra está rodando                           │
│   2. Verificar se Discord webhook está ativo                    │
│   3. Pular para FASE 2                                          │
│                                                                  │
│   ⏱️ Tempo Setup Único: 2-4 horas                                │
│   ⏱️ Tempo Verificação: 5 minutos                                │
└─────────────────────────────────────────────────────────────────┘
```

**Checklist Fase 1 (Setup Único):**
- [ ] Conta Google Cloud criada
- [ ] Projeto GCP criado
- [ ] APIs habilitadas (Cloud Run, Build, Pub/Sub, Error Reporting)
- [ ] VM E2 criada
- [ ] Docker instalado na VM
- [ ] Kestra + PostgreSQL rodando
- [ ] Nginx + SSL configurado
- [ ] Domínio apontando (opcional)
- [ ] Discord webhook criado e testado
- [ ] Repositório template criado
- [ ] Hello World deployado no Cloud Run

---

### 📁 FASE 2: SETUP DO PROJETO

**Criar os recursos específicos DESTE projeto.**

```
┌─────────────────────────────────────────────────────────────────┐
│                    FASE 2: SETUP DO PROJETO                      │
│                                                                  │
│   1. REPOSITÓRIO                                                 │
│      ──────────────                                             │
│      # Clonar template                                          │
│      git clone git@github.com:seuuser/stack-template.git        │
│      mv stack-template nome-do-projeto                          │
│      cd nome-do-projeto                                         │
│      rm -rf .git && git init                                    │
│      git remote add origin git@github.com:seuuser/projeto.git   │
│      git push -u origin main                                    │
│                                                                  │
│   2. SUPABASE                                                    │
│      ──────────                                                 │
│      • Criar projeto no Supabase Dashboard                      │
│      • Ou usar projeto existente do cliente                     │
│      • Rodar migrations iniciais (se tiver)                     │
│      • Anotar:                                                  │
│        - SUPABASE_URL                                           │
│        - SUPABASE_ANON_KEY (frontend)                           │
│        - SUPABASE_SERVICE_KEY (backend)                         │
│                                                                  │
│   3. VERCEL (se tiver frontend)                                  │
│      ────────────────────────────                               │
│      • Criar projeto no Vercel                                  │
│      • Conectar ao repo GitHub (pasta /frontend)                │
│      • Configurar variáveis de ambiente                         │
│      • Deploy automático via git push                           │
│                                                                  │
│   4. NAMESPACE NO KESTRA                                         │
│      ──────────────────────                                     │
│      • Acessar Kestra UI                                        │
│      • Criar namespace: clientes.{nome-cliente}                 │
│      • Ou: projetos.{nome-projeto}                              │
│      • Configurar variáveis do namespace:                       │
│        - SUPABASE_URL                                           │
│        - SUPABASE_SERVICE_KEY                                   │
│        - DISCORD_WEBHOOK (se específico)                        │
│                                                                  │
│   5. CLOUD RUN (preparar)                                        │
│      ─────────────────────                                      │
│      • Configurar Cloud Build trigger:                          │
│        - Monitorar pasta: workers/{nome-worker}                 │
│        - Ao detectar push → build → deploy                      │
│      • Ou fazer deploy manual primeiro:                         │
│        gcloud run deploy nome-worker \                          │
│          --source=./workers/nome-worker \                       │
│          --region=us-central1                                   │
│                                                                  │
│   6. PUB/SUB (se precisar de filas)                              │
│      ─────────────────────────────                              │
│      • Criar tópico: {projeto}-{acao}                           │
│      • Criar subscription: {projeto}-{acao}-sub                 │
│      • Apontar subscription para URL do worker                  │
│                                                                  │
│   ⏱️ Tempo: 30 min - 1 hora                                      │
└─────────────────────────────────────────────────────────────────┘
```

**Checklist Fase 2:**
- [ ] Repositório criado a partir do template
- [ ] Supabase projeto criado/configurado
- [ ] Migrations rodadas (se aplicável)
- [ ] Credenciais Supabase anotadas
- [ ] Vercel projeto criado (se frontend)
- [ ] Namespace Kestra criado
- [ ] Variáveis de ambiente configuradas
- [ ] Cloud Build trigger configurado (ou deploy manual ok)
- [ ] Pub/Sub configurado (se precisar)

---

### 🔨 FASE 3: BUILD (Desenvolvimento)

**Criar os workers, flows e testar.**

```
┌─────────────────────────────────────────────────────────────────┐
│                    FASE 3: BUILD                                 │
│                                                                  │
│   PARA CADA WORKER:                                              │
│   ─────────────────                                             │
│   1. Copiar template                                            │
│      cp -r workers/_template workers/meu-worker                 │
│                                                                  │
│   2. Pedir para IA gerar código                                 │
│      "Altere o main.py para [descrição clara]"                  │
│                                                                  │
│   3. Revisar código gerado                                      │
│      • Faz sentido?                                             │
│      • Tratamento de erro ok?                                   │
│      • Notificação Discord incluída?                            │
│                                                                  │
│   4. Testar local                                               │
│      cd workers/meu-worker                                      │
│      docker build -t test .                                     │
│      docker run -p 8080:8080 --env-file .env test               │
│      curl -X POST http://localhost:8080/                        │
│                                                                  │
│   5. Deploy                                                     │
│      git add . && git commit -m "feat: worker X"                │
│      git push                                                    │
│      # Cloud Build faz o resto                                   │
│                                                                  │
│   6. Testar em produção                                         │
│      curl -X POST https://meu-worker-xxx.run.app/               │
│                                                                  │
│   PARA CADA FLOW (Kestra):                                       │
│   ────────────────────────                                      │
│   1. Criar YAML em /flows/{cliente}/                            │
│                                                                  │
│   2. Definir inputs, tasks, outputs                             │
│                                                                  │
│   3. Conectar aos workers via HTTP                              │
│                                                                  │
│   4. Testar no Kestra UI                                        │
│      • Acessar Flows → Execute                                  │
│      • Passar dados de teste                                    │
│      • Ver logs em tempo real                                   │
│                                                                  │
│   5. Commit do YAML                                             │
│      git add flows/                                              │
│      git commit -m "feat: flow Y"                               │
│      git push                                                    │
│                                                                  │
│   TESTES INTEGRADOS:                                             │
│   ─────────────────                                             │
│   • Testar fluxo completo: trigger → flow → worker → resultado  │
│   • Testar cenário de erro (worker falha, retry funciona?)      │
│   • Verificar se Discord recebe alertas                         │
│                                                                  │
│   ⏱️ Tempo por worker: 15-30 min                                 │
│   ⏱️ Tempo por flow: 10-20 min                                   │
│   ⏱️ Tempo total: depende do escopo                              │
└─────────────────────────────────────────────────────────────────┘
```

**Checklist Fase 3 (por entrega):**
- [ ] Worker criado e testado local
- [ ] Worker deployado no Cloud Run
- [ ] Worker testado em produção
- [ ] Flow criado (se aplicável)
- [ ] Flow testado no Kestra UI
- [ ] Teste integrado ok
- [ ] Erro simulado → Discord recebeu alerta

---

### 📊 FASE 4: MONITORAMENTO E ENTREGA

**Configurar observabilidade e entregar para o cliente/produção.**

```
┌─────────────────────────────────────────────────────────────────┐
│                    FASE 4: MONITORAMENTO & ENTREGA               │
│                                                                  │
│   MONITORAMENTO:                                                 │
│   ────────────────                                              │
│   1. Verificar Error Reporting                                  │
│      • Acessar Google Cloud Console → Error Reporting           │
│      • Verificar se erros estão sendo capturados                │
│      • Configurar alerta por email (opcional)                   │
│                                                                  │
│   2. Verificar Cloud Logging                                    │
│      • Logs dos workers aparecem?                               │
│      • Consegue filtrar por serviço?                            │
│                                                                  │
│   3. Verificar Discord                                          │
│      • Erros chegam no canal?                                   │
│      • Sucessos chegam (se configurado)?                        │
│                                                                  │
│   4. Configurar Budget Alert                                    │
│      • Billing → Budgets → Create Budget                        │
│      • Alertar se passar de $X/mês                              │
│                                                                  │
│   DOCUMENTAÇÃO:                                                  │
│   ─────────────                                                 │
│   1. README do projeto                                          │
│      • O que faz                                                │
│      • Como rodar local                                         │
│      • Variáveis de ambiente necessárias                        │
│      • URLs de produção                                         │
│                                                                  │
│   2. Diagrama de arquitetura                                    │
│      • Atualizar se mudou durante o build                       │
│                                                                  │
│   3. Runbook (se for entregar para cliente)                     │
│      • O que fazer se der erro X                                │
│      • Como reiniciar                                           │
│      • Contatos de suporte                                      │
│                                                                  │
│   ENTREGA:                                                       │
│   ────────                                                      │
│   1. Fazer demonstração para cliente                            │
│      • Mostrar fluxo funcionando                                │
│      • Mostrar onde ver logs/erros                              │
│                                                                  │
│   2. Treinar (se necessário)                                    │
│      • Como usar o sistema                                      │
│      • Como ver status                                          │
│                                                                  │
│   3. Handoff                                                    │
│      • Transferir credenciais (se infra do cliente)             │
│      • Definir modelo de suporte                                │
│                                                                  │
│   ⏱️ Tempo: 1-2 horas                                            │
└─────────────────────────────────────────────────────────────────┘
```

**Checklist Fase 4:**
- [ ] Error Reporting funcionando
- [ ] Cloud Logging acessível
- [ ] Discord recebendo alertas
- [ ] Budget Alert configurado
- [ ] README atualizado
- [ ] Diagrama de arquitetura atualizado
- [ ] Demonstração feita para cliente
- [ ] Treinamento feito (se necessário)
- [ ] Handoff completo

---

### 📋 RESUMO: TODAS AS FASES

```
┌─────────────────────────────────────────────────────────────────┐
│                    VISÃO GERAL DO PROCESSO                       │
│                                                                  │
│   FASE 0: PLANEJAMENTO                    ⏱️ 1-4h                │
│   ─────────────────────                                         │
│   • Entender problema                                           │
│   • Mapear integrações                                          │
│   • Desenhar arquitetura                                        │
│   • Criar tasks                                                  │
│   • OUTPUT: Documento de escopo                                 │
│                                                                  │
│   FASE 1: SETUP INFRA                     ⏱️ 2-4h (1x)          │
│   ──────────────────                                            │
│   • Google Cloud + APIs                                         │
│   • VM + Kestra                                                  │
│   • Discord Webhook                                              │
│   • Repo Template                                                │
│   • OUTPUT: Infra pronta                                        │
│                                                                  │
│   FASE 2: SETUP PROJETO                   ⏱️ 30min-1h           │
│   ────────────────────                                          │
│   • Criar repo do projeto                                       │
│   • Supabase                                                     │
│   • Vercel (se frontend)                                        │
│   • Namespace Kestra                                             │
│   • Cloud Run / Pub/Sub                                          │
│   • OUTPUT: Projeto configurado                                 │
│                                                                  │
│   FASE 3: BUILD                           ⏱️ Depende do escopo  │
│   ───────────                                                   │
│   • Criar workers                                                │
│   • Criar flows                                                  │
│   • Testar                                                       │
│   • OUTPUT: Sistema funcionando                                 │
│                                                                  │
│   FASE 4: MONITORAMENTO & ENTREGA         ⏱️ 1-2h               │
│   ──────────────────────────                                    │
│   • Configurar alertas                                          │
│   • Documentar                                                   │
│   • Entregar                                                     │
│   • OUTPUT: Projeto em produção                                 │
│                                                                  │
│   TOTAL APROXIMADO:                                              │
│   ─────────────────                                             │
│   • Projeto simples: 1-2 dias                                   │
│   • Projeto médio: 1-2 semanas                                  │
│   • Projeto complexo: 2-4 semanas                               │
└─────────────────────────────────────────────────────────────────┘
```

---

### ✅ CHECKLIST MASTER (Copiar e usar)

```markdown
## Checklist: [Nome do Projeto]

### FASE 0: Planejamento
- [ ] Entendimento do problema
- [ ] Mapeamento de integrações
- [ ] Arquitetura desenhada
- [ ] Lista de tasks criada
- [ ] Prazo estimado
- [ ] Cliente/stakeholder aprovou

### FASE 1: Infra (pular se já existe)
- [ ] Conta Google Cloud
- [ ] APIs habilitadas
- [ ] VM com Kestra rodando
- [ ] Discord webhook configurado
- [ ] Repo template pronto

### FASE 2: Setup Projeto
- [ ] Repositório criado
- [ ] Supabase configurado
- [ ] Vercel configurado (se frontend)
- [ ] Namespace Kestra criado
- [ ] Variáveis de ambiente configuradas
- [ ] Cloud Build/Pub/Sub configurado

### FASE 3: Build
- [ ] Worker 1 criado e testado
- [ ] Worker 2 criado e testado
- [ ] Flow 1 criado e testado
- [ ] Teste integrado ok
- [ ] Alertas funcionando

### FASE 4: Entrega
- [ ] Error Reporting ok
- [ ] Budget Alert configurado
- [ ] README atualizado
- [ ] Demonstração feita
- [ ] Handoff completo
```

---

## 🔄 PLAYBOOK: Operações do Dia a Dia

Esta seção cobre **quando você já tem um projeto rodando** e precisa fazer manutenções ou adições.

---

### 🏗️ Setup ÚNICO (Fazer uma vez só)

Antes de criar qualquer projeto, você precisa ter a infraestrutura base:

```
┌─────────────────────────────────────────────────────────────────┐
│                    SETUP ÚNICO (1x na vida)                      │
│                                                                  │
│   1. Conta Google Cloud ─────────────────── Ganhar $300 crédito │
│   2. VM E2-micro ────────────────────────── Kestra self-hosted  │
│   3. Repositório Template ───────────────── Estrutura base      │
│   4. Discord Webhook ────────────────────── Canal de alertas    │
│   5. Domínio (opcional) ─────────────────── kestra.seusite.com  │
│                                                                  │
│   ⏱️ Tempo: 2-4 horas                                            │
│   💰 Custo: $0                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Checklist do Setup Único:**
- [ ] Criar conta Google Cloud
- [ ] Habilitar APIs (Cloud Run, Pub/Sub, Cloud Build, Error Reporting)
- [ ] Criar VM E2-micro com Kestra + PostgreSQL
- [ ] Criar repositório template no GitHub
- [ ] Configurar Discord Webhook para alertas
- [ ] Testar deploy de "Hello World" no Cloud Run

---

### 🚀 NOVO PROJETO: O que fazer?

Quando um cliente novo chega ou você tem uma ideia:

```
┌─────────────────────────────────────────────────────────────────┐
│                    NOVO PROJETO                                  │
│                                                                  │
│   PASSO 1: Criar Repositório                                     │
│   ─────────────────────────                                     │
│   • Usar o template base (estrutura de pastas pronta)           │
│   • Nome: cliente-nome-projeto ou projeto-nome                  │
│   • git clone template → renomear → git push novo repo          │
│                                                                  │
│   PASSO 2: Configurar Supabase                                   │
│   ─────────────────────────────                                 │
│   • Criar projeto no Supabase (ou usar existente do cliente)    │
│   • Rodar migrations da pasta /database                         │
│   • Salvar credenciais no .env (nunca commitar!)                │
│                                                                  │
│   PASSO 3: Criar Namespace no Kestra                             │
│   ────────────────────────────────                              │
│   • Acessar seu Kestra: https://kestra.seusite.com              │
│   • Criar namespace: clientes.nome-cliente                      │
│   • Configurar variáveis de ambiente do namespace               │
│                                                                  │
│   PASSO 4: Primeiro Worker                                       │
│   ────────────────────────                                      │
│   • Copiar template de /workers/_template                       │
│   • Renomear para o caso de uso                                 │
│   • Pedir para IA ajustar a lógica                              │
│   • git push → deploy automático                                │
│                                                                  │
│   PASSO 5: Primeiro Flow                                         │
│   ─────────────────────                                         │
│   • Criar YAML em /flows/nome-cliente/                          │
│   • Conectar ao worker                                          │
│   • Testar no Kestra UI                                         │
│                                                                  │
│   ⏱️ Tempo: 30 min - 2 horas                                     │
└─────────────────────────────────────────────────────────────────┘
```

**Checklist Novo Projeto:**
- [ ] Criar repo a partir do template
- [ ] Configurar Supabase (projeto + migrations)
- [ ] Criar namespace no Kestra
- [ ] Configurar variáveis de ambiente
- [ ] Criar primeiro worker (copiar template)
- [ ] Criar primeiro flow
- [ ] Testar ciclo completo

---

### ⚙️ NOVO WORKER: O que fazer?

Quando precisa de um novo serviço/endpoint:

```
┌─────────────────────────────────────────────────────────────────┐
│                    NOVO WORKER                                   │
│                                                                  │
│   1. DECIDIR O PADRÃO                                           │
│      ───────────────────                                        │
│      • É simples (1 ação)? → Padrão A (Direto)                 │
│      • Tem múltiplos passos? → Padrão B (Orquestrado)          │
│      • É disparo em massa? → Padrão C (Com Fila)               │
│                                                                  │
│   2. CRIAR A PASTA                                               │
│      ─────────────────                                          │
│      workers/                                                    │
│      └── {dominio}-{acao}/           Ex: hotmart-sync           │
│          ├── main.py                 Código principal            │
│          ├── Dockerfile              Sempre igual               │
│          ├── requirements.txt        Dependências               │
│          └── README.md               O que faz, como testar     │
│                                                                  │
│   3. COPIAR TEMPLATE                                             │
│      ───────────────────                                        │
│      cp -r workers/_template workers/meu-novo-worker            │
│                                                                  │
│   4. PEDIR PARA IA                                               │
│      ────────────────                                           │
│      "Altere o main.py para [descrever o que precisa]"          │
│      A IA já tem o template, só ajusta a lógica                 │
│                                                                  │
│   5. TESTAR LOCAL                                                │
│      ─────────────────                                          │
│      docker build -t test . && docker run -p 8080:8080 test     │
│      curl http://localhost:8080/health                          │
│                                                                  │
│   6. DEPLOY                                                      │
│      ──────                                                     │
│      git add . && git commit -m "feat: novo worker X"           │
│      git push                                                    │
│      → Cloud Build detecta e faz deploy automático              │
│                                                                  │
│   ⏱️ Tempo: 15-30 min                                            │
└─────────────────────────────────────────────────────────────────┘
```

**Checklist Novo Worker:**
- [ ] Decidir padrão (A, B ou C)
- [ ] Criar pasta com nome `{dominio}-{acao}`
- [ ] Copiar template
- [ ] Ajustar main.py (com IA)
- [ ] Testar local
- [ ] git push → deploy

---

### 🔄 NOVO FLOW (Kestra): O que fazer?

Quando precisa orquestrar múltiplos passos:

```
┌─────────────────────────────────────────────────────────────────┐
│                    NOVO FLOW                                     │
│                                                                  │
│   1. CRIAR ARQUIVO YAML                                          │
│      ─────────────────────                                      │
│      flows/                                                      │
│      └── {cliente}/                                             │
│          └── {nome-do-flow}.yaml                                │
│                                                                  │
│   2. ESTRUTURA BASE                                              │
│      ────────────────                                           │
│      id: nome-do-flow                                           │
│      namespace: clientes.nome-cliente                           │
│      description: O que esse flow faz                           │
│                                                                  │
│      inputs:                                                     │
│        - id: cliente_id                                         │
│          type: STRING                                            │
│                                                                  │
│      tasks:                                                      │
│        - id: passo_1                                            │
│          type: io.kestra.plugin.scripts.python.Commands         │
│          commands:                                               │
│            - python main.py                                      │
│                                                                  │
│   3. CONECTAR AOS WORKERS                                        │
│      ────────────────────                                       │
│      Usar HTTP Task para chamar Cloud Run:                      │
│      - id: chamar_worker                                        │
│        type: io.kestra.plugin.core.http.Request                 │
│        uri: https://meu-worker-xxx.run.app/processar            │
│        method: POST                                              │
│        body: "{{ inputs.cliente_id }}"                           │
│                                                                  │
│   4. TESTAR NO KESTRA UI                                         │
│      ────────────────────                                       │
│      • Acessar Kestra → Flows → Execute                         │
│      • Passar inputs de teste                                   │
│      • Ver logs em tempo real                                   │
│                                                                  │
│   5. GIT PUSH                                                    │
│      ────────                                                   │
│      O Kestra pode sincronizar automaticamente com o repo       │
│                                                                  │
│   ⏱️ Tempo: 10-20 min                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

### 📋 RESUMO: Fluxo de Trabalho Diário

```
┌─────────────────────────────────────────────────────────────────┐
│                 SEU DIA A DIA                                    │
│                                                                  │
│   VOCÊ (Orquestrador):                                          │
│   ────────────────────                                          │
│   • Define o que precisa                                        │
│   • Escolhe o padrão (A, B, C)                                  │
│   • Descreve para a IA                                          │
│   • Revisa o código gerado                                      │
│   • git push                                                     │
│   • Testa no Kestra/Cloud Run                                   │
│   • Monitora (Discord + Logs)                                   │
│                                                                  │
│   IA (Executor):                                                │
│   ────────────────                                              │
│   • Gera código baseado nos templates                           │
│   • Ajusta lógica conforme sua descrição                        │
│   • Cria flows YAML                                             │
│   • Sugere melhorias                                            │
│                                                                  │
│   GOOGLE CLOUD (Infraestrutura):                                │
│   ─────────────────────────────                                 │
│   • Detecta git push                                            │
│   • Faz build do Docker                                         │
│   • Deploy automático                                           │
│   • Escala conforme demanda                                     │
│   • Monitora e alerta                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

### 🔧 Comandos Frequentes

```bash
# Novo projeto a partir do template
git clone git@github.com:seuuser/stack-template.git novo-projeto
cd novo-projeto
rm -rf .git && git init
git remote add origin git@github.com:seuuser/novo-projeto.git

# Novo worker
cp -r workers/_template workers/meu-worker
# Editar main.py

# Testar local
cd workers/meu-worker
docker build -t test .
docker run -p 8080:8080 --env-file .env test

# Deploy
git add .
git commit -m "feat: descrição do que fez"
git push

# Ver logs no Google Cloud
gcloud logs read --project=meu-projeto --limit=50

# Ver status do deploy
gcloud run services list --project=meu-projeto
```

---

## 🗺️ Roadmap de Implementação

### Fase 1: Setup Base (1-2 dias)
- [ ] Criar conta Google Cloud (ganhar $300 crédito)
- [ ] Habilitar APIs: Cloud Run, Pub/Sub, Cloud Build, Error Reporting
- [ ] Criar repositório monorepo no GitHub
- [ ] Deploy de "Hello World" no Cloud Run
- [ ] Configurar Discord Webhook para alertas

### Fase 2: Módulos Base (2-3 dias)
- [ ] Criar módulo `notify/discord.py`
- [ ] Criar módulo `error_handler`
- [ ] Criar módulo `supabase_client`
- [ ] Testar módulos isoladamente

### Fase 3: Primeiro Worker (1 semana)
- [ ] Escolher um caso simples (ex: processar webhook)
- [ ] Criar worker Python/FastAPI
- [ ] Configurar Dockerfile
- [ ] Deploy no Cloud Run
- [ ] Testar ciclo completo

### Fase 4: Kestra (1 semana)
- [ ] Subir Kestra (Cloud Run ou VM pequena)
- [ ] Criar primeiro flow YAML
- [ ] Integrar Kestra → Cloud Run
- [ ] Testar orquestração visual

### Fase 5: Filas (3-5 dias)
- [ ] Configurar Pub/Sub (tópico + subscription)
- [ ] Criar dispatcher + worker
- [ ] Testar disparo de 100 mensagens
- [ ] Configurar rate limiting

### Fase 6: CI/CD (2 dias)
- [ ] Configurar Cloud Build triggers por pasta
- [ ] Testar: git push → deploy automático
- [ ] Documentar processo

### Fase 7: Em Paralelo com n8n
- [ ] Continuar usando n8n para fluxos existentes
- [ ] Criar novos projetos na nova stack
- [ ] Migrar gradualmente quando pronto

---

## 🔌 CONFIGURAÇÕES E INTEGRAÇÕES

O que faltava: como vincular tudo (GitHub, Cloud Run, Vercel, MCP, tokens).

### Tokens e Credenciais

```
┌─────────────────────────────────────────────────────────────────┐
│                    GESTÃO DE CREDENCIAIS                         │
│                                                                  │
│   NUNCA NO CÓDIGO. SEMPRE EM:                                    │
│   ─────────────────────────                                     │
│                                                                  │
│   1. VARIÁVEIS DE AMBIENTE (por serviço)                         │
│      • Cloud Run: Console → Service → Variables                 │
│      • Kestra: Namespace → Variables                            │
│      • Vercel: Project → Settings → Environment Variables       │
│      • Local: arquivo .env (NUNCA commitar!)                    │
│                                                                  │
│   2. GOOGLE SECRET MANAGER (para dados sensíveis)                │
│      • API Keys                                                  │
│      • Tokens de terceiros                                       │
│      • Acesso: Cloud Run automaticamente                        │
│                                                                  │
│   CREDENCIAIS NECESSÁRIAS:                                       │
│   ──────────────────────                                        │
│   • SUPABASE_URL                                                 │
│   • SUPABASE_ANON_KEY (frontend)                                │
│   • SUPABASE_SERVICE_KEY (backend)                              │
│   • GCP_PROJECT_ID                                              │
│   • DISCORD_WEBHOOK_URL                                         │
│   • [API específicas: HOTMART_KEY, WHATSAPP_TOKEN, etc]         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Vínculo GitHub → Cloud Run (CI/CD)

```
┌─────────────────────────────────────────────────────────────────┐
│                 GITHUB → CLOUD RUN (Automático)                  │
│                                                                  │
│   1. NO GOOGLE CLOUD CONSOLE:                                    │
│      ─────────────────────────                                  │
│      Cloud Build → Triggers → Create Trigger                    │
│                                                                  │
│   2. CONFIGURAR:                                                 │
│      ────────────                                               │
│      • Nome: deploy-{nome-worker}                               │
│      • Evento: Push to branch (main)                            │
│      • Source: GitHub (conectar conta)                          │
│      • Repositório: seu-repo                                    │
│      • Included files: workers/{nome-worker}/**                 │
│      • Build config: Cloud Build inline ou cloudbuild.yaml      │
│                                                                  │
│   3. RESULTADO:                                                  │
│      ─────────                                                  │
│      git push → Cloud Build detecta → Build Docker → Deploy     │
│                                                                  │
│   TOKEN NECESSÁRIO:                                              │
│   ─────────────────                                             │
│      GitHub OAuth (configurado uma vez no Cloud Build)          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Vínculo GitHub → Vercel (Automático)

```
┌─────────────────────────────────────────────────────────────────┐
│                 GITHUB → VERCEL (Zero config)                    │
│                                                                  │
│   1. NO VERCEL:                                                  │
│      ──────────                                                 │
│      • Import Project → Connect GitHub                          │
│      • Selecionar repositório                                   │
│      • Root Directory: /frontend (ou pasta do front)            │
│                                                                  │
│   2. RESULTADO:                                                  │
│      ─────────                                                  │
│      git push → Vercel detecta → Build → Deploy                 │
│      (automático, zero configuração)                            │
│                                                                  │
│   3. VARIÁVEIS:                                                  │
│      ───────────                                                │
│      Settings → Environment Variables                           │
│      • NEXT_PUBLIC_SUPABASE_URL                                 │
│      • NEXT_PUBLIC_SUPABASE_ANON_KEY                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Supabase MCP (Model Context Protocol)

```
┌─────────────────────────────────────────────────────────────────┐
│                    SUPABASE MCP                                  │
│                                                                  │
│   O QUE É:                                                       │
│   ────────                                                      │
│   MCP permite que a IA (eu) acesse seu Supabase diretamente     │
│   para consultar estrutura, criar migrations, executar SQL.     │
│                                                                  │
│   COMO CONFIGURAR:                                               │
│   ─────────────────                                             │
│   1. Supabase CLI instalado                                     │
│   2. MCP server configurado (já está ativo nesta sessão!)       │
│   3. Project ID do Supabase                                     │
│                                                                  │
│   O QUE EU POSSO FAZER:                                          │
│   ──────────────────────                                        │
│   • Listar tabelas: mcp_supabase-mcp-server_list_tables         │
│   • Executar SQL: mcp_supabase-mcp-server_execute_sql           │
│   • Criar migration: mcp_supabase-mcp-server_apply_migration    │
│   • Gerar types: mcp_supabase-mcp-server_generate_typescript... │
│   • Ver logs: mcp_supabase-mcp-server_get_logs                  │
│                                                                  │
│   BENEFÍCIO:                                                     │
│   ───────────                                                   │
│   "Crie uma tabela de clientes com nome, email e telefone"      │
│   → Eu executo a migration diretamente no seu Supabase          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ BANCO DE DADOS (Supabase + SQL)

### Estrutura de Pastas SQL

```
database/
├── migrations/                 # Migrations versionadas
│   ├── 001_criar_clientes.sql
│   ├── 002_criar_pedidos.sql
│   ├── 003_add_status_pedido.sql
│   └── ...
├── seed/                       # Dados iniciais
│   ├── seed_produtos.sql
│   └── seed_usuarios.sql
├── functions/                  # Functions e Triggers
│   ├── fn_calcular_total.sql
│   └── trigger_notificar.sql
├── policies/                   # RLS Policies
│   └── policies_clientes.sql
└── types/                      # Types gerados
    └── database.types.ts       # Gerado via Supabase CLI
```

### Padrão de Migration

```sql
-- migrations/001_criar_clientes.sql
-- Descrição: Tabela de clientes com dados básicos
-- Data: 2024-12-25
-- Autor: Tiago (via IA)

create table if not exists public.clientes (
    id uuid default gen_random_uuid() primary key,
    nome text not null,
    email text unique not null,
    telefone text,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Comentários na tabela
comment on table public.clientes is 'Tabela de clientes do sistema';
comment on column public.clientes.nome is 'Nome completo do cliente';

-- RLS
alter table public.clientes enable row level security;

-- Trigger de updated_at
create or replace function update_updated_at_column()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

create trigger update_clientes_updated_at
    before update on public.clientes
    for each row
    execute function update_updated_at_column();
```

### Workflow de Banco de Dados

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW DE BANCO                             │
│                                                                  │
│   1. CRIAR MIGRATION                                             │
│      ──────────────────                                         │
│      • Pedir para IA: "Crie tabela X com campos Y, Z"           │
│      • IA gera SQL e salva em database/migrations/              │
│      • OU IA executa via MCP diretamente                        │
│                                                                  │
│   2. APLICAR MIGRATION                                           │
│      ────────────────────                                       │
│      Opção A: Via Supabase Dashboard (SQL Editor)               │
│      Opção B: Via CLI: supabase db push                         │
│      Opção C: Via MCP: eu aplico diretamente                    │
│                                                                  │
│   3. GERAR TYPES                                                 │
│      ──────────────                                             │
│      supabase gen types typescript --project-id xxx > types.ts  │
│      OU via MCP: mcp_supabase-mcp-server_generate_typescript... │
│                                                                  │
│   4. VERSIONAR                                                   │
│      ────────────                                               │
│      git add database/                                           │
│      git commit -m "db: adiciona tabela X"                      │
│      git push                                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🧠 ENGENHARIA DE CONTEXTO (Para a IA não se perder)

Baseado nos conceitos de **Design System** aplicados a automação e **Context Engineering**.

### O Problema

```
SEM ENGENHARIA DE CONTEXTO:
─────────────────────────
Você: "Crie um worker para processar pagamentos"
IA: "Qual linguagem? Qual estrutura? Onde salva? Como erro?"
     → Precisa explicar TUDO de novo a cada tarefa

COM ENGENHARIA DE CONTEXTO:
────────────────────────────
Você: "Crie um worker para processar pagamentos"
IA: Lê as regras → Usa Python/FastAPI → Copia template → 
    Inclui tratamento de erro → Notifica Discord
     → Código consistente e alinhado ao projeto
```

### Os 5 Pilares da Engenharia de Contexto

```
┌─────────────────────────────────────────────────────────────────┐
│              5 PILARES DA ENGENHARIA DE CONTEXTO                 │
│                                                                  │
│   1. 📄 DOCUMENTAÇÃO VIVA                                        │
│      ─────────────────────                                      │
│      • README.md atualizado                                     │
│      • ESTRATEGIA_MIGRACAO.md (este documento)                  │
│      • Diagramas de arquitetura                                 │
│      • Checklists e playbooks                                   │
│                                                                  │
│   2. 📁 ESTRUTURA DE PASTAS PADRONIZADA                          │
│      ──────────────────────────────────                         │
│      • Sempre igual entre projetos                              │
│      • IA sabe onde encontrar cada coisa                        │
│      • Nomes consistentes (dominio-acao)                        │
│                                                                  │
│   3. 📝 TEMPLATES REUTILIZÁVEIS                                  │
│      ────────────────────────                                   │
│      • workers/_template/ (modelo de worker)                    │
│      • flows/_template.yaml (modelo de flow)                    │
│      • IA pega o template e ajusta                              │
│                                                                  │
│   4. 📋 REGRAS DO PROJETO (.agent/rules.md)                      │
│      ────────────────────────────────────                       │
│      • Linguagem: Python/FastAPI                                │
│      • Padrões de código                                        │
│      • Nomenclaturas                                            │
│      • A IA lê estas regras antes de agir                       │
│                                                                  │
│   5. 🔄 WORKFLOWS DOCUMENTADOS (.agent/workflows/)               │
│      ──────────────────────────────────────────                 │
│      • Como criar worker                                        │
│      • Como criar flow                                          │
│      • Como fazer deploy                                        │
│      • IA segue o passo-a-passo                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Estrutura .agent/ (Contexto para IA)

```
.agent/
├── rules.md                    # Regras gerais do projeto
├── context.md                  # Contexto atual (atualizado)
└── workflows/
    ├── criar-worker.md         # Como criar um worker
    ├── criar-flow.md           # Como criar um flow Kestra
    ├── deploy.md               # Como fazer deploy
    ├── debug.md                # Como debugar problemas
    └── novo-projeto.md         # Como iniciar novo projeto
```

### Arquivo: .agent/rules.md

```markdown
# Regras do Projeto

## Stack Tecnológica
- **Backend**: Python 3.11+ com FastAPI
- **Banco**: Supabase (PostgreSQL)
- **Orquestração**: Kestra
- **Execução**: Google Cloud Run
- **Filas**: Google Pub/Sub
- **Frontend**: Next.js no Vercel

## Padrões de Código

### Nomenclatura
- Workers: `{dominio}-{acao}` (ex: `hotmart-sync`)
- Flows: `{dominio}/{acao}.yaml`
- Funções: `snake_case`
- Classes: `PascalCase`

### Estrutura de Worker
Todo worker DEVE ter:
1. Endpoint `/` (POST) - principal
2. Endpoint `/health` (GET) - health check
3. Tratamento de erro com notificação Discord
4. Logs estruturados

### Tratamento de Erro
SEMPRE incluir:
```python
from modules.error_handler import ErrorHandler
handler = ErrorHandler()

try:
    # código
except Exception as e:
    handler.capture(e, context={...})
    raise
```

### Commits
Seguir Conventional Commits:
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `db:` mudança no banco
- `docs:` documentação
- `refactor:` refatoração
```

### Arquivo: .agent/workflows/criar-worker.md

```markdown
---
description: Como criar um novo worker para Cloud Run
---

# Criar Novo Worker

## Pré-requisitos
- Repositório já configurado
- Template workers/_template existe

## Passos

### 1. Copiar template
```bash
cp -r workers/_template workers/{nome-do-worker}
```

### 2. Editar main.py
- Alterar lógica do endpoint `/`
- Manter estrutura de erro
- Manter endpoint `/health`

### 3. Atualizar requirements.txt
- Adicionar dependências necessárias

### 4. Testar local
```bash
cd workers/{nome-do-worker}
docker build -t test .
docker run -p 8080:8080 --env-file .env test
```
// turbo

### 5. Commit e push
```bash
git add workers/{nome-do-worker}
git commit -m "feat: worker {nome-do-worker}"
git push
```

### 6. Verificar deploy
- Cloud Build executa automaticamente
- Verificar logs no Console
```

### Tokenização (Conceito de Design System)

```
┌─────────────────────────────────────────────────────────────────┐
│               TOKENIZAÇÃO (Design System para Código)            │
│                                                                  │
│   DESIGN SYSTEM (UI)          AUTOMAÇÃO (Nossa Stack)           │
│   ──────────────────          ─────────────────────             │
│   Cores, fontes               Variáveis de ambiente             │
│   Componentes                 Módulos reutilizáveis             │
│   Tokens CSS                  Padrões de código                 │
│   System Prompt               .agent/rules.md                   │
│                                                                  │
│   NOSSOS "TOKENS":                                               │
│   ─────────────────                                             │
│   • modules/notify/           → Como notificar                  │
│   • modules/error_handler/    → Como tratar erro                │
│   • modules/supabase_client/  → Como acessar banco              │
│   • modules/queue/            → Como usar filas                 │
│   • workers/_template/        → Estrutura de worker             │
│   • flows/_template.yaml      → Estrutura de flow               │
│                                                                  │
│   BENEFÍCIO:                                                     │
│   ───────────                                                   │
│   • Consistência entre projetos                                 │
│   • IA não precisa "inventar" - usa o que existe                │
│   • Menos tokens gastos por conversa                            │
│   • Menos erros por variação                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Ciclo de Trabalho com IA (Context-First)

```
┌─────────────────────────────────────────────────────────────────┐
│              CICLO DE TRABALHO COM IA                            │
│                                                                  │
│   1. IA LÊ CONTEXTO                                              │
│      ────────────────                                           │
│      • .agent/rules.md                                          │
│      • .agent/workflows/                                        │
│      • README.md                                                 │
│      • docs/apis/ (documentação de APIs)                        │
│      • Estrutura de pastas                                      │
│                                                                  │
│   2. VOCÊ DÁ A TAREFA                                            │
│      ────────────────────                                       │
│      "Crie um worker para sincronizar vendas da Hotmart"        │
│                                                                  │
│   3. IA EXECUTA COM CONTEXTO                                     │
│      ─────────────────────────                                  │
│      • Lê docs/apis/hotmart.md para entender a API              │
│      • Usa template workers/_template                           │
│      • Segue padrões de .agent/rules.md                         │
│      • Inclui módulos padrão                                    │
│      • Gera código consistente                                  │
│                                                                  │
│   4. VOCÊ REVISA E COMMITA                                       │
│      ─────────────────────────                                  │
│      • Verifica se faz sentido                                  │
│      • git push                                                  │
│      • Deploy automático                                        │
│                                                                  │
│   5. CONTEXTO ATUALIZADO                                        │
│      ───────────────────                                        │
│      • Novo worker documentado                                  │
│      • IA já conhece para próximas tarefas                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Melhores Práticas da Anthropic (Context Engineering)

Baseado no artigo [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):

```
┌─────────────────────────────────────────────────────────────────┐
│         MELHORES PRÁTICAS DA ANTHROPIC                           │
│                                                                  │
│   1. CONTEXT ROT (Degradação)                                    │
│      ──────────────────────────                                 │
│      Quanto mais tokens na janela de contexto, pior a           │
│      recordação de informação. Contexto é recurso FINITO.       │
│                                                                  │
│      → Solução: Manter contexto ENXUTO e RELEVANTE              │
│                                                                  │
│   2. ALTITUDE CERTA DOS PROMPTS                                  │
│      ─────────────────────────────                              │
│      • NÃO muito rígido (hardcoded, frágil)                     │
│      • NÃO muito vago (falta contexto)                          │
│      • CERTO: Específico o suficiente + flexível                │
│                                                                  │
│   3. FERRAMENTAS BEM DEFINIDAS                                   │
│      ─────────────────────────────                              │
│      • Cada ferramenta faz UMA coisa bem                        │
│      • Sem overlap de funcionalidade                            │
│      • Parâmetros claros e descritivos                          │
│                                                                  │
│   4. JUST-IN-TIME CONTEXT                                        │
│      ────────────────────────                                   │
│      • Não carregar tudo de uma vez                             │
│      • Manter referências leves (paths, queries, links)         │
│      • Carregar dados dinamicamente quando precisar             │
│                                                                  │
│      Exemplo: Claude Code usa glob e grep para navegar          │
│      ao invés de carregar todos os arquivos de uma vez.         │
│                                                                  │
│   5. COMPACTION (Para tarefas longas)                            │
│      ───────────────────────────────                            │
│      Resumir conversa quando chega perto do limite,             │
│      preservando: decisões, bugs não resolvidos, detalhes       │
│      de implementação.                                          │
│                                                                  │
│   6. STRUCTURED NOTE-TAKING                                      │
│      ──────────────────────────                                 │
│      Agente mantém arquivo de notas (NOTES.md, TODO.md)         │
│      que persiste entre sessões.                                │
│                                                                  │
│      → É isso que fazemos com .agent/context.md                 │
│                                                                  │
│   7. SUB-AGENT ARCHITECTURES                                     │
│      ──────────────────────────                                 │
│      Para tarefas complexas, usar sub-agentes especializados:   │
│      • Agente principal: coordena                               │
│      • Sub-agentes: fazem trabalho focado, retornam resumo      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Princípio Guia

> **"Encontrar o menor conjunto possível de tokens de alto sinal que maximize a probabilidade do resultado desejado."**
> — Anthropic

---

## 📚 DOCUMENTAÇÃO DE APIs E FERRAMENTAS

**Sua sugestão (excelente!)**: Ter uma pasta com toda a documentação das APIs e ferramentas que o projeto usa.

### Por que isso é importante?

```
┌─────────────────────────────────────────────────────────────────┐
│              POR QUE DOCUMENTAR APIs                             │
│                                                                  │
│   SEM DOCUMENTAÇÃO:                                              │
│   ─────────────────                                             │
│   Você: "Integre com a Hotmart"                                 │
│   IA: Busca na internet, pode achar info desatualizada,         │
│       gasta tokens, pode errar endpoints                        │
│                                                                  │
│   COM DOCUMENTAÇÃO:                                              │
│   ──────────────────                                            │
│   Você: "Integre com a Hotmart"                                 │
│   IA: Lê docs/apis/hotmart.md → Já sabe endpoints,              │
│       autenticação, exemplos, limitações                        │
│       → Código certeiro de primeira                             │
│                                                                  │
│   BENEFÍCIOS:                                                    │
│   ───────────                                                   │
│   • IA não precisa pesquisar (economia de tokens)               │
│   • Informação sempre atualizada (você controla)                │
│   • Padrões específicos do seu uso                              │
│   • Exemplos reais do seu contexto                              │
│   • Menos erros, mais velocidade                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Estrutura da Pasta docs/

```
docs/
├── apis/                           # Documentação de APIs externas
│   ├── hotmart.md                  # API Hotmart
│   ├── whatsapp-evolution.md       # API WhatsApp (Evolution)
│   ├── sendflow.md                 # API Sendflow
│   ├── pipedrive.md                # API Pipedrive
│   ├── google-sheets.md            # API Google Sheets
│   └── _template.md                # Template para nova API
│
├── ferramentas/                    # Documentação de ferramentas usadas
│   ├── supabase.md                 # Como usamos Supabase
│   ├── kestra.md                   # Como usamos Kestra
│   ├── cloud-run.md                # Como usamos Cloud Run
│   ├── pubsub.md                   # Como usamos Pub/Sub
│   └── vercel.md                   # Como usamos Vercel
│
├── internas/                       # Documentação de coisas internas
│   ├── modulos.md                  # Nossos módulos Python
│   ├── padroes-codigo.md           # Padrões de código
│   └── troubleshooting.md          # Problemas comuns e soluções
│
└── clientes/                       # Documentação específica por cliente
    ├── cliente-a/
    │   ├── escopo.md
    │   └── integrações.md
    └── cliente-b/
        └── ...
```

### Template de Documentação de API

```markdown
# API: [Nome da API]

## Informações Gerais
- **Base URL**: https://api.exemplo.com/v1
- **Autenticação**: Bearer Token / API Key
- **Rate Limit**: 100 requests/minuto
- **Documentação Oficial**: [link]

## Credenciais Necessárias
| Variável | Onde Conseguir | Onde Salvar |
|----------|----------------|-------------|
| API_KEY | Dashboard → API | .env / Secret Manager |
| API_SECRET | Dashboard → API | .env / Secret Manager |

## Endpoints que Usamos

### 1. Endpoint Principal
```
POST /recurso
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
  "message": "campo1 é obrigatório"
}
```

### 2. Webhook que Recebemos
```
POST /nosso-endpoint
```

**Payload que a API envia:**
```json
{
  "event": "purchase",
  "data": {...}
}
```

## Exemplos de Código

### Python (nosso padrão)
```python
import httpx

async def buscar_recurso(id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.exemplo.com/v1/recurso/{id}",
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        return response.json()
```

## Limitações e Gotchas
- ⚠️ Rate limit de 100/min (usar fila para massa)
- ⚠️ Webhook não tem retry (precisa idempotência)
- ⚠️ Campo X pode vir null (tratar!)

## Histórico de Mudanças
| Data | Mudança |
|------|---------|
| 2024-12-25 | Documentação criada |
```

### Workflow de Documentação de APIs

```
┌─────────────────────────────────────────────────────────────────┐
│              WORKFLOW DE DOCUMENTAÇÃO                            │
│                                                                  │
│   QUANDO ADICIONAR:                                              │
│   ─────────────────                                             │
│   • Ao integrar com nova API                                    │
│   • Ao descobrir limitação/gotcha                               │
│   • Ao mudar como usamos algo                                   │
│                                                                  │
│   COMO ADICIONAR:                                                │
│   ───────────────                                               │
│   1. Copiar template: cp docs/apis/_template.md docs/apis/X.md  │
│   2. Preencher com info da API                                  │
│   3. Adicionar exemplos reais                                   │
│   4. Documentar gotchas encontrados                             │
│   5. git commit -m "docs: adiciona API X"                       │
│                                                                  │
│   QUEM MANTÉM:                                                   │
│   ────────────                                                  │
│   • Você: Atualiza quando descobre algo novo                    │
│   • IA: Pode sugerir atualizações após erros                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Exemplo Real: docs/apis/hotmart.md

```markdown
# API: Hotmart

## Informações Gerais
- **Base URL**: https://developers.hotmart.com/payments/api/v1
- **Autenticação**: OAuth 2.0 (client_credentials)
- **Rate Limit**: 500 requests/minuto
- **Documentação Oficial**: https://developers.hotmart.com/docs

## Credenciais
| Variável | Onde | 
|----------|------|
| HOTMART_CLIENT_ID | Hotmart Club → Ferramentas → API |
| HOTMART_CLIENT_SECRET | Hotmart Club → Ferramentas → API |

## Autenticação (OAuth 2.0)

```python
async def get_hotmart_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api-sec-vlc.hotmart.com/security/oauth/token",
            data={
                "grant_type": "client_credentials",
                "client_id": HOTMART_CLIENT_ID,
                "client_secret": HOTMART_CLIENT_SECRET
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        return response.json()["access_token"]
```

## Endpoints que Usamos

### 1. Listar Vendas
```
GET /sales/history
```

**Query Params:**
- `start_date`: timestamp (ms)
- `end_date`: timestamp (ms)
- `product_id`: (opcional)

### 2. Webhook de Compra
Evento: `PURCHASE_APPROVED`

**Payload:**
```json
{
  "event": "PURCHASE_APPROVED",
  "data": {
    "buyer": {
      "name": "João Silva",
      "email": "joao@email.com"
    },
    "product": {
      "name": "Curso X"
    }
  }
}
```

## Gotchas
- ⚠️ Token expira em 1 hora (cachear e renovar)
- ⚠️ Webhook não tem secret (validar por IP ou payload)
- ⚠️ Paginação máxima de 500 itens
```

---

## ✅ Decisões Tomadas

| Questão | Decisão | Motivo |
|---------|---------|--------|
| **Orquestrador** | ✅ Kestra | Visual como n8n, mas YAML versionável |
| **Linguagem** | ✅ Python (FastAPI) | IA-friendly, robusta, legível |
| **Logs de Erro** | ✅ Google Error Reporting | Nativo, sem mais uma ferramenta |
| **Alertas** | ✅ Discord (modular) | Começar simples, expandir depois |
| **Migração** | ✅ Não migrar agora | Criar novos na nova stack, aprender |
| **Filas** | ✅ Pub/Sub | Serverless, retry automático |
| **Infra** | ✅ 100% Google Cloud | Elimina Docker Swarm, Traefik, Portainer |

---

## 📝 Próximos Passos para Refinar

1. **Onde rodar o Kestra?**
   - Cloud Run (serverless, mas pode ter cold start)?
   - VM pequena (sempre ligada, ~$5/mês)?
   - Kestra Cloud (SaaS, free tier)?

2. **Primeiro projeto piloto?**
   - Qual seria um bom caso de uso para testar a stack completa?

3. **Estrutura de variáveis de ambiente?**
   - Por worker no Cloud Run?
   - Secret Manager centralizado?

4. **Templates de código?**
   - Criar templates que a IA pode usar como base?

---

*Documento vivo - Atualizar conforme refinamos* 🔄
