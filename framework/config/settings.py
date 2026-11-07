"""Configuration du projet, lue depuis les variables d'environnement.

Ordre de priorité (du plus fort au plus faible) :
1. variables d'environnement réelles (Jenkins, terminal) ;
2. fichier .env local (secrets, jamais versionné) ;
3. fichier environments/<ENV>.env (URLs de l'environnement, versionné).
"""

import os
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_ENV = "demo"


class MissingSettingError(RuntimeError):
    """Une variable obligatoire est absente."""


@dataclass(frozen=True)
class Credentials:
    email: str
    password: str


def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise MissingSettingError(
            f"Variable d'environnement manquante : {name}. "
            "La renseigner dans .env (en local, voir .env.example) ou dans Jenkins (en CI)."
        )
    return value


@dataclass(frozen=True)
class Settings:
    env: str
    base_url: str
    api_url: str
    playwright_server: str | None

    # Propriétés (et non champs) : un identifiant manquant ne fait échouer
    # que les tests qui en ont besoin.
    @property
    def customer(self) -> Credentials:
        return Credentials(_require("CUSTOMER_EMAIL"), _require("CUSTOMER_PASSWORD"))

    @property
    def admin(self) -> Credentials:
        return Credentials(_require("ADMIN_EMAIL"), _require("ADMIN_PASSWORD"))


@cache
def get_settings() -> Settings:
    # load_dotenv ne remplace jamais une variable déjà définie :
    # on charge donc d'abord la source la plus prioritaire.
    load_dotenv(ROOT_DIR / ".env")
    env = os.environ.get("ENV", DEFAULT_ENV)

    env_file = ROOT_DIR / "environments" / f"{env}.env"
    if not env_file.exists():
        raise MissingSettingError(f"Environnement inconnu : {env} (fichier {env_file} absent).")
    load_dotenv(env_file)

    return Settings(
        env=env,
        base_url=_require("BASE_URL"),
        api_url=_require("API_URL"),
        playwright_server=os.environ.get("PLAYWRIGHT_SERVER") or None,
    )
