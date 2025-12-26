"""
Módulo de Tratamento de Erros
=============================
Captura, registra e notifica erros de forma padronizada.
"""

import os
import logging
import traceback
from typing import Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class ErrorHandler:
    """
    Handler centralizado para tratamento de erros.
    
    Uso:
        handler = ErrorHandler()
        
        try:
            # código
        except Exception as e:
            handler.capture(e, context={"worker": "nome", "input": data})
            raise
    """
    
    def __init__(self, service_name: Optional[str] = None):
        """
        Args:
            service_name: Nome do serviço para logs
        """
        self.service_name = service_name or os.environ.get("SERVICE_NAME", "unknown")
        self.discord_webhook = os.environ.get("DISCORD_WEBHOOK_URL")
    
    def capture(
        self,
        exception: Exception,
        context: Optional[dict] = None,
        notify: bool = True,
        log_level: str = "error"
    ) -> dict:
        """
        Captura e processa um erro.
        
        Args:
            exception: A exceção capturada
            context: Contexto adicional (dados relevantes)
            notify: Se deve notificar via Discord
            log_level: Nível do log (error, warning, critical)
        
        Returns:
            dict com informações do erro
        """
        error_info = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service_name,
            "error_type": type(exception).__name__,
            "message": str(exception),
            "context": context or {},
            "traceback": traceback.format_exc()
        }
        
        # Log
        log_message = f"[{self.service_name}] {type(exception).__name__}: {exception}"
        if context:
            log_message += f" | Context: {context}"
        
        getattr(logger, log_level)(log_message)
        
        # Google Error Reporting (automático via Cloud Run logs estruturados)
        self._log_for_error_reporting(error_info)
        
        # Discord (se habilitado)
        if notify and self.discord_webhook:
            self._notify_discord(error_info)
        
        return error_info
    
    def _log_for_error_reporting(self, error_info: dict):
        """
        Loga no formato que Google Error Reporting captura automaticamente.
        """
        import json
        
        log_entry = {
            "severity": "ERROR",
            "message": error_info["message"],
            "serviceContext": {"service": self.service_name},
            "context": {
                "reportLocation": {
                    "functionName": error_info.get("context", {}).get("function", "unknown")
                }
            },
            "@type": "type.googleapis.com/google.devtools.clouderrorreporting.v1beta1.ReportedErrorEvent"
        }
        
        print(json.dumps(log_entry))
    
    def _notify_discord(self, error_info: dict):
        """Envia notificação de erro para Discord."""
        import httpx
        
        try:
            message = f"❌ **Erro em {error_info['service']}**\n"
            message += f"```\n{error_info['error_type']}: {error_info['message']}\n```"
            
            if error_info['context']:
                message += f"\n**Contexto:** `{error_info['context']}`"
            
            # Truncar se muito longo
            if len(message) > 2000:
                message = message[:1997] + "..."
            
            with httpx.Client() as client:
                client.post(
                    self.discord_webhook,
                    json={"content": message},
                    timeout=10.0
                )
        except Exception as e:
            logger.warning(f"Falha ao notificar Discord: {e}")


# Instância global para uso rápido
_default_handler = None

def get_handler() -> ErrorHandler:
    """Retorna handler global singleton."""
    global _default_handler
    if _default_handler is None:
        _default_handler = ErrorHandler()
    return _default_handler
