import sys
import utils
import eulerian
import dijkstra_functions


class EulerianPathSolver:
    def __init__(self, edges, n):
        self.edges = edges.copy()
        self.n = n

    def is_bridge(self, adj, start, dst):
        """
        :param adj: graph's adjacency list
        :param start: the starting vertex
        :param dst: the destination vertex
        :return: true if start <-> dst is a bridge
        meaning going through this edge would ruin the eulerian path
        """
        if len(adj[start]) == 1:
            utils.remove_edge(adj, start, dst)
            return False

        count_1 = utils.reachable(adj, start, [False] * len(adj))
        utils.remove_edge(adj, start, dst)

        if count_1 == utils.reachable(adj, start, [False] * len(adj)):
            return False
        adj[start].append(dst)
        adj[dst].append(start)
        return True

    def path_aux(self, adj, start, res):
        """
        recursive function to find an eulerian path
        :param res the resulting path
        """
        for dst in adj[start]:
            if not self.is_bridge(adj, start, dst):
                res.append(dst)
                self.path_aux(adj, dst, res)

    def find_eulerian_path(self, edges):
        """
        :return: an array with the vertices to go through in order to have an eulerian path/cycle

        the graph is undirected
        """
        start = 0
        adj = utils.adj_list(edges, self.n)

        assert (eulerian.is_eulerian(adj))
        degrees = eulerian.degres(adj)

        for i in range(len(degrees)):
            if degrees[i] % 2 == 1:
                start = i
                break

        res = [start]
        self.path_aux(adj, start, res)

        return res

    def matchings_gen(self, pairs, matchings, n_pairs, done=None, final=None):
        """
        :param pairs: all possible pairings between odd vertices
        :param matchings: the resulting list of list of all possible matchings
        :param nb: the number of pairs in a single matching
        :param done: vertices already stored in the current matching
        :param final: a possible list of pairing covering all vertices
        """
        if done is None:
            done = []
        if final is None:
            final = []

        if pairs[0][0][0] not in done:
            done.append(pairs[0][0][0])
            for i in pairs[0]:
                f = final[:]
                val = done[:]
                if i[1] not in val:
                    f.append(i)
                else:
                    continue

                if len(f) == n_pairs:
                    matchings.append(f)
                    return
                else:
                    val.append(i[1])
                    self.matchings_gen(pairs[1:], matchings, n_pairs, val, f)

        else:
            self.matchings_gen(pairs[1:], matchings, n_pairs, done, final)

    def eulerianise(self, edges, matches, adj_mat):
        """
        :param matches: the list of odd vertices between which we must add their shortest path to make the graph eulerian
        :param adj_mat: the graph adjacency matrix
        :return: a pair representing the solution path to the chinese postman problem and its total length
        """
        n = self.n
        for (source, destination) in matches:
            path = dijkstra_functions.single_source_distances(
                n, adj_mat, source, destination)
            for i in range(len(path)-1):
                edges.append((path[i], path[i+1]))
        eulerian_path = self.find_eulerian_path(edges)
        length = 0
        for i in range(len(eulerian_path) - 1):
            source = eulerian_path[i]
            destination = eulerian_path[i + 1]
            length += adj_mat[source][destination]
        return (length, eulerian_path)

    def solving(self):
        """
        :return: an  array representing the cycle solution to the problem
        """
        edges = self.edges
        n = self.n
        adj_mat = utils.adj_matrix(edges, n)
        odd_vertices = utils.extract_odd_vertices(adj_mat)
        if len(odd_vertices) == 0:
            return self.find_eulerian_path(edges)

        paths = []
        for i in range(n):
            if i in odd_vertices:
                paths.append(
                    dijkstra_functions.multi_dest_distances(n, adj_mat, i))
            else:
                paths.append([])

        pairs = []
        for i in range(len(odd_vertices) - 1):
            pairs.append([])
            for j in range(i + 1, len(odd_vertices)):
                pairs[i].append([odd_vertices[i], odd_vertices[j]])

        # [ [AB, AC, AD] , [ BC, BD], [ CD]  ]

        matchings = []

        self.matchings_gen(pairs, matchings, (len(pairs) + 1) // 2)

        minimal_match = []
        minimum = sys.maxsize
        for matching in matchings:
            size = 0
            for (source, destination) in matching:
                size += paths[source][destination]
            if size < minimum:
                minimum = size
                minimal_match = matching

        return self.eulerianise(edges, minimal_match, adj_mat)
