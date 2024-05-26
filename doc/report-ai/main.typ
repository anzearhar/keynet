#import "@preview/cetz:0.2.2"

#let accent_color = purple

#set document(title: "Project report", author: "Arhar, Kostanjšek, Ločičnik", date: datetime.today())
#set page(
    numbering: "1",
    header: locate(loc => {
        set text(fill: luma(120))
        if counter(page).at(loc).first() > 1 [#h(1fr)KeyNet #h(2mm) --- #h(2mm) #counter(page).display("1/1", both: true)]
        }),
    footer: [],
    header-ascent: 25%
)

#set text(font: "Source Sans Pro", weight: "light", size: 9pt)
#set par(justify: true, leading: .55em, first-line-indent: 1.8em)

#show par: set block(spacing: 0.55em)
#show heading: set block(above: 1.4em, below: .5em)
#show ref: set text(fill: accent_color)
#show footnote: set text(fill: accent_color)

#set table(stroke: none)
#set table.hline(stroke: .15mm + black)
#set table.vline(stroke: .15mm + black)
#set footnote.entry(separator: line(length: 30%, stroke: .15mm))

#align(right)[
    #set text(fill: luma(120))
    FRI Artificial intelligence course 2023\
    Project report
]

#v(1em)
#text(fill: luma(120), size: 10pt)[
    #heading()[
        #set text(weight: "regular")
        KeyNet: keyboard layout optimization using network analysis and genetic algorithms
    ]
    Anže Arhar, Kristjan Kostanjšek, and Nejc Ločičnik
]
#v(3em)

#set text(font: "New Computer Modern")
#set heading(numbering: "1.1")
// #show heading: set text(fill: luma(120), weight: "semibold")
#show heading: set block(above: 1.4em, below: .8em)
#show: columns.with(2)
#set math.mat(delim: "[")

= Introduction

As we know, typing speed is one of the most important quality measures for every dedicated computer science engineer.
A significant factor influencing typing speed is the keyboard layout used.
The most popular keyboard layouts today include QWERTY, AZERTY, Dvorak, and Colemak.
Of these, QWERTY remains the dominant layout, despite its origins dating back to the 1870s.
While QWERTY has been incrementally improved over time, resulting in a relatively optimal layout given its historical constraints, there is potential for entirely different layouts that could significantly enhance typing speed and comfort.
Moreover, the optimal keyboard layout can vary depending on the specific typing task, such as coding versus writing a novel.
The layout can also vary significantly depending on the language being typed.

To address the challenge of optimizing keyboard layouts, we employed an ortholinear keyboard.
We began by utilizing network analysis to construct a weighted directed graph, where the nodes represented keys and the links represented the frequency of successive key presses.
With the analysis of this graph we built the foundation for our initial layout.
Subsequently, we applied genetic algorithms to refine and optimize this layout to the greatest extent possible.
Although we did not have sufficient time to personally become fully proficient with the new layouts, we evaluated them using other metrics, such as the distance our fingers traveled while typing various texts.

This paper aims to optimize keyboard layouts tailored to specific types of text, including programming code, English language text, Slovenian language text, and more.
Additionally, we seek to evaluate the efficiency of the layouts we developed and compare them to current popular keyboard layouts, such as QWERTY and Dvorak.
By doing so, we hope to identify layouts that offer superior performance for specific tasks, ultimately enhancing typing speed and comfort for users.

= Methods

In this section, we will detail the process of designing the keyboard layout.
First, we gather text samples  (e.g. Wikipedia articles and programming code) and preprocess them by removing unnecessary symbols, spaces, line breaks, and tabs.
This preprocessing results in a string composed solely of the 26 English alphabet letters and 4 additional symbols: period, comma, hyphen, and a colon.
This gives us a total of 30 characters, suitable for our 3 x 10 ortholinear keyboard.
Next, we use this preprocessed text to construct a graph, employing network analysis methods to establish the foundation of our keyboard layout.
Finally, this foundational layout is subjected to a genetic algorithm to achieve full optimization.

== Network analysis

#text(fill: accent_color)[TODO]

== Genetic algorithms <genetic>

As key layout optimization is a permutation problem, we decided to optimize our layout using a genetic algorithm.
By defining the problem in this way, we can easily design a cost function that is defined only using matrix operations.
This allows us to speed up the computations significantly, resulting in better layout designs.

