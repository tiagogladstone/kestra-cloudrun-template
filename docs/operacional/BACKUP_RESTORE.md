# Backup e Restauração (Disaster Recovery)

Como a VM do Kestra é um ponto único de falha (Self-Hosted), backups são obrigatórios.

---

## 💾 O que precisa ser salvo?

1.  **banco de dados PostgreSQL**: Contém todos os flows, execuções e logs.
2.  **`docker-compose.yml`**: Configuração da infra.
3.  **Storage Local**: Se você usar o driver de storage local para arquivos grandes (`kestra-data`).

---

## 🔄 Backup Manual (Snapshot)

A forma mais fácil de garantir segurança é via **Google Cloud Snapshots**.

1.  Acesse o Console -> Compute Engine -> Snapshots.
2.  Crie um Snapshot Schedule.
3.  **Frequência:** Diária (ex: 3:00 AM).
4.  **Retenção:** 14 dias.
5.  **Região:** Multi-regional (para proteger contra queda de zona).

> **Custo:** Snapshots são baratos (~$0.026/GB). Para 30GB, custa menos de $1/mês.

---

## 🔄 Backup Lógico (SQL Dump)

Para ter um backup portável (para migrar de servidor), faça um dump do Postgres.

### Script de Backup (`backup.sh`)
Coloque este script na VM:

```bash
#!/bin/bash
DATE=$(date +%Y-%m-%d_%H%M)
BACKUP_DIR="/home/seu-usuario/backups"
BUCKET="gs://seu-bucket-de-backups"

# Criar pasta se não existir
mkdir -p $BACKUP_DIR

# 1. Dump do Banco
echo "Iniciando backup..."
docker exec kestra-postgres-1 pg_dump -U kestra kestra > "$BACKUP_DIR/kestra_$DATE.sql"

# 2. Compactar
gzip "$BACKUP_DIR/kestra_$DATE.sql"

# 3. Enviar para Cloud Storage (Opcional mas recomendado)
# gsutil cp "$BACKUP_DIR/kestra_$DATE.sql.gz" $BUCKET

# 4. Limpar locais antigos (manter 7 dias)
find $BACKUP_DIR -type f -name "*.gz" -mtime +7 -delete

echo "Backup concluído: kestra_$DATE.sql.gz"
```

---

## 🚑 Como Restaurar (Disaster Recovery)

Se a VM explodir, siga estes passos para voltar em 15 minutos:

### Opção A: Restaurar Snapshot (Mais rápido)
1.  Vá em Compute Engine -> Snapshots.
2.  Selecione o último snapshot.
3.  Clique em "Create Instance" a partir dele.
4.  A VM sobe exatamente como estava.

### Opção B: Restaurar SQL (Instalação Limpa)
1.  Crie uma nova VM e instale Docker (via `setup-projeto` ou manual).
2.  Suba o `docker-compose.yml`.
3.  Pare o Kestra (mas deixe o Postgres rodando):
    ```bash
    docker stop kestra-kestra-1
    ```
4.  Restaure o banco:
    ```bash
    gunzip -c kestra_2024-12-25.sql.gz | docker exec -i kestra-postgres-1 psql -U kestra kestra
    ```
5.  Inicie o Kestra:
    ```bash
    docker start kestra-kestra-1
    ```

---

## ✅ Checklist de Segurança

- [ ] Snapshot Diário configurado no GCP?
- [ ] Teste de restore realizado pelo menos 1 vez?
