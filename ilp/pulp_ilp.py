import pulp

def graph_coloring_pulp(graph, max_colors=None):
    """
    Resolve o problema de coloração mínima usando programação inteira com PuLP.
    
    Parâmetros:
    - graph: dict {vértice: [vizinhos]}
    - max_colors: número máximo de cores para tentar (se None, usa |V|)
    
    Retorna:
    - dict {vértice: cor} se for factível
    - None se não encontrar solução factível
    """
    vertices = list(graph.keys())
    n = len(vertices)
    
    if max_colors is None:
        max_colors = n  # No pior caso, usa tantas cores quanto vértices
    
    # Criar o problema
    prob = pulp.LpProblem("GraphColoring", pulp.LpMinimize)
    
    # Variáveis y_c indicando se cor c é usada
    y = pulp.LpVariable.dicts("y", range(max_colors), cat='Binary')
    
    # Variáveis x_{v,c} indicando se vértice v recebe cor c
    x = pulp.LpVariable.dicts("x",
                              ((v, c) for v in vertices for c in range(max_colors)),
                              cat='Binary')
    
    # Função objetivo: minimizar número de cores usadas
    prob += pulp.lpSum(y[c] for c in range(max_colors))
    
    # Restrição: cada vértice recebe exatamente uma cor
    for v in vertices:
        prob += pulp.lpSum(x[(v, c)] for c in range(max_colors)) == 1, f"OneColor_{v}"
    
    # Restrição: vértices adjacentes não podem ter mesma cor
    for v in vertices:
        for u in graph[v]:
            if u > v:  # evitar repetir restrições simétricas
                for c in range(max_colors):
                    prob += x[(v, c)] + x[(u, c)] <= 1, f"AdjDiffColor_{v}_{u}_cor{c}"
    
    # Relacionar x e y: se algum vértice usa cor c, então y_c = 1
    for v in vertices:
        for c in range(max_colors):
            prob += x[(v, c)] <= y[c], f"ColorUsed_{v}_cor{c}"
    
    # Resolver
    #solver = pulp.PULP_CBC_CMD(msg=True)  # Mudar para outro solver se quiser
    #solver = pulp.CPLEX_CMD(msg=True)
    #solver = pulp.CPLEX_PY(msg=True)
    solver = pulp.GUROBI_CMD(msg=True)
    #solver = pulp.GUROBI(msg=True)


    
    result_status = prob.solve(solver)
    
    if pulp.LpStatus[result_status] != 'Optimal':
        print("Não foi encontrada solução ótima.")
        return None
    
    # Montar resultado
    coloring = {}
    for v in vertices:
        for c in range(max_colors):
            if pulp.value(x[(v, c)]) == 1:
                coloring[v] = c
                break
    # Remapeamento sequencial das cores
    used_colors = sorted(set(coloring.values()))
    color_map = {c: i for i, c in enumerate(used_colors)}
    remapped = {v: color_map[coloring[v]] for v in coloring}
    return remapped