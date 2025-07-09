import networkx as nx
import matplotlib
# Tentar diferentes backends para compatibilidade
try:
    matplotlib.use('TkAgg')
except:
    try:
        matplotlib.use('Qt5Agg')
    except:
        matplotlib.use('Agg')  # Backend não-interativo como fallback
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.lines as mlines
import random

def visualizar_grafo(graph, coloring, algoritmo_nome, instancia_nome):
    """
    Visualiza um grafo com sua coloração.
    
    Parâmetros:
    - graph: dict {vértice: [vizinhos]}
    - coloring: dict {vértice: cor}
    - algoritmo_nome: string com o nome do algoritmo usado
    - instancia_nome: string com o nome da instância
    """
    if not coloring:
        print("Coloração vazia ou inválida.")
        return
    
    # Criar grafo NetworkX
    G = nx.Graph()
    
    # Adicionar vértices e arestas
    for vertex in graph:
        G.add_node(vertex)
        for neighbor in graph[vertex]:
            if neighbor > vertex:  # Evitar adicionar a mesma aresta duas vezes
                G.add_edge(vertex, neighbor)
    
    # Preparar cores para visualização
    cores_disponiveis = list(mcolors.TABLEAU_COLORS.keys())
    cores_unicas_set = set(coloring.values())
    num_cores_unicas = len(cores_unicas_set)
    
    # Se precisar de mais cores que as disponíveis, gerar cores adicionais
    if num_cores_unicas > len(cores_disponiveis):
        cores_adicionais = []
        for i in range(num_cores_unicas - len(cores_disponiveis)):
            # Gerar cores aleatórias
            r = random.random()
            g = random.random()
            b = random.random()
            cores_adicionais.append((r, g, b))
        cores_disponiveis.extend(cores_adicionais)
    
    # Mapear cores dos vértices
    cores_vertices = []
    for node in G.nodes():
        cor_idx = coloring.get(str(node), 0)
        cores_vertices.append(cores_disponiveis[cor_idx % len(cores_disponiveis)])
    
    # Configurar a figura
    plt.figure(figsize=(12, 8))
    
    # Layout do grafo
    if len(G.nodes()) <= 50:
        pos = nx.spring_layout(G, k=1, iterations=50)
    else:
        # Para grafos grandes, usar layout mais simples
        pos = nx.kamada_kawai_layout(G)
    
    # Desenhar o grafo
    nx.draw(G, pos, 
            node_color=cores_vertices,
            node_size=500,
            with_labels=True,
            font_size=8,
            font_weight='bold',
            edge_color='gray',
            width=1)
    
    # Título
    plt.title(f'Coloração do Grafo - {algoritmo_nome}\nInstância: {instancia_nome}\n'
              f'Número de cores: {num_cores_unicas}', 
              fontsize=14, fontweight='bold')
    
    # Adicionar legenda de cores
    cores_unicas = sorted(set(coloring.values()))
    legend_elements = []
    for i, cor in enumerate(cores_unicas):
        color = cores_disponiveis[cor % len(cores_disponiveis)]
        legend_elements.append(mlines.Line2D([0], [0], marker='o', color='w', 
                                        markerfacecolor=color, markersize=10, 
                                        label=f'Cor {cor}'))
    
    plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
    
    # Ajustar layout
    plt.tight_layout()
    
    # Mostrar a visualização
    plt.show()
    
    # Salvar a figura
    nome_arquivo = f"visualizacao_{instancia_nome.replace('.col', '')}_{algoritmo_nome.replace(' ', '_')}.png"
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    print(f"Visualização salva como: {nome_arquivo}")

def visualizar_comparacao_grafos(graph, colorings, instancia_nome):
    """
    Visualiza múltiplas colorações do mesmo grafo para comparação.
    
    Parâmetros:
    - graph: dict {vértice: [vizinhos]}
    - colorings: dict {algoritmo: coloring}
    - instancia_nome: string com o nome da instância
    """
    if not colorings:
        print("Nenhuma coloração fornecida para comparação.")
        return
    
    num_algoritmos = len(colorings)
    fig, axes = plt.subplots(1, num_algoritmos, figsize=(6*num_algoritmos, 6))
    
    if num_algoritmos == 1:
        axes = [axes]
    
    cores_disponiveis = list(mcolors.TABLEAU_COLORS.keys())
    
    for i, (algoritmo, coloring) in enumerate(colorings.items()):
        if not coloring:
            continue
            
        # Criar grafo NetworkX
        G = nx.Graph()
        for vertex in graph:
            G.add_node(vertex)
            for neighbor in graph[vertex]:
                if neighbor > vertex:
                    G.add_edge(vertex, neighbor)
        
        # Preparar cores dos vértices
        cores_vertices = []
        for node in G.nodes():
            cor_idx = coloring.get(str(node), 0)
            cores_vertices.append(cores_disponiveis[cor_idx % len(cores_disponiveis)])
        
        # Layout
        if len(G.nodes()) <= 50:
            pos = nx.spring_layout(G, k=1, iterations=30)
        else:
            pos = nx.kamada_kawai_layout(G)
        
        # Desenhar
        nx.draw(G, pos, 
                node_color=cores_vertices,
                node_size=300,
                with_labels=True,
                font_size=6,
                font_weight='bold',
                edge_color='gray',
                width=0.8,
                ax=axes[i])
        
        cores_set = set(coloring.values())
        num_cores = len(cores_set)
        axes[i].set_title(f'{algoritmo}\n{num_cores} cores', fontsize=10)
    
    plt.suptitle(f'Comparação de Algoritmos - {instancia_nome}', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
    
    # Salvar
    nome_arquivo = f"comparacao_{instancia_nome.replace('.col', '')}.png"
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    print(f"Comparação salva como: {nome_arquivo}")

def visualizar_estatisticas_cores(coloring, algoritmo_nome, instancia_nome):
    """
    Visualiza estatísticas da coloração (distribuição de cores).
    
    Parâmetros:
    - coloring: dict {vértice: cor}
    - algoritmo_nome: string com o nome do algoritmo
    - instancia_nome: string com o nome da instância
    """
    if not coloring:
        print("Coloração vazia ou inválida.")
        return
    
    # Contar vértices por cor
    contagem_cores = {}
    for cor in coloring.values():
        contagem_cores[cor] = contagem_cores.get(cor, 0) + 1
    
    # Preparar dados para o gráfico
    cores = list(contagem_cores.keys())
    contagens = list(contagem_cores.values())
    
    # Criar gráfico de barras
    plt.figure(figsize=(10, 6))
    bars = plt.bar(cores, contagens, color='skyblue', edgecolor='navy', alpha=0.7)
    
    # Adicionar valores nas barras
    for bar, count in zip(bars, contagens):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(count), ha='center', va='bottom', fontweight='bold')
    
    plt.xlabel('Cor')
    plt.ylabel('Número de Vértices')
    plt.title(f'Distribuição de Cores - {algoritmo_nome}\nInstância: {instancia_nome}')
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Salvar
    nome_arquivo = f"estatisticas_{instancia_nome.replace('.col', '')}_{algoritmo_nome.replace(' ', '_')}.png"
    plt.savefig(nome_arquivo, dpi=300, bbox_inches='tight')
    print(f"Estatísticas salvas como: {nome_arquivo}") 