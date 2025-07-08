from collections import defaultdict

def dsatur_coloring(graph):
    """
    DSATUR: ordena vértices por saturação (nº de cores vizinhas distintas).
    
    Retorna: dict {vértice: cor}
    """
    

    color = {}
    saturation = defaultdict(int)
    degrees = {v: len(graph[v]) for v in graph}

    uncolored = set(graph.keys())

    while uncolored:
        # Escolher vértice com maior saturação; em empate, maior grau
        v = max(uncolored, key=lambda x: (saturation[x], degrees[x]))

        # Cores dos vizinhos já coloridos
        used = set(color.get(n) for n in graph[v] if n in color)
        c = 0
        while c in used:
            c += 1
        color[v] = c
        uncolored.remove(v)

        # Atualiza saturação dos vizinhos não coloridos
        for u in graph[v]:
            if u in uncolored:
                neighbor_colors = set(color.get(n) for n in graph[u] if n in color)
                saturation[u] = len(neighbor_colors)

    return color