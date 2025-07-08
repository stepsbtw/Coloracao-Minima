def welsh_powell_coloring(graph):
    """
    Welsh-Powell: ordena os vértices por grau e colore gulosamente.
    
    Retorna: dict {vértice: cor}
    """
    # Ordena vértices por grau (desc)
    vertices = sorted(graph, key=lambda v: len(graph[v]), reverse=True)
    color = {}
    current_color = 0

    for v in vertices:
        if v not in color:
            color[v] = current_color
            # Tenta colorir vértices não adjacentes com a mesma cor
            for u in vertices:
                if u not in color and all(color.get(n) != current_color for n in graph[u]):
                    color[u] = current_color
            current_color += 1

    return color