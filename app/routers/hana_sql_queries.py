from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.db.hana_client import HanaClient, HanaClientError
from app.dependencies import get_hana_client, get_settings


router = APIRouter(prefix="/hana/sql", tags=["HANA SQL"])


@router.get("/ee-site")
def list_ee_site(
    limit: int = Query(10, ge=1, le=1000),
    client: HanaClient = Depends(get_hana_client),
):
    """Devuelve hasta 'limit' filas de GLOBALHITSS_EE_SITE."""
    settings = get_settings()
    # Construir tabla calificada con el schema si está disponible
    if settings.hana_schema:
        table_name = f'"{settings.hana_schema}".GLOBALHITSS_EE_SITE'
    else:
        table_name = "GLOBALHITSS_EE_SITE"

    # LIMIT no siempre admite bind param; validamos entero y lo interpolamos
    sql = f"SELECT * FROM {table_name} LIMIT {int(limit)}"
    try:
        rows = client.execute_query(sql)
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")
    return {"count": len(rows), "rows": rows}


