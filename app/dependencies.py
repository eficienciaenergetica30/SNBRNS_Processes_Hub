from functools import lru_cache

from app.core.settings import Settings, load_settings
from app.db.hana_client import HanaClient


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return load_settings()


def get_hana_client() -> HanaClient:
    settings = get_settings()
    return HanaClient(settings)