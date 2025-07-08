from collections import deque

def bfs_ca_coloring(graph, start=None):
    """
    Algoritmo BFS-CA para coloração mínima aproximada do grafo.
    
    Parâmetros:
    - graph: dict {vértice: [vizinhos]}
    - start: vértice inicial para o BFS (se None, escolhe um arbitrário)
    
    Retorna:
    - dict {vértice: cor}, onde cor é um inteiro >= 0
    """
    if not graph:
        return {}

    if start is None:
        start = next(iter(graph))  # Escolhe um vértice arbitrário

    color = {}
    visited = set()
    queue = deque([start])

    while queue:
        u = queue.popleft()
        if u not in visited:
            visited.add(u)
            # Cores usadas pelos vizinhos já coloridos
            used_colors = set(color.get(v) for v in graph[u] if v in color)

            # Atribui a menor cor possível que não esteja em used_colors
            c = 0
            while c in used_colors:
                c += 1
            color[u] = c

            # Adiciona vizinhos à fila
            for v in graph[u]:
                if v not in visited:
                    queue.append(v)

    # Para o caso de o grafo ser desconexo, colore os componentes restantes
    for v in graph:
        if v not in color:
            # Colore componente desconexa a partir desse vértice
            queue = deque([v])
            while queue:
                u = queue.popleft()
                if u not in color:
                    used_colors = set(color.get(w) for w in graph[u] if w in color)
                    c = 0
                    while c in used_colors:
                        c += 1
                    color[u] = c
                    for w in graph[u]:
                        if w not in color:
                            queue.append(w)

    return color