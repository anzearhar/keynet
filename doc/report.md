# Abstract

In our report we introduce a novel approach to keyboard layout optimization using network analysis and genetic algorithms. We constructed a weighted directed graph based on text samples and used centrality measures to create a baseline layout. This initial layout was then optimized with genetic algorithms. Evaluations, visualized through heatmaps, highlight the efficiency of our layouts compared to traditional ones like QWERTY and Dvorak. While limited to the text of "War and Peace," our framework is adaptable to various text types, offering potential for task-specific optimization. Future work will focus on unbiased evaluation methods and user testing to validate real-world effectiveness.

# Introduction

As we know, typing speed is one of the most important quality measures for every dedicated computer science engineer. A significant factor influencing typing speed is the keyboard layout used. The most popular keyboard layouts today include QWERTY, AZERTY, Dvorak, and Colemak. Of these, QWERTY remains the dominant layout, despite its origins dating back to the 1870s. While QWERTY has been incrementally improved over time, resulting in a relatively optimal layout given its historical constraints, there is potential for entirely different layouts that could significantly enhance typing speed and comfort. Moreover, the optimal keyboard layout can vary depending on the specific typing task, such as coding versus writing a novel. The layout can also vary significantly depending on the language being typed. 

To address the challenge of optimizing keyboard layouts, we employed an ortholinear keyboard. We began by utilizing network analysis to construct a weighted directed graph, where the nodes represented keys and the links represented the frequency of successive key presses. With the analysis of this graph we built the foundation for our initial layout. Subsequently, we applied genetic algorithms to refine and optimize this layout to the greatest extent possible. Although we did not have sufficient time to personally become fully proficient with the new layouts, we evaluated them using other metrics, such as the distance our fingers traveled while typing various texts.

This paper aims to optimize keyboard layouts tailored to specific types of text, including programming code, English language text, Slovenian language text, and more. Additionally, we seek to evaluate the efficiency of the layouts we developed and compare them to current popular keyboard layouts, such as QWERTY and Dvorak. By doing so, we hope to identify layouts that offer superior performance for specific tasks, ultimately enhancing typing speed and comfort for users.





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



# Related work 

Keyboard layout optimization is a popular problem with no unique solution. Most approaches utilize genetic algorithms or a combination of genetic algorithms and deep learning to tackle this issue. Notable examples include works by Švigelj \cite{svigelj2019}, Nivasch & Azaria \cite{NiAz2021, NiAz2023}, Onsorodi & Korhan \cite{onsorodi2020}, and Khan & Deb \cite{KhDe2023}. Additionally, two articles specifically focus on optimizing keyboard layouts based on the language being typed: Pacheco et al. \cite{eniac} and Liao & Choe \cite{ChCh2013}.

Genetic algorithms are particularly well-suited for this problem, which is why we partially incorporated them in our approach. However, we found few articles leveraging network analysis for keyboard layout optimization. Despite this, we believe network analysis can effectively establish a solid foundation for layout design.

# Related work (shortened version - ce bo predolgo vse skupaj)

Keyboard layout optimization is a popular problem with no unique solution. Most approaches use genetic algorithms or a combination of genetic algorithms and deep learning, as seen in works by Švigelj \cite{svigelj2019}, Nivasch & Azaria \cite{NiAz2021, NiAz2023}, Onsorodi & Korhan \cite{onsorodi2020}, and Khan & Deb \cite{KhDe2023}. Some focus on language-specific layouts, such as Pacheco et al. \cite{eniac} and Liao & Choe \cite{ChCh2013}.

Genetic algorithms are well-suited for this problem, which is why we used them partially. Few articles leverage network analysis for keyboard optimization, but we believe it can effectively establish a solid layout foundation.

# Related work bibliography

@phdthesis{svigelj2019, 
title={Optimizacija razporeditve tipk tipkovnice za pisanje slovenskega besedila}, 
url={https://repozitorij.uni-lj.si/IzpisGradiva.php?lang=eng&id=110203}, 
author={Švigelj, Mihael}, 
year={2019}}

@INPROCEEDINGS{NiAz2021,
author={Nivasch, Keren and Azaria, Amos},
booktitle={2021 IEEE 33rd International Conference on Tools with Artificial Intelligence (ICTAI)}, 
title={A Deep Genetic Method for Keyboard Layout Optimization}, 
year={2021},
pages={435-441},
doi={10.1109/ICTAI52525.2021.00070}}

@article{NiAz2023,
title={Keyboard Layout Optimization and Adaptation},
author={Nivasch, Keren and Azaria, Amos},
journal={International Journal on Artificial Intelligence Tools},
volume={32},
number={05},
pages={2360002},
year={2023},
publisher={World Scientific Publishing Company}
}

@article{onsorodi2020,
title={Application of a genetic algorithm to the keyboard layout problem},
author={Onsorodi, Amir Hosein Habibi and Korhan, Orhan},
journal={PloS one},
volume={15},
number={1},
pages={e0226611},
year={2020},
publisher={Public Library of Science San Francisco, CA USA}
}

@inproceedings{KhDe2023,
author = {Khan, Ahmer and Deb, Kalyanmoy},
title = {Optimizing Keyboard Configuration Using Single and Multi-Objective Evolutionary Algorithms},
year = {2023},
isbn = {9798400701207},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3583133.3590580},
doi = {10.1145/3583133.3590580},
booktitle = {Proceedings of the Companion Conference on Genetic and Evolutionary Computation},
pages = {219–222},
numpages = {4},
keywords = {combinatorial optimization, keyboard layout, multi-objective optimization},
location = {Lisbon, Portugal},
series = {GECCO '23 Companion}
}

@inproceedings{eniac,
 author = {Gustavo Pacheco and Eduardo Palmeira and Keiji Yamanaka},
 title = { Using Genetic Algorithms to Design an Optimized Keyboard Layout for Brazilian Portuguese},
 booktitle = {Anais do XVII Encontro Nacional de Inteligência Artificial e Computacional},
 location = {Evento Online},
 year = {2020},
 keywords = {},
 issn = {2763-9061},
 pages = {437--448},
 publisher = {SBC},
 address = {Porto Alegre, RS, Brasil},
 doi = {10.5753/eniac.2020.12149},
 url = {https://sol.sbc.org.br/index.php/eniac/article/view/12149}
}

@article{ChCh2013,
author = {Chen Liao and Pilsung Choe},
title = {Chinese Keyboard Layout Design Based on Polyphone Disambiguation and a Genetic Algorithm},
journal = {International Journal of Human–Computer Interaction},
volume = {29},
number = {6},
pages = {391--403},
year = {2013},
publisher = {Taylor \& Francis},
doi = {10.1080/10447318.2013.777827},
}


