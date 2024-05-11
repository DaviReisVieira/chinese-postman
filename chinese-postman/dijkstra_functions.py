import heapq
from collections import deque

INF = float('inf')


def multi_dest_distances(n, adj, src):
    """
    :param n: o número de vértices
    :param adj: a matriz de adjacência com pesos
    :param src: o vértice de origem
    :return: uma lista com o comprimento do caminho mais curto para cada outro vértice
    """
    # Inicializa a lista de distâncias com valores None para todos os vértices
    dist = [None] * n
    # Define a distância do vértice de origem para ele mesmo como 0
    dist[src] = 0
    # Inicializa uma fila (deque) com o vértice de origem
    todo = deque([src])

    # Enquanto houver vértices na fila
    while todo:
        # Remove o primeiro vértice da fila
        s = todo.popleft()
        # Itera sobre os vértices adjacentes ao vértice atual
        for d in range(n):
            # Verifica se há uma aresta entre s e d (weight != 0)
            if adj[s][d] != 0:
                # Calcula a nova distância para o vértice d
                new_dist = dist[s] + adj[s][d]
                # Se a nova distância for menor que a distância atual para d, atualiza
                if dist[d] is None or new_dist < dist[d]:
                    dist[d] = new_dist
                    # Adiciona d à fila para processamento posterior
                    todo.append(d)

    return dist


def single_source_distances(n, adj, src, dst):
    """
    :param n: o número de vértices
    :param adj: a matriz de adjacência com pesos
    :param src: o vértice de origem
    :param dst: o vértice de destino
    :return: uma lista representando o caminho entre src e dst
    implementação do algoritmo de Dijkstra
    """
    dist = [INF] * n
    dist[src] = 0
    todo = [(0, src)]
    parent = [None] * n
    while todo:
        _, s = heapq.heappop(todo)
        for d in range(n):
            weight = adj[s][d]
            if weight != 0 and dist[d] > (dist[s] + weight):
                dist[d] = dist[s] + weight
                heapq.heappush(todo, (dist[d], d))
                parent[d] = s
    res = []
    while dst != src:
        res.insert(0, dst)
        dst = parent[dst]
    res.insert(0, src)
    return res
