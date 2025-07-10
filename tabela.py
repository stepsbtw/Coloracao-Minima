import csv
import statistics
from collections import defaultdict

# Estruturas para armazenar os dados
dados_gap = defaultdict(list)
dados_tempo = defaultdict(list)

# Lê o CSV com os resultados
with open('resultados_todos.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        algoritmo = row['Algoritmo']
        try:
            gap = int(row['Gap para otimo'])  # corrigido: sem acento
            tempo = float(row['Tempo (s)'])
            dados_gap[algoritmo].append(gap)
            dados_tempo[algoritmo].append(tempo)
        except:
            continue  # pula linhas com valores inválidos

# Exibe o resumo no terminal
print("\n" + "="*60)
print("COMPARAÇÃO FINAL - MÉDIA E DESVIO PADRÃO")
print("="*60)
print(f"{'Algoritmo':<20} {'Gap médio (±DP)':<20} {'Tempo médio (s) (±DP)':<25}")
print("-" * 60)

# Lista para salvar no CSV
resumo_resultados = []

for algoritmo in sorted(dados_gap.keys()):
    if dados_gap[algoritmo] and dados_tempo[algoritmo]:
        media_gap = statistics.mean(dados_gap[algoritmo])
        dp_gap = statistics.stdev(dados_gap[algoritmo]) if len(dados_gap[algoritmo]) > 1 else 0

        media_tempo = statistics.mean(dados_tempo[algoritmo])
        dp_tempo = statistics.stdev(dados_tempo[algoritmo]) if len(dados_tempo[algoritmo]) > 1 else 0

        print(f"{algoritmo:<20} {media_gap:.2f} ± {dp_gap:.2f}     {media_tempo:.4f} ± {dp_tempo:.4f}")

        resumo_resultados.append({
            'Algoritmo': algoritmo,
            'Gap médio': f"{media_gap:.2f}",
            'Desvio padrão do Gap': f"{dp_gap:.2f}",
            'Tempo médio (s)': f"{media_tempo:.4f}",
            'Desvio padrão do Tempo': f"{dp_tempo:.4f}"
        })

# Salvar no CSV
with open('comparacao_algoritmos.csv', 'w', newline='') as csvfile:
    fieldnames = ['Algoritmo', 'Gap médio', 'Desvio padrão do Gap', 'Tempo médio (s)', 'Desvio padrão do Tempo']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for linha in resumo_resultados:
        writer.writerow(linha)

print("\nResumo salvo em 'comparacao_algoritmos.csv'. ✅")
