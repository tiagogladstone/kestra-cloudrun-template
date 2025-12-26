# Riscos e Mitigações

Documento com riscos identificados e como evitá-los.

---

## ⚠️ Riscos Críticos

### 1. OOM Kills na VM do Kestra

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | VM e2-micro (1GB RAM) não suporta Kestra + PostgreSQL |
| **Sintoma** | Servidor travando, Kestra reiniciando, orquestração parando |
| **Impacto** | Toda a orquestração para silenciosamente |
| **Mitigação** | Usar VM **e2-medium (4GB RAM)** - custo ~$25/mês |
| **Alternativa** | Usar Supabase como banco do Kestra (reduz carga) |

### 2. Cobrança Infinita (Billing Loop)

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | Bug + retry infinito = Cloud Run escala infinitamente |
| **Sintoma** | Fatura de milhares de reais |
| **Impacto** | Prejuízo financeiro grave |
| **Mitigação** | **SEMPRE** usar `--max-instances=5` no deploy |
| **Extra** | Configurar Budget Alert que PARA faturamento, não apenas avisa |

```bash
# Deploy CORRETO com circuit breaker
gcloud run deploy worker \
  --max-instances=5 \    # ← OBRIGATÓRIO
  --memory=512Mi \
  --source .
```

### 3. Segredos Expostos

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | Usar .env em produção, commitar credenciais |
| **Sintoma** | Credenciais vazadas, contas comprometidas |
| **Impacto** | Segurança comprometida |
| **Mitigação** | **Google Secret Manager** para tudo sensível |
| **Regra** | .env APENAS para desenvolvimento local |

---

## ⚠️ Riscos Operacionais

### 4. Debug Impossível (Fragmentação de Logs)

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | Erro requer olhar Kestra UI + Cloud Logging + Pub/Sub Console |
| **Sintoma** | "Dança de abas", MTTR alto |
| **Impacto** | Tempo de resolução de problemas muito alto |
| **Mitigação** | **Correlation ID** em tudo |

```yaml
# No Kestra - SEMPRE passar execution.id
headers:
  X-Correlation-ID: "{{ execution.id }}"
```

```python
# No Worker - SEMPRE logar com correlation_id
correlation_id = request.headers.get("X-Correlation-ID", "unknown")
logger.info(f"[{correlation_id}] Processando...")
```

### 5. Single Point of Failure (VM Kestra)

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | VM cai → toda orquestração para |
| **Sintoma** | Flows não executam, agendamentos falham |
| **Impacto** | Operação parada até VM voltar |
| **Mitigação Atual** | Monitorar uptime da VM, alertas de disponibilidade |
| **Mitigação Futura** | Considerar Kestra Cloud para produção crítica |

### 6. Cold Start no Padrão B (Latência)

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | Fluxo com 10 passos = soma de 10 cold starts |
| **Sintoma** | Fluxos simples levam minutos |
| **Impacto** | UX ruim, timeout em integrações |
| **Mitigação** | Para workers críticos: `--min-instances=1` |

```bash
# Worker que precisa ser rápido
gcloud run deploy worker-critico \
  --min-instances=1 \    # ← Sempre quente
  --max-instances=5
```

> ⚠️ `--min-instances=1` gera custo contínuo (~$10-15/mês por worker)

---

## ⚠️ Riscos de Escala

### 7. Gerenciamento de 50+ Triggers

| Aspecto | Detalhe |
|---------|---------|
| **Problema** | Com muitos workers, gerenciar triggers no console é inviável |
| **Sintoma** | Erro humano, triggers desconfigurados |
| **Impacto** | Deploys falhando, workers desatualizados |
| **Mitigação Futura** | Adotar Terraform para IaC |

### 8. Limites de Free Tier

| Serviço | Limite | O que acontece |
|---------|--------|----------------|
| Cloud Run | 2M req/mês | Começa cobrar $0.40/milhão |
| Pub/Sub | 10GB/mês | Começa cobrar $0.04/GB |
| Cloud Logging | 50GB/mês | Começa cobrar $0.50/GB |
| VM e2-micro | 1 por conta | Segunda paga ~$4/mês |

**Mitigação:** Configurar Budget Alerts e monitorar uso mensalmente

---

## 📋 Checklist de Mitigação

Antes de ir para produção, verificar:

- [ ] VM é e2-medium ou maior
- [ ] Todos os deploys têm `--max-instances`
- [ ] Secrets estão no Secret Manager
- [ ] Correlation ID está implementado
- [ ] Budget Alert está configurado
- [ ] Monitoramento de uptime da VM está ativo
- [ ] Workers críticos têm `--min-instances=1`

---

## 🔮 Evoluções Futuras

Para quando escalar:

| Problema | Solução |
|----------|---------|
| Muitos triggers | Terraform/IaC |
| VM como SPOF | Kestra Cloud |
| Custos crescendo | Otimização, reserved instances |
| Complexidade | Multi-agent para projetos grandes |
