"""Interfaces (« ports ») dont dépend le code métier.

Le pipeline ne connaît que ces contrats. Les implémentations concrètes
(« adaptateurs ») vivent dans ``regumoa.adapters`` : Ollama en production,
modèles factices déterministes dans les tests.
"""

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

Vector = list[float]


@runtime_checkable
class Embedder(Protocol):
    """Transforme des textes en vecteurs pour la recherche sémantique."""

    @property
    def dimension(self) -> int:
        """Taille des vecteurs produits."""
        ...

    def embed(self, texts: Sequence[str]) -> list[Vector]:
        """Un vecteur normalisé (norme 1) par texte, dans le même ordre."""
        ...


@runtime_checkable
class LLM(Protocol):
    """Génère une réponse texte à partir d'instructions et d'une question."""

    @property
    def model_name(self) -> str: ...

    def generate(self, system: str, prompt: str, *, temperature: float = 0.0) -> str:
        """Température 0 par défaut : en réglementaire, on veut de la constance."""
        ...
