import random
import utils


def fitness(coloring, graph):
    """Avalia a qualidade da solução."""
    conflicts = utils.count_conflicts(coloring, graph)
    used_colors = len(set(coloring.values()))
    # Penalizar mais conflitos, depois cores
    return conflicts * 1000 + used_colors

def generate_individual(vertices, max_colors):
    return {v: random.randint(0, max_colors-1) for v in vertices}

def tournament_selection(population, scores, k=3):
    selected = random.sample(list(zip(population, scores)), k)
    selected.sort(key=lambda x: x[1])
    return selected[0][0]

def crossover(parent1, parent2):
    child = {}
    for v in parent1:
        child[v] = parent1[v] if random.random() < 0.5 else parent2[v]
    return child

def mutate(individual, max_colors, mutation_rate=0.1):
    for v in individual:
        if random.random() < mutation_rate:
            individual[v] = random.randint(0, max_colors-1)

def genetic_algorithm_coloring(graph, max_colors=5, population_size=50, generations=100, mutation_rate=0.1):
    vertices = list(graph.keys())

    # População inicial
    population = [generate_individual(vertices, max_colors) for _ in range(population_size)]
    scores = [fitness(ind, graph) for ind in population]

    best_index = scores.index(min(scores))
    best_solution = population[best_index].copy()
    best_score = scores[best_index]

    for gen in range(generations):
        new_population = []
        for _ in range(population_size):
            # Seleção dos pais
            parent1 = tournament_selection(population, scores)
            parent2 = tournament_selection(population, scores)

            # Crossover
            child = crossover(parent1, parent2)

            # Mutação
            mutate(child, max_colors, mutation_rate)

            new_population.append(child)

        population = new_population
        scores = [fitness(ind, graph) for ind in population]

        current_best_index = scores.index(min(scores))
        if scores[current_best_index] < best_score:
            best_score = scores[current_best_index]
            best_solution = population[current_best_index].copy()

        # Interrompe se solução válida (sem conflitos) encontrada
        if best_score < 1000:
            break

    # Remapeia cores sequencialmente
    used_colors = sorted(set(best_solution.values()))
    color_map = {c: i for i, c in enumerate(used_colors)}
    remapped = {v: color_map[best_solution[v]] for v in best_solution}
    conflicts = count_conflicts(remapped, graph)

    return remapped, len(used_colors), conflicts
