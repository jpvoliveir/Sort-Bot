"""
Teste de viés físico: as 60 dezenas saem com a mesma frequência?

Qui-quadrado de aderência à uniforme, no histórico todo e por blocos de concursos
(o equipamento de sorteio já mudou ao longo dos anos, então um viés pode existir
só em um período). Como as 6 dezenas de um concurso são sem reposição, as contagens
variam um pouco menos que no modelo do qui-quadrado: o teste fica levemente
conservador (tende a não acusar viés à toa).
"""
import numpy as np
from scipy.stats import chisquare

TAMANHO_BLOCO = 500


def frequencia_por_periodo(bolas: np.ndarray, concursos: np.ndarray, tamanho_bloco=TAMANHO_BLOCO):
    """
    Retorna lista de dicts: periodo, n_concursos, chi2, p_valor
    """
    blocos = [(0, len(bolas))]
    blocos += [(i, min(i + tamanho_bloco, len(bolas))) for i in range(0, len(bolas), tamanho_bloco)]

    resultados = []
    for ini, fim in blocos:
        contagem = np.bincount(bolas[ini:fim].ravel(), minlength=61)[1:]
        chi2, p = chisquare(contagem)
        resultados.append({
            "periodo": f"{concursos[ini]}-{concursos[fim - 1]}",
            "n_concursos": fim - ini,
            "chi2": float(chi2),
            "p_valor": float(p),
        })
    return resultados
