---
description: Como criar um novo flow no Kestra
---

# Criar Novo Flow (Kestra)

## Quando Usar

Use Kestra (Padrão B: Orquestrado) quando:
- Múltiplos passos dependentes
- Precisa de retry visual
- Tem lógica condicional (if/else)
- Precisa de aprovação manual
- Quer histórico de execuções

## Passos

### 1. Criar arquivo YAML

```bash
mkdir -p flows/{cliente-ou-dominio}
touch flows/{cliente-ou-dominio}/{nome-do-flow}.yaml
```

### 2. Estrutura base

```yaml
id: nome-do-flow
namespace: clientes.nome-cliente
description: |
  Descrição clara do que este flow faz.

inputs:
  - id: parametro1
    type: STRING
    description: Descrição do parâmetro
    required: true

tasks:
  - id: passo_1
    type: io.kestra.plugin.core.http.Request
    uri: https://meu-worker-xxx.run.app/
    method: POST
    headers:
      Content-Type: application/json
    body: |
      {"input": "{{ inputs.parametro1 }}"}

  - id: passo_2
    type: io.kestra.plugin.core.http.Request
    dependsOn:
      - passo_1
    uri: https://outro-worker-xxx.run.app/
    method: POST
    body: |
      {"resultado_anterior": "{{ outputs.passo_1.body }}"}

errors:
  - id: notificar_erro
    type: io.kestra.plugin.core.http.Request
    uri: "{{ secret('DISCORD_WEBHOOK_URL') }}"
    method: POST
    body: |
      {"content": "❌ Flow falhou: {{ flow.id }}"}
```

### 3. Conectar aos Workers

Usar HTTP Request para chamar Cloud Run:

```yaml
- id: chamar_worker
  type: io.kestra.plugin.core.http.Request
  uri: https://meu-worker-xxx.run.app/
  method: POST
  headers:
    Content-Type: application/json
  body: |
    {
      "dados": "{{ inputs.dados }}"
    }
```

### 4. Testar no Kestra UI

1. Acessar Kestra: https://kestra.seusite.com
2. Ir em Flows
3. Encontrar o flow
4. Clicar em "Execute"
5. Passar inputs de teste
6. Ver logs em tempo real

### 5. Commit do YAML

```bash
git add flows/
git commit -m "feat: flow {nome-do-flow}"
git push
```

O Kestra pode sincronizar automaticamente com o repositório.

## Padrões de Tasks Úteis

### Chamar Worker Cloud Run

```yaml
- id: chamar_worker
  type: io.kestra.plugin.core.http.Request
  uri: https://worker.run.app/
  method: POST
```

### Esperar N segundos

```yaml
- id: esperar
  type: io.kestra.plugin.core.flow.Sleep
  duration: PT30S  # 30 segundos
```

### Condição If/Else

```yaml
- id: verificar
  type: io.kestra.plugin.core.flow.If
  condition: "{{ outputs.passo_anterior.body.status == 'ok' }}"
  then:
    - id: sucesso
      type: ...
  else:
    - id: falha
      type: ...
```

### Loop em Lista

```yaml
- id: processar_cada
  type: io.kestra.plugin.core.flow.ForEach
  values: "{{ outputs.buscar_lista.body.items }}"
  tasks:
    - id: processar_item
      type: io.kestra.plugin.core.http.Request
      uri: https://worker.run.app/
      body: |
        {"item": "{{ taskrun.value }}"}
```

## Checklist

- [ ] Arquivo YAML criado
- [ ] Namespace definido
- [ ] Inputs documentados
- [ ] Tasks conectam aos workers
- [ ] Handler de erro configurado
- [ ] Testado no Kestra UI
- [ ] Commit feito
