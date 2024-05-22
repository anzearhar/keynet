import networkx as nx
from typing import Literal
import pandas as pd

def weighted_degree_ranking(G : nx.DiGraph, dc : list, degree_type : Literal["in", "out"] | None = None) -> list[tuple[int, str, float]]:
    """
    Returns a list [(id, label, weighted degree)], sorted by weighted degree.
    """

    # NOTE: Differentiating between all, in and out degree seems mostly pointless,
    # because the difference is small enough to not change order.
    # Kind off expected, because as long as the text used to get the weights
    # is long enough you would kind off expect all bigrams to appear uniformly.

    if degree_type == "in":
        weighted_degree = dict(G.in_degree(weight="weight"))
    elif degree_type == "out":
        weighted_degree = dict(G.out_degree(weight="weight"))
    else:
        weighted_degree = dict(G.degree(weight="weight"))

    s = sorted(weighted_degree, key=lambda i: weighted_degree.get(i), reverse=True)
    node_labels = {i: x for i, x in enumerate(dc)}
    out = [(node_id, node_labels[node_id], weighted_degree[node_id]) for node_id in s]
    return out

def weighted_eigenvector_centrality_ranking(G : nx.DiGraph, dc : list) -> list[tuple[int, str, float]]:
    """
    Returns a list [(id, label, EV centrality)], sorted by eigenvector centrality,
    while taking into account edge weights.
    """
    eig_centrality = nx.eigenvector_centrality_numpy(G, weight="weight")
    s = sorted(eig_centrality, key=lambda i: eig_centrality.get(i), reverse=True)
    node_labels = {i: x for i, x in enumerate(dc)}
    out = [(node_id, node_labels[node_id], eig_centrality[node_id]) for node_id in s]
    return out

def weighted_betweenness_centrality_ranking(G : nx.DiGraph, dc : list) -> list[tuple[int, str, float]]:
    """
    Returns a list [(id, label, betweenness centrality)], sorted by betweenness centrality,
    while taking into account edge weights.
    """

    # NOTE: betweenness centrality looks for shortest paths, so weights that denote importance
    # (higher is better) like in our case would flip this on it's head, and the nodes
    # that will be highlighted will actually be the least important nodes. Maybe change
    # weights: weight_new = 1 - weight_current

    G_tmp = G.copy()
    for u, v, weight in G_tmp.edges(data=True):
        weight["weight"] = 1 - weight["weight"]

    bet_centrality = nx.betweenness_centrality(G_tmp, weight="weight")
    s = sorted(bet_centrality, key=lambda i: bet_centrality.get(i), reverse=True)
    node_labels = {i: x for i, x in enumerate(dc)}
    out = [(node_id, node_labels[node_id], bet_centrality[node_id]) for node_id in s]
    return out

def weighted_closeness_centrality(G : nx.DiGraph) -> dict:
    """
    Weighted closeness centrality implementation, because networkx doesn't have it.
    """
    closeness_centrality = {}
    for node in G.nodes():
        shortest_paths = nx.single_source_dijkstra_path_length(G, node, weight="weight")
        total_distance = sum(shortest_paths.values())
        closeness_centrality[node] = 1 / total_distance
    return closeness_centrality

def weighted_closeness_centrality_ranking(G : nx.DiGraph, dc : list) -> list[tuple[int, str, float]]:
    """
    Returns a list [(id, label, closeness_centrality)], sorted by closeness centrality,
    while taking into account edge weights.
    """
    G_tmp = G.copy()
    for u, v, weight in G_tmp.edges(data=True):
        weight["weight"] = 1 - weight["weight"]

    close_centrality = weighted_closeness_centrality(G_tmp)
    s = sorted(close_centrality, key=lambda i: close_centrality.get(i), reverse=True)
    node_labels = {i: x for i, x in enumerate(dc)}
    out = [(node_id, node_labels[node_id], close_centrality[node_id]) for node_id in s]
    return out

def weighted_pagerank_ranking(G : nx.DiGraph, dc : list) -> list[tuple[int, str, float]]:
    """
    Returns a list [(id, label, pagerank_score)], sorted by pagerank score,
    while taking into account edge weights.
    """
    G_tmp = G.copy()
    for u, v, weight in G_tmp.edges(data=True):
        weight["weight"] = 1 - weight["weight"]

    close_centrality = nx.pagerank(G_tmp, weight="weight")
    s = sorted(close_centrality, key=lambda i: close_centrality.get(i), reverse=True)
    node_labels = {i: x for i, x in enumerate(dc)}
    out = [(node_id, node_labels[node_id], close_centrality[node_id]) for node_id in s]
    return out

def get_rankings(sorted_list) -> list:
    """
    Transforms a sorted list into a ranking. Returns [(rank, node_id)].
    """
    return [(i+1, sample[0]) for i, sample in enumerate(sorted_list)]

def construct_dataframe(G : nx.DiGraph, dc : list) -> pd.DataFrame:
    """
    Constructs and returns a pandas dataframe that stores characters, their ranking
    for each network analysis metric and their avarage rank. Indexes are node ids.
    """

    out_deg = weighted_degree_ranking(G, dc)
    out_ev = weighted_eigenvector_centrality_ranking(G, dc)
    out_bet = weighted_betweenness_centrality_ranking(G, dc)
    out_close = weighted_closeness_centrality_ranking(G, dc)
    out_pr = weighted_pagerank_ranking(G, dc)

    data = pd.DataFrame()
    data["Charecter"] = dc
    data["Degree"] = [rank for rank, _ in sorted(get_rankings(out_deg), key=lambda i: i[1])]
    data["Eigenvector"] = [rank for rank, _ in sorted(get_rankings(out_ev), key=lambda i: i[1])]
    data["Betweenness"] = [rank for rank, _ in sorted(get_rankings(out_bet), key=lambda i: i[1])]
    data["Closeness"] = [rank for rank, _ in sorted(get_rankings(out_close), key=lambda i: i[1])]
    data["PageRank"] = [rank for rank, _ in sorted(get_rankings(out_pr), key=lambda i: i[1])]
    data["Average"] = (data["Degree"] + data["Eigenvector"] + data["Betweenness"] + data["Closeness"] + data["PageRank"])/5
    return data

def sort_by_column(data : pd.DataFrame, column_name : str) -> pd.DataFrame:
    """
    Maybe an unnecessary function lol
    """
    return data.sort_values(by=column_name)
