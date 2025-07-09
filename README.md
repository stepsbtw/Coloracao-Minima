# Projeto de Coloração de Grafos

Este repositório implementa algoritmos clássicos de coloração mínima de grafos:

## Algoritmos Implementados

### Heurísticas
- **DSATUR**: Ordenação por saturação (nº de cores vizinhas distintas)
- **Welsh-Powell**: Ordenação por grau decrescente
- **BFS-CA**: Busca em largura com coloração adaptativa

### Metaheurísticas
- **GRASP**: Greedy Randomized Adaptive Search Procedure
- **Genetic Algorithm**: Algoritmo genético
- **Simulated Annealing**: Simulated Annealing
- **Tabu Search**: Busca tabu
- **Ant Colony**: Colônia de formigas

### Programação Inteira
- **OR-Tools CP-SAT**: Google OR-Tools
- **PuLP**: PuLP com diferentes solvers
- **AMPL**: AMPL com Gurobi

## Como Executar

```bash
python main.py
```

O programa irá:
1. Executar todos os algoritmos nas instâncias configuradas
2. Gerar arquivos CSV com os resultados
3. Mostrar uma comparação final dos resultados

## Instâncias

Instâncias clássicas estão em `instances/` no formato DIMACS.

Mais instâncias: https://mat.tepper.cmu.edu/COLOR/instances.html

## Requisitos

Veja `requirements.txt` para dependências.

## Resultados

Os resultados são salvos em arquivos CSV:
- `resultados_myciel3.col.csv`
- `resultados_myciel4.col.csv`
- `resultados_todos.csv`