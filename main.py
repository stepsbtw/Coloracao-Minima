from heuristics import dsatur, bfs_ca, welsh_powell
from metaheuristics import ant_colony, genetic, grasp, simulated_annealing, tabu_search
from ilp import ortools_scip, pulp_cbc
from utils import run_algorithm
from parse_instances import parse_dimacs

if __name__ == "__main__":
    grafo = parse_dimacs('instances/myciel5.col')

    results = []

    results.append(run_algorithm("BFS-CA", bfs_ca.bfs_ca_coloring, graph=grafo))
    results.append(run_algorithm("Welsh-Powell", welsh_powell.welsh_powell_coloring, graph=grafo))
    results.append(run_algorithm("DSATUR", dsatur.dsatur_coloring, graph=grafo))
    results.append(run_algorithm("Simulated Annealing", simulated_annealing.simulated_annealing_coloring, grafo))
    results.append(run_algorithm("Tabu Search", tabu_search.tabu_search_coloring, grafo, tabu_tenure=7))
    results.append(run_algorithm("GRASP", grasp.grasp_coloring, grafo, iterations=100, rcl_size=3))
    results.append(run_algorithm("Genetic Algorithm", genetic.genetic_algorithm_coloring, grafo, population_size=50, generations=200, mutation_rate=0.1))
    results.append(run_algorithm("Ant Colony", ant_colony.aco_coloring, grafo, num_ants=20, iterations=100, alpha=1.0, beta=3.0, evaporation=0.2))
    results.append(run_algorithm("OR-Tools CP-SAT", ortools_scip.graph_coloring_ortools, grafo))
    results.append(run_algorithm("PULP CBC", pulp_cbc.graph_coloring_pulp, grafo))

    print("\n--- COMPARAÇÃO FINAL ---")
    print(f"{'Algoritmo':<25} {'Cores':<6} {'Conflitos':<10} {'Tempo (s)':<10}")
    print("-" * 55)
    for r in results:
        print(f"{r['Algoritmo']:<25} {r['Cores']:<6} {r['Conflitos']:<10} {r['Tempo (s)']:<10}")
