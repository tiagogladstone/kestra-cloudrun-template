# Checklist: Novo Projeto

Copie este checklist para iniciar um novo projeto.

---

## Informações do Projeto

| Campo | Valor |
|-------|-------|
| **Nome** | |
| **Cliente** | |
| **Data Início** | |
| **Prazo** | |
| **Responsável** | |

---

## FASE 0: Planejamento

### Entendimento
- [ ] Objetivo claro definido
- [ ] Problema a resolver identificado
- [ ] Benefício esperado quantificado

### Integrações
- [ ] APIs externas mapeadas
- [ ] Credenciais identificadas
- [ ] Documentação das APIs salva em `docs/apis/`

### Arquitetura
- [ ] Padrão de fluxo definido (A, B ou C)
- [ ] Workers necessários listados
- [ ] Flows necessários listados
- [ ] Diagrama simples desenhado

### Tasks
- [ ] Lista de tasks criada
- [ ] Estimativa de horas por task
- [ ] Prazo acordado

---

## FASE 1: Infraestrutura

> **PULAR SE JÁ EXISTE**

- [ ] Google Cloud configurado
- [ ] APIs habilitadas
- [ ] VM com Kestra rodando
- [ ] Discord Webhook funcionando
- [ ] Cloud Build conectado ao GitHub
- [ ] Budget Alert configurado

---

## FASE 2: Setup do Projeto

### Repositório
- [ ] Repositório criado (ou branch)
- [ ] Estrutura de pastas copiada do template
- [ ] README atualizado com info do projeto

### Banco de Dados
- [ ] Tabelas criadas em `database/migrations/`
- [ ] Migrations aplicadas no Supabase
- [ ] RLS policies configuradas (se aplicável)

### Kestra
- [ ] Namespace criado: `clientes.{nome-cliente}`
- [ ] Variáveis configuradas no namespace

### Cloud Run
- [ ] Variáveis de ambiente definidas
- [ ] Trigger de Cloud Build criado (se automático)

### Frontend (se aplicável)
- [ ] Projeto Vercel criado
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy conectado ao GitHub

---

## FASE 3: Build

### Workers
- [ ] Worker 1: `{nome}` - Criado e testado local
- [ ] Worker 1: Deploy OK
- [ ] Worker 2: `{nome}` - Criado e testado local
- [ ] Worker 2: Deploy OK
- [ ] (adicionar mais conforme necessário)

### Flows
- [ ] Flow 1: `{nome}` - Criado
- [ ] Flow 1: Testado no Kestra UI
- [ ] (adicionar mais conforme necessário)

### Testes
- [ ] Teste unitário dos workers (se aplicável)
- [ ] Teste integrado end-to-end
- [ ] Teste com dados reais (staging)

### Alertas
- [ ] Erros notificam no Discord
- [ ] Logs aparecem no Cloud Logging

---

## FASE 4: Entrega

### Monitoramento
- [ ] Error Reporting está capturando erros
- [ ] Logs estão estruturados e úteis
- [ ] Alertas Discord testados

### Custos
- [ ] Budget Alert específico do projeto (se necessário)
- [ ] Custos estimados documentados

### Documentação
- [ ] README do projeto atualizado
- [ ] Diagrama de arquitetura criado
- [ ] APIs documentadas em `docs/apis/`
- [ ] Runbook de troubleshooting criado

### Entrega
- [ ] Demonstração feita para stakeholder
- [ ] Acesso concedido (se aplicável)
- [ ] Handoff documentado

---

## Notas do Projeto

*(Adicione notas, decisões e observações aqui)*

---

## Post-Mortem (Após Conclusão)

### O que funcionou bem?

### O que poderia melhorar?

### Lições aprendidas?
