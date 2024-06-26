import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import seaborn as sns
from text_parser import parse_text

def get_heat(keyboard_array: np.ndarray, text_path : str):
    heat = np.zeros_like(keyboard_array, dtype=float)
    parsed_text = parse_text(text_path)
    # create dictionary for chars and their positions in the keyboard
    char_to_position = {}
    for i, row in enumerate(keyboard_array):
        for j, char in enumerate(row):
            char_to_position[char] = (i,j)
    # go through every char in text and increase their heat
    for char in parsed_text:
        if char in char_to_position:
            pos = char_to_position[char]
            heat[pos[0], pos[1]] += 1
    # normalize the array
    heat = (heat - np.min(heat)) / (np.max(heat) - np.min(heat))
    return heat

def visualize_keyboard_seaborn(keyboard_array: np.ndarray, text_path : str | None = "./data/war_and_peace_by_tolstoy.txt", heat: np.ndarray | None = None, store = False, store_name = "keyboard_visualization"):
    """
    Visualize keyboard with seaborn.
    Pass the keys as keyboard_array.
    Pass the path of the text as text_path (for computing the heat map, default is War and Peace).
    (Optionally) Pass the heat values as heat array.
    (Optionally) Set store to True, to store the plot.
    (Optionally) Set store name to whatever you want the plot to be stored as.
    """
    ccbar = True
    if heat is None:
        if store_name is None:
            heat = np.zeros_like(keyboard_array, dtype=float)
            ccbar = False
        else:
            heat = get_heat(keyboard_array, text_path)
    plt.figure(figsize=(10, 3)) 
    sns.heatmap(
        heat,
        annot=keyboard_array,
        fmt="",
        cmap="viridis", # "coolwarm",
        # cbar=ccbar,
        cbar=False,
        # linewidths=1,
        # linecolor="black"
    )
    plt.axis("off")
    if store:
        plt.savefig(store_name+".pdf", format="pdf", bbox_inches="tight")
        # plt.savefig(store_name+".png", format="png", bbox_inches="tight")
    else:
        plt.show()

if __name__ == "__main__":
    # Seaborn

    # qwerty
    keyboard_array = np.array([["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
                               ["a", "s", "d", "f", "g", "h", "j", "k", "l", "-"],
                               ["z", "x", "c", "v", "b", "n", "m", ",", ".", ":"]])
    # dvorak
    keyboard_array = np.array([["-", ",", ".", "p", "y", "f", "g", "c", "r", "l"],
                               ["a", "o", "e", "u", "i", "d", "h", "t", "n", "s"],
                               [":", "q", "j", "k", "x", "b", "m", "w", "v", "z"]])
    # degree centrality
    keyboard_array = np.array([["g", "p", "d", "u", "j", "z", "s", ".", "m", ","],
                               ["r", "i", "o", "e", "-", "k", "t", "a", "n", "h"],
                               ["x", "v", "l", "w", "q", ":", "c", "f", "y", "b"]])
    # eigenvector centrality
    keyboard_array = np.array([["g", "v", "d", "u", "j", "z", "s", "m", ".", ","],
                               ["i", "r", "o", "e", "-", "k", "t", "n", "a", "h"],
                               ["x", "p", "l", "w", "q", ":", "c", "y", "f", "b"]])
    # betweenness centrality
    keyboard_array = np.array([["g", "w", "d", "i", "j", ":", "h", "c", "y", ","],
                               ["o", "r", "u", "e", "q", "k", "a", "t", "s", "n"],
                               ["x", "v", "l", "p", "-", "z", ".", "m", "f", "b"]])
    # closeness centrality
    keyboard_array = np.array([["g", "p", "d", "u", "j", ":", "t", "h", "c", ","],
                               ["r", "i", "o", "e", "-", "k", "a", "n", "s", "y"],
                               ["x", "v", "l", "w", "q", "z", ".", "m", "b", "f"]])
    # pagerank
    keyboard_array = np.array([["q", "p", "l", "e", "x", "b", "n", ":", "s", "c"],
                               ["o", "i", "r", "u", "-", "y", ",", "a", "k", "."],
                               ["v", "g", "w", "d", "j", "f", "t", "z", "h", "m"]])
    # average
    keyboard_array = np.array([["g", "v", "d", "u", "j", ":", "h", "m", "c", "y"],
                               ["i", "r", "o", "e", "-", "b", "a", "n", "t", "s"],
                               ["x", "p", "l", "w", "q", "z", ".", ",", "k", "f"]])
    # genetic
    keyboard_array = np.array([[",", "y", "g", "r", "q", "x", "c", "m", "u", "v"],
                               ["i", "n", "a", "e", "j", "z", "t", "h", "o", "s"],
                               [".", "p", "b", "d", "-", "k", "l", "w", "f", ":"]])
    #heat = np.random.rand(*keyboard_array.shape)
    visualize_keyboard_seaborn(keyboard_array, store=True)
