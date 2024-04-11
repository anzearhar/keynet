#import "@preview/fletcher:0.4.3" as fletcher: diagram, node, edge

#set page(width: 10cm, height: auto)

#set math.mat(delim: "[")
#set math.vec(delim: "[")

#let spread = .9
#let l = calc.sqrt(3) * spread
#let bend = 10deg
#let accent_color = purple

#align(center)[#text(fill: accent_color)[`BANANA`]]

Bigram counts

#align(center)[
    #diagram(
        node-stroke: .1em,
        spacing: 3em,

        node((0, 0), [B], radius: 1.2em, fill: accent_color),
        node((-spread, l), [A], radius: 1.2em, fill: accent_color),
        node((spread, l), [N], radius: 1.2em, fill: accent_color),

        edge((0, 0), (0, 0), [0], "-|>", bend: 135deg),
        edge((-spread, l), (-spread, l), [0], "-|>", bend: 135deg),
        edge((spread, l), (spread, l), [0], "-|>", bend: 135deg),

        edge((0, 0), (-spread, l), [1], "-|>", bend: bend),
        edge((-spread, l), (0, 0), [0], "-|>", bend: bend),

        edge((0, 0), (spread, l), [0], "-|>", bend: bend),
        edge((spread, l), (0, 0), [0], "-|>", bend: bend),

        edge((spread, l), (-spread, l), [2], "-|>", bend: bend),
        edge((-spread, l), (spread, l), [2], "-|>", bend: bend)
    )
]

Character map

$
["A ", "B ", "N "]
$

Probability matrix (global probabilities)

$
P = mat(0, 1/5, 2/5; 0, 0, 0; 2/5, 0, 0)
$

Markov chain transposition matrix (local outgoing edge probabilities)

$
A = mat(0, 1, 1; 0, 0, 0; 1, 0, 0)
$

Stationary probability vector (key importance)

$
pi A &= pi\
A^T pi^T &= pi^T "(eigenvalue " lambda "= 1)"\
pi &= mat(0.5, 0, 0.5)
$

Preferred position matrix (e.g. B and N are on the home row)

#align(center)[
    #grid(columns: 2,
          square(size: 1.5em, fill: accent_color, stroke: black, radius: .25em)[A],
          [],
          square(size: 1.5em, fill: accent_color, stroke: black, radius: .25em)[B],
          square(size: 1.5em, fill: accent_color, stroke: black, radius:.25em)[N])
]

$
R = mat(1, 0, 0; 0, 2, 0; 0, 0, 2)
$

Distance matrix (distance can be non-metric; must be positive, symmetric, $d_(i, i)=0$)

$
D = mat(0, 1, sqrt(2); 1, 0, 1; sqrt(2), 1, 0)
$

Same finger bigram matrix (e.g. left index finger is assigned to A and B)

$
F = mat(0, 1, 0; 1, 0, 0; 0, 0, 0)
$

Other matrices

#align(center)[#math.dots.v]

Permutation matrix (we need to find the optimal permutation)

$
E = mat(1, 0, 0; 0, 0, 1; 0, 1, 0)
$

Final cost $c$ ($C$ is a weighted sum of normalized matrices multiplied with probabilities) ... only some matrices are permuted with $E$

$
c = min_E sum_i sum_j C_(i,j)\
C(E) = E P dot.circle (w_1 F + w_2 (E pi) R + w_3 E D + ...)\
pi <- op("diag")(pi)\
w " " ... "weight vector"
$
