import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import count_conflicts
import random
from collections import deque

def tabu_search_coloring(graph, max_colors=5, tabu_tenure=7, max_iter=500):
    vertices = list(graph.keys())
    # Solução inicial aleatória
    current = {v: random.randint(0, max_colors - 1) for v in vertices}
    current_conflicts = count_conflicts(current, graph)

    best = current.copy()
    best_conflicts = current_conflicts

    tabu_list = deque(maxlen=tabu_tenure)

    for iteration in range(max_iter):
        if best_conflicts == 0:
            break

        best_candidate = None
        best_candidate_conflicts = float('inf')
        move_made = None

        for v in vertices:
            original_color = current[v]
            for new_color in range(max_colors):
                if new_color != original_color:
                    move = (v, new_color)
                    if move in tabu_list:
                        continue

                    candidate = current.copy()
                    candidate[v] = new_color
                    conflicts = count_conflicts(candidate, graph)

                    # Aceita movimento se melhora ou se é o melhor até agora
                    if conflicts < best_candidate_conflicts or (conflicts < best_conflicts):
                        best_candidate = candidate
                        best_candidate_conflicts = conflicts
                        move_made = move

        if best_candidate is None:
            break  # nenhuma melhoria possível

        current = best_candidate
        current_conflicts = best_candidate_conflicts

        tabu_list.append(move_made)

        if current_conflicts < best_conflicts:
            best = current.copy()
            best_conflicts = current_conflicts

    # Remapeamento de cores (opcional)
    used_colors = sorted(set(best.values()))
    color_map = {c: i for i, c in enumerate(used_colors)}
    final = {v: color_map[best[v]] for v in best}

    return final