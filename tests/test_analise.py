import numpy as np
import pandas as pd

from analysis.backtest import MEDIA_NULA, avaliar, melhor_significativa, rodar_laboratorio
from analysis.dados import adicionar_features
from analysis.estrategias import ESTRATEGIAS, atrasados, frios, quentes, repete_ultimo
from analysis.patterns import assinatura_faixas, contar_fibonacci, contar_pares, contar_quadrantes
from analysis.vies import frequencia_por_periodo


def sorteios_uniformes(n, seed=0):
    rng = np.random.default_rng(seed)
    return np.array([np.sort(rng.choice(np.arange(1, 61), 6, replace=False)) for _ in range(n)])


def test_contadores():
    jogo = [1, 12, 25, 34, 46, 55]
    assert contar_pares(jogo) == 3
    assert contar_fibonacci(jogo) == 3  # 1, 34, 55
    assert contar_quadrantes(jogo) == 4
    assert assinatura_faixas(jogo) == "1-1-1-1-1-1"
    assert assinatura_faixas([1, 2, 3, 58, 59, 60]) == "3-0-0-0-0-3"


def test_features_csv():
    df = pd.DataFrame({"Concurso": [1], "Data do Sorteio": ["11/03/1996"],
                       **{f"Bola{i}": [n] for i, n in enumerate([4, 5, 30, 33, 41, 52], 1)}})
    linha = adicionar_features(df).iloc[0]
    assert (linha["qtd_fibonacci"], linha["pares"], linha["impares"]) == (1, 3, 3)
    assert linha["assinatura_faixas"] == "2-0-1-1-1-1"


def test_estrategias_devolvem_permutacao_das_60():
    hist = sorteios_uniformes(150)
    for f in ESTRATEGIAS.values():
        assert sorted(f(hist)) == list(range(1, 61))


def test_estrategias_ordenam_conforme_hipotese():
    hist = np.array([[1, 2, 3, 4, 5, 6]] * 3 + [[7, 8, 9, 10, 11, 12]])
    assert set(quentes(hist)[:6]) == {1, 2, 3, 4, 5, 6}
    assert set(frios(hist)[:6]).isdisjoint(range(1, 13))
    assert set(repete_ultimo(hist)[:6]) == {7, 8, 9, 10, 11, 12}
    assert set(atrasados(hist)[:48]) == set(range(13, 61))


def test_backtest_sem_sinal_em_dados_uniformes():
    resultados = rodar_laboratorio(sorteios_uniformes(800), inicio=200)
    assert melhor_significativa(resultados) is None
    for r in resultados:
        assert abs(r.posicao_media - MEDIA_NULA) < 1.5


def test_backtest_detecta_vies_real():
    # globo viciado: dezenas 1-10 saem com o dobro da chance
    rng = np.random.default_rng(1)
    pesos = np.ones(60)
    pesos[:10] = 2
    pesos /= pesos.sum()
    bolas = np.array([np.sort(rng.choice(np.arange(1, 61), 6, replace=False, p=pesos)) for _ in range(800)])
    r = avaliar("quentes_historico", ESTRATEGIAS["quentes_historico"], bolas, inicio=200)
    assert r.p_valor < 1e-6
    assert frequencia_por_periodo(bolas, np.arange(1, 801))[0]["p_valor"] < 1e-6
