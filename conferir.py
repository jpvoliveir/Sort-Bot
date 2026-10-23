"""
Confere os jogos registrados contra os resultados e mostra o balanço.

    python conferir.py
"""
from analysis.dados import carregar_sorteios
from generator.registro import CAMINHO_REGISTRO, PRECO_JOGO, conferir
from tools.atualizar_dados import atualizar_se_possivel, formatar_reais


def conferir_apostas():
    atualizar_se_possivel()
    registro = conferir(carregar_sorteios())

    if registro.empty:
        print(f"Nenhuma aposta registrada em {CAMINHO_REGISTRO}. Gere jogos primeiro.")
        return

    conferidos = registro[registro["acertos"].notna()]
    pendentes = registro[registro["acertos"].isna()]

    for concurso, grupo in conferidos.groupby("concurso"):
        print(f"\nConcurso {concurso}")
        for _, aposta in grupo.iterrows():
            premio = f"  {formatar_reais(aposta['premio'])}" if aposta["premio"] > 0 else ""
            print(f"   {aposta['jogo']}  ({aposta['estrategia']:>17s})  {int(aposta['acertos'])} acerto(s){premio}")

    if not pendentes.empty:
        print(f"\nAguardando sorteio: {len(pendentes)} jogo(s) do(s) concurso(s) "
              f"{', '.join(map(str, sorted(pendentes['concurso'].unique())))}")

    if not conferidos.empty:
        gasto = len(conferidos) * PRECO_JOGO
        ganho = conferidos["premio"].sum()
        print("\n" + "=" * 60)
        print(f"BALANÇO ({len(conferidos)} jogos conferidos, {formatar_reais(PRECO_JOGO)} cada)")
        print("=" * 60)
        print(f"Gasto:   {formatar_reais(gasto)}")
        print(f"Prêmios: {formatar_reais(ganho)}")
        print(f"Saldo:   {formatar_reais(ganho - gasto)}")
        print(f"Acertos por jogo: {conferidos['acertos'].mean():.3f} (acaso: 0,600)")
        for estrategia, grupo in conferidos.groupby("estrategia"):
            print(f"   {estrategia:17s} {len(grupo):4d} jogos  {grupo['acertos'].mean():.3f} acertos/jogo")


if __name__ == "__main__":
    conferir_apostas()
