import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

edges1 = [(0, 1, 3), (0, 2, 1), (0, 4, 5), (2, 4, 2),
          (4, 5, 4), (1, 5, 6), (1, 3, 1), (5, 3, 1)]

best_path1 = [0, 1, 5, 3, 1, 3, 5, 4, 0, 2, 4, 2, 0]


def make_draw(edges, best_path):
    G = nx.Graph()
    G.add_weighted_edges_from(edges)

    pos = nx.spring_layout(G)

    fig, ax = plt.subplots()

    def update_plot(i):
        ax.clear()
        nx.draw(G, pos, with_labels=True, node_size=700,
                node_color="skyblue", ax=ax)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)

        # Highlight the edges in the best path
        for j in range(1, len(best_path)):
            if i >= j:
                # if visited, red, else, blue
                nx.draw_networkx_edges(G, pos, edgelist=[(
                    best_path[j-1], best_path[j])], edge_color='red', width=2, ax=ax)

        ax.set_title(f"Iteration {i+1}/{len(best_path)}")

    # Animate the plot
    ani = animation.FuncAnimation(fig, update_plot, frames=len(
        best_path), interval=1000, repeat=False)

    plt.show()


make_draw(edges1, best_path1)
