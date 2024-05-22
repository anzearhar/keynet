# KeyNet

Introduction to network analysis 2023/24 group project

## Reports

[Artificial intelligence](./doc/report-ai/main.pdf)

## Theory

1. Directed graph edge weights represent probability of a bigram.
   Node weights represent the probability that the key is pressed.

Design an iterative optimization algorithm

## Assumptions

- Ortholinear key layout
- 34 keys
- Symbols on another layer
- Space, backspace, enter, shift on thumbs

## Metrics

- Distance moved (per word)
- Distance from home row (0, 1, or 2)
- Single finger key presses
- Bigrams

- Position weights:\
  `1 2 2 2 1 _ 1 2 2 2 1`\
  `2 3 4 5 1 _ 1 5 4 3 2`\
  `1 2 2 2 1 _ 1 2 2 2 1`

## TODO

- Visualize the keymaps
- Display the heatmap (maybe as network and node sizes)
- Display the network with weights
- Plot sum of graph cost matrix for each iteration
- Plot of path cost of the whole text for every few iterations
