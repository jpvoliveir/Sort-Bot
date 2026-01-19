# Números de Fibonacci até 60
FIBONACCI = {1, 2, 3, 5, 8, 13, 21, 34, 55}


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
