from collections import defaultdict
import random
import utils

def aco_coloring(graph, max_colors=5, num_ants=10, iterations=100, alpha=1.0, beta=2.0, evaporation=0.1):
    vertices = list(graph.keys())
    pheromone = defaultdict(lambda: [1.0] * max_colors)

    best_solution = None
    best_conflicts = float('inf')
    best_used_colors = max_colors

    for it in range(iterations):
        all_solutions = []

        for _ in range(num_ants):
            coloring = {}
            for v in vertices:
                used_colors = {coloring[n] for n in graph[v] if n in coloring}
                probabilities = []

                for c in range(max_colors):
                    tau = pheromone[v][c] ** alpha
                    eta = (1.0 / (1 + (1 if c in used_colors else 0))) ** beta
                    probabilities.append(tau * eta)

                total = sum(probabilities)
                if total == 0:
                    chosen_color = random.randint(0, max_colors - 1)
                else:
                    probs = [p / total for p in probabilities]
                    chosen_color = random.choices(range(max_colors), weights=probs)[0]

                coloring[v] = chosen_color

            conflicts = utils.count_conflicts(coloring, graph)
            used_colors = len(set(coloring.values()))
            all_solutions.append((coloring, conflicts, used_colors))

            if conflicts < best_conflicts or (conflicts == best_conflicts and used_colors < best_used_colors):
                best_solution = coloring
                best_conflicts = conflicts
                best_used_colors = used_colors

        # Evaporação de feromônio
        for v in vertices:
            for c in range(max_colors):
                pheromone[v][c] *= (1 - evaporation)

        # Reforço de feromônio pelas melhores formigas (top 1 ou mais)
        all_solutions.sort(key=lambda x: (x[1], x[2]))
        for coloring, conflicts, used_colors in all_solutions[:3]:
            contribution = 1.0 / (1 + conflicts + used_colors)
            for v in coloring:
                pheromone[v][coloring[v]] += contribution

    # Remapeia cores sequencialmente
    used_colors = sorted(set(best_solution.values()))
    color_map = {c: i for i, c in enumerate(used_colors)}
    remapped = {v: color_map[best_solution[v]] for v in best_solution}

    return remapped, best_used_colors, best_conflicts