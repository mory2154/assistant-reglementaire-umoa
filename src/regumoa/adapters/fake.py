"""Adaptateurs factices pour les tests de ReguMOA."""

import hashlib
import math
import re
from collections.abc import Sequence
from dataclasses import dataclass, field

from regumoa.ports import Vector


@dataclass
class FakeLLM:
    """LLM factice permettant de tester le contrat LLM."""

    response: str = "Réponse factice."
    calls: list[tuple[str, str]] = field(default_factory=list)

    @property
    def model_name(self) -> str:
        """Nom du modèle factice."""
        return "fake-llm"

    def generate(
        self,
        system: str,
        prompt: str,
        *,
        temperature: float = 0.0,
    ) -> str:
        """Enregistre l'appel puis renvoie la réponse configurée."""
        self.calls.append((system, prompt))
        return self.response


class HashingEmbedder:
    """Génère des embeddings déterministes par hashing trick."""

    def __init__(self, dimension: int = 256) -> None:
        if dimension <= 0:
            raise ValueError("La dimension doit être strictement positive.")

        self._dimension = dimension

    @property
    def dimension(self) -> int:
        """Dimension des vecteurs générés."""
        return self._dimension

    def embed(self, texts: Sequence[str]) -> list[Vector]:
        """Transforme chaque texte en vecteur normalisé."""
        embeddings: list[list[float]] = []

        for texte in texts:
            vector = [0.0] * self.dimension
            mots = re.findall(r"\w+", texte.lower())

            for mot in mots:
                h = int.from_bytes(
                    hashlib.blake2b(
                        mot.encode(),
                        digest_size=8,
                    ).digest(),
                    "big",
                )

                index = h % self.dimension
                signe = 1.0 if (h >> 63) == 0 else -1.0
                vector[index] += signe

            norme = math.sqrt(sum(x * x for x in vector))

            if norme > 0:
                vector = [x / norme for x in vector]

            embeddings.append(vector)

        return embeddings
