from net_metrics import construct_dataframe, sort_by_column
from test import distinct_chars, bigram_probability, pi_vec, p_matrix, a_matrix
from visualization import visualize_keyboard_seaborn
import pandas as pd
import numpy as np
import networkx as nx
import text_parser as tp
import random
from typing import Literal, TypeAlias
import argparse
import matplotlib.pyplot as plt

Metric: TypeAlias = Literal['Average', 'Degree', 'Eigenvector', 'Betweenness', 'Closeness', 'PageRank']

def swap(l1, l2, i1, i2):
    tmp = l1[i1]
    l1[i1] = l2[i2]
    l2[i2] = tmp

def sum_between(G : nx.DiGraph, t1 : list, t2 : list) -> float:
    """
    Check edge weight sum between 2 subgraphs. Nodes of each subgraph are listed in t1 and t2.
    """
    return sum([G.get_edge_data(u, v)['weight'] for u, v in G.edges if ((u in t1 and v in t2) or (u in t2 and v in t1))])

def sum_within(G : nx.DiGraph, t : list) -> float:
    """
    Check edge weight sum within a subgraph. Nodes of the subgraph are listed in t.
    """
    s = G.subgraph(t)
    return np.sum([G.get_edge_data(u, v)['weight'] for u, v in s.edges()])

def split_graph(G : nx.DiGraph, df: pd.DataFrame) -> tuple[list, list]:
    """
    Split the graph on 2 subgraphs so that they are balanced in the weight they hold. 
    Each subgraphs internal edges should hold ~0.25 of the weights , and the edges between them should hold ~0.5.
    """
    s_data = sort_by_column(df, 'Degree')
    order = list(s_data.index)
    t1 =[order[i] for i in range(len(order)) if i % 2 == 0]
    t2 = [order[i] for i in range(len(order)) if i % 2 == 1]

    for _ in range(1000):
        w1 = sum_within(G, t1) # weights in subgraph 1
        w2 = sum_within(G, t2) # weights in subgraph 2
        diff = abs(w1-w2) # difference in weights between subgraphs
        if diff < 0.0001: # end early if difference is small enough
            break
        r1 = random.randint(1, len(t1)-1) # randomly select a node from subgraph 1
        r2 = random.randint(1, len(t1)-1) # randomly select a node from subgraph 2
        swap(t1, t2, r1, r2) # swap randomly selected nodes
        w1 = sum_within(G, t1) # recalculate weight sum in subgraph 1
        w2 = sum_within(G, t2) # recalculate weight sum in subgraph 2
        if diff < abs(w1-w2): # if the balance improved keep the change, otherwise swap back
            swap(t1, t2, r1, r2) # swap back

    return t1, t2 # return the nodes of each subgraph

def visualize_split(G : nx.DiGraph, pi : list, dc : list, t1 : list, t2 : list):
    color_map = []
    for node in G:
        if node in t1:
            color_map.append('#404788')
        elif node in t2:
            color_map.append('#6dcd59')
        else:
            color_map.append('grey')

    # Get all edge weights
    weights = np.array([d['weight'] for u, v, d in G.edges(data=True)])

    # Min-max normalization
    min_weight = weights.min()+0.001
    max_weight = weights.max()
    normalized_weights = (weights - min_weight) / (max_weight - min_weight)

    # Create a dictionary of normalized weights for easy lookup
    normalized_weights_dict = {(u, v): (w - min_weight) / (max_weight - min_weight) for u, v, w in G.edges(data='weight')}

    # Draw the graph
    pos = nx.circular_layout(G)  # You can use any layout you prefer
    dt = pd.DataFrame()
    dt['size'] = pi
    dt['col'] = [0 if c=='#404788' else 1 for c in color_map]
    dt = dt.sort_values(by=['col', 'size'])
    #dt = dt.sort_values(by='col')
    dt['pos'] = list(pos.values())
    #dt.loc[dt['col']=='red', 'pos'] = list(pos.values())[15:]
    pos = dt.sort_index()['pos'].to_dict()

    plt.figure(figsize=(6, 6))
    edges = [(u, v, (w - min_weight) / (max_weight - min_weight)) for u, v, w in G.edges(data='weight')]
    edges.sort(key=lambda x: x[2])
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=pi*10000, node_color=color_map, alpha=0.75, edgecolors="white")

    # Draw edges with color intensity based on normalized weights
    for (u, v, d) in edges:
        weight = normalized_weights_dict[(u, v)]
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], width=1, connectionstyle="arc3,rad=0.3", edge_color=plt.cm.Greys(weight))

    # Draw labels
    nx.draw_networkx_labels(G, pos, labels={i: x for i, x in enumerate(dc)})
    plt.axis("off")
    plt.savefig("net.pdf", format="pdf", bbox_inches="tight")
    # plt.show()

