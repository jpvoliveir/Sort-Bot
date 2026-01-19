# --- PESOS CALCULADOS A PARTIR DO POWER BI ---
# Pesos normalizados: percentual / maior_percentual

peso_pares = {
    0: 0.0428,  # 1,32% / 30,87%
    1: 0.2854,  # 8,81% / 30,87%
    2: 0.7804,  # 24,08% / 30,87%
    3: 1.0000,  # 30,87% / 30,87% (mais comum)
    4: 0.7840,  # 24,18% / 30,87%
    5: 0.3066,  # 9,46% / 30,87%
    6: 0.0415   # 1,28% / 30,87%
}

peso_fibonacci = {
    0: 0.8838,  # 36,98% / 41,84%
    1: 1.0000,  # 41,84% / 41,84% (mais comum)
    2: 0.4209,  # 17,63% / 41,84%
    3: 0.0808,  # 3,38% / 41,84%
    4: 0.0041   # 0,17% / 41,84%
}

peso_quadrantes = {
    1: 0.0014,  # 0,07% / 50,56%
    2: 0.1250,  # 6,32% / 50,56%
    3: 1.0000,  # 50,56% / 50,56% (mais comum)
    4: 0.8516   # 43,06% / 50,56%
}

peso_faixas = {
    "1-10": 0.90,
    "11-20": 1.00,
    "21-30": 1.00,
    "31-40": 0.95,
    "41-50": 0.85,
    "51-60": 0.70
}

# Pesos de assinaturas de faixas (normalizados: percentual / 2,03%)
peso_assinatura_faixas = {
    "1-1-1-1-1-1": 1.0000,  # 2,03% (mais comum)
    "1-1-0-2-1-1": 0.6305,  # 1,28%
    "0-1-1-2-1-1": 0.6010,  # 1,22%
    "2-1-1-1-0-1": 0.5468,  # 1,11%
    "2-0-1-1-1-1": 0.5320,  # 1,08%
    "1-1-1-0-2-1": 0.5172,  # 1,05%
    "0-1-2-1-1-1": 0.4975,  # 1,01%
    "0-1-1-1-2-1": 0.4828,  # 0,98%
    "1-0-1-1-1-2": 0.4828,  # 0,98%
    "1-0-1-1-2-1": 0.4828,  # 0,98%
    "1-1-0-1-1-2": 0.4828,  # 0,98%
    "1-1-1-1-2-0": 0.4828,  # 0,98%
    "1-1-2-1-0-1": 0.4828,  # 0,98%
    "2-1-1-1-1-0": 0.4483,  # 0,91%
    "1-1-1-0-1-2": 0.4335,  # 0,88%
    "1-1-1-2-0-1": 0.4335,  # 0,88%
    "1-2-1-1-1-0": 0.4335,  # 0,88%
    "1-0-1-2-1-1": 0.4138,  # 0,84%
    "1-1-0-1-2-1": 0.4138,  # 0,84%
    "1-1-1-1-0-2": 0.4138,  # 0,84%
    "1-1-1-2-1-0": 0.4138,  # 0,84%
    "1-2-0-1-1-1": 0.4138,  # 0,84%
    "1-2-1-0-1-1": 0.4138,  # 0,84%
    "1-1-2-1-1-0": 0.3990,  # 0,81%
    "2-1-0-1-1-1": 0.3990,  # 0,81%
    "0-1-1-1-1-2": 0.3842,  # 0,78%
    "1-0-2-1-1-1": 0.3842,  # 0,78%
    "1-1-2-0-0-2": 0.3350,  # 0,68%
    "1-2-1-1-0-1": 0.3350,  # 0,68%
    "2-1-1-0-1-1": 0.3350,  # 0,68%
    # ... (outras 353 assinaturas com pesos menores)
}

def calcular_score(jogo):
    """
    jogo = {
        'pares': int,
        'fibonacci': int,
        'quadrantes': int,
        'faixas': dict
    }
    """

    score_pares = peso_pares.get(jogo['pares'], 0.01)
    score_fibo = peso_fibonacci.get(jogo['fibonacci'], 0.01)
    score_quad = peso_quadrantes.get(jogo['quadrantes'], 0.01)
    score_fx = score_faixas(jogo['faixas'])

    score_final = (
        score_pares +
        score_fibo +
        score_quad +
        score_fx
    ) / 4

    return round(score_final, 3)


def score_faixas(faixas):
    """
    Calcula o score das faixas usando a assinatura
    faixas = {"1-10": 1, "11-20": 1, "21-30": 1, "31-40": 1, "41-50": 1, "51-60": 1}
    """
    # Gerar assinatura: "1-1-1-1-1-1" (quantidade em cada faixa na ordem)
    ordem_faixas = ["1-10", "11-20", "21-30", "31-40", "41-50", "51-60"]
    assinatura = "-".join(str(faixas.get(faixa, 0)) for faixa in ordem_faixas)
    
    # Obter peso da assinatura
    peso = peso_assinatura_faixas.get(assinatura, 0.05)
    
    return peso
