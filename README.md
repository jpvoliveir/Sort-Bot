# Mega-Sena: laboratório de previsão

Testa, com rigor estatístico, se algum padrão do histórico da Mega-Sena ajuda a prever
o próximo sorteio. Se uma estratégia passar no teste, o gerador de jogos passa a usá-la;
senão, gera jogos aleatórios. Em ambos os casos, descarta combinações populares
(datas, sequências, padrões no volante, sorteios anteriores), que não mudam a chance de
ganhar mas aumentam a chance de dividir o prêmio.

## Instalação

```bash
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

## Uso

**Com janela:** dois cliques em `Robo Mega-Sena.bat`. Escolha a estratégia e a quantidade,
clique em **Gerar jogos** e, depois do sorteio, em **Conferir resultados**.

**Pelo terminal:**

```bash
python main.py                        # gera os jogos do próximo concurso (atualiza os dados antes)
python main.py --estrategia quentes --qtd 5
python conferir.py                    # confere os jogos registrados e mostra o balanço
python backtest.py                    # laboratório: backtest das estratégias + teste de viés físico
python tools/atualizar_dados.py       # só atualiza os dados (API da Caixa)
python -m pytest                      # testes
```

Todo jogo gerado é salvo em `data/apostas/registro_apostas.csv` com o concurso a que se
destina; a conferência preenche acertos e prêmio. Se gerar jogos que não for jogar, apague
essas linhas para o balanço refletir só o que você apostou.

Sem internet, baixe o Excel em https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx e rode
`python tools/atualizar_dados.py --excel "caminho/do/arquivo.xlsx"`.

## Como o backtest funciona

Para cada concurso (a partir do 500º), cada estratégia vê só os sorteios anteriores e ordena
as 60 dezenas da "mais provável" para a menos. Medimos a posição média das 6 dezenas que
de fato saíram. Num sorteio justo ela é 30,5 para qualquer estratégia, com variância
conhecida, o que dá um teste z sem simulação. Como várias estratégias são testadas, o
limite de significância é corrigido por Bonferroni (0,05 / nº de estratégias). A estratégia
`aleatorio` é o controle: serve para ver como o puro acaso se comporta.

Para testar uma ideia nova, escreva uma função em `analysis/estrategias.py` que recebe o
histórico e devolve as 60 dezenas ordenadas, e registre-a em `ESTRATEGIAS`.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `data/raw/Mega-Sena.xlsx` | Histórico oficial (formato do Excel da Caixa) |
| `data/processed/analise_megasena.csv` | Histórico + colunas de análise (fonte do Power BI) |
| `data/apostas/registro_apostas.csv` | Jogos gerados por concurso, com acertos e prêmio |
| `data/outputs/` | Jogos gerados e resultados do laboratório (não versionado) |
| `analysis/` | Padrões, carregamento de dados, estratégias, backtest, teste de viés |
| `generator/` | Gerador de jogos e filtro de popularidade |
| `tools/atualizar_dados.py` | Atualização dos dados |
| `powerbi/` | Notas do painel |