Each gene in the population is represented as a permutation.
Our goal is to find the optimal permutation of keys that minimizes the cost function $c$.
In this section, the function $"diag"$ refers to creating a diagonal matrix from a vector $v in bb(R)^n$:
$
"diag"(v) = D in bb(R)^(n times n), "where" D_(i,j) = cases(
    v_i"," & i = j,
    0"," & "otherwise"
)
$
We define the cost function $c$ using the following matrices:

- Probability matrix $P$ contains the bigram probabilities

$
P_(i,j) = p_(i,j)
$

- Markov chain transposition matrix $A$ of the network is used to calculate the stationary probability vector $pi$

$
pi A = pi
$

- Preferred position matrix $R$ is a diagonal matrix of key importances

$
R = "diag"("vec"(mat(2, 3, 4, 5, 1, 1, 5, 4, 3, 2;
                     6, 7, 8, 9, 2, 2, 9, 8, 7, 6;
                     2, 3, 4, 5, 1, 1, 5, 4, 3, 2)^T))
$

- Distance matrix $D$ contains the physical distances between the keys

$
D_(i,j) = sqrt((x_i - x_j)^2 + (y_i - y_j)^2)
$

- Same finger bigram matrix $F$ groups keys assigned to the same finger

$
g = "vec"(mat(1, 2, 3, 4, 4, 5, 5, 6, 7, 8;
              1, 2, 3, 4, 4, 5, 5, 6, 7, 8;
              1, 2, 3, 4, 4, 5, 5, 6, 7, 8)^T)\
F_(i,j) = cases(
    1"," & g_i = g_j,
    0"," & "otherwise"
)
$

Cost $c$ is defined using a weighted sum of the permuted matrices which is finally element-wise summed into a single number

$
C(E) = E P dot.circle (w_1 F + w_2 D) - w_3"diag"(E pi)R\
c = sum_i sum_j C_(i,j)
$

Using a weighted sum allows us to assign more weight to some scores and less to other.
All of the aforementioned matrices are displayed in @matrices.

#let img_width = 25mm
#figure(
    caption: [Matrices visualized],
    grid(
        columns: 3,
        row-gutter: (1mm, 3mm, 1mm, 3mm),
        gutter: .4mm,
        image("./img/p.png", width: img_width),
        image("./img/pi.png", width: img_width),
        image("./img/d.png", width: img_width),
        [$P$], [$"diag"(pi)$], [$D$],
        image("./img/r.png", width: img_width),
        image("./img/f.png", width: img_width),
        image("./img/e.png", width: img_width),
        [$R$], [$F$], [$E$]
    )
)<matrices>

In each generation we keep the 10 % of the previous population with the lowest cost.
Next 50 % of the genes according to their cost are only mutated.
Mutations are represented using a random swap of two elements.
Other 40 % of genes are a recombination of all genes from the previous population.
This is achieved using the partially mapped crossover (PMX) algorithm, which swaps parts of two permutations in a way that keeps a part of the original permutation.
Candidates for recombination are selected according to their cost - lower cost has a higher probability of being selected and higher cost has a lower probability of being selected.
The mutation and crossover procedure operate only inclusively on homerow keys or other keys.
This limtation is added to keep similar structure to the layout designed using network analysis.

== Evaluation

We constructed our keyboard layouts using text from War and Peace @tolstoy_war by Leo Tolstoy.
Evaluating the effectiveness of these keyboards presents a unique challenge.
One potential method of evaluation involves using the cost function described in @genetic.
However, this approach could introduce bias, as the keyboards were optimized based on this very cost function.

To avoid this bias, we decided to take a different approach.
We visualized each keyboard layout with a heatmap representing the frequency of key presses.
By analyzing these heatmaps, we can gain insights into the distribution of key usage and provide qualitative commentary on the efficiency and comfort of the layouts.

= Results

#text(fill: accent_color)[TODO]

#let img_width = 95%
#figure(
    caption: [Keyboard layouts visualized using a heatmap],
    grid(
        columns: 1,
        row-gutter: (1mm, 3mm, 1mm, 3mm),
        gutter: .4mm,
        image("./img/qwerty.png", width: img_width),
        [QWERTY],
        image("./img/dvorak.png", width: img_width),
        [Dvorak],
        image("./img/degree.png", width: img_width),
        [Ours (degree centrality)],
        image("./img/genetic.png", width: img_width),
        [Ours (genetic algorithms)],
    )
)


= Discussion

Because of time limitations we managed to test it only on the War and Peace novel, but we've developed a framework where we could easily test it on different types of text as well (e.g. programming code).

#bibliography("refs.yml")
