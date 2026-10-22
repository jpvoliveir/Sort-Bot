"""
Backtest walk-forward das estratégias de previsão.

Para cada concurso t (a partir de `inicio`), a estratégia vê só os sorteios
anteriores e ordena as 60 dezenas. Medimos a posição (1 a 60) de cada dezena
sorteada nessa ordem.

Se o sorteio é justo, as 6 dezenas são uma amostra uniforme sem reposição,
independente do passado, então a posição média por concurso tem
    média = 30,5   e   variância = (60² - 1)/12 / 6 * (60 - 6)/(60 - 1)
qualquer que seja a estratégia. Isso dá um teste z exato o bastante, sem simulação.
"""
from dataclasses import dataclass

import numpy as np
from scipy.stats import norm

from analysis.estrategias import CONTROLE, ESTRATEGIAS

INICIO_PADRAO = 500
MEDIA_NULA = 30.5
VAR_NULA = (60**2 - 1) / 12 / 6 * (60 - 6) / (60 - 1)
ACERTOS_NULO = 6 * 6 / 60


@dataclass
class Resultado:
    nome: str
    n_concursos: int
    posicao_media: float  # menor que 30,5 = melhor que o acaso
    z: float
    p_valor: float
    acertos_top6: float  # média de acertos jogando as 6 primeiras (acaso = 0,6)
    quadras_ou_mais: int
    controle: bool = False
    significativa: bool = False


def avaliar(nome, estrategia, bolas: np.ndarray, inicio=INICIO_PADRAO, controle=False) -> Resultado:
    posicoes_medias = []
    acertos = []
    for t in range(inicio, len(bolas)):
        ranking = estrategia(bolas[:t])
        posicao = np.empty(61, dtype=int)
        posicao[ranking] = np.arange(1, 61)
        sorteadas = posicao[bolas[t]]
        posicoes_medias.append(sorteadas.mean())
        acertos.append(int((sorteadas <= 6).sum()))

    n = len(posicoes_medias)
    media = float(np.mean(posicoes_medias))
    z = (MEDIA_NULA - media) / np.sqrt(VAR_NULA / n)
    acertos = np.array(acertos)
    return Resultado(
        nome=nome,
        n_concursos=n,
        posicao_media=media,
        z=float(z),
        p_valor=float(norm.sf(z)),
        acertos_top6=float(acertos.mean()),
        quadras_ou_mais=int((acertos >= 4).sum()),
        controle=controle,
    )


def rodar_laboratorio(bolas, estrategias=ESTRATEGIAS, inicio=INICIO_PADRAO, alpha=0.05):
    """
    Avalia todas as estratégias. Como testamos várias hipóteses de uma vez,
    usamos a correção de Bonferroni: cada uma precisa de p < alpha / n_estrategias.
    """
    resultados = [avaliar(nome, f, bolas, inicio) for nome, f in estrategias.items()]
    limite = alpha / len(estrategias)
    for r in resultados:
        r.significativa = r.p_valor < limite
    resultados += [avaliar(nome, f, bolas, inicio, controle=True) for nome, f in CONTROLE.items()]
    return resultados


def melhor_significativa(resultados):
    candidatas = [r for r in resultados if r.significativa and not r.controle]
    return min(candidatas, key=lambda r: r.p_valor) if candidatas else None
