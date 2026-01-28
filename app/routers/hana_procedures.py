from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.db.hana_client import HanaClient, HanaClientError
from app.dependencies import get_hana_client


router = APIRouter(prefix="/hana/procedures", tags=["HANA Procedures"])

class SNBRNSTestInput(BaseModel):
    param1: int
    param2: str

@router.post("/snbrns-test")
def call_snbrns_test(input_data: SNBRNSTestInput, client: HanaClient = Depends(get_hana_client)):
    try:
        result = client.call_procedure_with_outputs("SP_SNBRS_TEST", [input_data.param1, input_data.param2])
        output_params = result.get("output_params")
        result_sets = result.get("result_sets", [])
        response = {
            "success": False,
            "success_flag": None,
            "message": None,
            "output_params": output_params,
            "result_sets_count": len(result_sets),
        }
        if result_sets:
            first_set = result_sets[0]
            if first_set:
                first_row = first_set[0]
                response.update({
                    "success": True,
                    "success_flag": first_row.get("SUCCESS_FLAG"),
                    "message": first_row.get("MESSAGE"),
                    "rows": first_set,
                    "count": len(first_set),
                })
        if output_params and isinstance(output_params, (list, tuple)) and len(output_params) >= 2:
            response.update({
                "success": True,
                "success_flag": output_params[0],
                "message": output_params[1],
            })
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")


# Modelo de entrada para SP_SNBRS_01
class SNBRNS01Input(BaseModel):
    param1: int
    param2: str
@router.post("/sp-snbrs-01")
def call_sp_snbrs_01(input_data: SNBRNS01Input, client: HanaClient = Depends(get_hana_client)):
    try:
        result = client.call_procedure_with_outputs("SP_SNBRS_01", [input_data.param1, input_data.param2])
        output_params = result.get("output_params")
        result_sets = result.get("result_sets", [])
        response = {
            "success": False,
            "success_flag": None,
            "message": None,
            "output_params": output_params,
            "result_sets_count": len(result_sets),
        }
        if result_sets:
            first_set = result_sets[0]
            if first_set:
                first_row = first_set[0]
                response.update({
                    "success": True,
                    "success_flag": first_row.get("SUCCESS_FLAG"),
                    "message": first_row.get("MESSAGE"),
                    "rows": first_set,
                    "count": len(first_set),
                })
        if output_params and isinstance(output_params, (list, tuple)) and len(output_params) >= 2:
            response.update({
                "success": True,
                "success_flag": output_params[0],
                "message": output_params[1],
            })
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")


# Modelo de entrada para SP_SNBRS_02
class SNBRNS02Input(BaseModel):
    param1: int
    param2: str
@router.post("/sp-snbrs-02")
def call_sp_snbrs_02(input_data: SNBRNS02Input, client: HanaClient = Depends(get_hana_client)):
    try:
        result = client.call_procedure_with_outputs("SP_SNBRS_02", [input_data.param1, input_data.param2])
        output_params = result.get("output_params")
        result_sets = result.get("result_sets", [])
        response = {
            "success": False,
            "success_flag": None,
            "message": None,
            "output_params": output_params,
            "result_sets_count": len(result_sets),
        }
        if result_sets:
            first_set = result_sets[0]
            if first_set:
                first_row = first_set[0]
                response.update({
                    "success": True,
                    "success_flag": first_row.get("SUCCESS_FLAG"),
                    "message": first_row.get("MESSAGE"),
                    "rows": first_set,
                    "count": len(first_set),
                })
        if output_params and isinstance(output_params, (list, tuple)) and len(output_params) >= 2:
            response.update({
                "success": True,
                "success_flag": output_params[0],
                "message": output_params[1],
            })
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")



# Modelo de entrada para SP_SNBRS_19
class SNBRNS19Input(BaseModel):
    param1: int
    param2: str
@router.post("/sp-snbrs-19")
def call_sp_snbrs_19(input_data: SNBRNS19Input, client: HanaClient = Depends(get_hana_client)):
    try:
        result = client.call_procedure_with_outputs("SP_SNBRS_19", [input_data.param1, input_data.param2])
        output_params = result.get("output_params")
        result_sets = result.get("result_sets", [])
        response = {
            "success": False,
            "success_flag": None,
            "message": None,
            "output_params": output_params,
            "result_sets_count": len(result_sets),
        }
        if result_sets:
            first_set = result_sets[0]
            if first_set:
                first_row = first_set[0]
                response.update({
                    "success": True,
                    "success_flag": first_row.get("SUCCESS_FLAG"),
                    "message": first_row.get("MESSAGE"),
                    "rows": first_set,
                    "count": len(first_set),
                })
        if output_params and isinstance(output_params, (list, tuple)) and len(output_params) >= 2:
            response.update({
                "success": True,
                "success_flag": output_params[0],
                "message": output_params[1],
            })
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")
