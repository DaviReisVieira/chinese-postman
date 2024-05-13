import pandas as pd
import networkx as nx


def show_stats(G, euler_circuit):
    total_length_of_circuit = sum(
        [edge[2][0]['length'] for edge in euler_circuit])
    total_length_on_orig_map = sum(
        nx.get_edge_attributes(G, 'length').values())
    _vcn = pd.value_counts(pd.value_counts(
        [(e[0]) for e in euler_circuit]), sort=False)
    node_visits = pd.DataFrame(
        {'número de visitas': _vcn.index, 'número de nós': _vcn.values})
    _vce = pd.value_counts(pd.value_counts(
        [sorted(e)[0] + sorted(e)[1] for e in nx.MultiDiGraph(euler_circuit).edges()]))
    edge_visits = pd.DataFrame(
        {'número de visitas': _vce.index, 'número de arestas': _vce.values})
    edge_visits = edge_visits.sort_values(by='número de visitas')

    print('Comprimento do caminho: {0:.2f} m'.format(total_length_of_circuit))
    print('Comprimento do mapa original: {0:.2f} m'.format(
        total_length_on_orig_map))
    print('Comprimento gasto refazendo arestas: {0:.2f} m'.format(
        total_length_of_circuit - total_length_on_orig_map))
    if (total_length_on_orig_map != 0):
        percent = ((1 - total_length_of_circuit /
                   total_length_on_orig_map) * - 100)
    else:
        percent = 0
    print('Porcentagem do trajeto refeito: {0:.2f}% \n'.format(percent))

    print('Número de arestas no circuito: {}'.format(len(euler_circuit)))
    print('Número de arestas no grafo original: {}'.format(len(G.edges())))
    print('Número de nós no grafo original: {}\n'.format(len(G.nodes())))

    print('Número de arestas atravessadas mais de uma vez: {}\n'.format(
        len(euler_circuit) - len(G.edges())))
