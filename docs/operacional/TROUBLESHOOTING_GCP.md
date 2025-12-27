# Troubleshooting: Google Cloud Platform

Problemas comuns encontrados durante o setup e como resolvê-los.

---

## Erro: "does not have permission to access projects"

### Sintoma
```
ERROR: (gcloud.services.enable) [email@gmail.com] does not have permission to access projects instance [project-id]
```

### Causas Possíveis

1. **Billing não configurado**
2. **Usuário não é Owner/Editor do projeto**
3. **Projeto não existe**
4. **Conta errada ativa no gcloud**

### Soluções

#### 1. Verificar conta ativa
```bash
gcloud config list
```

Se a conta errada estiver ativa:
```bash
gcloud config set account SEU_EMAIL@gmail.com
```

Ou crie uma configuração separada:
```bash
gcloud config configurations create minha-config --activate
gcloud auth login
gcloud config set project MEU_PROJETO
```

#### 2. Verificar billing
```bash
gcloud billing projects describe MEU_PROJETO
```

Se `billingEnabled: false`, vincule uma conta de faturamento:
> https://console.cloud.google.com/billing/linkedaccount?project=MEU_PROJETO

#### 3. Verificar permissões
```bash
gcloud projects get-iam-policy MEU_PROJETO --format="table(bindings.role,bindings.members)"
```

Se você não for Owner/Editor, peça para o dono te adicionar:
```bash
# Comando para o dono rodar:
gcloud projects add-iam-policy-binding MEU_PROJETO \
  --member="user:seu-email@gmail.com" \
  --role="roles/editor"
```

---

## Erro: "SERVICE_CONFIG_NOT_FOUND_OR_PERMISSION_DENIED"

### Sintoma
```
SERVICE_CONFIG_NOT_FOUND_OR_PERMISSION_DENIED
services: errorreporting.googleapis.com
```

### Causa
O nome da API está incorreto ou a API não está disponível no projeto.

### Solução

O nome correto é `clouderrorreporting.googleapis.com` (com "cloud" no início):

```bash
# ❌ Errado
gcloud services enable errorreporting.googleapis.com

# ✅ Correto
gcloud services enable clouderrorreporting.googleapis.com
```

---

## Erro: "Quota exceeded" ou "Rate limit"

### Sintoma
```
ERROR: (gcloud.services.enable) RESOURCE_EXHAUSTED: Quota exceeded
```

### Solução

Aguarde alguns minutos e tente novamente. O Google Cloud tem rate limits para habilitação de APIs.

```bash
# Aguarde 2-3 minutos e tente uma API por vez
gcloud services enable run.googleapis.com
sleep 30
gcloud services enable cloudbuild.googleapis.com
# etc...
```

---

## Erro: "Project not found"

### Sintoma
```
ERROR: (gcloud.config.set) The project property must be set to a valid project ID
```

### Causa
O ID do projeto está errado ou o projeto não existe.

### Solução

1. Listar seus projetos:
```bash
gcloud projects list
```

2. Usar o ID correto (não o nome!):
```bash
gcloud config set project ID-DO-PROJETO-AQUI
```

---

## Como listar APIs habilitadas

```bash
# Listar todas
gcloud services list --enabled

# Filtrar por nome
gcloud services list --enabled --filter="name:(run OR cloudbuild OR pubsub)"
```

---

## Como desabilitar uma API (se necessário)

```bash
gcloud services disable NOME_DA_API.googleapis.com
```

> ⚠️ Cuidado: desabilitar APIs pode afetar recursos em uso.

---

## Checklist de Pré-requisitos

Antes de habilitar APIs, confirme:

- [ ] Conta Google logada (`gcloud auth login`)
- [ ] Projeto selecionado (`gcloud config set project ID`)
- [ ] Billing vinculado ao projeto
- [ ] Permissão de Owner ou Editor no projeto

---

## Links Úteis

- [Console GCP - IAM](https://console.cloud.google.com/iam-admin/iam)
- [Console GCP - Billing](https://console.cloud.google.com/billing)
- [Console GCP - APIs](https://console.cloud.google.com/apis/library)
- [Documentação gcloud CLI](https://cloud.google.com/sdk/gcloud/reference)
