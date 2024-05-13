def adj_matrix(edges, n, is_directed=False):
    """"
    edges = graph's edges
    n = graph's number of vertices
    is_directed = is the graph is directed
    return : the adjacency matrix of the graph
    """
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    for (source, destination, weight) in edges:
        matrix[source][destination] = weight
        if not is_directed:
            matrix[destination][source] = weight

    return matrix


def adj_list(edges, n, is_directed=False):
    """"
    edges = graph's edges
    n = graph's number of vertices
    is_directed = is the graph is directed
    return : the adjacency list of the graph
    """
    successor = [[] for _ in range(n)]

    for edge in edges:
        successor[edge[0]].append(edge[1])
        if not is_directed:
            successor[edge[1]].append(edge[0])

    return successor


def extract_odd_vertices(adj_mat):
    """
    :param adj_mat: the graph adj matrix
    :return: a list of all the odd degree vertices
    """

    odds = []
    n = len(adj_mat)
    for i in range(n):
        if (n - adj_mat[i].count(0)) % 2 == 1:
            odds.append(i)

    return odds


def remove_edge(adj, vertex, dest, is_directed=False):
    """
    function used in eulerian path
    removes an edge from the list.
    Tries both permutations for undirected graph
    :param adj:  the graph adjacency matrix from which we are removing edges
    :param vertex:
    :param dest: vertex <-> dest represents the edge to remove
    :param is_directed:  whether the graph is directed or not
    """
    try:
        index = adj[vertex].index(dest)
        adj[vertex].pop(index)
    except ValueError:
        index = adj[dest].index(vertex)
        adj[dest].pop(index)
    if not is_directed:
        index = adj[dest].index(vertex)
        adj[dest].pop(index)
