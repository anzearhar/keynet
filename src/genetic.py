import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from typing import Optional, Tuple
from text_parser import parse_text
import networkx as nx
from base_layout import full_layout
from visualization import visualize_keyboard_seaborn

HOMEROW = [10, 11, 12, 13, 16, 17, 18, 19]
OTHER = [ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
                         14, 15,
         20, 21, 22, 23, 24, 25, 26, 27, 28, 29]


class Permutation():
    def __init__(self, permutation: Optional[np.ndarray] = None) -> None:
        if permutation is None:
            self.permutation = np.random.permutation(30)
        else:
            self.permutation = permutation

    def __str__(self) -> str:
        return str(self.permutation)

    def mutate(self) -> None:
        n = len(self.permutation)
        a = random.randint(0, n-1)
        if a in HOMEROW:
            b = random.choice(HOMEROW)
        else:
            b = random.choice(OTHER)
        c = self.permutation[a]
        self.permutation[a] = self.permutation[b]
        self.permutation[b] = c

    @staticmethod
    def crossover(p0: "Permutation", p1: "Permutation") -> Tuple["Permutation", "Permutation"]:
        """
        Partially mapped crossover (PMX)
        """
        n = len(p0.permutation)
        a = random.randint(0, n-1)
        if a in HOMEROW:
            b = random.choice(HOMEROW)
        else:
            b = random.choice(OTHER)
        c = [a, b]
        c.sort()

        def pmx(p0: "Permutation", p1: "Permutation", c0: int, c1: int) -> "Permutation":
            pc = Permutation(permutation=np.zeros(n))
            pc.permutation[c0:c1] = p0.permutation[c0:c1]
            for i in np.concatenate([np.arange(0, c0), np.arange(c1, n)]):
                m = p1.permutation[i]
                while m in p0.permutation[c0:c1]:
                    m = p1.permutation[np.where(p0.permutation == m)[0][0]]
                pc.permutation[i] = m
            return pc

        return pmx(p0=p0, p1=p1, c0=c[0], c1=c[1]), pmx(p0=p1, p1=p0, c0=c[0], c1=c[1])


def distinct_chars(text: str) -> list[str]:
    return list(set(text))

def bigram_probability(text: str) -> Tuple[dict[str, float], Counter[str]]:
    bigrams = Counter([text[i:i+2] for i in range(len(text)-1)])
    n = sum(bigrams.values())
    return {x: y/n for x, y in bigrams.items()}, bigrams

def p_matrix(chars: list[str], probabilities: dict[str, float]) -> np.ndarray:
    """
    Probability matrix
    """
    n = len(chars)
    p = np.zeros(shape=(n, n))
    for k, v in probabilities.items():
        p[chars.index(k[0]), chars.index(k[1])] = v
    return p

def a_matrix(chars: list[str], bigrams: Counter[str]) -> np.ndarray:
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

def d_matrix() -> np.ndarray:
    """
    Distance matrix
    """
    d = np.zeros(shape=(30, 30))
    for y in range(30):
        for x in range(30):
            px, py = x%10, x//10
            qx, qy = y%10, y//10
            d[y,x] = np.sqrt((px-qx)**2 + (py-qy)**2)
    return d/np.max(d)

def preferred_position_matrix() -> np.ndarray:
    """
    Preferred position matrix
    """
    return np.diag([2, 3, 4, 5, 1, 1, 5, 4, 3, 2,
                    6, 7, 8, 9, 2, 2, 9, 8, 7, 6,
                    2, 3, 4, 5, 1, 1, 5, 4, 3, 2]) / 9

def pi_vec(a_matrix: np.ndarray) -> np.ndarray:
    """
    Stationary probability vector
    """
    eig_val, eig_vec = np.linalg.eig(a_matrix.T)
    pi = eig_vec[:, np.isclose(eig_val, 1, atol=1e-2)]
    return np.real(pi/sum(pi)).T[0]

def pi_matrix(a_matrix: np.ndarray) -> np.ndarray:
    """
    Pi matrix
    """
    return np.diag(pi_vec(a_matrix=a_matrix))

def f_matrix() -> np.ndarray:
    """
    Same finger bigram matrix
    """
    f = np.zeros(shape=(30, 30))
    sfb = [[1, 2, 3, 4, 4, 5, 5, 6, 7, 8],
           [1, 2, 3, 4, 4, 5, 5, 6, 7, 8],
           [1, 2, 3, 4, 4, 5, 5, 6, 7, 8]]
    for y in range(30):
        for x in range(30):
            px, py = x%10, x//10
            qx, qy = y%10, y//10
            f[y,x] = sfb[py][px] == sfb[qy][qx]
    return f

