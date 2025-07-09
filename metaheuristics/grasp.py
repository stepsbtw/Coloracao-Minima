import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils import count_conflicts
import random

def local_search_grasp(coloring, graph, max_colors):
    """Busca local simples: tenta mudar a cor de um vértice para reduzir conflitos."""
    current = coloring.copy()
    improved = True

    while improved:
        improved = False
        for v in current:
            original_color = current[v]
            used_colors = set(current.get(n) for n in graph[v])
            for c in range(max_colors):
                if c != original_color and c not in used_colors:
                    candidate = current.copy()
                    candidate[v] = c
                    if count_conflicts(candidate, graph) < count_conflicts(current, graph):
                        current = candidate
                        improved = True
                        break
            if improved:
                break

    used_colors = set(current.values())
    return current, len(used_colors), count_conflicts(current, graph)

def grasp_coloring(graph, max_colors=10, iterations=50, rcl_size=3):
    vertices = list(graph.keys())

    best_solution = None
    best_conflicts = float('inf')
    best_num_colors = max_colors

    for it in range(iterations):
        # Construção gulosa randomizada
        coloring = {}
        available_colors = list(range(max_colors))

        # Ordem aleatória para diversificar as soluções
        random.shuffle(vertices)

        for v in vertices:
            used_colors = set(coloring.get(n) for n in graph[v] if n in coloring)
            candidate_colors = [c for c in available_colors if c not in used_colors]

            # RCL (Restricted Candidate List): os top-rcl_size melhores candidatos (menor cor)
            if len(candidate_colors) > rcl_size:
                candidate_colors = random.sample(candidate_colors, rcl_size)
            
            if candidate_colors:
                chosen_color = min(candidate_colors)  # guloso, escolhe menor cor
            else:
                # Se não tem cor disponível sem conflito, força nova cor
                chosen_color = max(coloring.values(), default=-1) + 1
                if chosen_color >= max_colors:
                    chosen_color = random.choice(available_colors)  # fallback

            coloring[v] = chosen_color

        # Busca local simples: tentar reduzir conflitos mudando cores
        coloring, num_colors, conflicts = local_search_grasp(coloring, graph, max_colors)

        if conflicts < best_conflicts or (conflicts == best_conflicts and num_colors < best_num_colors):
            best_solution = coloring
            best_conflicts = conflicts
            best_num_colors = num_colors

    # Remapeia cores para contagem sequencial
    if best_solution is None:
        return None
    used_colors = sorted(set(best_solution.values()))
    color_map = {c: i for i, c in enumerate(used_colors)}
    remapped = {v: color_map[best_solution[v]] for v in best_solution}

    return remapped
