import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
from typing import Tuple


def distinct_chars(text:str) -> list[str]:
    return list(set(text))


def bigram_probability(text:str) -> Tuple[dict[str, float], Counter[str]]:
    bigrams = Counter([text[i:i+2] for i in range(len(text)-1)])
    n = sum(bigrams.values())
    return {x: y/n for x, y in bigrams.items()}, bigrams


def p_matrix(chars:list[str], probabilities:dict[str, float]) -> np.ndarray:
    """
    Probability matrix
    """
    n = len(chars)
    p = np.zeros(shape=(n, n))
    for k, v in probabilities.items():
        p[chars.index(k[0]), chars.index(k[1])] = v
    return p


def a_matrix(chars:list[str], bigrams: Counter[str]) -> np.ndarray:
    """
    Stochastic matrix (Markov transition matrix)
    """
    n = len(chars)
    a = np.zeros(shape=(n, n))
    for char in chars:
        filtered = {k: v for k, v in bigrams.items() if k[0] == char}
        count = sum(filtered.values())
        for k, v in filtered.items():
            a[chars.index(k[0]), chars.index(k[1])] = v/count
    return a


def pi_vec(a_matrix:np.ndarray) -> np.ndarray:
    """
    Stationary probability vector
    """
    eig_val, eig_vec = np.linalg.eig(a_matrix.T)
    pi = eig_vec[:, np.isclose(eig_val, 1, atol=1e-2)]
    return np.real(pi/sum(pi)).T[0]


def split_graph(G:nx.Graph) -> Tuple[nx.Graph, nx.Graph]:
    a, b = nx.community.kernighan_lin_bisection(G, weight="weight", max_iter=26)
    score_a, score_b = 0, 0
    for i in list(a):
        score_a += pi[i]
    for i in list(b):
        score_b += pi[i]
    if score_a > score_b:
        return G.subgraph(a), G.subgraph(b)
    else:
        return G.subgraph(b), G.subgraph(a)


def plot_matrix(matrix:np.ndarray) -> None:
    plt.imshow(matrix)
    plt.show()


def plot_network(G:nx.Graph, l:nx.Graph, r:nx.Graph) -> None:
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=pi*10000)
    nx.draw_networkx_edges(G, pos, alpha=.2)
    nx.draw_networkx_edges(G, pos, edgelist=list(G.subgraph(l).edges), edge_color="tab:red", alpha=.8)
    nx.draw_networkx_edges(G, pos, edgelist=list(G.subgraph(r).edges), edge_color="tab:green", alpha=.8)
    nx.draw_networkx_labels(G, pos, labels={i: x for i, x in enumerate(dc)})
    plt.show()


if __name__ == "__main__":
    with open("./data/test.txt") as file:
        text = file.read()
        text = text[1:-1]
    dc = distinct_chars(text=text)
    bp, bs = bigram_probability(text=text)
    p = p_matrix(chars=dc, probabilities=bp)
    a = a_matrix(chars=dc, bigrams=bs)
    pi = pi_vec(a_matrix=a)

    print("Keys ordered by pi:")
    print(np.flip(np.array(dc)[pi.argsort()]))
    print()

    G = nx.from_numpy_array(p+p.T)

    # Split G three more times to get four sections for each hand.
    l, r = split_graph(G)
    l_1, l_2 = split_graph(l)
    l_11, l_12 = split_graph(l_1)
    l_21, l_22 = split_graph(l_2)
    r_1, r_2 = split_graph(r)
    r_11, r_12 = split_graph(r_1)
    r_21, r_22 = split_graph(r_2)

    print("Splits [keys, sum(pi)]:")
    print([dc[i] for i in list(l_11.nodes())], sum([pi[i] for i in list(l_11.nodes())]))
    print([dc[i] for i in list(l_12.nodes())], sum([pi[i] for i in list(l_12.nodes())]))
    print([dc[i] for i in list(l_21.nodes())], sum([pi[i] for i in list(l_21.nodes())]))
    print([dc[i] for i in list(l_22.nodes())], sum([pi[i] for i in list(l_22.nodes())]))
    print([dc[i] for i in list(r_11.nodes())], sum([pi[i] for i in list(r_11.nodes())]))
    print([dc[i] for i in list(r_12.nodes())], sum([pi[i] for i in list(r_12.nodes())]))
    print([dc[i] for i in list(r_21.nodes())], sum([pi[i] for i in list(r_21.nodes())]))
    print([dc[i] for i in list(r_22.nodes())], sum([pi[i] for i in list(r_22.nodes())]))

    plot_matrix(p)
    plot_network(G=G, l=l, r=r)
