from ortools.sat.python import cp_model


def graph_coloring_ortools(graph, max_colors=None):
    vertices = list(graph.keys())
    n = len(vertices)
    if max_colors is None:
        max_colors = n  # máximo de cores possíveis

    model = cp_model.CpModel()

    # Variável x[v][c] = 1 se vértice v recebe cor c
    x = {
        (v, c): model.NewBoolVar(f"x_{v}_{c}")
        for v in vertices
        for c in range(max_colors)
    }

    # Variável y[c] = 1 se a cor c é usada
    y = {
        c: model.NewBoolVar(f"y_{c}")
        for c in range(max_colors)
    }

    # Cada vértice recebe exatamente uma cor
    for v in vertices:
        model.AddExactlyOne(x[v, c] for c in range(max_colors))

    # Vértices adjacentes não podem ter a mesma cor
    for v in vertices:
        for u in graph[v]:
            if u > v:  # evitar duplicar restrições
                for c in range(max_colors):
                    model.Add(x[v, c] + x[u, c] <= 1)

    # Se um vértice usa cor c, então y[c] deve ser 1
    for v in vertices:
        for c in range(max_colors):
            model.Add(x[v, c] <= y[c])

    # Minimizar o número total de cores usadas
    model.Minimize(sum(y[c] for c in range(max_colors)))

    # Resolver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        coloring = {}
        for v in vertices:
            for c in range(max_colors):
                if solver.Value(x[v, c]) == 1:
                    coloring[v] = c
                    break
        # Remapeamento sequencial das cores
        used_colors = sorted(set(coloring.values()))
        color_map = {c: i for i, c in enumerate(used_colors)}
        remapped = {v: color_map[coloring[v]] for v in coloring}
        return remapped
    else:
        print("Não foi encontrada solução viável.")
        return None