"""
Backtest do robô da Mega-Sena

Este módulo testa o desempenho do gerador de jogos
usando dados históricos reais.
"""

import pandas as pd

from generator.score import calcular_score
from generator.gerador import (
    contar_pares,
    contar_fibonacci,
    contar_quadrantes,
    distribuicao_faixas,
    gerar_jogos_filtrados
)

# ajuste o caminho se necessário
df = pd.read_excel("data/raw/Mega-Sena.xlsx")

# Verificar se os dados estão atualizados
from datetime import datetime
# Converter data corretamente (pode estar como string)
ultima_data_dt = pd.to_datetime(df["Data do Sorteio"], format="%d/%m/%Y", errors="coerce").max()
hoje = datetime.now()

dias_atrasado = (hoje - ultima_data_dt).days if pd.notna(ultima_data_dt) else 999
if dias_atrasado > 30:
    print(f"[ATENCAO] Arquivo esta {dias_atrasado} dias atrasado!")
    print(f"Ultima data: {ultima_data_dt.strftime('%d/%m/%Y') if pd.notna(ultima_data_dt) else 'N/A'}")
    print("Considere atualizar data/raw/Mega-Sena.xlsx com dados mais recentes\n")
elif dias_atrasado >= 0:
    print(f"[OK] Arquivo atualizado. Ultima data: {ultima_data_dt.strftime('%d/%m/%Y') if pd.notna(ultima_data_dt) else 'N/A'}\n")


def calcular_score_sorteio(row):
    jogo = sorted([
        row["Bola1"],
        row["Bola2"],
        row["Bola3"],
        row["Bola4"],
        row["Bola5"],
        row["Bola6"]
    ])

    dados = {
        "pares": contar_pares(jogo),
        "fibonacci": contar_fibonacci(jogo),
        "quadrantes": contar_quadrantes(jogo),
        "faixas": distribuicao_faixas(jogo)
    }

    return calcular_score(dados)


df["score"] = df.apply(calcular_score_sorteio, axis=1)

jogos_gerados = gerar_jogos_filtrados(
    qtd_jogos=500,
    score_min=0.7
)

df_gerados = pd.DataFrame(jogos_gerados)

print("REAIS")
print(df["score"].describe())

print("\nGERADOS")
print(df_gerados["score"].describe())

print("\n" + "="*60)
print("INTERPRETACAO:")
print("="*60)
print("""
[OK] Modelo saudavel:
   - Medias proximas
   - Quartis parecidos
   - Gerados nao muito melhores que os reais

[X] Modelo enviesado:
   - Gerados so com score > 0.95
   - Reais concentrados abaixo de 0.6
   - Distribuicao muito diferente

Regra de ouro:
   O robo deve gerar jogos como se fossem sorteios reais comuns, nao "perfeitos".
""")

# Exportar para visualização no Power BI
from pathlib import Path

output_dir = Path("data/outputs")
output_dir.mkdir(parents=True, exist_ok=True)

df[["score"]].to_excel("data/outputs/scores_reais.xlsx", index=False)
df_gerados[["score"]].to_excel("data/outputs/scores_gerados.xlsx", index=False)

print("\n[OK] Arquivos exportados:")
print("   - data/outputs/scores_reais.xlsx")
print("   - data/outputs/scores_gerados.xlsx")
