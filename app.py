"""
Janela do robô: gerar jogos, conferir resultados e atualizar dados com um clique.

    python app.py   (ou dois cliques em "Robo Mega-Sena.bat")
"""
import contextlib
import io
import threading
import tkinter as tk
import traceback
from tkinter import ttk

from conferir import conferir_apostas
from main import OPCOES_ESTRATEGIA, QTD_JOGOS, gerar
from tools.atualizar_dados import atualizar_se_possivel


class App:
    def __init__(self, root):
        self.root = root
        root.title("Robô Mega-Sena")
        root.geometry("720x560")
        root.minsize(560, 420)

        topo = ttk.Frame(root, padding=12)
        topo.pack(fill="x")

        ttk.Label(topo, text="Estratégia:").pack(side="left")
        self.estrategia = ttk.Combobox(topo, values=OPCOES_ESTRATEGIA, state="readonly", width=18)
        self.estrategia.set("auto")
        self.estrategia.pack(side="left", padx=(4, 16))

        ttk.Label(topo, text="Jogos:").pack(side="left")
        self.qtd = ttk.Spinbox(topo, from_=1, to=20, width=4)
        self.qtd.set(QTD_JOGOS)
        self.qtd.pack(side="left", padx=4)

        botoes = ttk.Frame(root, padding=(12, 0))
        botoes.pack(fill="x")
        self.botoes = [
            ttk.Button(botoes, text="Gerar jogos", command=self.gerar),
            ttk.Button(botoes, text="Conferir resultados", command=lambda: self.executar(conferir_apostas)),
            ttk.Button(botoes, text="Atualizar dados", command=lambda: self.executar(atualizar_se_possivel)),
        ]
        for b in self.botoes:
            b.pack(side="left", padx=(0, 8), ipady=6, ipadx=6)

        self.status = ttk.Label(root, text="", padding=(12, 8), foreground="gray")
        self.status.pack(fill="x")

        self.saida = tk.Text(root, font=("Consolas", 11), wrap="none", padx=10, pady=10)
        self.saida.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.mostrar("Escolha a estratégia e clique em \"Gerar jogos\".\n\n"
                     "auto = usa uma estratégia só se ela vencer o acaso no backtest.\n"
                     "Depois do sorteio, clique em \"Conferir resultados\".")

    def gerar(self):
        try:
            qtd = max(1, int(self.qtd.get()))
        except ValueError:
            qtd = QTD_JOGOS
        self.executar(gerar, self.estrategia.get(), qtd)

    def executar(self, funcao, *args):
        """Roda em segundo plano (API e backtest levam alguns segundos) e mostra o que foi impresso"""
        for b in self.botoes:
            b.state(["disabled"])
        self.status.config(text="Trabalhando...")

        def tarefa():
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                try:
                    funcao(*args)
                except Exception:
                    print(traceback.format_exc())
            self.root.after(0, self.concluir, buffer.getvalue())

        threading.Thread(target=tarefa, daemon=True).start()

    def concluir(self, texto):
        self.mostrar(texto or "(sem saída)")
        self.status.config(text="")
        for b in self.botoes:
            b.state(["!disabled"])

    def mostrar(self, texto):
        self.saida.config(state="normal")
        self.saida.delete("1.0", "end")
        self.saida.insert("1.0", texto)
        self.saida.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
