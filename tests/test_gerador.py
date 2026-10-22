import random

import pytest

from generator.gerador import TOP_RANKING, gerar_jogos
from generator.popularidade import motivos_popularidade


@pytest.mark.parametrize("jogo, motivo", [
    ([3, 7, 12, 19, 25, 48], "datas"),
    ([10, 11, 12, 35, 47, 58], "sequencia"),
    ([5, 15, 25, 35, 45, 55], "progressao"),
    ([2, 4, 6, 8, 35, 52], "linha_volante"),
    ([3, 13, 23, 33, 44, 58], "coluna_volante"),
])
def test_motivos_popularidade(jogo, motivo):
    assert motivo in motivos_popularidade(jogo)


def test_jogo_comum_nao_e_popular():
    assert motivos_popularidade([4, 17, 29, 38, 46, 53]) == []


def test_sorteio_anterior_e_popular():
    assert "sorteio_anterior" in motivos_popularidade([4, 17, 29, 38, 46, 53], {(4, 17, 29, 38, 46, 53)})


def test_gerar_jogos_distintos_e_validos():
    jogos = gerar_jogos(50, rng=random.Random(0))
    assert len(jogos) == 50
    assert len({tuple(j) for j in jogos}) == 50
    for j in jogos:
        assert j == sorted(j) and len(set(j)) == 6 and all(1 <= n <= 60 for n in j)
        assert motivos_popularidade(j) == []


def test_gerar_jogos_respeita_ranking():
    ranking = list(range(60, 0, -1))
    jogos = gerar_jogos(10, ranking=ranking, rng=random.Random(0))
    assert all(set(j) <= set(ranking[:TOP_RANKING]) for j in jogos)
