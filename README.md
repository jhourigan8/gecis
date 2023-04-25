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

## pennCube
The main file to open for testing the MIP solver is the `pennCube.ipynb`. If opening run the first 3 code cells, 
which are the imports, solver, and testing helpers. The next cell is a tool used to take a real-life scramble and get the array representation for testing
and thus can be ignored. Then follows some test arrays. Then comes the next section in which you have the ability to run a test as it would run on the front end. 
Replace the input array with any failing test case to see the output of the solver. 

Bellow all of this was an all in one tester that allows you to take a real-life scramble and input it to be solved. This was helpful for debugging however 
to use one must fully understand our numbering of the cubes as described in the diagrams at the top of the file. 

The last thing to note is that if you wish to modify the constraints one must do that within the solve method (comment out/add the function
calls for the other constraints.) 

If you wish to see the cube in action recomend using the webapp to interface with it, since the code is a bit complex and not fully setup for the 
user to easily interface with it, without knowing how it works.


## Solver
We decided to implement a solver using both MIP and SAT to experimentally compare the two.

As a starting point for our solver we read [GECIS PAPER].
[TALK ABOUT MIP].




