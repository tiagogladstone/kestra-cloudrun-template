# Padrões de Fluxo

A decisão mais importante da arquitetura: **quando usar cada padrão**.

## Visão Geral

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

---

## Padrão A: DIRETO (Simples)

### Quando usar

- ✅ Operação única e rápida (< 30 segundos)
- ✅ Não precisa de retry visual/manual
- ✅ Não tem dependência de outros passos
- ✅ Log de erro é suficiente

### Fluxo

```
Frontend → Supabase (trigger) → Cloud Run → Supabase (resultado)
```

### Exemplos

- Cadastrar cliente e buscar dados de API externa
- Processar webhook de pagamento
- Gerar e salvar um cálculo

---

## Padrão B: ORQUESTRADO (Complexo)

### Quando usar

- ✅ Múltiplos passos dependentes
- ✅ Precisa de retry visual (ver onde falhou)
- ✅ Tem lógica condicional (if/else)
- ✅ Precisa de aprovação manual no meio
- ✅ Quer histórico visual de execuções

### Fluxo

```
Frontend → Kestra (orquestra) → Cloud Run (workers) → Supabase
```

### Exemplos

- Onboarding: criar conta → buscar Hotmart → enviar email → criar grupo WhatsApp
- Processamento de pedido: validar → cobrar → gerar NF → enviar
- Qualquer coisa com "se der erro, espera 1h e tenta de novo"

---

## Padrão C: COM FILA (Massa/Assíncrono)

### Quando usar

- ✅ Processar muitos itens (10+)
- ✅ Precisa de rate limiting (evitar ban)
- ✅ Pode demorar (minutos a horas)
- ✅ Precisa de retry automático por item
- ✅ Não quer travar quem disparou

### Fluxo

```
Trigger → Dispatcher (joga na fila) → Pub/Sub → Worker (processa 1)
```

### Exemplos

- Enviar 1000 mensagens WhatsApp
- Processar 500 linhas de planilha
- Sincronizar 200 clientes de API externa

---

## Tabela de Decisão Rápida

| Situação | Padrão | Usa Kestra? | Usa Pub/Sub? |
|----------|--------|-------------|--------------|
| Webhook simples (1 ação) | A | ❌ | ❌ |
| Cadastro + busca API | A | ❌ | ❌ |
| Onboarding multi-etapas | B | ✅ | ❌ |
| Fluxo com aprovação manual | B | ✅ | ❌ |
| Disparo 1000 mensagens | C | Opcional | ✅ |
| Sincronização em massa | C | Opcional | ✅ |
| Onboarding + disparo massa | B + C | ✅ | ✅ |

---

## Regra de Ouro

> **Comece simples (Padrão A). Só adicione complexidade quando precisar.**
> 
> - Precisa ver onde parou? → Adiciona Kestra (B)
> - Precisa processar muitos? → Adiciona Pub/Sub (C)
> - Precisa dos dois? → Kestra orquestra, Pub/Sub executa
