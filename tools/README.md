# Ferramentas de Atualização

## 📊 Atualizar Distribuições

### Opção 1: Automática (a partir do CSV processado)

Execute:

```bash
python tools/atualizar_distribuicoes.py
```

Isso vai:
- Ler o arquivo `data/processed/analise_megasena.csv`
- Calcular as distribuições de pares/ímpares e Fibonacci
- Atualizar automaticamente o arquivo `generator/distributions.py`

### Opção 2: Manual (a partir do Power BI)

Se você tem números diferentes ou mais precisos no Power BI:

1. **Exporte do Power BI** as distribuições:
   - Distribuição de pares/ímpares
   - Distribuição de Fibonacci

2. **Edite manualmente** o arquivo `generator/distributions.py`:

```python
# Exemplo de como editar:
PARES_IMPARES_DIST = {
    (0, 6): 0.0132,  # Coloque aqui os valores do Power BI
    (1, 5): 0.0881,
    # ... etc
}

FIBONACCI_DIST = {
    0: 0.3698,  # Coloque aqui os valores do Power BI
    1: 0.4184,
    # ... etc
}
```

**Importante:** Os valores devem somar 1.0 (ou 100%) para cada distribuição.

## 🔍 Verificar distribuições atuais

Para ver as distribuições que estão sendo usadas atualmente:

```bash
python -c "from generator.distributions import PARES_IMPARES_DIST, FIBONACCI_DIST; print('PARES/IMPARES:', PARES_IMPARES_DIST); print('FIBONACCI:', FIBONACCI_DIST)"
```
