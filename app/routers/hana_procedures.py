from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.db.hana_client import HanaClient, HanaClientError
from app.dependencies import get_hana_client

router = APIRouter(prefix="/hana/procedures", tags=["HANA Procedures"])


class SNBRNSTestInput(BaseModel):
    param1: int
    param2: str


@router.post("/snbrns-test")
def call_snbrns_test(
    input_data: SNBRNSTestInput, client: HanaClient = Depends(get_hana_client)
):
    try:
        result = client.call_procedure_with_outputs(
            "SP_SNBRS_TEST", [input_data.param1, input_data.param2]
        )
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
                response.update(
                    {
                        "success": True,
                        "success_flag": first_row.get("SUCCESS_FLAG"),
                        "message": first_row.get("MESSAGE"),
                        "rows": first_set,
                        "count": len(first_set),
                    }
                )
        if (
            output_params
            and isinstance(output_params, (list, tuple))
            and len(output_params) >= 2
        ):
            response.update(
                {
                    "success": True,
                    "success_flag": output_params[0],
                    "message": output_params[1],
                }
            )
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")


# Modelo de entrada para SP_SNBRS_01
class SNBRNS01Input(BaseModel):
    rows_read: int
    rows_inserted_init: int
    execution_id_in: str
    user: str


@router.post("/sp-snbrs-01")
def call_sp_snbrs_01(
    input_data: SNBRNS01Input, client: HanaClient = Depends(get_hana_client)
):
    try:
        result = client.call_procedure_with_outputs(
            "SP_SNBRS_01",
            [
                input_data.rows_read,
                input_data.rows_inserted_init,
                input_data.execution_id_in,
                input_data.user,
            ],
            out_params_count=4,
        )
        output_params = result.get("output_params")
        result_sets = result.get("result_sets", [])
        response = {
            "success": False,
            "success_flag": None,
            "message": None,
            "execution_id_out": None,
            "rows_processed": None,
            "output_params": output_params,
            "result_sets_count": len(result_sets),
        }
        if result_sets:
            first_set = result_sets[0]
            if first_set:
                first_row = first_set[0]
                response.update(
                    {
                        "success": True,
                        "success_flag": first_row.get("SUCCESS_FLAG"),
                        "message": first_row.get("MESSAGE"),
                        "rows": first_set,
                        "count": len(first_set),
                    }
                )
        if (
            output_params
            and isinstance(output_params, (list, tuple))
            and len(output_params) >= 4
        ):
            response.update(
                {
                    "success": True,
                    "success_flag": output_params[0],
                    "message": output_params[1],
                    "execution_id_out": output_params[2],
                    "rows_processed": output_params[3],
                }
            )
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")


# Modelo de entrada para SP_SNBRS_02
class SNBRNS02Input(BaseModel):
    rows_read: int
    rows_inserted_init: int
    execution_id_in: str
    user: str


@router.post("/sp-snbrs-02")
def call_sp_snbrs_02(
    input_data: SNBRNS02Input, client: HanaClient = Depends(get_hana_client)
):
    try:
        result = client.call_procedure_with_outputs(
            "SP_SNBRS_02",
            [
                input_data.rows_read,
                input_data.rows_inserted_init,
                input_data.execution_id_in,
                input_data.user,
            ],
            out_params_count=4,
        )
        output_params = result.get("output_params")
        result_sets = result.get("result_sets", [])
        response = {
            "success": False,
            "success_flag": None,
            "message": None,
            "execution_id_out": None,
            "rows_processed": None,
            "output_params": output_params,
            "result_sets_count": len(result_sets),
        }
        if result_sets:
            first_set = result_sets[0]
            if first_set:
                first_row = first_set[0]
                response.update(
                    {
                        "success": True,
                        "success_flag": first_row.get("SUCCESS_FLAG"),
                        "message": first_row.get("MESSAGE"),
                        "rows": first_set,
                        "count": len(first_set),
                    }
                )
        if (
            output_params
            and isinstance(output_params, (list, tuple))
            and len(output_params) >= 4
        ):
            response.update(
                {
                    "success": True,
                    "success_flag": output_params[0],
                    "message": output_params[1],
                    "execution_id_out": output_params[2],
                    "rows_processed": output_params[3],
                }
            )
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")


# Modelo de entrada para SP_SNBRS_03
class SNBRNS03Input(BaseModel):
    rows_read: int
    rows_inserted_init: int
    execution_id_in: str
    user: str


@router.post("/sp-snbrs-03")
def call_sp_snbrs_03(
    input_data: SNBRNS03Input, client: HanaClient = Depends(get_hana_client)
):
    try:
        result = client.call_procedure_with_outputs(
            "SP_SNBRS_03",
            [
                input_data.rows_read,
                input_data.rows_inserted_init,
                input_data.execution_id_in,
                input_data.user,
            ],
            out_params_count=4,
        )
        output_params = result.get("output_params")
        result_sets = result.get("result_sets", [])
        response = {
            "success": False,
            "success_flag": None,
            "message": None,
            "execution_id_out": None,
            "rows_processed": None,
            "output_params": output_params,
            "result_sets_count": len(result_sets),
        }
        if result_sets:
            first_set = result_sets[0]
            if first_set:
                first_row = first_set[0]
                response.update(
                    {
                        "success": True,
                        "success_flag": first_row.get("SUCCESS_FLAG"),
                        "message": first_row.get("MESSAGE"),
                        "rows": first_set,
                        "count": len(first_set),
                    }
                )
        if (
            output_params
            and isinstance(output_params, (list, tuple))
            and len(output_params) >= 4
        ):
            response.update(
                {
                    "success": True,
                    "success_flag": output_params[0],
                    "message": output_params[1],
                    "execution_id_out": output_params[2],
                    "rows_processed": output_params[3],
                }
            )
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")


