import pandas as pd

from generator.registro import carregar_registro, conferir, ler_reais, registrar_jogos


def sorteios():
    return pd.DataFrame({
        "Concurso": [3073],
        **{f"Bola{i}": [n] for i, n in enumerate([4, 13, 23, 28, 41, 58], 1)},
        "Rateio 6 acertos": ["R$0,00"],
        "Rateio 5 acertos": ["R$23.138,67"],
        "Rateio 4 acertos": ["R$510,55"],
    })


def test_ler_reais():
    assert ler_reais("R$1.389,80") == 1389.8
    assert ler_reais("R$0,00") == 0.0


def test_registrar_e_conferir(tmp_path):
    caminho = tmp_path / "registro.csv"
    registrar_jogos([[6, 17, 27, 30, 43, 58], [4, 13, 23, 28, 1, 2]], 3073, "quentes", caminho)
    registrar_jogos([[4, 13, 23, 28, 41, 60]], 3073, "aleatorio", caminho)
    registrar_jogos([[1, 2, 3, 4, 5, 6]], 3074, "aleatorio", caminho)

    registro = conferir(sorteios(), caminho)

    assert registro["acertos"].tolist()[:3] == [1, 4, 5]
    assert registro["premio"].tolist()[:3] == [0.0, 510.55, 23138.67]
    assert pd.isna(registro["acertos"].iloc[3])  # concurso 3074 ainda não sorteado
    assert carregar_registro(caminho)["acertos"].tolist()[:3] == [1, 4, 5]  # foi salvo


def test_conferir_nao_reconfere(tmp_path):
    caminho = tmp_path / "registro.csv"
    registrar_jogos([[6, 17, 27, 30, 43, 58]], 3073, "quentes", caminho)
    conferir(sorteios(), caminho)
    assert conferir(sorteios(), caminho)["acertos"].tolist() == [1]
