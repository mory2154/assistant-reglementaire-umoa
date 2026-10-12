from importlib.metadata import version

import regumoa


def test_version_du_code_identique_au_paquet_installe() -> None:
    assert regumoa.__version__ == version("regumoa")
