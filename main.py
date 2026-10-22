from analysis.backtest import melhor_significativa, rodar_laboratorio
from analysis.dados import carregar_sorteios, matriz_bolas
from analysis.estrategias import ESTRATEGIAS
from generator.exportador import exportar_jogos
from generator.gerador import gerar_jogos

QTD_JOGOS = 3

df = carregar_sorteios()
bolas = matriz_bolas(df)
print(f"Dados até o concurso {df['Concurso'].iloc[-1]} ({df['Data do Sorteio'].iloc[-1]})")

# Só usa uma estratégia de previsão se ela passou no backtest
melhor = melhor_significativa(rodar_laboratorio(bolas))
if melhor:
    ranking = ESTRATEGIAS[melhor.nome](bolas)
    origem = melhor.nome
    print(f"Estratégia aprovada no backtest: {melhor.nome} (p = {melhor.p_valor:.4f})")
else:
    ranking = None
    origem = "aleatorio"
    print("Nenhuma estratégia superou o acaso no backtest -> jogos aleatórios (rode backtest.py para detalhes)")

jogos = gerar_jogos(
    qtd_jogos=QTD_JOGOS,
    ranking=ranking,
    sorteios_anteriores={tuple(sorted(j)) for j in bolas},
)

# Exibir no terminal
print("=" * 60)
print("JOGOS GERADOS PARA A MEGA-SENA (sem combinações populares)")
print("=" * 60)
for idx, jogo in enumerate(jogos, 1):
    print(f"{idx:2d}. {'-'.join(f'{n:02d}' for n in jogo)}")
print("=" * 60)

# Exportar para arquivo
exportar_jogos(jogos, origem)
