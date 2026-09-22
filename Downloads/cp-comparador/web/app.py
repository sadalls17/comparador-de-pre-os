"""
CP — Comparador de Preços — versão web

Ponto de entrada da aplicação web (Flask).
"""

from flask import Flask, render_template, request

from scraper.kabum import ColetorKabum

app = Flask(__name__)

COLETORES = [ColetorKabum()]


def buscar_em_todos(termo: str):
    resultados = []
    erros = []
    for coletor in COLETORES:
        try:
            resultados.extend(coletor.buscar(termo))
        except Exception as erro:
            erros.append(f"{coletor.nome_site}: {erro}")
    resultados.sort(key=lambda r: r.preco)
    return resultados, erros


@app.route("/")
def index():
    termo = request.args.get("q", "").strip()
    resultados, erros = ([], [])
    if termo:
        resultados, erros = buscar_em_todos(termo)
    return render_template("index.html", termo=termo, resultados=resultados, erros=erros)


if __name__ == "__main__":
    app.run(debug=True)
