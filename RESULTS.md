# Testing Data
We generated random N-move scrambles starting from the solved position and entered them into each solver.
For each value of N we took 5 samples and calculated the empirical average time to solve for each solver.

## 3-move scrambles
SAT: 0.04s
MIP: 0.56s

## 5-move scrambles
SAT: 0.38s
MIP: 1.06s

## 7-move scrambles
SAT: 0.98s
MIP: 2.38s

## 9-move scrambles
SAT: 84.14s
MIP: 44.92s