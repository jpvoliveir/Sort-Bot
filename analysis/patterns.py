# Números de Fibonacci até 60
FIBONACCI = {1, 2, 3, 5, 8, 13, 21, 34, 55}

ORDEM_FAIXAS = ["1-10", "11-20", "21-30", "31-40", "41-50", "51-60"]


def is_fibonacci(n: int) -> bool:
    """
    Retorna True se o número pertence à sequência de Fibonacci
    """
    return n in FIBONACCI


def quadrante(n: int) -> int:
    """
    Divide os números da Mega-Sena em 4 quadrantes
    """
    if n <= 15:
        return 1
    elif n <= 30:
        return 2
    elif n <= 45:
        return 3
    else:
        return 4


def linha(n: int) -> int:
    """
    Divide os números em linhas de 10 (1–10, 11–20, etc.)
    """
    return (n - 1) // 10 + 1


def contar_pares(jogo) -> int:
    return sum(1 for n in jogo if n % 2 == 0)


def contar_fibonacci(jogo) -> int:
    return sum(1 for n in jogo if is_fibonacci(n))


def contar_quadrantes(jogo) -> int:
    """
    Conta quantos quadrantes diferentes existem no jogo
    """
    return len({quadrante(n) for n in jogo})


def assinatura_faixas(jogo) -> str:
    """
    Quantidade de números em cada faixa de 10, ex.: "1-1-1-1-1-1"
    """
    contagem = [0] * 6
    for n in jogo:
        contagem[linha(n) - 1] += 1
    return "-".join(map(str, contagem))
