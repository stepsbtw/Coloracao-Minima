from amplpy import AMPL

def graph_coloring_ampl(graph, max_colors=None, ampl_model_path='graph_coloring.mod', solver='gurobi'):
    # Converta os nomes dos vértices para inteiros
    vertices = sorted(set(int(v) for v in graph.keys()))
    graph_int = {int(v): [int(u) for u in vizinhos] for v, vizinhos in graph.items()}
    n = len(vertices)
    if max_colors is None:
        max_colors = n

    colors = list(range(max_colors))

    ampl = AMPL()
    ampl.read(ampl_model_path)

    # Define sets
    ampl.set['VERTICES'] = vertices
    ampl.set['COLORS'] = colors

    # Define adjacency matrix
    adj = {}
    for v in vertices:
        for u in vertices:
            adj[(v, u)] = 1 if u in graph_int[v] else 0
    ampl.param['adj'] = adj

    ampl.setOption('solver', solver)
    ampl.solve()

    x = ampl.getVariable('x')
    coloring = {}
    for v in vertices:
        for c in colors:
            try:
                if x[v, c].value() > 0.5:
                    coloring[v] = c
                    break
            except:
                continue

    # Remapeamento sequencial das cores
    used_colors = sorted(set(coloring.values()))
    color_map = {c: i for i, c in enumerate(used_colors)}
    # Converta as chaves de volta para string para compatibilidade
    remapped = {str(v): color_map[coloring[v]] for v in coloring}
    return remapped 