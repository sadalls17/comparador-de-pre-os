import pytest

from scraper.base import ResultadoPreco


def _resultado(preco):
    return ResultadoPreco(
        site="KaBuM",
        produto="Placa de video RTX 4060",
        preco=preco,
        disponivel=True,
        url="https://www.kabum.com.br/produto/exemplo",
    )


def test_recusa_preco_negativo():
    with pytest.raises(ValueError, match="nao pode ser negativo"):
        _resultado(-1.0)


def test_aceita_preco_zero_e_positivo():
    assert _resultado(0.0).preco == 0.0
    assert _resultado(1899.90).preco == 1899.90
