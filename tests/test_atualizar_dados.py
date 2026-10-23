import pandas as pd

import tools.atualizar_dados as atualizar
from analysis.dados import CAMINHO_EXCEL
from tools.atualizar_dados import concurso_para_linha, formatar_reais

# Resposta real da API da Caixa para o concurso 2961 (campos usados)
API_2961 = {
    "numero": 2961,
    "dataApuracao": "17/01/2026",
    "listaDezenas": ["10", "13", "55", "56", "59", "60"],
    "listaMunicipioUFGanhadores": [],
    "listaRateioPremio": [
        {"faixa": 1, "numeroDeGanhadores": 0, "valorPremio": 0.0},
        {"faixa": 2, "numeroDeGanhadores": 74, "valorPremio": 29835.57},
        {"faixa": 3, "numeroDeGanhadores": 4863, "valorPremio": 748.36},
    ],
    "observacao": "",
    "valorArrecadado": 55405092.0,
    "valorAcumuladoConcursoEspecial": 7681261.41,
    "valorAcumuladoProximoConcurso": 40920414.1,
    "valorEstimadoProximoConcurso": 50000000.0,
}


def test_formatar_reais():
    assert formatar_reais(1389.8) == "R$1.389,80"
    assert formatar_reais(0) == "R$0,00"


def test_api_reproduz_linha_do_excel_da_caixa():
    excel = pd.read_excel(CAMINHO_EXCEL)
    esperado = excel[excel["Concurso"] == 2961].iloc[0]
    linha = concurso_para_linha(API_2961)
    assert list(linha) == list(excel.columns)
    for coluna, valor in linha.items():
        if pd.isna(esperado[coluna]):
            assert valor is None, coluna
        else:
            assert valor == esperado[coluna], coluna


def test_cidades_dos_ganhadores():
    d = dict(API_2961, listaMunicipioUFGanhadores=[
        {"municipio": "CANAL ELETRONICO", "uf": "--"},
        {"municipio": "PONTA PORA", "uf": "MS"},
    ])
    assert concurso_para_linha(d)["Cidade / UF"] == "CANAL ELETRONICO; PONTA PORA/MS"


def test_busca_concursos_ate_a_api_dizer_que_nao_existe(monkeypatch, tmp_path):
    excel = pd.read_excel(CAMINHO_EXCEL).head(3)  # concursos 1 a 3
    destino = tmp_path / "Mega-Sena.xlsx"
    pedidos = []

    def api_falsa(numero):
        pedidos.append(numero)
        return dict(API_2961, numero=numero) if numero <= 5 else None

    monkeypatch.setattr(atualizar, "carregar_sorteios", lambda: excel)
    monkeypatch.setattr(atualizar, "CAMINHO_EXCEL", destino)
    monkeypatch.setattr(atualizar, "buscar_concurso", api_falsa)
    monkeypatch.setattr(atualizar.time, "sleep", lambda s: None)

    atualizar.atualizar_pela_api()

    assert pedidos == [4, 5, 6]
    assert pd.read_excel(destino)["Concurso"].tolist() == [1, 2, 3, 4, 5]
