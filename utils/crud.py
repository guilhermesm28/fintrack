from sqlalchemy import text, inspect
from typing import Dict, Any, Tuple
import pandas as pd
from utils.db import get_engine

def _build_where_clause(where: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """Constrói cláusula WHERE com parâmetros nomeados."""
    if not where:
        return "", {}

    conditions = [f"{k} = :w_{k}" for k in where.keys()]
    params = {f"w_{k}": v for k, v in where.items()}
    return " WHERE " + " AND ".join(conditions), params

def select(query) -> pd.DataFrame:
    """Seleciona dados de uma tabela usando uma query SQL customizada."""
    engine = get_engine()

    if query:
        sql = text(query)
        with engine.connect() as conn:
            df = pd.read_sql(sql, conn)
        return df

def insert(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Insere um registro na tabela a partir de um dicionário."""
    engine = get_engine()

    columns = ", ".join(data.keys())
    placeholders = ", ".join([f":{k}" for k in data.keys()])
    sql = text(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})")

    try:
        with engine.begin() as conn:
            result = conn.execute(sql, data)
            return {
                "success": True,
                "rows_affected": result.rowcount,
                "message": f"Registro inserido com sucesso"
            }
    except Exception as e:
        return {
            "success": False,
            "rows_affected": 0,
            "message": f"Erro ao inserir: {str(e)}"
        }

def update(table: str, data: Dict[str, Any], where: Dict[str, Any]) -> Dict[str, Any]:
    """Atualiza registros na tabela a partir de um dicionário."""
    if not where:
        return {
            "success": False,
            "rows_affected": 0,
            "message": "Condição WHERE é obrigatória para UPDATE"
        }

    engine = get_engine()

    set_clause = ", ".join([f"{k} = :{k}" for k in data.keys()])
    where_clause, where_params = _build_where_clause(where)

    params = {**data, **where_params}
    sql = text(f"UPDATE {table} SET {set_clause}{where_clause}")

    try:
        with engine.begin() as conn:
            result = conn.execute(sql, params)
            return {
                "success": True,
                "rows_affected": result.rowcount,
                "message": f"{result.rowcount} registro(s) atualizado(s)"
            }
    except Exception as e:
        return {
            "success": False,
            "rows_affected": 0,
            "message": f"Erro ao atualizar: {str(e)}"
        }