def check_balance(G : nx.DiGraph, t1 : list, t2 : list):
    """
    Prints out the weight sum of each subgraphs internal edges (~0.25), 
    weight sum between subgraphs (~0.5) and a total weight sum (1).
    """
    w1 = sum_within(G, t1)
    w2 = sum_within(G, t2)
    w3 = sum_between(G, t1, t2)
    sum_w = w1+w2+w3
    print(f"T1 holds: {round(w1, 3)}, T2 holds: {round(w2, 3)}, edges between hold: {round(w3, 3)}, sums to: {round(sum_w, 3)}")

def get_target_avoids(pos : tuple, key_array : np.array) -> tuple[list, list]:
    """
    Based on input pos determine the location of the avoid node (the node right below this position) and
    the locations of the target (other) nodes in the home row.
    """
    _, l = key_array.shape
    target_nodes = [int(key_array[pos[0]+1, i]) for i in range(l-1) if i != pos[1]]

    avoid_node = [int(key_array[pos[0]+1, pos[1]])]

    return target_nodes, avoid_node

def calculate_score(G : nx.DiGraph, candidates : list, target_nodes : list, avoid_node : list) -> dict:
    """
    Calculate the ranking of the available nodes (candidates), based on the target and avoid nodes.
    """
    scores = {}
    for letter in candidates:
        to_targets = sum(G[letter][node]['weight'] for node in target_nodes if G.has_edge(letter, node))
        from_targets = sum(G[node][letter]['weight'] for node in target_nodes if G.has_edge(node, letter))
        to_avoid = sum(G[letter][avoid_node]['weight'] for avoid_node in avoid_node if G.has_edge(letter, avoid_node))
        from_avoid = sum(G[avoid_node][letter]['weight'] for avoid_node in avoid_node if G.has_edge(avoid_node, letter))

        score = (to_targets + from_targets) - (to_avoid + from_avoid)
        scores[letter] = score

    scores = sorted(scores, key= lambda k: scores.get(k), reverse=True)
    return scores

def place_important(key_array : np.array, subgraph_nodes : list, placed : set) -> None:
    """
    Places the most important keys into the homerow in the following order: index, middle, ring, little finger.
    Index finger having the most important key (obviously).
    """
    # fill in the fixed positions based on the choosen node importance metric
    prio = [(1, 3), (1, 2), (1, 1), (1, 0)]
    for i in range(4):
        x, y = prio[i]
        node = subgraph_nodes[i]
        placed.add(node)
        key_array[x, y] = node

def place_adjacent_important(G : nx.DiGraph, key_array : np.array, subgraph_nodes : list, placed : set) -> None:
    """
    Places the 8 keys with adjacent importance. Keys are placed in order of finger dexterity (index, middle, ring, little).
    Top row is placed first, then the bottom row (for each finger).
    This is based on score: weights to the rest of the homerow - weights of the key right below
    """
    # fill in positions above and below the fixed positions, based on edge weights score
    positions = [(0, 3), (0, 2), (0, 1), (0, 0)]
    for position in positions:
        positives, negatives = get_target_avoids(position, key_array)
        candidates = [node for node in subgraph_nodes if node not in placed]
        scores = calculate_score(G.subgraph(subgraph_nodes), candidates, positives, negatives)

        # check relations to other keys on homerow, and avoid the key right bellow
        # add first options on this scoring to the top row (top row has higher prio)
        placed.add(scores[0])
        key_array[position[0], position[1]] = scores[0]

        # add the second option of this scoring to the bottom row
        placed.add(scores[1])
        key_array[position[0]+2, position[1]] = scores[1]

