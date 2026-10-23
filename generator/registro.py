"""
Registro das apostas: cada jogo gerado é salvo com o concurso a que se destina.
Depois do sorteio, conferir() preenche acertos e prêmio.
"""
from datetime import datetime
from pathlib import Path

import pandas as pd

from analysis.dados import COLUNAS_BOLAS, RAIZ

CAMINHO_REGISTRO = RAIZ / "data" / "apostas" / "registro_apostas.csv"
PRECO_JOGO = 6.00  # aposta simples de 6 dezenas
COLUNAS = ["concurso", "gerado_em", "estrategia", "jogo", "acertos", "premio"]


def ler_reais(texto) -> float:
    """'R$1.389,80' -> 1389.8"""
    return float(str(texto).replace("R$", "").replace(".", "").replace(",", "."))


def carregar_registro(caminho=CAMINHO_REGISTRO) -> pd.DataFrame:
    if not Path(caminho).exists():
        return pd.DataFrame(columns=COLUNAS)
    return pd.read_csv(caminho)


def registrar_jogos(jogos, concurso, estrategia, caminho=CAMINHO_REGISTRO):
    novos = pd.DataFrame({
        "concurso": concurso,
        "gerado_em": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "estrategia": estrategia,
        "jogo": ["-".join(f"{n:02d}" for n in j) for j in jogos],
    }).reindex(columns=COLUNAS)
    registro = carregar_registro(caminho)
    registro = novos if registro.empty else pd.concat([registro, novos], ignore_index=True)
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    registro[COLUNAS].to_csv(caminho, index=False, encoding="utf-8")


def conferir(sorteios: pd.DataFrame, caminho=CAMINHO_REGISTRO) -> pd.DataFrame:
    """
    Preenche acertos e prêmio dos jogos cujo concurso já foi sorteado e salva o registro
    """
    registro = carregar_registro(caminho)
    por_concurso = sorteios.set_index("Concurso")
    for i, aposta in registro.iterrows():
        if pd.notna(aposta["acertos"]) or aposta["concurso"] not in por_concurso.index:
            continue
        sorteio = por_concurso.loc[aposta["concurso"]]
        acertos = len(set(map(int, aposta["jogo"].split("-"))) & set(sorteio[COLUNAS_BOLAS]))
        registro.loc[i, "acertos"] = acertos
        registro.loc[i, "premio"] = ler_reais(sorteio[f"Rateio {acertos} acertos"]) if acertos >= 4 else 0.0
    if not registro.empty:
        registro[COLUNAS].to_csv(caminho, index=False, encoding="utf-8")
    return registro
