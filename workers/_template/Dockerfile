# Dockerfile otimizado para Monorepo
# ⚠️ IMPORTANTE: Execute o build DA RAIZ DO PROJETO, não de dentro do worker!
# Exemplo: docker build -f workers/meu-worker/Dockerfile -t meu-worker .
#
# O cloudbuild.yaml já faz a substituição de TODO_WORKER_NAME automaticamente.

FROM python:3.11-slim

WORKDIR /app

# 1. Copiar requirements do worker
COPY workers/TODO_WORKER_NAME/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copiar código do worker
COPY workers/TODO_WORKER_NAME/ .

# 3. Copiar módulos compartilhados (A mágica acontece aqui)
# O build context deve ser a raiz do projeto!
COPY modules/ ./modules/
# Garantir que modules tem __init__.py
RUN touch modules/__init__.py

# Expor porta
EXPOSE 8080

# Comando de execução
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
