"""
Gerador de jogos da Mega-Sena baseado em regras e análises estatísticas
"""
import random
from analysis.patterns import quadrante

FIBONACCI = {1, 2, 3, 5, 8, 13, 21, 34}


def gerar_jogo():
    """
    Gera um jogo da Mega-Sena (6 números únicos entre 1 e 60)
    """
    jogo = set()
    while len(jogo) < 6:
        jogo.add(random.randint(1, 60))
    return sorted(list(jogo))


def contar_fibonacci(jogo):
    """
    Conta quantos números Fibonacci existem no jogo
    """
    return sum(1 for n in jogo if n in FIBONACCI)


def contar_pares_impares(jogo):
    pares = sum(1 for n in jogo if n % 2 == 0)
    impares = sum(1 for n in jogo if n % 2 != 0)
    return pares, impares


def contar_quadrantes(jogo):
    """
    Conta quantos quadrantes diferentes existem no jogo
    """
    quadrantes_unicos = {quadrante(n) for n in jogo}
    return len(quadrantes_unicos)


def peso_pares(pares):
    """
    Retorna o peso probabilístico normalizado baseado na distribuição real de pares
    Pesos normalizados: percentual / maior_percentual (30,87%)
    Valores baseados na análise do Power BI
    """
    pesos = {
        0: 0.0428,  # 1,32% / 30,87% ≈ 0,04
        1: 0.2854,  # 8,81% / 30,87% ≈ 0,29
        2: 0.7804,  # 24,08% / 30,87% ≈ 0,78
        3: 1.0000,  # 30,87% / 30,87% = 1,00 (mais comum)
        4: 0.7840,  # 24,18% / 30,87% ≈ 0,78
        5: 0.3066,  # 9,46% / 30,87% ≈ 0,31
        6: 0.0415   # 1,28% / 30,87% ≈ 0,04
    }
    return pesos.get(pares, 0.05)  # Fallback para valores fora do esperado


def peso_fibonacci(qtd):
    """
    Retorna o peso probabilístico normalizado baseado na distribuição real de Fibonacci
    Pesos normalizados: percentual / maior_percentual (41,84%)
    Valores baseados na análise do Power BI
    """
    pesos = {
        0: 0.8838,  # 36,98% / 41,84% ≈ 0,88
        1: 1.0000,  # 41,84% / 41,84% = 1,00 (mais comum)
        2: 0.4209,  # 17,63% / 41,84% ≈ 0,42
        3: 0.0808,  # 3,38% / 41,84% ≈ 0,08
        4: 0.0041   # 0,17% / 41,84% ≈ 0,01
    }
    return pesos.get(qtd, 0.05)  # Fallback para valores fora do esperado


def peso_quadrantes(qtd):
    """
    Retorna o peso probabilístico normalizado baseado na distribuição real de quadrantes
    Pesos normalizados: percentual / maior_percentual (50,56%)
    Valores baseados na análise do Power BI
    """
    pesos = {
        1: 0.0014,  # 0,07% / 50,56% ≈ 0,001 (quase nunca)
        2: 0.1250,  # 6,32% / 50,56% ≈ 0,12 (raramente)
        3: 1.0000,  # 50,56% / 50,56% = 1,00 (mais comum)
        4: 0.8516   # 43,06% / 50,56% ≈ 0,85 (frequentemente)
    }
    return pesos.get(qtd, 0.05)  # Fallback para valores fora do esperado
