"""
Módulo de Notificação
=====================
Exporta funções de notificação para diversos canais.
"""

from .discord import notify_discord, notify_discord_sync

__all__ = ["notify_discord", "notify_discord_sync"]
