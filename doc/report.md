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
First, we gather text samples  (e.g. Wikipedia articles and programming code) and preprocess them by removing unnecessary symbols, spaces, line breaks, and tabs. This preprocessing results in a string composed solely of the 26 English alphabet letters and 4 additional symbols: period, comma, hyphen, and a punctuation mark. This gives us a total of 30 characters, suitable for our 3 x 10 ortholinear keyboard.
Next, we use this cleaned string to construct a graph, employing network analysis methods to establish the foundation of our keyboard layout. Finally, this foundational layout is subjected to a genetic algorithm to achieve full optimization.

# Evaluation



# Results



# Discussion