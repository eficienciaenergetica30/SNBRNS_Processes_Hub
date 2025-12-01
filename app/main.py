import logging
from typing import Dict

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from pydantic import BaseModel

from app.dependencies import get_settings, get_hana_client
from app.db.hana_client import HanaClient, HanaClientError
from app.routers.hana_sql_queries import router as sql_router
from app.routers.hana_procedures import router as proc_router


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0")

    def _to_list(value: str | None, default: list[str]) -> list[str]:
        if not value:
            return default
        v = value.strip()
        if v == "*":
            return ["*"]
        return [item.strip() for item in v.split(",") if item.strip()]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=_to_list(settings.cors_allow_origins, ["*"]),
        allow_methods=_to_list(settings.cors_allow_methods, ["*"]),
        allow_headers=_to_list(settings.cors_allow_headers, ["*"]),
        allow_credentials=settings.cors_allow_credentials,
    )

    # Routers (prefijo global)
    app.include_router(sql_router, prefix="/snbrns-hub")
    app.include_router(proc_router, prefix="/snbrns-hub")

    @app.get("/health", tags=["Core"])
    def health() -> Dict[str, str]:
        return {"status": "ok", "environment": settings.environment}

    # (eliminado alias de health con prefijo)

    

    # Home en ruta raíz
    @app.get("/", tags=["General"], summary="Root")
    def root() -> dict:
        return {
            "name": settings.app_name,
            "version": "0.1.0",
            "base_path": "/snbrns-hub",
            "sections": {
                "General": {"root": "/"},
                "HANA DB - SQL": {
                    "ee_site": {
                        "path": "/snbrns-hub/hana/sql/ee-site",
                        "description": "Lista filas de GLOBALHITSS_EE_SITE",
                        "sample": "/snbrns-hub/hana/sql/ee-site?limit=10",
                    }
                },
                "HANA Stored Procedures": {
                    "snbrns01": {
                        "path": "/snbrns-hub/hana/procedures/snbrns01",
                        "description": "Ejecuta SNBRNS01 (param1, param2)",
                        "sample": "/snbrns-hub/hana/procedures/snbrns01",
                    }
                },
            },
            "hana": {
                "host": settings.hana_host,
                "port": settings.hana_port,
                "schema": settings.hana_schema,
                "encrypt": settings.hana_encrypt,
                "ssl_validate": settings.hana_ssl_validate,
            },
            "links": {
                "docs": "/docs",
                "openapi": "/openapi.json",
            },
        }

    return app


app = create_app()

# Configuración de logging básica
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
