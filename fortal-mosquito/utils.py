import numpy as np
import networkx as nx
from itertools import combinations
from heapq import heappop, heapify


def get_odd_degree_nodes(graph):
    """ 
    Finds all nodes with odd degree in the graph.
    :param graph: a graph
    :return: a list of nodes with odd degree
    """
    return [v for v, d in graph.degree() if d % 2 == 1]


def get_shortest_distance_for_odd_degrees(graph, odd_degree_nodes):
    """ 
    Finds shortest distance for all odd degree nodes combinations
    :param graph: a graph
    :param odd_degree_nodes: a list of nodes with odd degree
    :return: a dictionary of shortest distances for all odd degree nodes combinations

    """

    pairs = combinations(odd_degree_nodes, 2)

    return {(v, u): nx.dijkstra_path_length(graph, v, u, weight="length") for v, u in pairs}


def min_matching(pair_weights):
    """ 
    Finds the minimum matching for the given pair weights
    :param pair_weights: list of 3-tuples denoting an edge with weight
    :return: a list triples of matching weights denoting an edge with weight

    .. [1] Galil, Z. (1986). Efficient algorithms for finding maximum matching in graphs. ACM Comput. Surv., 18, 23-38.
    https://www.semanticscholar.org/paper/Efficient-algorithms-for-finding-maximum-matching-Galil/ef1b31b4728615a52e3b8084379a4897b8e526ea?p2df
    """

    complete_graph = create_weighted_complete_graph(pair_weights)
    matching = nx.algorithms.max_weight_matching(complete_graph, True)

    matching_weights = []
    for v, u in matching:
        if (v, u) in pair_weights:
            matching_weights.append((v, u, np.round(pair_weights[v, u], 2)))
        else:
            matching_weights.append((v, u, np.round(pair_weights[u, v], 2)))

    return matching_weights


def create_eulerian_circuit(graph_augmented, graph_original, starting_node=None):
    """
    Create the eulerian path using only edges from the original graph.
    :param graph_augmented: an augmented graph
    :param graph_original: the original graph
    :param starting_node: the starting node
    :return: eulerian circuit
    """
    euler_circuit = []
    naive_circuit = list(nx.eulerian_circuit(
        graph_augmented, source=starting_node))

    for edge in naive_circuit:
        edge_data = graph_augmented.get_edge_data(edge[0], edge[1])
        if "attr_dict" in edge_data[0] and edge_data[0]['attr_dict']['trail'] != 'augmented':
            # If `edge` exists in original graph, grab the edge attributes and add to eulerian circuit.
            edge_att = graph_original[edge[0]][edge[1]]
            euler_circuit.append((edge[0], edge[1], edge_att))
        else:
            aug_path = nx.shortest_path(
                graph_original, edge[0], edge[1], weight='distance')
            aug_path_pairs = list(zip(aug_path[:-1], aug_path[1:]))

            for edge_aug in aug_path_pairs:
                edge_aug_att = graph_original[edge_aug[0]][edge_aug[1]]
                euler_circuit.append((edge_aug[0], edge_aug[1], edge_aug_att))

    return euler_circuit


def create_weighted_complete_graph(pair_weights):
    """ Creates a weighted complete graph with [inverse] negative weights given list of weighted edges.
    (Negative weights are due to using maximal matching algorithm instead of minimal matching algorithm)

    Args:
        - pair_weights (list): list of 3-tuples denoting an edge with weight

    Returns:
        - graph (networkx.Graph): complete graph
    """

    graph = nx.Graph()
    graph.add_weighted_edges_from(
        [(e[0], e[1], - np.round(w, 2)) for e, w in pair_weights.items()])

    return graph


def get_shortest_paths(graph, nodes):
    """ Creates a list of shortest paths between two [not neighboring] nodes.

    Args:
        - graph (networkx.Graph): undirected graph
        - nodes (list): list of tuples (start, end, weight) for which we find a shortest path

    Return:
        - shortest_paths (list): list of shortest paths between two [not neighboring] nodes
    """

    shortest_paths = []

    for u, v, _ in nodes:
        path = nx.dijkstra_path(graph, u, v)
        shortest_paths.extend([(path[i - 1], path[i])
                              for i in range(1, len(path))])

    return shortest_paths


def convert_final_path_to_coordinates(org_graph, final_path):
    """ Converts final path of [osmnx] edges into list of (lat, log) tuples which are then read by Leaflet JS library.

    Args:
        - org_graph (networkx.Graph): directed [original] graph
        - final_path (list): list of [edges] tuples that form a final path

    Returns:
        - path (list): list of (lat, log) tuples
    """

    path = []

    for (u, v, i) in final_path:
        if not org_graph.get_edge_data(u, v):
            coords = list(i[0]["geometry"].coords)[::-1]

            for (x, y) in coords:
                path.append([y, x])

            continue

        if "geometry" not in org_graph.get_edge_data(u, v)[0]:
            x1 = org_graph.nodes[u]["x"]
            x2 = org_graph.nodes[v]["x"]

            y1 = org_graph.nodes[u]["y"]
            y2 = org_graph.nodes[v]["y"]

            path.extend([[y1, x1], [y2, x2]])
            continue

        coords = list(org_graph.get_edge_data(u, v)[0]["geometry"].coords)

        for (x, y) in coords:
            path.append([y, x])

    return path
