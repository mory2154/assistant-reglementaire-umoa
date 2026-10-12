import math

import pytest

from regumoa.adapters.fake import FakeLLM, HashingEmbedder
from regumoa.ports import LLM, Embedder


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def test_les_faux_respectent_les_contrats() -> None:
    assert isinstance(HashingEmbedder(), Embedder)
    assert isinstance(FakeLLM(), LLM)


def test_embedding_deterministe_et_normalise() -> None:
    emb = HashingEmbedder(dimension=64)
    v1, v2 = emb.embed(["Ratio de solvabilité", "Ratio de solvabilité"])
    assert v1 == v2
    assert len(v1) == 64
    assert math.isclose(math.sqrt(sum(x * x for x in v1)), 1.0)


def test_textes_proches_plus_similaires_que_textes_eloignes() -> None:
    emb = HashingEmbedder()
    q, proche, loin = emb.embed(
        [
            "fonds propres effectifs des banques",
            "calcul des fonds propres effectifs",
            "horaires d'ouverture des guichets",
        ]
    )
    assert cosine(q, proche) > cosine(q, loin)


def test_texte_vide_donne_un_vecteur_nul() -> None:
    (v,) = HashingEmbedder(dimension=8).embed([""])
    assert v == [0.0] * 8


def test_dimension_invalide() -> None:
    with pytest.raises(ValueError):
        HashingEmbedder(dimension=0)


def test_fake_llm_enregistre_les_appels() -> None:
    llm = FakeLLM(response="Article 12.")
    assert llm.generate("système", "question") == "Article 12."
    assert llm.calls == [("système", "question")]


def test_conformite_statique_aux_contrats() -> None:
    """Vérifié par mypy : les signatures doivent correspondre aux ports."""
    embedder: Embedder = HashingEmbedder()
    llm: LLM = FakeLLM()
    assert embedder.dimension > 0
    assert llm.model_name
