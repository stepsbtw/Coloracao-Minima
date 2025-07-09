import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import csv

from heuristics import dsatur, bfs_ca, welsh_powell
from metaheuristics import ant_colony, genetic, grasp, simulated_annealing, tabu_search
from ilp import ortools_sat, pulp_ilp
from utils import run_algorithm
from parse_instances import parse_dimacs
# from wireless_simulation.visualizacao import visualizar_grafo  # Módulo não existe
from ampl_coloring import graph_coloring_ampl

# Dicionário de ótimos conhecidos para instâncias Myciel
OTIMOS = {
    'myciel3.col': 4,
    'myciel4.col': 5,
    'myciel5.col': 6,
    'myciel6.col': 7,
    'myciel7.col': 8,
}

if __name__ == "__main__":
    instancias = [
        'instances/myciel3.col',
        'instances/myciel4.col',
        'instances/myciel5.col',
        'instances/myciel6.col',
        'instances/myciel7.col',
    ]
    todos_resultados = []
    for instancia in instancias:
        grafo = parse_dimacs(instancia)
        nome_instancia = os.path.basename(instancia)
        otimo = OTIMOS.get(nome_instancia)

        results = []
        colorings = {}

        results.append(run_algorithm("BFS-CA", bfs_ca.bfs_ca_coloring, graph=grafo))
        colorings["BFS-CA"] = bfs_ca.bfs_ca_coloring(grafo)
        results.append(run_algorithm("Welsh-Powell", welsh_powell.welsh_powell_coloring, graph=grafo))
        colorings["Welsh-Powell"] = welsh_powell.welsh_powell_coloring(grafo)
        results.append(run_algorithm("DSATUR", dsatur.dsatur_coloring, graph=grafo))
        colorings["DSATUR"] = dsatur.dsatur_coloring(grafo)
        results.append(run_algorithm("Simulated Annealing", simulated_annealing.simulated_annealing_coloring, grafo))
        colorings["Simulated Annealing"] = simulated_annealing.simulated_annealing_coloring(grafo)
        results.append(run_algorithm("Tabu Search", tabu_search.tabu_search_coloring, grafo, tabu_tenure=7))
        colorings["Tabu Search"] = tabu_search.tabu_search_coloring(grafo)
        results.append(run_algorithm("GRASP", grasp.grasp_coloring, grafo, iterations=100, rcl_size=3))
        colorings["GRASP"] = grasp.grasp_coloring(grafo)
        results.append(run_algorithm("Genetic Algorithm", genetic.genetic_algorithm_coloring, grafo, population_size=50, generations=200, mutation_rate=0.1))
        colorings["Genetic Algorithm"] = genetic.genetic_algorithm_coloring(grafo)
        results.append(run_algorithm("Ant Colony", ant_colony.aco_coloring, grafo, num_ants=20, iterations=100, alpha=1.0, beta=3.0, evaporation=0.2))
        colorings["Ant Colony"] = ant_colony.aco_coloring(grafo)
        results.append(run_algorithm("OR-Tools CP-SAT", ortools_sat.graph_coloring_ortools, grafo))
        colorings["OR-Tools CP-SAT"] = ortools_sat.graph_coloring_ortools(grafo)
        results.append(run_algorithm("AMPL (Gurobi)", graph_coloring_ampl, grafo, ampl_model_path='graph_coloring.mod', solver='gurobi'))
        colorings["AMPL (Gurobi)"] = graph_coloring_ampl(grafo, ampl_model_path='graph_coloring.mod', solver='gurobi')

        # Salvar resultados individuais
        with open(f'resultados_{nome_instancia}.csv', 'w', newline='') as csvfile:
            fieldnames = ['Instancia', 'Algoritmo', 'Cores', 'Conflitos', 'Tempo (s)', 'Gap para ótimo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                gap = None
                if otimo and r['Cores'] != '-' and r['Cores'] != '':
                    try:
                        gap = int(r['Cores']) - otimo
                    except Exception:
                        gap = None
                row = {
                    'Instancia': nome_instancia,
                    'Algoritmo': r['Algoritmo'],
                    'Cores': r['Cores'],
                    'Conflitos': r['Conflitos'],
                    'Tempo (s)': r['Tempo (s)'],
                    'Gap para ótimo': gap if gap is not None else ''
                }
                writer.writerow(row)
                todos_resultados.append(row)
        print(f'Resultados salvos em resultados_{nome_instancia}.csv')

        print("\n--- COMPARAÇÃO FINAL ---")
        print(f"{'Algoritmo':<25} {'Cores':<6} {'Conflitos':<10} {'Tempo (s)':<10}")
        print("-" * 55)
        for r in results:
            print(f"{r['Algoritmo']:<25} {r['Cores']:<6} {r['Conflitos']:<10} {r['Tempo (s)']:<10}")
        
        # Pergunta ao usuário se deseja visualizar
        try:
            resposta = input("\nDeseja visualizar a coloração de algum algoritmo? (digite o nome exato ou ENTER para pular): ")
            if resposta in colorings and colorings[resposta] is not None:
                # visualizar_grafo(grafo, colorings[resposta], resposta, instancia) # Módulo não existe
                print(f"Visualização de {resposta} não disponível no momento.")
            elif resposta.strip() != '':
                print("Nome de algoritmo não encontrado ou sem coloração disponível.")
        except Exception as e:
            print(f"Erro na visualização: {e}")

    # Salvar todos os resultados em um único CSV
    with open('resultados_todos.csv', 'w', newline='') as csvfile:
        fieldnames = ['Instancia', 'Algoritmo', 'Cores', 'Conflitos', 'Tempo (s)', 'Gap para ótimo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in todos_resultados:
            writer.writerow(row)
    print('Todos os resultados salvos em resultados_todos.csv')