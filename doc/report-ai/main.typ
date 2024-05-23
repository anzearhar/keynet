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

// #set text(font: "New Computer Modern")
#set heading(numbering: "1.1")
#show heading: set text(fill: luma(120), weight: "semibold")
#show heading: set block(above: 1.4em, below: .8em)
#show: columns.with(2)
#set math.mat(delim: "[")

= Introduction

#lorem(100)

= Methods

#lorem(50)

== Network analysis

#lorem(220)

== Genetic algorithms

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

#lorem(200)

= Results

#lorem(200)

= Discussion

#lorem(100)

#bibliography("refs.yml")
