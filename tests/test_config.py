from pathlib import Path

import pytest
from pydantic import ValidationError

from regumoa.config import Settings


@pytest.fixture(autouse=True)
def _isoler(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Chaque test démarre dans un dossier vide : aucun fichier .env n'est lu."""
    monkeypatch.chdir(tmp_path)


def test_valeurs_par_defaut() -> None:
    s = Settings()
    assert s.env == "dev"
    assert s.log_level == "INFO"
    assert s.ollama_base_url == "http://localhost:11434"


def test_surcharge_par_variable_d_environnement(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("REGUMOA_LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("REGUMOA_LLM_MODEL", "qwen2.5:7b")
    s = Settings()
    assert s.log_level == "DEBUG"
    assert s.llm_model == "qwen2.5:7b"


def test_lecture_du_fichier_env(tmp_path: Path) -> None:
    (tmp_path / ".env").write_text("REGUMOA_ENV=prod\n", encoding="utf-8")
    assert Settings().env == "prod"


def test_valeur_invalide_rejetee_au_demarrage(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("REGUMOA_ENV", "staging")
    with pytest.raises(ValidationError):
        Settings()


def test_le_mot_de_passe_ne_fuit_pas_dans_les_logs(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("REGUMOA_DATABASE_URL", "postgresql://u:SuperSecret@db/x")
    s = Settings()
    assert "SuperSecret" not in repr(s)
    assert "SuperSecret" in s.database_url.get_secret_value()
