def parse_dimacs(caminho_arquivo):
    grafo = {}
    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            if linha.startswith('c') or linha.strip() == '':
                continue
            elif linha.startswith('p'):
                _, _, num_vertices, _ = linha.strip().split()
                for i in range(1, int(num_vertices) + 1):
                    grafo[str(i)] = []
            elif linha.startswith('e'):
                _, u, v = linha.strip().split()
                if v not in grafo[u]:
                    grafo[u].append(v)
                if u not in grafo[v]:
                    grafo[v].append(u)
    return grafo