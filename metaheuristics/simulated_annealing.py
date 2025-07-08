import random
import math

import utils

def simulated_annealing_coloring(graph, max_colors=10, initial_temp=100.0, alpha=0.95, max_iter=1000):
    """Heurística Simulated Annealing para coloração de grafos."""

    vertices = list(graph.keys())
    # Solução inicial aleatória
    current = {v: random.randint(0, max_colors - 1) for v in vertices}
    current_conflicts = utils.count_conflicts(current, graph)

    best = current.copy()
    best_conflicts = current_conflicts

    T = initial_temp

    for iteration in range(max_iter):
        if best_conflicts == 0:
            break

        neighbors = utils.get_neighbors(current, graph, max_colors)
        next_choice = random.choice(neighbors)
        next_conflicts = utils.count_conflicts(next_choice, graph)

        delta = next_conflicts - current_conflicts
        if delta < 0 or random.random() < math.exp(-delta / T):
            current = next_choice
            current_conflicts = next_conflicts
            if current_conflicts < best_conflicts:
                best = current.copy()
                best_conflicts = current_conflicts

        T *= alpha

    # Minimizar número de cores usadas na solução final (opcional)
    used_colors = list(set(best.values()))
    color_map = {c: i for i, c in enumerate(sorted(used_colors))}
    remapped = {v: color_map[best[v]] for v in best}

    return remapped, len(set(remapped.values())), best_conflicts