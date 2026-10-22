"""
Laboratório de previsão da Mega-Sena

1. Backtest walk-forward: cada estratégia tenta prever cada concurso usando só o passado
2. Teste de viés físico: as dezenas saem com frequências iguais?

Resultados também são exportados para data/outputs/ (Power BI).
"""
from datetime import datetime

import pandas as pd

from analysis.backtest import ACERTOS_NULO, MEDIA_NULA, rodar_laboratorio
from analysis.dados import RAIZ, carregar_sorteios, matriz_bolas
from analysis.vies import frequencia_por_periodo

df = carregar_sorteios()
bolas = matriz_bolas(df)

ultima_data = pd.to_datetime(df["Data do Sorteio"].iloc[-1], format="%d/%m/%Y")
dias_atrasado = (datetime.now() - ultima_data).days
print(f"Último concurso: {df['Concurso'].iloc[-1]} ({ultima_data:%d/%m/%Y})")
if dias_atrasado > 7:
    print(f"[ATENCAO] Dados {dias_atrasado} dias atrasados. Rode: python tools/atualizar_dados.py")

print("\n" + "=" * 78)
print("1. BACKTEST WALK-FORWARD")
print("=" * 78)
resultados = rodar_laboratorio(bolas)
print(f"{'estratégia':20s} {'posição média':>13s} {'z':>6s} {'p-valor':>8s} {'acertos/jogo':>12s} {'quadras+':>9s}")
print(f"{'(acaso)':20s} {MEDIA_NULA:13.2f} {0:6.2f} {'':>8s} {ACERTOS_NULO:12.3f}")
for r in resultados:
    marca = " <- SIGNIFICATIVA" if r.significativa else (" (controle)" if r.controle else "")
    print(f"{r.nome:20s} {r.posicao_media:13.2f} {r.z:6.2f} {r.p_valor:8.4f} "
          f"{r.acertos_top6:12.3f} {r.quadras_ou_mais:9d}{marca}")
print(f"\nConcursos testados: {resultados[0].n_concursos}. Posição média menor que {MEDIA_NULA} = melhor que o acaso.")
print("Significativa = p-valor abaixo de 0,05 / nº de estratégias (correção de Bonferroni).")
if not any(r.significativa for r in resultados):
    print("Veredito: nenhuma estratégia prevê melhor que o acaso.")

print("\n" + "=" * 78)
print("2. TESTE DE VIÉS FÍSICO (qui-quadrado de frequência das 60 dezenas)")
print("=" * 78)
vies = frequencia_por_periodo(bolas, df["Concurso"].to_numpy())
for v in vies:
    alerta = "  <- frequências desiguais (p < 0,05)" if v["p_valor"] < 0.05 else ""
    print(f"concursos {v['periodo']:>11s}  n={v['n_concursos']:5d}  chi2={v['chi2']:6.1f}  p={v['p_valor']:.3f}{alerta}")
print("Com vários períodos testados, um p < 0,05 isolado é esperado por acaso (1 em 20).")

# Exportar para visualização no Power BI
saida = RAIZ / "data" / "outputs"
saida.mkdir(parents=True, exist_ok=True)
pd.DataFrame([vars(r) for r in resultados]).to_excel(saida / "backtest_estrategias.xlsx", index=False)
pd.DataFrame(vies).to_excel(saida / "teste_vies.xlsx", index=False)
print(f"\n[OK] Exportado: {saida / 'backtest_estrategias.xlsx'}, {saida / 'teste_vies.xlsx'}")
