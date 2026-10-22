"""
Combinações que muita gente joga. Todas têm a mesma chance de sair, mas, se saírem,
o prêmio é dividido com mais ganhadores. Evitá-las é a única vantagem real disponível.
"""
from analysis.patterns import linha

LIMITE_DATAS = 31  # dias do mês
MAX_DATAS = 4  # 5 ou 6 dezenas <= 31 parece data de aniversário
MAX_SEQUENCIA = 2  # 3 ou mais consecutivas (ex.: 10-11-12)
MAX_MESMA_LINHA = 3  # volante tem 6 linhas de 10 dezenas
MAX_MESMA_COLUNA = 3  # e 10 colunas (mesmo final)


def _maior_sequencia(jogo):
    maior = atual = 1
    for a, b in zip(jogo, jogo[1:]):
        atual = atual + 1 if b == a + 1 else 1
        maior = max(maior, atual)
    return maior


def _max_repeticao(valores):
    return max(valores.count(v) for v in valores)


def motivos_popularidade(jogo, sorteios_anteriores=frozenset()):
    """
    jogo: lista ordenada de 6 dezenas
    sorteios_anteriores: conjunto de tuplas ordenadas já sorteadas
    Retorna a lista de motivos pelos quais o jogo é "popular" (vazia = ok)
    """
    motivos = []
    if sum(n <= LIMITE_DATAS for n in jogo) > MAX_DATAS:
        motivos.append("datas")
    if _maior_sequencia(jogo) > MAX_SEQUENCIA:
        motivos.append("sequencia")
    diferencas = {b - a for a, b in zip(jogo, jogo[1:])}
    if len(diferencas) == 1:
        motivos.append("progressao")
    if _max_repeticao([linha(n) for n in jogo]) > MAX_MESMA_LINHA:
        motivos.append("linha_volante")
    if _max_repeticao([n % 10 for n in jogo]) > MAX_MESMA_COLUNA:
        motivos.append("coluna_volante")
    if tuple(jogo) in sorteios_anteriores:
        motivos.append("sorteio_anterior")
    return motivos
