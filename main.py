import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import csv

from heuristics import dsatur, bfs_ca, welsh_powell
from metaheuristics import ant_colony, genetic, grasp, simulated_annealing, tabu_search
#from ilp import ortools_sat, pulp_ilp
from utils import run_algorithm
from parse_instances import parse_dimacs
#from visualizacao import visualizar_grafo, visualizar_comparacao_grafos, visualizar_estatisticas_cores
#from ampl_coloring import graph_coloring_ampl, graph_coloring_ampl_cplex

# Dicionário de ótimos conhecidos para instâncias
OTIMOS = {
    "fpsol2.i.1.col": 65,
    "fpsol2.i.2.col": 30,
    "fpsol2.i.3.col": 30,
    "inithx.i.1.col": 54,
    "inithx.i.2.col": 31,
    "inithx.i.3.col": 31,
    "le450_15a.col": 15,
    "le450_15b.col": 15,
    "le450_15c.col": 15,
    "le450_15d.col": 15,
    "le450_25a.col": 25,
    "le450_25b.col": 25,
    "le450_25c.col": 25,
    "le450_25d.col": 25,
    "le450_5a.col": 5,
    "le450_5b.col": 5,
    "le450_5c.col": 5,
    "le450_5d.col": 5,
    "mulsol.i.1.col": 49,
    "mulsol.i.2.col": 31,
    "mulsol.i.3.col": 31,
    "mulsol.i.4.col": 31,
    "mulsol.i.5.col": 31,
    "zeroin.i.1.col": 49,
    "zeroin.i.2.col": 30,
    "zeroin.i.3.col": 30,
    "anna.col": 11,
    "david.col": 11,
    "homer.col": 13,
    "huck.col": 11,
    "jean.col": 10,
    "games120.col": 9,
    "miles1000.col": 42,
    "miles1500.col": 73,
    "miles250.col": 8,
    "miles500.col": 20,
    "miles750.col": 31,
    "queen11_11.col": 11,
    "queen13_13.col": 13,
    "queen5_5.col": 5,
    "queen6_6.col": 7,
    "queen7_7.col": 7,
    "queen8_12.col": 12,
    "queen8_8.col": 9,
    "queen9_9.col": 10,
    "myciel3.col": 4,
    "myciel4.col": 5,
    "myciel5.col": 6,
    "myciel6.col": 7,
    "myciel7.col": 8
}

