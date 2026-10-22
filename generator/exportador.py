from pathlib import Path

import pandas as pd

from analysis.dados import RAIZ

CAMINHO_PADRAO = RAIZ / "data" / "outputs" / "jogos_gerados.xlsx"


def exportar_jogos(jogos, origem, nome_arquivo=CAMINHO_PADRAO):
    if not jogos:
        print("Nenhum jogo para exportar.")
        return

    df = pd.DataFrame({
        "jogo": ["-".join(map(str, j)) for j in jogos],
        "origem": origem,
    })

    Path(nome_arquivo).parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(nome_arquivo, index=False)

    print(f"Arquivo exportado com sucesso: {nome_arquivo}")
