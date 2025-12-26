"""
Worker Template
===============
Este é o template base para criar novos workers.

Substitua:
- TODO_WORKER_NAME pelo nome do worker
- A lógica do endpoint /
"""

import os
import logging
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional

# ============================================
# IMPORTS DOS MÓDULOS COMPARTILHADOS
# ============================================
# Os módulos são copiados automaticamente pelo Dockerfile
from modules.error_handler import ErrorHandler
from modules.notify.discord import send_message as notify_discord

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializa FastAPI
app = FastAPI(
    title="TODO_WORKER_NAME",
    description="Descrição do que este worker faz",
    version="1.0.0"
)

# Inicializa Error Handler
error_handler = ErrorHandler(service_name="TODO_WORKER_NAME")

# ============================================
# MODELOS (Pydantic)
# ============================================

class InputModel(BaseModel):
    """Define os dados de entrada esperados"""
    # Exemplo:
    # cliente_id: str
    # dados: Optional[dict] = None
    pass


class OutputModel(BaseModel):
    """Define os dados de saída"""
    success: bool
    message: str
    data: Optional[dict] = None


# ============================================
# ENDPOINTS
# ============================================

@app.get("/health")
async def health():
    """Health check endpoint - obrigatório para Cloud Run"""
    return {"status": "healthy", "service": "TODO_WORKER_NAME"}


@app.post("/", response_model=OutputModel)
async def process(request: Request):
    """
    Endpoint principal do worker.
    
    Substitua a lógica abaixo pela sua implementação.
    """
    # Captura Correlation ID para rastreamento (vem do Kestra)
    correlation_id = request.headers.get("X-Correlation-ID", "unknown")
    
    try:
        # Pegar dados da requisição
        body = await request.json()
        logger.info(f"[{correlation_id}] Recebido: {body}")
        
        # ============================================
        # TODO: SUA LÓGICA AQUI
        # ============================================
        
        # Exemplo:
        # resultado = await processar_dados(body)
        resultado = {"processado": True}
        
        # ============================================
        # FIM DA LÓGICA
        # ============================================
        
        # Notificar sucesso (opcional)
        # notify_discord(f"[{correlation_id}] Processado com sucesso")
        
        logger.info(f"[{correlation_id}] Processado com sucesso")
        
        return OutputModel(
            success=True,
            message="Processado com sucesso",
            data=resultado
        )
        
    except Exception as e:
        logger.error(f"[{correlation_id}] Erro no processamento: {e}", exc_info=True)
        
        # Captura erro com contexto para debug
        error_handler.capture(e, context={
            "correlation_id": correlation_id,
            "worker": "TODO_WORKER_NAME"
        })
        
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ============================================
# PARA RODAR LOCALMENTE
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
