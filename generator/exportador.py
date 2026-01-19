import pandas as pd

def exportar_jogos(jogos, nome_arquivo="data/outputs/jogos_rankeados.xlsx"):
    if not jogos:
        print("Nenhum jogo para exportar.")
        return

    df = pd.DataFrame(jogos)

    # transforma a lista do jogo em texto
    df["jogo"] = df["jogo"].apply(lambda x: "-".join(map(str, x)))

    # ordena pelo score
    df = df.sort_values(by="score", ascending=False)

    # cria ranking
    df.insert(0, "ranking", range(1, len(df) + 1))

    df.to_excel(nome_arquivo, index=False)

    print(f"Arquivo exportado com sucesso: {nome_arquivo}")
