# Como Atualizar os Dados da Mega-Sena

## ⚠️ Importante

O arquivo `data/raw/Mega-Sena.xlsx` precisa ser atualizado periodicamente para manter o backtest e as análises atualizadas.

## 📥 Como Atualizar

### Opção 1: Download Manual da Caixa

1. Acesse o site da Caixa Econômica Federal:
   - https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx

2. Baixe o arquivo Excel com todos os sorteios

3. Substitua o arquivo `data/raw/Mega-Sena.xlsx` pelo novo arquivo

4. Execute o backtest novamente:
   ```bash
   python backtest.py
   ```

### Opção 2: Verificar Atualização

Execute o script de verificação:

```bash
python verificar_atualizacao.py
```

Isso vai mostrar:
- Última data no arquivo
- Quantos dias está atrasado
- Total de sorteios

## 🔄 Após Atualizar

Depois de atualizar o arquivo, você pode:

1. **Recalcular as distribuições** (se necessário):
   ```bash
   python tools/atualizar_distribuicoes.py
   ```

2. **Executar o backtest** para ver os novos scores:
   ```bash
   python backtest.py
   ```

3. **Gerar novos jogos** com dados atualizados:
   ```bash
   python main.py
   ```

## 📊 Estrutura Esperada do Arquivo

O arquivo Excel deve ter as seguintes colunas:
- `Concurso`
- `Data do Sorteio`
- `Bola1`, `Bola2`, `Bola3`, `Bola4`, `Bola5`, `Bola6`
- Outras colunas (opcionais)

## ⏰ Frequência Recomendada

- **Mínimo**: Mensalmente
- **Ideal**: Semanalmente ou após cada sorteio importante
- **Máximo**: Não deixar passar mais de 3 meses
