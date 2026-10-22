"""
Carregamento dos sorteios históricos e geração do CSV de análise (usado no Power BI)
"""
from pathlib import Path

import numpy as np
import pandas as pd

from analysis.patterns import (
    assinatura_faixas,
    contar_fibonacci,
    contar_pares,
    contar_quadrantes,
)

RAIZ = Path(__file__).resolve().parent.parent
CAMINHO_EXCEL = RAIZ / "data" / "raw" / "Mega-Sena.xlsx"
CAMINHO_CSV = RAIZ / "data" / "processed" / "analise_megasena.csv"
COLUNAS_BOLAS = [f"Bola{i}" for i in range(1, 7)]


def carregar_sorteios(caminho=CAMINHO_EXCEL) -> pd.DataFrame:
    """
    Carrega o Excel oficial da Caixa, ordenado por concurso
    """
    df = pd.read_excel(caminho)
    faltando = [c for c in ["Concurso", "Data do Sorteio", *COLUNAS_BOLAS] if c not in df.columns]
    if faltando:
        raise ValueError(f"Colunas ausentes em {caminho}: {faltando}")
    return df.sort_values("Concurso").reset_index(drop=True)


def matriz_bolas(df: pd.DataFrame) -> np.ndarray:
    """
    Matriz (n_sorteios, 6) com as dezenas de cada sorteio, em ordem cronológica
    """
    return df[COLUNAS_BOLAS].to_numpy(dtype=int)


def adicionar_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Acrescenta as colunas descritivas usadas no Power BI
    """
    jogos = [sorted(j) for j in matriz_bolas(df)]
    df = df.copy()
    df["qtd_fibonacci"] = [contar_fibonacci(j) for j in jogos]
    df["pares"] = [contar_pares(j) for j in jogos]
    df["impares"] = 6 - df["pares"]
    df["quadrantes"] = [contar_quadrantes(j) for j in jogos]
    df["assinatura_faixas"] = [assinatura_faixas(j) for j in jogos]
    return df


def gerar_csv_analise(caminho_excel=CAMINHO_EXCEL, caminho_csv=CAMINHO_CSV) -> pd.DataFrame:
    df = adicionar_features(carregar_sorteios(caminho_excel))
    Path(caminho_csv).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(caminho_csv, index=False, encoding="utf-8")
    return df
