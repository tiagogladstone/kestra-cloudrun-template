"""
Módulo de Filas (Pub/Sub)
=========================
Helpers para trabalhar com Google Pub/Sub.
"""

import os
import json
from typing import Callable, Optional, Any
import logging

logger = logging.getLogger(__name__)

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")


async def publish_message(
    topic_name: str,
    data: dict,
    attributes: Optional[dict] = None
) -> str:
    """
    Publica mensagem no Pub/Sub.
    
    Args:
        topic_name: Nome do tópico (sem o path completo)
        data: Dados a enviar (será JSON encoded)
        attributes: Atributos adicionais da mensagem
    
    Returns:
        Message ID publicado
    
    Exemplo:
        message_id = await publish_message(
            "hotmart-processar",
            {"cliente_id": "123", "acao": "sincronizar"}
        )
    """
    from google.cloud import pubsub_v1
    
    if not GCP_PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID não configurado")
    
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GCP_PROJECT_ID, topic_name)
    
    # Encode data
    message_data = json.dumps(data).encode("utf-8")
    
    # Publish
    future = publisher.publish(
        topic_path,
        message_data,
        **(attributes or {})
    )
    
    message_id = future.result()
    logger.info(f"Publicado no {topic_name}: {message_id}")
    
    return message_id


def create_push_handler(
    process_func: Callable[[dict], Any],
    error_handler: Optional[Callable[[Exception, dict], None]] = None
):
    """
    Cria um handler para receber mensagens Pub/Sub via push.
    
    Args:
        process_func: Função que processa os dados da mensagem
        error_handler: Função opcional para tratar erros
    
    Returns:
        Função handler para usar com FastAPI
    
    Exemplo:
        from fastapi import FastAPI, Request
        from modules.queue import create_push_handler
        
        async def processar(data: dict):
            # sua lógica
            pass
        
        handler = create_push_handler(processar)
        
        @app.post("/")
        async def receive(request: Request):
            return await handler(request)
    """
    from fastapi import Request, HTTPException
    import base64
    
    async def handler(request: Request):
        try:
            body = await request.json()
            
            # Mensagem vem em body.message.data (base64 encoded)
            if "message" in body and "data" in body["message"]:
                message_data = base64.b64decode(body["message"]["data"])
                data = json.loads(message_data)
            else:
                # Caso seja chamada direta (não Pub/Sub)
                data = body
            
            # Processar
            result = await process_func(data)
            
            return {"success": True, "result": result}
            
        except Exception as e:
            logger.error(f"Erro no handler Pub/Sub: {e}")
            
            if error_handler:
                error_handler(e, body if 'body' in dir() else {})
            
            # Retornar erro para Pub/Sub tentar novamente
            raise HTTPException(status_code=500, detail=str(e))
    
    return handler


def ensure_topic_exists(topic_name: str) -> bool:
    """
    Garante que o tópico existe, criando se necessário.
    
    Args:
        topic_name: Nome do tópico
    
    Returns:
        True se existe ou foi criado
    """
    from google.cloud import pubsub_v1
    from google.api_core.exceptions import AlreadyExists
    
    if not GCP_PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID não configurado")
    
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(GCP_PROJECT_ID, topic_name)
    
    try:
        publisher.create_topic(request={"name": topic_path})
        logger.info(f"Tópico criado: {topic_name}")
        return True
    except AlreadyExists:
        logger.debug(f"Tópico já existe: {topic_name}")
        return True
    except Exception as e:
        logger.error(f"Erro ao criar tópico: {e}")
        return False
