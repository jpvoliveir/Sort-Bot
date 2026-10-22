import random

from generator.popularidade import motivos_popularidade

TOP_RANKING = 20  # com estratégia aprovada, sorteia entre as 20 dezenas mais bem ranqueadas


def gerar_jogos(qtd_jogos=10, ranking=None, sorteios_anteriores=frozenset(),
                rng=None, tentativas_max=100000):
    """
    Gera jogos distintos e não populares.

    ranking: ordem de dezenas de uma estratégia aprovada no backtest; None = sorteio uniforme
    """
    rng = rng or random.Random()
    universo = list(ranking[:TOP_RANKING]) if ranking is not None else list(range(1, 61))

    jogos = set()
    tentativas = 0
    while len(jogos) < qtd_jogos and tentativas < tentativas_max:
        tentativas += 1
        jogo = sorted(int(n) for n in rng.sample(universo, 6))
        if not motivos_popularidade(jogo, sorteios_anteriores):
            jogos.add(tuple(jogo))

    if len(jogos) < qtd_jogos:
        print(f"[AVISO] Só foi possível gerar {len(jogos)} de {qtd_jogos} jogos.")
    return [list(j) for j in sorted(jogos)]
