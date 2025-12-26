# Custos Estimados (Análise Realista)

## ⚠️ PREMISSAS FINANCEIRAS
- Cotação Estimada: **USD 1,00 = R$ 6,00** (margem de segurança)
- IOF + Taxas cartão: **+4.38%** (aprox)
- Custo Base Mínimo: **~$30/mês (~R$ 190)** para infraestrutura estável

---

## 📊 Resumo Realista (USD vs BRL)

| Componente | Custo Mensal (USD) | Custo Mensal (R$) | Notas CRÍTICAS |
|------------|--------------------|-------------------|----------------|
| **Kestra (VM e2-medium)** | **~$25.00** | **~R$ 165,00** | Mínimo para não travar (JVM). |
| Cloud Run | $0 - $5.00 | R$ 0 - 33,00 | Free tier cobre ~2M requests. |
| Artifact Registry | ~$0.50 | ~R$ 3,30 | Armazenamento de imagens Docker. |
| Network Egress | ~$1.00 | ~R$ 6,60 | Tráfego de saída (workers → internet). |
| Pub/Sub + Logs | $0 | R$ 0 | Dentro do free tier generoso. |
| Supabase | $0 - $25.00 | R$ 0 - 165,00 | Free pausa após inatividade. |
| **TOTAL MENSAL** | **~$31.50** | **~R$ 208,00** | **Base sólida de operação.** |

> **Conclusão:** Esta stack **NÃO É MAIS BARATA** que a anterior (R$ 150).
> **A Vantagem:** Pelo mesmo preço (~R$ 200), você ganha **escalabilidade infinita** e **orquestração profissional**, enquanto a stack antiga (Docker Swarm em 1 VM) trava se a carga subir.

---

## Detalhamento Técnico

### 1. Kestra (O Coração da Operação) - ~$25/mês

A orquestração exige memória RAM. O Kestra roda sobre a JVM (Java).
- **e2-micro (1GB)**: ❌ **NÃO USE**. Vai sofrer OOM Kills (falta de memória) e parar seus fluxos silenciosamente.
- **e2-medium (4GB)**: ✅ **OBRIGATÓRIO**. Garante estabilidade para o orquestrador e o banco de dados interno (Postgres).

### 2. Custos Ocultos (O que ninguém conta)

1.  **Artifact Registry (Imagens Docker)**
    - O Cloud Build gera novas imagens a cada deploy.
    - Free tier: 500MB (acaba rápido).
    - Custo: ~$0.10/GB/mês. Limpe imagens antigas regularmente.

2.  **Network Egress (Tráfego de Saída)**
    - Seus workers baixam dados e enviam para APIs externas.
    - Primeiros 100GB/mês: Grátis (geralmente suficiente).
    - Excedente: ~$0.12/GB.

3.  **Supabase Free Tier (Risco de Pausa)**
    - Projetos Free são **PAUSADOS** após 1 semana sem atividade.
    - Para produção crítica 24/7, considere o plano Pro ($25) no futuro.

---

## Comparativo: Antes vs Depois

| Aspecto | Stack Antiga (Swarm/n8n) | Nova Stack (Kestra/Cloud Run) |
|---------|--------------------------|-------------------------------|
| **Custo Base** | ~R$ 150,00 (Fixo) | ~R$ 200,00 (Fixo + Variável) |
| **Escalabilidade** | Limitada à CPU da VM | **Infinita** (Serverless) |
| **Pico de Carga** | VM trava/lentidão | Cloud Run escala automaticamente |
| **Manutenção** | Alta (atualizar Docker, OS) | Média (cuidar apenas da VM Kestra) |
| **Confiabilidade** | Média | Alta (componentes desacoplados) |

**Veredito:** Você paga um pouco mais (~R$ 50) para ter uma arquitetura que aguenta crescer 100x sem quebrar.

---

## Cenários de Custo (Revisados)

### Custo Mínimo (Start)
- VM Kestra (e2-medium)
- Poucos workers
- Rateio de custos fixos
- **Total: ~$30 USD (~R$ 200 BRL)**

### Custo Escala (Crescimento)
- VM Kestra (e2-medium)
- Supabase Pro (para não pausar)
- Muitos workers e tráfego
- **Total: ~$60 USD (~R$ 400 BRL)**

---

## Alertas de Orçamento (Trava de Segurança)

Para evitar surpresas com o cartão de crédito em Dólar:

1.  **Budget Alert:** Configure em $40 (R$ 260).
2.  **Circuit Breaker:** Mantenha `--max-instances=5` em todos os Cloud Runs.
