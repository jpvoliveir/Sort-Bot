"""
Atualiza data/raw/Mega-Sena.xlsx e regenera data/processed/analise_megasena.csv.

Modo automático (busca os concursos que faltam na API pública da Caixa):
    python tools/atualizar_dados.py

Modo manual (usa um Excel baixado do site da Caixa):
    python tools/atualizar_dados.py --excel "C:/Users/.../Downloads/Mega-Sena.xlsx"
"""
import argparse
import json
import shutil
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.dados import CAMINHO_CSV, CAMINHO_EXCEL, carregar_sorteios, gerar_csv_analise

URL_API = "https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena/"
ABA = "MEGA SENA"


def buscar_concurso(numero):
    """Retorna None se o concurso ainda não foi sorteado (a API responde com erro HTTP)"""
    req = urllib.request.Request(f"{URL_API}{numero}", headers={"User-Agent": "Mozilla/5.0"})
    for tentativa in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError:
            return None
        except OSError:
            if tentativa == 2:
                raise
            time.sleep(2)


def formatar_reais(valor):
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R${texto}"


def concurso_para_linha(d):
    """Converte o JSON da API para uma linha no formato do Excel da Caixa"""
    dezenas = sorted(int(n) for n in d["listaDezenas"])
    rateio = {r["faixa"]: r for r in d["listaRateioPremio"]}
    cidades = "; ".join(
        g["municipio"] if g["uf"] == "--" else f"{g['municipio']}/{g['uf']}"
        for g in d["listaMunicipioUFGanhadores"]
    )
    linha = {"Concurso": d["numero"], "Data do Sorteio": d["dataApuracao"]}
    linha.update({f"Bola{i}": n for i, n in enumerate(dezenas, 1)})
    linha.update({
        "Ganhadores 6 acertos": rateio[1]["numeroDeGanhadores"],
        "Cidade / UF": cidades or None,
        "Rateio 6 acertos": formatar_reais(rateio[1]["valorPremio"]),
        "Ganhadores 5 acertos": rateio[2]["numeroDeGanhadores"],
        "Rateio 5 acertos": formatar_reais(rateio[2]["valorPremio"]),
        "Ganhadores 4 acertos": rateio[3]["numeroDeGanhadores"],
        "Rateio 4 acertos": formatar_reais(rateio[3]["valorPremio"]),
        "Acumulado 6 acertos": formatar_reais(d["valorAcumuladoProximoConcurso"]),
        "Arrecadação Total": formatar_reais(d["valorArrecadado"]),
        "Estimativa prêmio": formatar_reais(d["valorEstimadoProximoConcurso"]),
        "Acumulado Sorteio Especial Mega da Virada": formatar_reais(d["valorAcumuladoConcursoEspecial"]),
        "Observação": d["observacao"] or None,
    })
    return linha


def atualizar_pela_api():
    df = carregar_sorteios()
    ultimo_local = int(df["Concurso"].max())

    # Não usa o endpoint de "último concurso": ele fica em cache e chega a atrasar
    # quase 1h depois do sorteio. Busca número a número até a API dizer que não existe.
    novas = []
    numero = ultimo_local + 1
    while (dados := buscar_concurso(numero)) is not None:
        novas.append(concurso_para_linha(dados))
        print(f"   {numero}: {novas[-1]['Data do Sorteio']}")
        numero += 1
        time.sleep(0.3)  # não sobrecarregar a API

    if not novas:
        print(f"Já atualizado (concurso {ultimo_local}).")
        return

    df = pd.concat([df, pd.DataFrame(novas)[df.columns]], ignore_index=True)
    df.to_excel(CAMINHO_EXCEL, sheet_name=ABA, index=False)
    print(f"   -> {CAMINHO_EXCEL}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--excel", type=Path, help="Excel baixado do site da Caixa (substitui data/raw)")
    args = parser.parse_args()

    if args.excel:
        carregar_sorteios(args.excel)  # valida as colunas antes de substituir
        shutil.copy2(args.excel, CAMINHO_EXCEL)
        print(f"Copiado para {CAMINHO_EXCEL}")
    else:
        atualizar_pela_api()

    df = gerar_csv_analise()
    print(f"[OK] {CAMINHO_CSV}: {len(df)} sorteios, último concurso "
          f"{df['Concurso'].iloc[-1]} ({df['Data do Sorteio'].iloc[-1]})")


if __name__ == "__main__":
    main()
