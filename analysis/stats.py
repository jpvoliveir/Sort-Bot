import pandas as pd
from analysis.patterns import is_fibonacci


def carregar_dados(path: str) -> pd.DataFrame:
    """
    Carrega os dados da Mega-Sena (CSV ou Excel)
    """
    if path.endswith('.xlsx') or path.endswith('.xls'):
        return pd.read_excel(path)
    else:
        return pd.read_csv(path)


def analisar_fibonacci(df: pd.DataFrame) -> pd.Series:
    """
    Conta quantos números Fibonacci existem em cada sorteio
    """
    numeros = df.iloc[:, 2:8]
    return numeros.apply(
        lambda linha: sum(is_fibonacci(n) for n in linha),
        axis=1
    )


def analisar_par_impar(df: pd.DataFrame) -> pd.DataFrame:
    """
    Conta pares e ímpares em cada sorteio
    """
    numeros = df.iloc[:, 2:8]

    pares = numeros.apply(
        lambda linha: sum(n % 2 == 0 for n in linha),
        axis=1
    )

    return pd.DataFrame({
        "pares": pares,
        "impares": 6 - pares
    })


def estatisticas_fibonacci(df: pd.DataFrame):
    """
    Retorna as estatísticas de Fibonacci (mesma conta que o Power BI)
    """
    return df["qtd_fibonacci"].value_counts(normalize=True)
