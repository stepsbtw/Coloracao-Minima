import random
import time
from inspect import signature

def count_conflicts(coloring, graph):
    """Conta o número de conflitos: arestas entre vértices com mesma cor."""
    conflicts = 0
    for v in graph:
        for u in graph[v]:
            if coloring[v] == coloring[u]:
                conflicts += 1
    return conflicts // 2  # cada conflito é contado duas vezes


def get_neighbors(coloring, graph, num_colors):
    """Gera vizinhos mudando a cor de um vértice aleatório."""
    neighbors = []
    vertices = list(graph.keys())
    v = random.choice(vertices)
    current_color = coloring[v]
    for c in range(num_colors):
        if c != current_color:
            neighbor = coloring.copy()
            neighbor[v] = c
            neighbors.append(neighbor)
    return neighbors

def run_algorithm(name, func, *args, **kwargs):
    graph = kwargs.get("graph") or (args[0] if args else None)

    # Detectar e passar max_colors se necessário
    if graph:
        grau_max = max(len(vizinhos) for vizinhos in graph.values())
        from inspect import signature
        sig = signature(func)
        if "max_colors" in sig.parameters and "max_colors" not in kwargs:
            kwargs["max_colors"] = grau_max + 1

    import time
    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()

    if result is None:
        return {"Algoritmo": name, "Cores": "-", "Conflitos": "-", "Tempo (s)": round(end - start, 4)}

    coloring = result
    num_cores = len(set(coloring.values())) if coloring else "-"
    conflitos = count_conflicts(coloring, graph) if coloring else "-"

    return {
        "Algoritmo": name,
        "Cores": num_cores,
        "Conflitos": conflitos,
        "Tempo (s)": round(end - start, 4)
    }