import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import seaborn as sns


def visualize_keyboard_old_school(keyboard_array: np.ndarray, colors_array: np.ndarray | None = None):
    """
    Visualize the keyboard.
    The keyboard keys should be passed as a 2D numpy array.
    Optionally the colors_array includes the color for each key on a visualized keyboard.
    """
    rows, cols = keyboard_array.shape
    if colors_array is None:
        colors_array = np.full((rows, cols), 'white', dtype=object)
    _, ax = plt.subplots()

    for i in range(rows):
        for j in range(cols):
            color = colors_array[i,j]
            rect = patches.Rectangle((j - 0.5, i - 0.5), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
            ax.add_patch(rect)

    ax.set_xticks(np.arange(cols), minor=False)
    ax.set_yticks(np.arange(rows), minor=False)
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
    ax.grid(which='major', color='none')
    ax.tick_params(which="major", bottom=False, left=False, labelbottom=False, labelleft=False)
    for i in range(rows):
        for j in range(cols):
            ax.text(j, i, keyboard_array[i, j], ha='center', va='center', fontsize=20)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, cols - 0.5)
    ax.set_ylim(rows - 0.5, -0.5)
    plt.show()


def visualize_keyboard_seaborn(keyboard_array: np.ndarray, heat: np.ndarray | None = None, store = False, store_name = "keyboard_visualization"):
    """
    Visualize keyboard with seaborn.
    Pass the keys as keyboard_array.
    Pass the heat values as heat array.
    Optionally set store to True, to store the plot.
    Optionally set store name to whatever you want the plot to be stored as.
    """
    ccbar = True
    if heat is None:
        heat = np.zeros_like(keyboard_array, dtype=float)
        ccbar = False
    plt.figure(figsize=(10, 3)) 
    sns.heatmap(
        heat,
        annot=keyboard_array,
        fmt='',
        cmap='Blues', # 'coolwarm',
        cbar=ccbar,
        linewidths=1, 
        linecolor='black'
    )
    plt.axis('off')
    if store:
        plt.savefig(store_name+".pdf", format="pdf", bbox_inches="tight")
    else:
        plt.show()


if __name__ == "__main__":
    # Matplotlib
    keyboard_array = np.array([['q','w','e','r','t','z','u','i','o','p'],
                               ['a','s','d','f','g','h','j','k','l','-'],
                               ['y','x','c','v','b','n','m',',','.','\'']])
    colors_array = np.array([['red','orangered','orange','yellow','greenyellow','mediumseagreen','blue','indigo','purple','mediumorchid'],
                             ['red','orangered','orange','yellow','greenyellow','mediumseagreen','blue','indigo','purple','mediumorchid'],
                             ['red','orangered','orange','yellow','greenyellow','mediumseagreen','blue','indigo','purple','mediumorchid']])
    # Keyboard with some colors
    #visualize_keyboard_old_school(keyboard_array, colors_array)
    # Keyboard without colors
    #visualize_keyboard_old_school(keyboard_array)

    # Seaborn
    heat = np.random.rand(*keyboard_array.shape)
    visualize_keyboard_seaborn(keyboard_array, heat)