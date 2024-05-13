from osmnx.plot import plot_graph, _save_and_show


def plot_graph_route(
    graph,
    route,
    route_color="r",
    route_linewidth=4,
    route_alpha=0.5,
    orig_dest_size=100,
    ax=None,
    **pg_kwargs
):
    if ax is None:
        # plot the graph but not the route, and override any user show/close
        # args for now: we'll do that later
        override = {"show", "save", "close"}
        kwargs = {k: v for k, v in pg_kwargs.items() if k not in override}
        fig, ax = plot_graph(graph, show=False, save=False,
                             close=False, **kwargs)
    else:
        fig = ax.figure

    # scatterplot origin and destination points (first/last nodes in route)
    x = (graph.nodes[route[0][0]]["x"], graph.nodes[route[-1][1]]["x"])
    y = (graph.nodes[route[0][0]]["y"], graph.nodes[route[-1][1]]["y"])
    ax.scatter(x, y, s=orig_dest_size, c=route_color,
               alpha=route_alpha, edgecolor="none")

    x = []
    y = []
    for r in route:
        u, v, d = r
        if "geometry" in d[0]:
            # if geometry attribute exists, add all its coords to list
            xs, ys = d[0]["geometry"].xy
            x.extend(xs)
            y.extend(ys)
        else:
            # otherwise, the edge is a straight line from node to node
            x.extend((graph.nodes[u]["x"], graph.nodes[v]["x"]))
            y.extend((graph.nodes[u]["y"], graph.nodes[v]["y"]))
    ax.plot(x, y, c=route_color, lw=route_linewidth, alpha=route_alpha)

    # save and show the figure as specified, passing relevant kwargs
    sas_kwargs = {"save", "show", "close", "filepath", "file_format", "dpi"}
    kwargs = {k: v for k, v in pg_kwargs.items() if k in sas_kwargs}
    fig, ax = _save_and_show(fig, ax, **kwargs)
    return fig, ax
