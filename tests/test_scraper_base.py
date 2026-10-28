from scraper.base import ColetorBase


def test_coletor_base_levanta_erro_nao_implementado():
    coletor = ColetorBase()
    try:
        coletor.buscar("teste")
        assert False, "Deveria ter levantado NotImplementedError"
    except NotImplementedError:
        pass
