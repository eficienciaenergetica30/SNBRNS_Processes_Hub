from contextlib import contextmanager
from typing import Any, Dict, Iterable, List, Optional

from hdbcli import dbapi

from app.core.settings import Settings


class HanaClientError(Exception):
    pass


class HanaClient:
    """Cliente HANA con helpers para consultas y procedimientos."""

    def __init__(self, settings: Settings):
        self.settings = settings

    @contextmanager
    def _connection(self):
        conn = None
        try:
            kwargs = self.settings.hana_connection_kwargs()
            if not kwargs.get("address") or not kwargs.get("port"):
                raise HanaClientError("Faltan parámetros de conexión HANA (host/port).")
            conn = dbapi.connect(**kwargs)
            yield conn
        except Exception as exc:
            raise HanaClientError(str(exc)) from exc
        finally:
            try:
                if conn:
                    conn.close()
            except Exception:
                pass

    def execute_query(self, sql: str, params: Optional[Iterable[Any]] = None) -> List[Dict[str, Any]]:
        """Ejecuta una consulta SELECT y devuelve lista de diccionarios."""
        with self._connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(sql, list(params))
                else:
                    cursor.execute(sql)
                columns = [desc[0] for desc in (cursor.description or [])]
                rows = cursor.fetchall()
                result: List[Dict[str, Any]] = []
                for row in rows:
                    result.append({columns[i]: row[i] for i in range(len(columns))})
                return result
            except Exception as exc:
                raise HanaClientError(str(exc)) from exc
            finally:
                try:
                    cursor.close()
                except Exception:
                    pass

    def call_procedure(self, procedure_name: str, params: Optional[Iterable[Any]] = None) -> List[Dict[str, Any]]:
        """Llama un procedimiento almacenado. Devuelve filas si el procedimiento devuelve un result set."""
        schema_prefix = f'"{self.settings.hana_schema}".' if self.settings.hana_schema else ""
        # Usamos CALL explícito para capturar posibles result sets
        placeholders = ""
        if params:
            placeholders = ",".join(["?"] * len(list(params)))
        call_sql = f"CALL {schema_prefix}\"{procedure_name}\"({placeholders})"
        with self._connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(call_sql, list(params))
                else:
                    cursor.execute(call_sql)
                # Si hay result set
                if cursor.description:
                    columns = [d[0] for d in cursor.description]
                    rows = cursor.fetchall()
                    return [{columns[i]: row[i] for i in range(len(columns))} for row in rows]
                return []
            except Exception as exc:
                raise HanaClientError(str(exc)) from exc
            finally:
                try:
                    cursor.close()
                except Exception:
                    pass

    def call_procedure_qualified(self, qualified_name: str, params: Optional[Iterable[Any]] = None) -> List[Dict[str, Any]]:
        placeholders = ""
        if params:
            placeholders = ",".join(["?"] * len(list(params)))
        call_sql = f"CALL {qualified_name}({placeholders})"
        with self._connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(call_sql, list(params))
                else:
                    cursor.execute(call_sql)
                if cursor.description:
                    columns = [d[0] for d in cursor.description]
                    rows = cursor.fetchall()
                    return [{columns[i]: row[i] for i in range(len(columns))} for row in rows]
                return []
            except Exception as exc:
                raise HanaClientError(str(exc)) from exc
            finally:
                try:
                    cursor.close()
                except Exception:
                    pass

    def call_procedure_multi(self, procedure_name: str, params: Optional[Iterable[Any]] = None) -> List[List[Dict[str, Any]]]:
        schema_prefix = f'"{self.settings.hana_schema}".' if self.settings.hana_schema else ""
        placeholders = ""
        if params:
            placeholders = ",".join(["?"] * len(list(params)))
        call_sql = f"CALL {schema_prefix}\"{procedure_name}\"({placeholders})"
        with self._connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(call_sql, list(params))
                else:
                    cursor.execute(call_sql)
                result_sets: List[List[Dict[str, Any]]] = []
                while True:
                    if cursor.description:
                        columns = [d[0] for d in cursor.description]
                        rows = cursor.fetchall()
                        result_sets.append([{columns[i]: row[i] for i in range(len(columns))} for row in rows])
                    else:
                        pass
                    if not getattr(cursor, "nextset", None) or not cursor.nextset():
                        break
                return result_sets
            except Exception as exc:
                raise HanaClientError(str(exc)) from exc
            finally:
                try:
                    cursor.close()
                except Exception:
                    pass

    def call_procedure_multi_qualified(self, qualified_name: str, params: Optional[Iterable[Any]] = None) -> List[List[Dict[str, Any]]]:
        placeholders = ""
        if params:
            placeholders = ",".join(["?"] * len(list(params)))
        call_sql = f"CALL {qualified_name}({placeholders})"
        with self._connection() as conn:
            cursor = conn.cursor()
            try:
                if params:
                    cursor.execute(call_sql, list(params))
                else:
                    cursor.execute(call_sql)
                result_sets: List[List[Dict[str, Any]]] = []
                while True:
                    if cursor.description:
                        columns = [d[0] for d in cursor.description]
                        rows = cursor.fetchall()
                        result_sets.append([{columns[i]: row[i] for i in range(len(columns))} for row in rows])
                    else:
                        pass
                    if not getattr(cursor, "nextset", None) or not cursor.nextset():
                        break
                return result_sets
            except Exception as exc:
                raise HanaClientError(str(exc)) from exc
            finally:
                try:
                    cursor.close()
                except Exception:
                    pass

    def call_procedure_with_outputs(self, procedure_name: str, params: Optional[Iterable[Any]] = None) -> Dict[str, Any]:
        schema_prefix = f'"{self.settings.hana_schema}".' if self.settings.hana_schema else ""
        proc = f"{schema_prefix}\"{procedure_name}\""
        with self._connection() as conn:
            cursor = conn.cursor()
            try:
                out_params = cursor.callproc(proc, list(params) if params else [])
                result_sets: List[List[Dict[str, Any]]] = []
                while True:
                    if cursor.description:
                        columns = [d[0] for d in cursor.description]
                        rows = cursor.fetchall()
                        result_sets.append([{columns[i]: row[i] for i in range(len(columns))} for row in rows])
                    if not getattr(cursor, "nextset", None) or not cursor.nextset():
                        break
                return {"output_params": out_params, "result_sets": result_sets}
            except Exception as exc:
                raise HanaClientError(str(exc)) from exc
            finally:
                try:
                    cursor.close()
                except Exception:
                    pass

    def call_procedure_with_outputs_qualified(self, qualified_name: str, params: Optional[Iterable[Any]] = None) -> Dict[str, Any]:
        with self._connection() as conn:
            cursor = conn.cursor()
            try:
                out_params = cursor.callproc(qualified_name, list(params) if params else [])
                result_sets: List[List[Dict[str, Any]]] = []
                while True:
                    if cursor.description:
                        columns = [d[0] for d in cursor.description]
                        rows = cursor.fetchall()
                        result_sets.append([{columns[i]: row[i] for i in range(len(columns))} for row in rows])
                    if not getattr(cursor, "nextset", None) or not cursor.nextset():
                        break
                return {"output_params": out_params, "result_sets": result_sets}
            except Exception as exc:
                raise HanaClientError(str(exc)) from exc
            finally:
                try:
                    cursor.close()
                except Exception:
                    pass
