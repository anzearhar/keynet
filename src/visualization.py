import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

def visualize_keyboard(keyboard_array: np.ndarray, colors_array: np.ndarray | None = None):
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



if __name__ == "__main__":
    # For testing
    keyboard_array = np.array([['a','b','c','d','e','f','1'],
                               ['g','h','i','j','k','l','2'],
                               ['m','n','o','p','q','r','3']])
    colors_array = np.array([['red','orange','yellow','green','blue','indigo','violet'],
                             ['violet','red','orange','yellow','green','blue','indigo'],
                             ['indigo','violet','red','orange','yellow','green','blue']])
    # Keyboard with some colors
    visualize_keyboard(keyboard_array, colors_array)
    # Keyboard without colors
    visualize_keyboard(keyboard_array)