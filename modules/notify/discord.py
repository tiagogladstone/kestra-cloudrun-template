"""
Módulo de Notificação Discord
=============================
Envia mensagens para Discord via Webhook.
"""

import os
import httpx
from typing import Optional
import logging

logger = logging.getLogger(__name__)

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")


async def notify_discord(
    message: str,
    is_error: bool = False,
    title: Optional[str] = None,
    fields: Optional[dict] = None,
    webhook_url: Optional[str] = None
) -> bool:
    """
    Envia mensagem para Discord.
    
    Args:
        message: Mensagem principal
        is_error: Se True, usa emoji de erro
        title: Título opcional (cria embed)
        fields: Campos adicionais {nome: valor}
        webhook_url: Webhook específico (override)
    
    Returns:
        bool: True se enviou com sucesso
    
    Exemplo:
        await notify_discord("Operação concluída!")
        await notify_discord("Erro no processamento", is_error=True)
        await notify_discord("Novo pedido", fields={"ID": "123", "Valor": "R$ 100"})
    """
    url = webhook_url or DISCORD_WEBHOOK_URL
    
    if not url:
        logger.warning("DISCORD_WEBHOOK_URL não configurado")
        return False
    
    emoji = "❌" if is_error else "✅"
    
    try:
        # Formato simples
        if not title and not fields:
            payload = {"content": f"{emoji} {message}"}
        
        # Formato com embed
        else:
            embed = {
                "title": title or ("Erro" if is_error else "Notificação"),
                "description": message,
                "color": 15158332 if is_error else 3066993  # Vermelho ou Verde
            }
            
            if fields:
                embed["fields"] = [
                    {"name": k, "value": str(v), "inline": True}
                    for k, v in fields.items()
                ]
            
            payload = {"embeds": [embed]}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            response.raise_for_status()
            return True
            
    except Exception as e:
        logger.error(f"Erro ao notificar Discord: {e}")
        return False


def notify_discord_sync(
    message: str,
    is_error: bool = False,
    webhook_url: Optional[str] = None
) -> bool:
    """
    Versão síncrona do notify_discord.
    Use apenas quando não puder usar async.
    """
    import httpx
    
    url = webhook_url or DISCORD_WEBHOOK_URL
    
    if not url:
        logger.warning("DISCORD_WEBHOOK_URL não configurado")
        return False
    
    emoji = "❌" if is_error else "✅"
    
    try:
        with httpx.Client() as client:
            response = client.post(
                url,
                json={"content": f"{emoji} {message}"},
                timeout=10.0
            )
            response.raise_for_status()
            return True
    except Exception as e:
        logger.error(f"Erro ao notificar Discord: {e}")
        return False
