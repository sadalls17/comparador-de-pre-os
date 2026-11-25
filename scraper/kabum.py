"""
Coletor de preços para o site KaBuM! (https://www.kabum.com.br)

A página de busca do KaBuM! é renderizada com Next.js. O HTML retornado
para o navegador já vem com uma tag <script id="__NEXT_DATA__"> contendo,
em JSON, os dados iniciais da página — incluindo a lista de produtos
encontrados na busca. Ler esse JSON é bem mais confiável do que tentar
casar classes CSS (que mudam com frequência em sites que usam frameworks
JS modernos).

Uso rápido:
    python -m scraper.kabum "rtx 4060"
"""

from __future__ import annotations

import json
import sys
from typing import Any

import requests
from bs4 import BeautifulSoup

from scraper.base import ColetorBase, ResultadoPreco

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
}

# Chaves que costumam identificar um "produto" dentro do JSON da página.
CHAVES_NOME = {"name", "nome", "title"}
CHAVES_PRECO = {
    "price",
    "priceWithDiscount",
    "salePrice",
    "bestPrice",
    "finalPrice",
    "priceFrom",
}


def _extrair_preco(valor: Any) -> float | None:
    """Converte valores de preço em diferentes formatos (str/num) para float."""
    if valor is None:
        return None
    if isinstance(valor, (int, float)):
        return float(valor)
    if isinstance(valor, str):
        limpo = (
            valor.replace("R$", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
        )
        try:
            return float(limpo)
        except ValueError:
            return None
    return None


def _procurar_produtos(node: Any, encontrados: list[dict]) -> None:
    """
    Percorre recursivamente o JSON do __NEXT_DATA__ e coleta todo dicionário
    que pareça representar um produto (tem um campo de nome e um de preço).
    """
    if isinstance(node, dict):
        chaves = set(node.keys())
        tem_nome = chaves & CHAVES_NOME
        tem_preco = chaves & CHAVES_PRECO
        if tem_nome and tem_preco:
            nome = next(node[k] for k in tem_nome if node.get(k))
            preco = None
            for k in CHAVES_PRECO:
                if node.get(k) is not None:
                    preco = _extrair_preco(node[k])
                    if preco:
                        break
            if isinstance(nome, str) and preco:
                encontrados.append(
                    {
                        "nome": nome,
                        "preco": preco,
                        "url": node.get("url") or node.get("slug") or "",
                        "disponivel": bool(node.get("available", True)),
                    }
                )
        for valor in node.values():
            _procurar_produtos(valor, encontrados)
    elif isinstance(node, list):
        for item in node:
            _procurar_produtos(item, encontrados)


class ColetorKabum(ColetorBase):
    nome_site = "KaBuM!"
    base_url = "https://www.kabum.com.br/busca/"

    def buscar(self, termo: str) -> list[ResultadoPreco]:
        url = self.base_url + termo.strip().replace(" ", "+")
        resposta = requests.get(url, headers=HEADERS, timeout=15)
        resposta.raise_for_status()

        soup = BeautifulSoup(resposta.text, "html.parser")
        script = soup.find("script", id="__NEXT_DATA__")
        if script is None or not script.string:
            # A estrutura da página pode ter mudado, ou o acesso foi bloqueado.
            raise RuntimeError(
                "Não foi possível encontrar os dados da página do KaBuM! "
                "(tag __NEXT_DATA__ ausente). O site pode ter mudado a "
                "estrutura ou bloqueado a requisição."
            )

        dados = json.loads(script.string)

        brutos: list[dict] = []
        _procurar_produtos(dados, brutos)

        # Remove duplicados (o mesmo produto pode aparecer em mais de um
        # trecho do JSON, ex.: lista de resultados + dados de SEO).
        vistos = set()
        resultados: list[ResultadoPreco] = []
        for item in brutos:
            chave = (item["nome"], item["preco"])
            if chave in vistos:
                continue
            vistos.add(chave)
            url_produto = item["url"]
            if url_produto and not url_produto.startswith("http"):
                url_produto = "https://www.kabum.com.br/" + url_produto.lstrip("/")
            resultados.append(
                ResultadoPreco(
                    site=self.nome_site,
                    produto=item["nome"],
                    preco=item["preco"],
                    disponivel=item["disponivel"],
                    url=url_produto or url,
                )
            )

        return resultados


if __name__ == "__main__":
    termo_busca = " ".join(sys.argv[1:]) or "rtx 4060"
    coletor = ColetorKabum()
    print(f"Buscando '{termo_busca}' no {coletor.nome_site}...\n")
    try:
        for resultado in coletor.buscar(termo_busca)[:15]:
            status = "disponível" if resultado.disponivel else "indisponível"
            print(f"R$ {resultado.preco:>10,.2f}  |  {status:12}  |  {resultado.produto}")
    except Exception as erro:
        print(f"Erro ao buscar no {coletor.nome_site}: {erro}")
