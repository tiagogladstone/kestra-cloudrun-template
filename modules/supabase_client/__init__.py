"""
Cliente Supabase
================
Wrapper para operações com Supabase.

NOTA: A biblioteca supabase-py é SÍNCRONA.
As funções abaixo são síncronas também.
Para uso assíncrono, considere usar run_in_executor ou httpx direto.
"""

import os
from typing import Optional, Any
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

# Configuração
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

# Cliente singleton
_client: Optional[Client] = None


def get_client() -> Client:
    """
    Retorna cliente Supabase singleton.
    
    Uso:
        from modules.supabase_client import get_client
        
        client = get_client()
        result = client.table("clientes").select("*").execute()
    """
    global _client
    
    if _client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("SUPABASE_URL e SUPABASE_SERVICE_KEY são obrigatórios")
        
        _client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Cliente Supabase inicializado")
    
    return _client


def insert(table: str, data: dict) -> dict:
    """
    Insere registro e retorna o resultado.
    
    Args:
        table: Nome da tabela
        data: Dados a inserir
    
    Returns:
        Registro inserido
    """
    client = get_client()
    result = client.table(table).insert(data).execute()
    return result.data[0] if result.data else {}


def select(
    table: str,
    columns: str = "*",
    filters: Optional[dict] = None,
    limit: Optional[int] = None
) -> list:
    """
    Busca registros.
    
    Args:
        table: Nome da tabela
        columns: Colunas a retornar
        filters: Filtros {coluna: valor}
        limit: Limite de resultados
    
    Returns:
        Lista de registros
    """
    client = get_client()
    query = client.table(table).select(columns)
    
    if filters:
        for col, val in filters.items():
            query = query.eq(col, val)
    
    if limit:
        query = query.limit(limit)
    
    result = query.execute()
    return result.data or []


def update(table: str, id: str, data: dict) -> dict:
    """
    Atualiza registro por ID.
    
    Args:
        table: Nome da tabela
        id: ID do registro
        data: Dados a atualizar
    
    Returns:
        Registro atualizado
    """
    client = get_client()
    result = client.table(table).update(data).eq("id", id).execute()
    return result.data[0] if result.data else {}


def delete(table: str, id: str) -> bool:
    """
    Deleta registro por ID.
    
    Args:
        table: Nome da tabela
        id: ID do registro
    
    Returns:
        True se deletou
    """
    client = get_client()
    result = client.table(table).delete().eq("id", id).execute()
    return len(result.data) > 0 if result.data else False


def upsert(table: str, data: dict, on_conflict: str = "id") -> dict:
    """
    Insert ou Update baseado na chave.
    
    Args:
        table: Nome da tabela
        data: Dados
        on_conflict: Coluna para identificar conflito
    
    Returns:
        Registro inserido/atualizado
    """
    client = get_client()
    result = client.table(table).upsert(data, on_conflict=on_conflict).execute()
    return result.data[0] if result.data else {}
