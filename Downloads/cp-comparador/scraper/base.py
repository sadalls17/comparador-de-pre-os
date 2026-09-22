"""
Módulo base para os coletores de preço.

Cada varejista suportado deve implementar uma classe que segue esta
interface, para que o restante da aplicação (web e desktop) possa
tratar todos os coletores de forma uniforme.
"""

from dataclasses import dataclass


@dataclass
class ResultadoPreco:
    site: str
    produto: str
    preco: float
    disponivel: bool
    url: str


class ColetorBase:
    """Interface que cada coletor de site deve implementar."""

    nome_site: str = "base"

    def buscar(self, termo: str) -> list[ResultadoPreco]:
        """Busca um termo no site e retorna os resultados encontrados."""
        raise NotImplementedError(
            f"Implemente o método buscar() para o site {self.nome_site}"
        )
