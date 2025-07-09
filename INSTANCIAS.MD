# INSTANCIAS.MD

Este documento descreve instâncias de grafos utilizadas em problemas de coloração e otimização combinatória. As instâncias são organizadas por classe e incluem informações relevantes como número de vértices, arestas e número cromático ótimo conhecido.

---

## Classe: SGB (Stanford GraphBase)

Grafos criados por Donald Knuth como parte da Stanford GraphBase, com base em obras literárias, dados geográficos e construções clássicas.

### Grafos de Livros (Personagens e Coocorrência)

- `jean.col`  
  Obra: *Les Misérables*  
  Vértices/Arestas: 80 / 254  
  Número Cromático Ótimo: 10  
  Descrição: Grafo de coocorrência entre personagens; comunidades densamente conectadas.

- `david.col`  
  Obra: *David Copperfield*  
  Vértices/Arestas: 87 / 406  
  Número Cromático Ótimo: 11

- `homer.col`  
  Obra: *Ilíada*  
  Vértices/Arestas: 561 / 1629  
  Número Cromático Ótimo: 13

### Grafos da Rainha (Queen Graphs)

- `queen8_12.col`  
  Tabuleiro: 8 × 12  
  Vértices/Arestas: 96 / 1368  
  Número Cromático Ótimo: 12  
  Descrição: Cada nó representa uma casa; conectados por linha, coluna e diagonal. Alta simetria e densidade.

- `queen13_13.col`  
  Tabuleiro: 13 × 13  
  Vértices/Arestas: 169 / 6656  
  Número Cromático Ótimo: 13

### Grafos de Milhas (Miles Graphs)

- `miles500.col`  
  Distância máxima: 500 milhas  
  Vértices/Arestas: 128 / 1170  
  Número Cromático Ótimo: 20

- `miles750.col`  
  Distância máxima: 750 milhas  
  Vértices/Arestas: 128 / 2113  
  Número Cromático Ótimo: 31

- `miles1000.col`  
  Distância máxima: 1000 milhas  
  Vértices/Arestas: 128 / 3216  
  Número Cromático Ótimo: 42

- `miles1500.col`  
  Distância máxima: 1500 milhas  
  Vértices/Arestas: 128 / 5198  
  Número Cromático Ótimo: 73

---

## Classe: MYC (Mycielski Graphs)

Grafos livres de triângulos com número cromático crescente. Usados para avaliar algoritmos que não dependem apenas do tamanho do clique máximo.

- `myciel3.col`  
  Vértices/Arestas: 11 / 20  
  Número Cromático Ótimo: 4  
  Descrição: Clique máxima = 2, mas número cromático 4.

- `myciel4.col`  
  Vértices/Arestas: 23 / 71  
  Número Cromático Ótimo: 5

- `myciel5.col`  
  Vértices/Arestas: 47 / 236  
  Número Cromático Ótimo: 6

- `myciel6.col`  
  Vértices/Arestas: 95 / 755  
  Número Cromático Ótimo: 7

- `myciel7.col`  
  Vértices/Arestas: 191 / 2360  
  Número Cromático Ótimo: 8

---

## Classe: LEI (Leighton Graphs)

Grafos sintéticos com coloração ótima conhecida, frequentemente usados como benchmarks em problemas de coloração de grafos densos.

- `le450_5a.col`  
  Vértices/Arestas: 450 / 5714  
  Número Cromático Ótimo: 5  
  Descrição: Usado para testar desempenho em grafos densos com baixa coloração.

- `le450_15b.col`  
  Vértices/Arestas: 450 / 8169  
  Número Cromático Ótimo: 15

---

## Observações

- As instâncias da classe SGB incluem dados reais e construções clássicas, ideais para testes de algoritmos com estrutura interpretável.
- Os grafos MYC são excelentes para avaliar limites superiores de coloração sem dependência direta de cliques.
- Os grafos LEI são amplamente usados em comparações de desempenho entre heurísticas e algoritmos exatos.

---

**Fontes:**  
- Michael Trick (trick@cmu.edu)  
- Donald Knuth – Stanford GraphBase  
- DIMACS Benchmark Instances