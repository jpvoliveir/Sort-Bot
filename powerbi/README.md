# Power BI

## Fontes

| Arquivo | Gerado por | Conteúdo |
|---|---|---|
| `data/processed/analise_megasena.csv` | `tools/atualizar_dados.py` | Um sorteio por linha (UTF-8, separador vírgula) |
| `data/outputs/backtest_estrategias.xlsx` | `backtest.py` | Resultado de cada estratégia de previsão |
| `data/outputs/teste_vies.xlsx` | `backtest.py` | Qui-quadrado de frequência por período |

Depois de atualizar os dados, use **Página Inicial → Atualizar** no Power BI.

## Colunas de análise do CSV

Além das colunas do Excel da Caixa (`Concurso`, `Data do Sorteio`, `Bola1`…`Bola6`, rateios):

| Coluna | Significado |
|---|---|
| `qtd_fibonacci` | Dezenas em {1, 2, 3, 5, 8, 13, 21, 34, 55} |
| `pares` / `impares` | Contagem de pares e ímpares |
| `quadrantes` | Quantos quadrantes (1–15, 16–30, 31–45, 46–60) têm dezenas |
| `assinatura_faixas` | Dezenas por faixa de 10, ex.: `1-1-1-1-1-1` |

## Observação

As distribuições dessas colunas (ex.: 3 pares em ~31% dos sorteios) são as mesmas que
jogos totalmente aleatórios produzem. Elas descrevem o histórico, mas não indicam quais
jogos têm mais chance: todas as combinações têm 1 chance em 50.063.860.
