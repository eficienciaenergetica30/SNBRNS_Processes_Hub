import json
import os
import tempfile
from typing import Any, Dict, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


class Settings(BaseSettings):
    """Configuración de la aplicación y credenciales de HANA.

    Carga variables desde `.env` y/o variables de entorno.
    Si existe `VCAP_SERVICES`, se intentan extraer credenciales de HANA automáticamente.
    """

    app_name: str = Field(default="SNBRNS Processes Hub")
    environment: str = Field(default="development", env="ENV")

    # Credenciales HANA
    hana_host: Optional[str] = None
    hana_port: Optional[int] = None
    hana_user: Optional[str] = None
    hana_password: Optional[str] = None
    hana_schema: Optional[str] = None

    # TLS/SSL
    hana_encrypt: bool = Field(default=True)
    hana_ssl_validate: bool = Field(default=False)
    hana_cert_path: Optional[str] = None

    # CORS
    cors_allow_origins: Optional[str] = Field(default=None, env="CORS_ALLOW_ORIGINS")
    cors_allow_methods: Optional[str] = Field(default=None, env="CORS_ALLOW_METHODS")
    cors_allow_headers: Optional[str] = Field(default=None, env="CORS_ALLOW_HEADERS")
    cors_allow_credentials: bool = Field(default=False, env="CORS_ALLOW_CREDENTIALS")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    def hana_connection_kwargs(self) -> Dict[str, Any]:
        """Devuelve kwargs para `hdbcli.dbapi.connect` basados en la configuración actual."""
        kwargs: Dict[str, Any] = {
            "address": self.hana_host,
            "port": int(self.hana_port) if self.hana_port else None,
            "user": self.hana_user,
            "password": self.hana_password,
            "encrypt": self.hana_encrypt,
            "sslValidateCertificate": self.hana_ssl_validate,
        }
        if self.hana_cert_path:
            kwargs["sslTrustStore"] = self.hana_cert_path
        # Elimina claves None
        return {k: v for k, v in kwargs.items() if v is not None}


def _extract_hana_from_vcap(vcap_services: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Intenta extraer credenciales HANA desde VCAP_SERVICES.

    Busca claves típicas de servicio: 'hana', 'hanatrial', 'sap-hana'.
    Devuelve el dict `credentials` del primer servicio encontrado.
    """
    candidate_keys = ["hana", "hanatrial", "sap-hana"]
    for key in candidate_keys:
        if key in vcap_services and isinstance(vcap_services[key], list) and vcap_services[key]:
            entry = vcap_services[key][0]
            creds = entry.get("credentials") or {}
            if creds:
                return creds
    # Si no se encontraron claves conocidas, intenta cualquier servicio con 'hana' en nombre
    for key, services in vcap_services.items():
        if "hana" in key and isinstance(services, list) and services:
            entry = services[0]
            creds = entry.get("credentials") or {}
            if creds:
                return creds
    return None


def _write_certificate_tmp_if_present(credentials: Dict[str, Any]) -> Optional[str]:
    """Escribe el certificado en un archivo temporal si está presente en las credenciales.

    Devuelve la ruta del archivo o None si no aplica.
    """
    cert = credentials.get("certificate") or credentials.get("ca")
    if not cert:
        return None
    fd, path = tempfile.mkstemp(prefix="hana-ca-", suffix=".pem")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(cert)
    return path


def load_settings() -> Settings:
    """Carga las `Settings` combinando `.env`/entorno y VCAP_SERVICES si existe."""
    # Cargar .env para entorno local
    load_dotenv(override=False)

    # Primero, cargar valores desde Pydantic BaseSettings (env/.env)
    base = Settings()

    # Luego, si hay VCAP_SERVICES, tratar de completar/overrides
    vcap_raw = os.getenv("VCAP_SERVICES")
    if vcap_raw:
        try:
            vcap = json.loads(vcap_raw)
            creds = _extract_hana_from_vcap(vcap)
            if creds:
                cert_path = _write_certificate_tmp_if_present(creds)
                # Crear una nueva instancia con overrides desde VCAP
                base = Settings(
                    hana_host=creds.get("host") or creds.get("hostname") or base.hana_host,
                    hana_port=int(creds.get("port")) if creds.get("port") else base.hana_port,
                    hana_user=creds.get("user") or creds.get("username") or base.hana_user,
                    hana_password=creds.get("password") or base.hana_password,
                    hana_schema=creds.get("schema") or base.hana_schema,
                    hana_encrypt=bool(creds.get("encrypt", base.hana_encrypt)),
                    hana_ssl_validate=bool(creds.get("sslValidateCertificate", base.hana_ssl_validate)),
                    hana_cert_path=cert_path or base.hana_cert_path,
                    app_name=base.app_name,
                    environment=os.getenv("ENV", base.environment),
                )
        except Exception:
            # Si VCAP_SERVICES no es válido, continuar con base
            pass

    return base