# SNBRNS Processes Hub

Base de una app Python con FastAPI preparada para desplegar en SAP BTP - Cloud Foundry.

## Estructura

```
SNBRNS Processes Hub/
├─ app/
│  ├─ core/
│  │  └─ settings.py
│  ├─ db/
│  │  └─ hana_client.py
│  ├─ routers/
│  │  ├─ hana_sql_queries.py
│  │  └─ hana_procedures.py
│  ├─ dependencies.py
│  └─ main.py
├─ .env.example
├─ requirements.txt
├─ Procfile
├─ manifest.yml
└─ README.md
```

## Requisitos

- Python 3.10+
- Acceso a SAP HANA (local o vía servicio CF)
- `cf` CLI para despliegue en Cloud Foundry

## Configuración

- Para desarrollo local, copia `.env.example` a `.env` y ajusta valores.
- En Cloud Foundry, las credenciales de HANA se obtienen desde `VCAP_SERVICES` automáticamente.

## Ejecutar en local

```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows PowerShell
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- Health check: `GET http://localhost:8000/health`
- SQL ejemplo: `GET http://localhost:8000/snbrns-hub/hana/sql/ee-site?limit=10`
- Procedimiento ejemplo: `POST http://localhost:8000/snbrns-hub/hana/procedures/snbrns01` con cuerpo JSON:

```json
{
  "param1": 1,
  "param2": "ABC"
}
```

## Despliegue en Cloud Foundry (SAP BTP)

1. Inicia sesión y selecciona espacio:
   ```bash
   cf login
   cf target -o <org> -s <space>
   ```
2. Asegúrate de tener el servicio HANA creado y ligado a la app (ejemplo):
   ```bash
   # Crear servicio HANA (variable según plan/nombre disponible)
   cf create-service hana <plan> snbrns-hana
   # Crear/actualizar app leyendo manifest.yml y ligando servicio
   cf push -f manifest.yml
   cf bind-service snbrns-processes-hub snbrns-hana
   cf restage snbrns-processes-hub
   ```

- El `Procfile` inicia `gunicorn` con worker de Uvicorn.
- `PORT` es gestionado por CF; no necesita configurarse manualmente.

## Mejores prácticas incluidas

- Carga de configuración con `pydantic-settings` y `.env` para local.
- Detección y parseo de `VCAP_SERVICES` (HANA) con soporte de certificado CA.
- Cliente HANA con ejecución de consultas parametrizadas y procedimientos.
- Routers separados para SQL y procedimientos.
- Dependencias cacheadas (Settings) y separación de responsabilidades.

## Notas

- Si tu servicio HANA proporciona un certificado CA en `VCAP_SERVICES`, el proyecto lo escribe temporalmente y valida SSL si `HANA_SSL_VALIDATE=true`.
- Si no hay certificado, se puede usar `HANA_SSL_VALIDATE=false` (no recomendado en producción).