def permutation_matrix(p: Permutation) -> np.ndarray:
    """
    Permutation matrix
    """
    n = len(p.permutation)
    e = np.zeros(shape=(n, n))
    for i, idx in enumerate(p.permutation):
        e[int(idx),i] = 1
    return e

if __name__ == "__main__":
    text = parse_text("./data/war_and_peace_by_tolstoy.txt")
    dc = distinct_chars(text=text)
    dc.sort()
    bp, bs = bigram_probability(text=text)
    a = a_matrix(chars=dc, bigrams=bs)

    P = p_matrix(chars=dc, probabilities=bp)
    PI = pi_matrix(a_matrix=a)
    pi = pi_vec(a_matrix=a)
    D = d_matrix()
    R = preferred_position_matrix()
    F = f_matrix()

    def cost(p: Permutation) -> float:
        w1 = 0.6 # Same finger bigram weight
        w2 = 0.3 # Distance weight
        w3 = 1.0 # Preferred position weight
        E = permutation_matrix(p=p)
        s = pi[p.permutation.astype(int)]
        return np.sum(E@P*(w1*F + w2*D) - w3*np.diag(s)*R).astype(float)

    # TODO: import layout
    network_layout = ["m", "g", "h", ":", ",", "q", "f", "s", "w", "b",
                      "n", "i", "r", "e", ".", "x", "a", "o", "u", "t",
                      "v", "p", "l", "-", "k", "y", "j", "d", "c", "z"]
    
    G = nx.from_numpy_array(P, create_using=nx.DiGraph)
    network_layout = full_layout(G, "Degree", dc) # this metric parameter should be variable

    starting_permutation = np.zeros(30)
    for i in range(len(network_layout)):
        starting_permutation[i] = dc.index(network_layout[i])

    population_size = 100
    keep_top = .1
    only_mutate = .5
    mutation_rate = .5
    plot_costs = []
    population = np.array([Permutation(permutation=starting_permutation) for _ in range(population_size)])
    for x in range(100):
        costs = np.array([cost(p) for p in population])
        # Sort
        sort = np.argsort(costs)
        population = population[sort]
        costs = costs[sort]
        # Selection probabilities
        probabilities = costs[-1] - costs
        probabilities /= sum(probabilities) + 1e-8
        # Plot
        plot_costs.append(cost(population[0]))
        plt.plot(plot_costs, c="black")
        plt.pause(.005)
        # Cross and mutate
        for i in range(int(keep_top*population_size), int(only_mutate*population_size)):
            population[i] = Permutation(np.copy(population[i-10].permutation))
            population[i].mutate()
        for i in range(int(only_mutate*population_size)+int(keep_top*population_size), population_size-1, 2):
            def sample() -> Permutation:
                r = random.random()
                j = 0
                while r > 0:
                    if j == population_size:
                        break
                    r -= probabilities[j]
                    j += 1
                return population[j-1]
            population[i], population[i+1] = Permutation.crossover(sample(), sample())
    plt.show()
    
    print(f"\nFinal cost: {plot_costs[-1]}")
    sort = np.argsort(np.array([cost(p) for p in population]))
    population = population[sort]
    permutation = population[0].permutation

    res = np.array(dc)[permutation.astype(int)]
    print()
    print(res[:10])
    print(res[10:20])
    print(res[20:])
    print()
    visualize_keyboard_seaborn(np.array([res[:10], res[10:20], res[20:]]))

    """
    E = permutation_matrix(p=Permutation())
    fig, ax = plt.subplots(nrows=3, ncols=2)
    ax[0,0].imshow(P)
    # ax[0,0].imshow(-np.log(P, where=P>0))
    ax[0,0].set_title("P")
    ax[0,1].imshow(PI)
    ax[0,1].set_title("PI")
    ax[1,0].imshow(D)
    ax[1,0].set_title("D")
    ax[1,1].imshow(R)
    ax[1,1].set_title("R")
    ax[2,0].imshow(F)
    ax[2,0].set_title("F")
    ax[2,1].imshow(E)
    ax[2,1].set_title("E")
    plt.show()

    plt.imsave("p.png", P)
    plt.imsave("pi.png", PI)
    plt.imsave("d.png", D)
    plt.imsave("r.png", R)
    plt.imsave("f.png", F)
    plt.imsave("e.png", E)
    """
