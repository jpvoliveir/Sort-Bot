from generator.gerador import gerar_jogos_filtrados
from generator.exportador import exportar_jogos

jogos = gerar_jogos_filtrados(
    qtd_jogos=50,
    score_min=0.75
)

# Ordenar jogos por score (maior para menor)
jogos_ordenados = sorted(jogos, key=lambda x: x['score'], reverse=True)

# Exibir no terminal
print("="*60)
print("JOGOS GERADOS PARA A MEGA-SENA")
print("="*60)
print(f"\nTotal de jogos: {len(jogos_ordenados)}\n")

for idx, jogo_info in enumerate(jogos_ordenados, 1):
    jogo_str = "-".join(map(str, jogo_info['jogo']))
    score = jogo_info['score']
    pares = jogo_info['pares']
    fib = jogo_info['fibonacci']
    quad = jogo_info['quadrantes']
    print(f"{idx:2d}. {jogo_str:20s} | Score: {score:.3f} | Pares: {pares} | Fib: {fib} | Quad: {quad}")

print("\n" + "="*60)

# Exportar para arquivo
exportar_jogos(jogos)