def place_least_important(G : nx.DiGraph, key_array : np.array, subgraph_nodes : list, placed : set) -> None:
    """
    Places the 3 least important keys, first the one in the homerow (center), then the one above and lastly the one below.
    Order is ranked by score: rest of keyboard weight - weight of keys on index finger.
    """
    # home row center, check high relation to the rest of the keyboard, as little relation
    # as possible to the index line
    positions = [(1, 4), (0, 4), (2, 4)] # middle, up, down order
    negatives = [int(key_array[0, 3]), int(key_array[1, 3]), int(key_array[2, 3])]
    positives = [node for node in subgraph_nodes if node not in negatives and node in placed]
    candidates = [node for node in subgraph_nodes if node not in placed]
    scores = calculate_score(G.subgraph(subgraph_nodes), candidates, positives, negatives)
    #nodes = sorted(scores, key= lambda k: scores.get(k), reverse=True)
    for i in range(3):
        x, y = positions[i]
        node = scores[i]
        placed.add(node)
        key_array[x, y] = node

def determine_key_layout(G : nx.DiGraph, subgraph_nodes : list) -> np.array:
    """
    Fills out a half of the keyboard layout (for a single hand). First places the homerow, 
    then the adjacent important keys and finally whatever is left.
    """
    shape = (3, 5)

    key_array = np.full(shape, -1) 
    placed = set()

    place_important(key_array, subgraph_nodes, placed)
    place_adjacent_important(G, key_array, subgraph_nodes, placed)
    place_least_important(G, key_array, subgraph_nodes, placed)

    return key_array

def place_labels(key_array, labels):
    return np.vectorize(labels.get)(key_array)

def full_layout(G : nx.DiGraph, metric : Metric, dc : list, pi : list) -> np.array:
    """
    Creates a layout for each hand (half of the keyboard) before joining them into a full keyboard layout.
    """

    # check centrality measures, save to pandas dataframe
    data = construct_dataframe(G, dc)

    # split the graph on 2 subgraphs (balanced by amount of weight they hold)
    t1, t2 = split_graph(G, data)
    visualize_split(G, pi, dc, t1, t2)

    left = data.loc[t1]
    left = sort_by_column(left, metric)
    nodes = list(left.index)
    key_array1 = determine_key_layout(G, nodes)

    right = data.loc[t2]
    right = sort_by_column(right, metric)
    nodes = list(right.index)
    key_array2 = determine_key_layout(G, nodes)

    layout = np.concatenate((key_array1, np.fliplr(key_array2)), axis=1)
    labels={i: x for i, x in enumerate(dc)}
    layout = place_labels(layout, labels)

    return layout.flatten()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='SiamFC Runner Script')

    parser.add_argument("--metric", 
                        help="Choosen centrality measure.", 
                        required=False, 
                        action='store', 
                        default="Degree")

    args = parser.parse_args()
    metric = args.metric

    # build directional graph based on choosen text
    seq = tp.parse_text("./data/war_and_peace_by_tolstoy.txt", )
    seq = seq[seq.find("well,prince")-9:]
    text = seq
    dc = distinct_chars(text=text)
    bp, bs = bigram_probability(text=text)

    p = p_matrix(chars=dc, probabilities=bp)
    a = a_matrix(chars=dc, bigrams=bs)
    pi = pi_vec(a_matrix=a)

    print("Keys ordered by pi:")
    print(np.flip(np.array(dc)[pi.argsort()]))

    G = nx.from_numpy_array(p, create_using=nx.DiGraph)
    print(f"Weights sum to: {sum([G[i][j]['weight'] for i, j in G.edges()])}")
    print(f"Number of letters: {len(G)}")

    # build keyboard layout (based on the split)
    keyboard = full_layout(G, metric, dc, pi)

    print()
    print(keyboard[:10])
    print(keyboard[10:20])
    print(keyboard[20:])
    # visualize keyboard
    visualize_keyboard_seaborn(np.array([keyboard[:10], keyboard[10:20], keyboard[20:]]))
