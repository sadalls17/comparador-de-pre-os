"""
CP — Comparador de Preços — versão desktop (Tkinter)

Ponto de entrada da aplicação desktop.
"""

import threading
import tkinter as tk
from tkinter import ttk, messagebox

from scraper.kabum import ColetorKabum

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


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("CP — Comparador de Preços")
        root.geometry("720x480")

        topo = tk.Frame(root)
        topo.pack(fill="x", padx=10, pady=10)

        tk.Label(topo, text="Produto:").pack(side="left")
        self.entrada = tk.Entry(topo)
        self.entrada.pack(side="left", fill="x", expand=True, padx=8)
        self.entrada.bind("<Return>", lambda _evt: self.buscar())

        self.botao = tk.Button(topo, text="Buscar", command=self.buscar)
        self.botao.pack(side="left")

        colunas = ("preco", "site", "disponivel", "produto")
        self.tabela = ttk.Treeview(root, columns=colunas, show="headings")
        self.tabela.heading("preco", text="Preço")
        self.tabela.heading("site", text="Site")
        self.tabela.heading("disponivel", text="Disponível")
        self.tabela.heading("produto", text="Produto")
        self.tabela.column("preco", width=100, anchor="e")
        self.tabela.column("site", width=100)
        self.tabela.column("disponivel", width=90)
        self.tabela.column("produto", width=380)
        self.tabela.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.status = tk.Label(root, text="Digite um produto e clique em Buscar.", anchor="w")
        self.status.pack(fill="x", padx=10, pady=(0, 10))

    def buscar(self):
        termo = self.entrada.get().strip()
        if not termo:
            messagebox.showinfo("CP — Comparador de Preços", "Digite o nome de um produto.")
            return

        self.botao.config(state="disabled")
        self.status.config(text=f"Buscando '{termo}'...")
        self.tabela.delete(*self.tabela.get_children())

        def tarefa():
            resultados, erros = buscar_em_todos(termo)
            self.root.after(0, lambda: self._mostrar_resultados(resultados, erros))

        threading.Thread(target=tarefa, daemon=True).start()

    def _mostrar_resultados(self, resultados, erros):
        for r in resultados:
            self.tabela.insert(
                "",
                "end",
                values=(
                    f"R$ {r.preco:,.2f}",
                    r.site,
                    "Sim" if r.disponivel else "Não",
                    r.produto,
                ),
            )
        partes = [f"{len(resultados)} resultado(s) encontrado(s)."]
        if erros:
            partes.append("Falhas: " + "; ".join(erros))
        self.status.config(text=" ".join(partes))
        self.botao.config(state="normal")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
