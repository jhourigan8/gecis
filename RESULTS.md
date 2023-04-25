# Testing Data
We generated random N-move scrambles starting from the solved position and entered them into each solver.
For each value of N we took 5 samples and calculated the empirical average time to solve for each solver.

- 3-move scrambles
    SAT: 0.04s
    MIP: 0.56s

- 5-move scrambles
    SAT: 0.38s
    MIP: 1.06s

- 7-move scrambles
    SAT: 0.98s
    MIP: 2.38s

- 9-move scrambles
    SAT: 84.14s
    MIP: 44.92s

# Conclusions
The data shows that our SAT solver is significantly faster on smaller instances but loses its advantage as the solution size grows.
There are a number of reasons which might cause this trend.
- First, our MIP solver may have greater overhead than our SAT solver due to the greater general complexity of MIP problems.
This would cause our MIP solver to be much slower on simple instances but have less of an effect on large instances.
- Second, our MIP solver may perform better than SAT on large instances due to the greater number of variables in our SAT formulae.
While MIP uses on variable to represent the color of square i at time t, SAT has to use 6 0/1 variables for each square and time to represent whether or not that square is each particular color c.
- Finally, our MIP solver may perform better than SAT since the paper we initially based our solvers off of was originally implemented in MIP.
For consistency, we implemented the same solver in both MIP and SAT.
It may be the case that different implementation choices would benefit SAT.
