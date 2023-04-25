# Overview
Our PennCube project consists of an app and a solver.
TODO: explain each file

## App
Our app shows a realistic 3D-rendered Rubik's cube which can be controlled via the mouse.
At any point the user can click the `solve` button to have our solver solve the cube.
The user can select either the `MIP` or `SAT` solver using the buttons on the bottom. 
While the solver is running a timer shows the amount of time elapsed.
Once an optimal solution has been found the app animates the solution on the cube.

The frontend for our app consists of `app/index.html`, `app/style.css`, and `app/app.js`.
The original Rubik's cube animation code was sourced from [https://codepen.io/jhourigan8/pen/LYgpLzj].
Most of the work here dealt with keeping track of the cube state as the user moved the cube.
To start the frontend run `node app` from the `app` directory in bash.
To communicate with the solver our app sends a request to a flask server with code located in `pennCube/app.py`.
The flask server translates from our javascript representation to our python representation and calls the solvers.
It then returns the results to the user.
To start the flask server run `flask run` from the `pennCube` directory in bash.

## Solver
We decided to implement a solver using both MIP and SAT to experimentally compare the two.

As a starting point for our solver we read [GECIS PAPER].
[TALK ABOUT MIP].




