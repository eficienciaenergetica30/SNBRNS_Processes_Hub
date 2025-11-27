from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.db.hana_client import HanaClient, HanaClientError
from app.dependencies import get_hana_client


router = APIRouter(prefix="/hana/procedures", tags=["HANA Procedures"])


class SNBRNS01Input(BaseModel):
    param1: int
    param2: str


@router.post("/snbrns01")
def call_snbrns01(input_data: SNBRNS01Input, client: HanaClient = Depends(get_hana_client)):
    """Ejemplo de endpoint que invoca el procedimiento SNBRNS01."""
    try:
        rows = client.call_procedure("SNBRNS01", [input_data.param1, input_data.param2])
        return {"count": len(rows), "items": rows}
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")