# Abstract

TODO

# Introduction

As we know, typing speed is one of the most important quality measures for every dedicated computer science engineer. A significant factor influencing typing speed is the keyboard layout used. The most popular keyboard layouts today include QWERTY, AZERTY, Dvorak, and Colemak. Of these, QWERTY remains the dominant layout, despite its origins dating back to the 1870s. While QWERTY has been incrementally improved over time, resulting in a relatively optimal layout given its historical constraints, there is potential for entirely different layouts that could significantly enhance typing speed and comfort. Moreover, the optimal keyboard layout can vary depending on the specific typing task, such as coding versus writing a novel. The layout can also vary significantly depending on the language being typed. 

To address the challenge of optimizing keyboard layouts, we employed an ortholinear keyboard. We began by utilizing network analysis to construct a weighted directed graph, where the nodes represented keys and the links represented the frequency of successive key presses. With the analysis of this graph we built the foundation for our initial layout. Subsequently, we applied genetic algorithms to refine and optimize this layout to the greatest extent possible. Although we did not have sufficient time to personally become fully proficient with the new layouts, we evaluated them using other metrics, such as the distance our fingers traveled while typing various texts.

This paper aims to optimize keyboard layouts tailored to specific types of text, including programming code, English language text, Slovenian language text, and more. Additionally, we seek to evaluate the efficiency of the layouts we developed and compare them to current popular keyboard layouts, such as QWERTY and Dvorak. By doing so, we hope to identify layouts that offer superior performance for specific tasks, ultimately enhancing typing speed and comfort for users.

# Related worka (za INA report)



# Methods

## Methods Introduction

In this section, we will detail the process of designing the keyboard layout.
First, we gather text samples  (e.g. Wikipedia articles and programming code) and preprocess them by removing unnecessary symbols, spaces, line breaks, and tabs. This preprocessing results in a string composed solely of the 26 English alphabet letters and 4 additional symbols: period, comma, hyphen, and a colon. This gives us a total of 30 characters, suitable for our 3 x 10 ortholinear keyboard.
Next, we use this cleaned string to construct a graph, employing network analysis methods to establish the foundation of our keyboard layout. Finally, this foundational layout is subjected to a genetic algorithm to achieve full optimization.

# Evaluation

We constructed our keyboard layouts using text from War and Peace (DODAJ CITAT) by Leo Tolstoy. Evaluating the effectiveness of these keyboards presents a unique challenge. One potential method of evaluation involves using the cost function described in Section 2.2 (Genetic Algorithms). However, this approach could introduce bias, as the keyboards were optimized based on this very cost function.

To avoid this bias, we decided to take a different approach. We visualized each keyboard layout with a heatmap representing the frequency of key presses. By analyzing these heatmaps, we can gain insights into the distribution of key usage and provide qualitative commentary on the efficiency and comfort of the layouts. 

# Results



# Discussion

Due to time limitations, we were able to test our keyboard layout optimizer only on the "War and Peace" novel. However, we have developed a flexible framework that allows for easy testing on various types of text (so the optimization of e.g. keyboard used for writing programing code would be effortlessly). This capability opens up the possibility for text-specific keyboard optimization, catering to different user needs.

One limitation of our current evaluation method is that we only visualizes the heatmap based on key frequency. We does not visualize the relationships between different keys, as such a visualization would be overly complex and unclear. A potential future improvement would be to develop an unbiased method for evaluating different keyboards that takes key relationships into account without compromising clarity.

Additionally, we did not have sufficient time to test the keyboards ourselves. Future work should include thorough user testing to validate the effectiveness and comfort of the optimized layouts in real-world scenarios. This will provide practical insights and further refine our optimization framework.