if __name__ == "__main__":
    # Lista de todas as instâncias disponíveis
    todas_instancias = OTIMOS.keys()
    instancias_padrao = OTIMOS.keys()

    print("="*60)
    print("COLORAÇÃO MÍNIMA DE GRAFOS")
    print("="*60)
    print("1. Executar instâncias padrão")
    print("2. Executar todas as instâncias")
    print("3. Executar uma instância específica")
    print("4. Listar instâncias disponíveis")
    print("="*60)
    
    opcao_execucao = input("\nEscolha uma opção (1-4): ").strip()
    
    if opcao_execucao == "1":
        instancias = instancias_padrao
        print(f"\nExecutando {len(instancias)} instâncias padrão...")
    elif opcao_execucao == "2":
        instancias = todas_instancias
        print(f"\nExecutando todas as {len(instancias)} instâncias...")
    elif opcao_execucao == "3":
        print("\nInstâncias disponíveis:")
        for i, inst in enumerate(todas_instancias, 1):
            nome = os.path.basename(inst)
            print(f"{i}. {nome}")
        try:
            escolha = int(input("\nDigite o número da instância: ")) - 1
            if 0 <= escolha < len(todas_instancias):
                instancias = [todas_instancias[escolha]]
                print(f"\nExecutando instância: {os.path.basename(instancias[0])}")
            else:
                print("Número inválido. Usando instâncias padrão.")
                instancias = instancias_padrao
        except ValueError:
            print("Entrada inválida. Usando instâncias padrão.")
            instancias = instancias_padrao
    elif opcao_execucao == "4":
        print("\nInstâncias disponíveis:")
        for i, inst in enumerate(todas_instancias, 1):
            nome = os.path.basename(inst)
            print(f"{i}. {nome}")
        print("\nSaindo...")
        exit()
    else:
        print("Opção inválida. Usando instâncias padrão.")
        instancias = instancias_padrao
    todos_resultados = []
    for instancia in instancias:
        grafo = parse_dimacs(instancia)
        nome_instancia = os.path.basename(instancia)
        otimo = OTIMOS.get(nome_instancia)

        results = []
        colorings = {}

        results.append(run_algorithm("BFS-CA", bfs_ca.bfs_ca_coloring, graph=grafo))
        colorings["BFS-CA"] = bfs_ca.bfs_ca_coloring(grafo)
        results.append(run_algorithm("Welsh-Powell", welsh_powell.welsh_powell_coloring, graph=grafo))
        colorings["Welsh-Powell"] = welsh_powell.welsh_powell_coloring(grafo)
        results.append(run_algorithm("DSATUR", dsatur.dsatur_coloring, graph=grafo))
        colorings["DSATUR"] = dsatur.dsatur_coloring(grafo)
        #results.append(run_algorithm("Simulated Annealing", simulated_annealing.simulated_annealing_coloring, grafo))
        #colorings["Simulated Annealing"] = simulated_annealing.simulated_annealing_coloring(grafo)
        #results.append(run_algorithm("Tabu Search", tabu_search.tabu_search_coloring, grafo, tabu_tenure=7))
        #colorings["Tabu Search"] = tabu_search.tabu_search_coloring(grafo)
        #results.append(run_algorithm("GRASP", grasp.grasp_coloring, grafo, iterations=100, rcl_size=3))
        #colorings["GRASP"] = grasp.grasp_coloring(grafo)
        #results.append(run_algorithm("Genetic Algorithm", genetic.genetic_algorithm_coloring, grafo, population_size=50, generations=200, mutation_rate=0.1))
        #colorings["Genetic Algorithm"] = genetic.genetic_algorithm_coloring(grafo)
        #results.append(run_algorithm("Ant Colony", ant_colony.aco_coloring, grafo, num_ants=20, iterations=100, alpha=1.0, beta=3.0, evaporation=0.2))
        #colorings["Ant Colony"] = ant_colony.aco_coloring(grafo)
        #results.append(run_algorithm("OR-Tools CP-SAT", ortools_sat.graph_coloring_ortools, grafo))
        #colorings["OR-Tools CP-SAT"] = ortools_sat.graph_coloring_ortools(grafo)
        #results.append(run_algorithm("AMPL (Gurobi)", graph_coloring_ampl, grafo, ampl_model_path='graph_coloring.mod', solver='gurobi'))
        #colorings["AMPL (Gurobi)"] = graph_coloring_ampl(grafo, ampl_model_path='graph_coloring.mod', solver='gurobi')

        # Salvar resultados individuais
        with open(f'resultados/resultados_{nome_instancia}.csv', 'w', newline='') as csvfile:
            fieldnames = ['Instancia', 'Algoritmo', 'Cores', 'Conflitos', 'Tempo (s)', 'Gap para otimo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for r in results:
                gap = None
                if otimo and r['Cores'] != '-' and r['Cores'] != '':
                    try:
                        gap = int(r['Cores']) - otimo
                    except Exception:
                        gap = None
                row = {
                    'Instancia': nome_instancia,
                    'Algoritmo': r['Algoritmo'],
                    'Cores': r['Cores'],
                    'Conflitos': r['Conflitos'],
                    'Tempo (s)': r['Tempo (s)'],
                    'Gap para otimo': gap if gap is not None else ''
                }
                writer.writerow(row)
                todos_resultados.append(row)
        print(f'Resultados salvos em resultados_{nome_instancia}.csv')

        print("\n--- COMPARAÇÃO FINAL ---")
        print(f"{'Algoritmo':<25} {'Cores':<6} {'Conflitos':<10} {'Tempo (s)':<10}")
        print("-" * 55)
        for r in results:
            print(f"{r['Algoritmo']:<25} {r['Cores']:<6} {r['Conflitos']:<10} {r['Tempo (s)']:<10}")
        
        '''
        # Menu de visualização
        print("\n" + "="*60)
        print("OPÇÕES DE VISUALIZAÇÃO")
        print("="*60)
        print("1. Visualizar coloração de um algoritmo específico")
        print("2. Comparar todas as colorações lado a lado")
        print("3. Ver estatísticas de distribuição de cores")
        print("4. Pular visualização")
        print("="*60)
        
        try:
            opcao = input("\nEscolha uma opção (1-4): ").strip()
            
            if opcao == "1":
                # Mostrar algoritmos disponíveis
                algoritmos_disponiveis = []
                print("\nAlgoritmos disponíveis:")
                for i, algoritmo in enumerate(colorings.keys(), 1):
                    if colorings[algoritmo] is not None:
                        num_cores = len(set(colorings[algoritmo].values()))
                        print(f"{i}. {algoritmo} ({num_cores} cores)")
                        algoritmos_disponiveis.append(algoritmo)
                
                try:
                    resposta = input("\nDigite o número ou nome do algoritmo (ou ENTER para cancelar): ").strip()
                except EOFError:
                    print("Input não disponível. Pulando visualização.")
                    continue
                
                # Tentar interpretar como número
                algoritmo_selecionado = None
                try:
                    if resposta.isdigit():
                        idx = int(resposta) - 1
                        if 0 <= idx < len(algoritmos_disponiveis):
                            algoritmo_selecionado = algoritmos_disponiveis[idx]
                except ValueError:
                    pass
                
                # Se não foi número, tentar como nome
                if algoritmo_selecionado is None and resposta in colorings:
                    algoritmo_selecionado = resposta
                
                if algoritmo_selecionado and colorings[algoritmo_selecionado] is not None:
                    print(f"\nVisualizando coloração de {algoritmo_selecionado}...")
                    visualizar_grafo(grafo, colorings[algoritmo_selecionado], algoritmo_selecionado, nome_instancia)
                    
                    # Perguntar se quer ver estatísticas também
                    try:
                        if input("\nDeseja ver as estatísticas de distribuição de cores? (s/n): ").lower() == 's':
                            visualizar_estatisticas_cores(colorings[algoritmo_selecionado], algoritmo_selecionado, nome_instancia)
                    except EOFError:
                        print("Input não disponível. Pulando estatísticas.")
                elif resposta.strip() != '':
                    print("Algoritmo não encontrado ou sem coloração disponível.")
                    
            elif opcao == "2":
                # Filtrar colorações válidas
                colorings_validas = {k: v for k, v in colorings.items() if v is not None}
                if len(colorings_validas) > 1:
                    print(f"\nComparando {len(colorings_validas)} algoritmos...")
                    visualizar_comparacao_grafos(grafo, colorings_validas, nome_instancia)
                else:
                    print("É necessário pelo menos 2 algoritmos válidos para comparação.")
                    
            elif opcao == "3":
                # Mostrar estatísticas para todos os algoritmos
                print("\nEstatísticas de distribuição de cores:")
                for algoritmo, coloring in colorings.items():
                    if coloring is not None:
                        print(f"\n{algoritmo}:")
                        contagem = {}
                        for cor in coloring.values():
                            contagem[cor] = contagem.get(cor, 0) + 1
                        for cor in sorted(contagem.keys()):
                            print(f"  Cor {cor}: {contagem[cor]} vértices")
                        
                        # Perguntar se quer visualizar as estatísticas
                        try:
                            if input(f"\nDeseja visualizar o gráfico de estatísticas para {algoritmo}? (s/n): ").lower() == 's':
                                visualizar_estatisticas_cores(coloring, algoritmo, nome_instancia)
                        except EOFError:
                            print("Input não disponível. Pulando visualização de estatísticas.")
                            
            elif opcao == "4":
                print("Visualização pulada.")
                
            else:
                print("Opção inválida. Visualização pulada.")
                
        except Exception as e:
            print(f"Erro na visualização: {e}")
            print("Continuando para a próxima instância...")
    '''
    # Resumo final
    print("\n" + "="*80)
    print("RESUMO FINAL - TODAS AS INSTÂNCIAS")
    print("="*80)
    print(f"{'Instância':<20} {'Algoritmo':<20} {'Cores':<8} {'Conflitos':<10} {'Tempo (s)':<10}")
    print("-" * 80)
    
    for resultado in todos_resultados:
        print(f"{resultado['Instancia']:<20} {resultado['Algoritmo']:<20} {resultado['Cores']:<8} {resultado['Conflitos']:<10} {resultado['Tempo (s)']:<10}")
    
    import csv


    # --- Fora do loop, escreve todos os resultados num CSV único ---
    with open('resultados_todos.csv', 'w', newline='') as csvfile:
        fieldnames = ['Instancia', 'Algoritmo', 'Cores', 'Conflitos', 'Tempo (s)', 'Gap para otimo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in todos_resultados:
            writer.writerow(row)

    print('Todos os resultados foram salvos em resultados_todos.csv')

    print("\n" + "="*80)
    print("EXECUÇÃO CONCLUÍDA!")
    print("="*80)