# Modelo de entrada para SP_SNBRS_11
class SNBRNS11Input(BaseModel):
    rows_read: int
    rows_inserted_init: int
    execution_id_in: str
    user: str


@router.post("/sp-snbrs-11")
def call_sp_snbrs_11(
    input_data: SNBRNS11Input, client: HanaClient = Depends(get_hana_client)
):
    try:
        result = client.call_procedure_with_outputs(
            "SP_SNBRS_11",
            [
                input_data.rows_read,
                input_data.rows_inserted_init,
                input_data.execution_id_in,
                input_data.user,
            ],
            out_params_count=4,
        )

        output_params = result.get("output_params")
        result_sets = result.get("result_sets", [])
        response = {
            "success": False,
            "success_flag": None,
            "message": None,
            "execution_id_out": None,
            "rows_processed": None,
            "output_params": output_params,
            "result_sets_count": len(result_sets),
        }
        if result_sets:
            first_set = result_sets[0]
            if first_set:
                first_row = first_set[0]
                response.update(
                    {
                        "success": True,
                        "success_flag": first_row.get("SUCCESS_FLAG"),
                        "message": first_row.get("MESSAGE"),
                        "rows": first_set,
                        "count": len(first_set),
                    }
                )
        if (
            output_params
            and isinstance(output_params, (list, tuple))
            and len(output_params) >= 2
        ):
            response.update(
                {
                    "success": True,
                    "success_flag": output_params[0],
                    "message": output_params[1],
                    "execution_id_out": output_params[2] if len(output_params) > 2 else None,
                    "rows_processed": output_params[3] if len(output_params) > 3 else None,
                }
            )
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")


# Modelo de entrada para SP_SNBRS_12
class SNBRNS12Input(BaseModel):
    param1: int
    param2: str


@router.post("/sp-snbrs-12")
def call_sp_snbrs_12(
    input_data: SNBRNS12Input, client: HanaClient = Depends(get_hana_client)
):
    try:
        result = client.call_procedure_with_outputs(
            "SP_SNBRS_12", [input_data.param1, input_data.param2]
        )
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
                response.update(
                    {
                        "success": True,
                        "success_flag": first_row.get("SUCCESS_FLAG"),
                        "message": first_row.get("MESSAGE"),
                        "rows": first_set,
                        "count": len(first_set),
                    }
                )
        if (
            output_params
            and isinstance(output_params, (list, tuple))
            and len(output_params) >= 2
        ):
            response.update(
                {
                    "success": True,
                    "success_flag": output_params[0],
                    "message": output_params[1],
                }
            )
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")


# Modelo de entrada para SP_SNBRS_15
class SNBRNS15Input(BaseModel):
    param1: int
    param2: str


@router.post("/sp-snbrs-15")
def call_sp_snbrs_15(
    input_data: SNBRNS15Input, client: HanaClient = Depends(get_hana_client)
):
    try:
        result = client.call_procedure_with_outputs(
            "SP_SNBRS_15", [input_data.param1, input_data.param2]
        )
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
                response.update(
                    {
                        "success": True,
                        "success_flag": first_row.get("SUCCESS_FLAG"),
                        "message": first_row.get("MESSAGE"),
                        "rows": first_set,
                        "count": len(first_set),
                    }
                )
        if (
            output_params
            and isinstance(output_params, (list, tuple))
            and len(output_params) >= 2
        ):
            response.update(
                {
                    "success": True,
                    "success_flag": output_params[0],
                    "message": output_params[1],
                }
            )
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")


# Modelo de entrada para SP_SNBRS_18
class SNBRNS18Input(BaseModel):
    param1: int
    param2: str


@router.post("/sp-snbrs-18")
def call_sp_snbrs_18(
    input_data: SNBRNS18Input, client: HanaClient = Depends(get_hana_client)
):
    try:
        result = client.call_procedure_with_outputs(
            "SP_SNBRS_18", [input_data.param1, input_data.param2]
        )
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
                response.update(
                    {
                        "success": True,
                        "success_flag": first_row.get("SUCCESS_FLAG"),
                        "message": first_row.get("MESSAGE"),
                        "rows": first_set,
                        "count": len(first_set),
                    }
                )
        if (
            output_params
            and isinstance(output_params, (list, tuple))
            and len(output_params) >= 2
        ):
            response.update(
                {
                    "success": True,
                    "success_flag": output_params[0],
                    "message": output_params[1],
                }
            )
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")


# Modelo de entrada para SP_SNBRS_19
class SNBRNS19Input(BaseModel):
    param1: int
    param2: str


@router.post("/sp-snbrs-19")
def call_sp_snbrs_19(
    input_data: SNBRNS19Input, client: HanaClient = Depends(get_hana_client)
):
    try:
        result = client.call_procedure_with_outputs(
            "SP_SNBRS_19", [input_data.param1, input_data.param2]
        )
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
                response.update(
                    {
                        "success": True,
                        "success_flag": first_row.get("SUCCESS_FLAG"),
                        "message": first_row.get("MESSAGE"),
                        "rows": first_set,
                        "count": len(first_set),
                    }
                )
        if (
            output_params
            and isinstance(output_params, (list, tuple))
            and len(output_params) >= 2
        ):
            response.update(
                {
                    "success": True,
                    "success_flag": output_params[0],
                    "message": output_params[1],
                }
            )
        return response
    except HanaClientError as exc:
        raise HTTPException(status_code=500, detail=f"HANA error: {exc}")
