"""
Script para atualizar as distribuições a partir dos dados processados
ou permitir atualização manual com dados do Power BI
"""
import pandas as pd
import sys
from pathlib import Path

# Adicionar raiz do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def calcular_distribuicoes_do_csv():
    """
    Calcula as distribuições diretamente do CSV processado
    """
    csv_path = project_root / 'data' / 'processed' / 'analise_megasena.csv'
    df = pd.read_csv(csv_path)
    
    # Distribuição pares/ímpares
    dist_pi = df.groupby(['pares', 'impares']).size() / len(df)
    dist_pi_dict = {(int(p), int(i)): float(prob) for (p, i), prob in dist_pi.items()}
    
    # Distribuição Fibonacci
    dist_fib = df['qtd_fibonacci'].value_counts(normalize=True).sort_index()
    dist_fib_dict = {int(k): float(v) for k, v in dist_fib.items()}
    
    return dist_pi_dict, dist_fib_dict


def gerar_codigo_python(pares_impares_dist, fibonacci_dist):
    """
    Gera o código Python para o arquivo distributions.py
    """
    codigo = '''"""
Distribuições estatísticas reais baseadas nos dados históricos da Mega-Sena
Calculadas a partir do Power BI / análise estatística
"""

# Distribuição de pares/ímpares (calculada dos dados reais)
PARES_IMPARES_DIST = {
'''
    
    # Ordenar pares/ímpares de forma lógica
    for (p, i), prob in sorted(pares_impares_dist.items()):
        codigo += f'    ({p}, {i}): {prob:.4f},  # {p} pares, {i} ímpares\n'
    
    codigo += '''}

# Distribuição de números Fibonacci (calculada dos dados reais)
FIBONACCI_DIST = {
'''
    
    for fib, prob in sorted(fibonacci_dist.items()):
        porcentagem = prob * 100
        codigo += f'    {fib}: {prob:.4f},  # {fib} números Fibonacci ({porcentagem:.2f}%)\n'
    
    codigo += '''}'''
    
    return codigo


def atualizar_automatico():
    """
    Atualiza automaticamente a partir do CSV
    """
    print("Calculando distribuicoes do CSV processado...")
    dist_pi, dist_fib = calcular_distribuicoes_do_csv()
    
    print("\n=== DISTRIBUICAO PARES/IMPARES ===")
    for (p, i), prob in sorted(dist_pi.items()):
        print(f"({p}, {i}): {prob:.4f} ({prob*100:.2f}%)")
    
    print("\n=== DISTRIBUICAO FIBONACCI ===")
    for fib, prob in sorted(dist_fib.items()):
        print(f"{fib}: {prob:.4f} ({prob*100:.2f}%)")
    
    # Gerar código e atualizar arquivo
    codigo = gerar_codigo_python(dist_pi, dist_fib)
    
    output_path = project_root / 'generator' / 'distributions.py'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(codigo)
    
    print(f"\n[OK] Arquivo atualizado: {output_path}")
    print("\nSe voce tem numeros diferentes no Power BI, edite manualmente o arquivo:")
    print(f"   {output_path}")


if __name__ == '__main__':
    atualizar_automatico()
