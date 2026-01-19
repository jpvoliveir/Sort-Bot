import random
from generator.score import calcular_score

FIBONACCI = {1, 2, 3, 5, 8, 13, 21, 34, 55}

def gerar_jogo():
    return sorted(random.sample(range(1, 61), 6))

def contar_pares(jogo):
    return sum(1 for n in jogo if n % 2 == 0)

def contar_fibonacci(jogo):
    return sum(1 for n in jogo if n in FIBONACCI)

def contar_quadrantes(jogo):
    quadrantes = set()

    for n in jogo:
        if 1 <= n <= 15:
            quadrantes.add(1)
        elif 16 <= n <= 30:
            quadrantes.add(2)
        elif 31 <= n <= 45:
            quadrantes.add(3)
        elif 46 <= n <= 60:
            quadrantes.add(4)

    return len(quadrantes)

def gerar_jogos_filtrados(qtd_jogos=10, score_min=0.75, tentativas_max=100000):
    jogos_aceitos = []
    tentativas = 0

    while len(jogos_aceitos) < qtd_jogos and tentativas < tentativas_max:
        tentativas += 1

        jogo = gerar_jogo()

        faixas = distribuicao_faixas(jogo)

        dados = {
            'pares': contar_pares(jogo),
            'fibonacci': contar_fibonacci(jogo),
            'quadrantes': contar_quadrantes(jogo),
            'faixas': faixas
        }

        score = calcular_score(dados)

        if score >= score_min:
            jogos_aceitos.append({
                'jogo': jogo,
                'score': score,
                'pares': dados['pares'],
                'fibonacci': dados['fibonacci'],
                'quadrantes': dados['quadrantes'],
                **faixas
            })

    return jogos_aceitos


def distribuicao_faixas(jogo):
    faixas = {
        "1-10": 0,
        "11-20": 0,
        "21-30": 0,
        "31-40": 0,
        "41-50": 0,
        "51-60": 0
    }

    for n in jogo:
        if 1 <= n <= 10:
            faixas["1-10"] += 1
        elif 11 <= n <= 20:
            faixas["11-20"] += 1
        elif 21 <= n <= 30:
            faixas["21-30"] += 1
        elif 31 <= n <= 40:
            faixas["31-40"] += 1
        elif 41 <= n <= 50:
            faixas["41-50"] += 1
        elif 51 <= n <= 60:
            faixas["51-60"] += 1

    return faixas
