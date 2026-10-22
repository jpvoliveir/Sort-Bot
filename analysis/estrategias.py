"""
Estratégias de "previsão": cada uma recebe o histórico (só o passado) e devolve
as 60 dezenas ordenadas da mais para a menos provável segundo a sua hipótese.

historico: matriz (n_sorteios, 6) em ordem cronológica
"""
import numpy as np

DEZENAS = np.arange(1, 61)
JANELA = 100


def _ordenar(pontos: np.ndarray) -> np.ndarray:
    # pontos indexados por dezena (posição 0 ignorada); empate -> dezena menor primeiro
    return DEZENAS[np.argsort(-pontos[1:], kind="stable")]


def _frequencia(historico: np.ndarray) -> np.ndarray:
    return np.bincount(historico.ravel(), minlength=61).astype(float)


def quentes(historico):
    """Mais sorteadas nos últimos JANELA concursos"""
    return _ordenar(_frequencia(historico[-JANELA:]))


def frios(historico):
    """Menos sorteadas nos últimos JANELA concursos"""
    return _ordenar(-_frequencia(historico[-JANELA:]))


def quentes_historico(historico):
    """Mais sorteadas em todo o histórico (hipótese de viés físico do globo)"""
    return _ordenar(_frequencia(historico))


def atrasados(historico):
    """Há mais tempo sem sair"""
    ultima = np.full(61, -1)
    indices = np.repeat(np.arange(len(historico)), 6)
    np.maximum.at(ultima, historico.ravel(), indices)
    return _ordenar(-ultima.astype(float))


def repete_ultimo(historico):
    """Dezenas do último sorteio primeiro"""
    pontos = np.zeros(61)
    pontos[historico[-1]] = 1
    return _ordenar(pontos)


def aleatorio(historico, _rng=np.random.default_rng(0)):
    """Controle: ordem aleatória (deve ficar dentro do acaso)"""
    return _rng.permutation(DEZENAS)


ESTRATEGIAS = {
    "quentes": quentes,
    "frios": frios,
    "quentes_historico": quentes_historico,
    "atrasados": atrasados,
    "repete_ultimo": repete_ultimo,
}
CONTROLE = {"aleatorio": aleatorio}
