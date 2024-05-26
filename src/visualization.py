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
        cmap="Blues", # "coolwarm",
        cbar=ccbar,
        linewidths=1,
        linecolor="black"
    )
    plt.axis("off")
    if store:
        plt.savefig(store_name+".pdf", format="pdf", bbox_inches="tight")
    else:
        plt.show()

if __name__ == "__main__":
    # Seaborn
    keyboard_array = np.array([["q","w","e","r","t","z","u","i","o","p"],
                               ["a","s","d","f","g","h","j","k","l","-"],
                               ["y","x","c","v","b","n","m",",",".",":"]])
    #heat = np.random.rand(*keyboard_array.shape)
    visualize_keyboard_seaborn(keyboard_array)
