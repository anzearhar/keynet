import numpy as np
import networkx as nx
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


if __name__ == "__main__":
    with open("./data/test.txt") as file:
        text = file.read()
        text = text[1:-1]
    dc = distinct_chars(text=text)
    bp, bs = bigram_probability(text=text)
    p = p_matrix(chars=dc, probabilities=bp)
    a = a_matrix(chars=dc, bigrams=bs)
    pi = pi_vec(a_matrix=a)

    """
    print(text)
    print()
    print(dc)
    print()
    print(bp)
    print()
    print(bs)
    print()
    print(p)
    print()
    print(a)
    print()
    print(pi)
    """

    G = nx.from_numpy_array(p+p.T)
    a, b = nx.community.kernighan_lin_bisection(G, weight="weight", max_iter=26)

    import matplotlib.pyplot as plt
    # plt.plot(np.log(np.sort(p.flatten())), range(26**2))
    plt.imshow(p)
    plt.show()
    # nx.draw(G)
    # """
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=pi*10000)
    # nx.draw_networkx_nodes(G, pos, nodelist=list(a), node_color="tab:red")
    # nx.draw_networkx_nodes(G, pos, nodelist=list(b), node_color="tab:green")
    nx.draw_networkx_edges(G, pos, alpha=.2)
    nx.draw_networkx_edges(G, pos, edgelist=list(G.subgraph(a).edges), edge_color="tab:red", alpha=.8)
    nx.draw_networkx_edges(G, pos, edgelist=list(G.subgraph(b).edges), edge_color="tab:green", alpha=.8)
    nx.draw_networkx_labels(G, pos, labels={i: x for i, x in enumerate(dc)})
    # """
    plt.show()
