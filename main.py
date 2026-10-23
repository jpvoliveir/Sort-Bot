"""
Gera os jogos do próximo concurso e salva no registro de apostas.

    python main.py                        # usa estratégia só se ela passar no backtest
    python main.py --estrategia quentes   # força uma estratégia
    python main.py --qtd 5                # quantidade de jogos
"""
import argparse

from analysis.backtest import avaliar, melhor_significativa, rodar_laboratorio
from analysis.dados import carregar_sorteios, matriz_bolas
from analysis.estrategias import ESTRATEGIAS
from generator.exportador import exportar_jogos
from generator.gerador import gerar_jogos
from generator.registro import CAMINHO_REGISTRO, registrar_jogos
from tools.atualizar_dados import atualizar_se_possivel

QTD_JOGOS = 3
OPCOES_ESTRATEGIA = ["auto", "aleatorio", *ESTRATEGIAS]


def gerar(estrategia="auto", qtd_jogos=QTD_JOGOS):
    atualizar_se_possivel()
    df = carregar_sorteios()
    bolas = matriz_bolas(df)
    proximo = int(df["Concurso"].iloc[-1]) + 1
    print(f"Dados até o concurso {proximo - 1} ({df['Data do Sorteio'].iloc[-1]})")

    if estrategia == "auto":
        # Só usa uma estratégia de previsão se ela passou no backtest
        melhor = melhor_significativa(rodar_laboratorio(bolas))
        origem = melhor.nome if melhor else "aleatorio"
        if melhor:
            print(f"Estratégia aprovada no backtest: {melhor.nome} (p = {melhor.p_valor:.4f})")
        else:
            print("Nenhuma estratégia superou o acaso no backtest -> jogos aleatórios")
    else:
        origem = estrategia
        if origem in ESTRATEGIAS:
            r = avaliar(origem, ESTRATEGIAS[origem], bolas)
            print(f"Estratégia escolhida: {origem} (backtest: p = {r.p_valor:.4f}, "
                  f"{r.acertos_top6:.3f} acertos/jogo contra 0,600 do acaso)")

    ranking = ESTRATEGIAS[origem](bolas) if origem in ESTRATEGIAS else None
    jogos = gerar_jogos(
        qtd_jogos=qtd_jogos,
        ranking=ranking,
        sorteios_anteriores={tuple(sorted(j)) for j in bolas},
    )

    # Exibir no terminal
    print("=" * 60)
    print(f"JOGOS PARA O CONCURSO {proximo} (sem combinações populares)")
    print("=" * 60)
    for idx, jogo in enumerate(jogos, 1):
        print(f"{idx:2d}. {'-'.join(f'{n:02d}' for n in jogo)}")
    print("=" * 60)

    # Exportar para arquivo e registrar para conferência após o sorteio
    exportar_jogos(jogos, origem)
    registrar_jogos(jogos, proximo, origem)
    print(f"Registrado em {CAMINHO_REGISTRO} -> depois do sorteio, confira os resultados")
    return jogos


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--estrategia", default="auto", choices=OPCOES_ESTRATEGIA)
    parser.add_argument("--qtd", type=int, default=QTD_JOGOS)
    args = parser.parse_args()
    gerar(args.estrategia, args.qtd)
