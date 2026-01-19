"""
Distribuições estatísticas reais baseadas nos dados históricos da Mega-Sena
Calculadas a partir do Power BI / análise estatística
"""
import pandas as pd
from pathlib import Path

# Distribuição de pares/ímpares (fallback - calculada dos dados reais)
PARES_IMPARES_DIST_FALLBACK = {
    (0, 6): 0.0132,  # 0 pares, 6 ímpares
    (1, 5): 0.0881,  # 1 pares, 5 ímpares
    (2, 4): 0.2408,  # 2 pares, 4 ímpares
    (3, 3): 0.3087,  # 3 pares, 3 ímpares
    (4, 2): 0.2418,  # 4 pares, 2 ímpares
    (5, 1): 0.0946,  # 5 pares, 1 ímpares
    (6, 0): 0.0128,  # 6 pares, 0 ímpares
}

# Distribuição de números Fibonacci (calculada dos dados reais)
FIBONACCI_DIST = {
    0: 0.3698,  # 0 números Fibonacci (36.98%)
    1: 0.4184,  # 1 números Fibonacci (41.84%)
    2: 0.1763,  # 2 números Fibonacci (17.63%)
    3: 0.0338,  # 3 números Fibonacci (3.38%)
    4: 0.0017,  # 4 números Fibonacci (0.17%)
}


def carregar_pares_impares(path: str = "data/processed/dist_pares_impares.csv"):
    """
    Carrega a distribuição de pares/ímpares do CSV exportado do Power BI
    
    Formato esperado do CSV:
        pares,impares,probabilidade
        3,3,0.42
        4,2,0.32
        ...
    
    Se o arquivo não existir, retorna a distribuição fallback.
    """
    csv_path = Path(path)
    
    if not csv_path.exists():
        print(f"[AVISO] Arquivo {path} não encontrado. Usando distribuição fallback.")
        return PARES_IMPARES_DIST_FALLBACK
    
    try:
        df = pd.read_csv(csv_path)
        
        # Tentar diferentes nomes de colunas (Power BI pode exportar de formas diferentes)
        # Opção 1: pares, impares, probabilidade
        if 'pares' in df.columns and 'impares' in df.columns:
            prob_col = None
            for col in ['probabilidade', 'Probabilidade', 'Percentual', 'percentual', 'Value', 'value']:
                if col in df.columns:
                    prob_col = col
                    break
            
            if prob_col is None:
                # Se não tiver coluna de probabilidade, calcular a partir da contagem
                if 'Count' in df.columns or 'Contagem' in df.columns:
                    count_col = 'Count' if 'Count' in df.columns else 'Contagem'
                    total = df[count_col].sum()
                    df['probabilidade'] = df[count_col] / total
                    prob_col = 'probabilidade'
                else:
                    raise ValueError("Não encontrou coluna de probabilidade ou contagem")
            
            dist = {
                (int(row['pares']), int(row['impares'])): float(row[prob_col])
                for _, row in df.iterrows()
            }
            
            # Normalizar para garantir que soma 1.0
            total = sum(dist.values())
            if total > 0:
                dist = {k: v / total for k, v in dist.items()}
            
            print(f"[OK] Distribuição carregada do Power BI: {len(dist)} combinações")
            return dist
        
        # Opção 2: Qtd_Pares, Qtd_Impares, Count (formato direto do Power BI)
        elif 'Qtd_Pares' in df.columns and 'Qtd_Impares' in df.columns:
            count_col = None
            for col in ['Count', 'Contagem', 'Count of Table', 'Count of Tabela']:
                if col in df.columns:
                    count_col = col
                    break
            
            if count_col is None:
                raise ValueError("Não encontrou coluna de contagem")
            
            total = df[count_col].sum()
            dist = {
                (int(row['Qtd_Pares']), int(row['Qtd_Impares'])): float(row[count_col]) / total
                for _, row in df.iterrows()
            }
            
            print(f"[OK] Distribuição carregada do Power BI: {len(dist)} combinações")
            return dist
        
        else:
            raise ValueError(f"Formato de CSV não reconhecido. Colunas encontradas: {list(df.columns)}")
    
    except Exception as e:
        print(f"[ERRO] Erro ao carregar {path}: {e}")
        print(f"[AVISO] Usando distribuição fallback.")
        return PARES_IMPARES_DIST_FALLBACK


# Carregar distribuição de pares/ímpares (tenta do Power BI, senão usa fallback)
PARES_IMPARES_DIST = carregar_pares_impares()