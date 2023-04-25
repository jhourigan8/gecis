# Overview
Our PennCube project consists of an app and a solver.

## Files
- `license.txt`: MIT license.
- `RESULTS.md`: Experimental testing results.
- `app/index.html`: HTML code for the web app.
- `app/style.css`: CSS code for the web app.
- `app/script.js`: Client side JS code for the web app.
- `pennCube/app.py`: Server side Python code to interface between app and solver.
- `pennCube/pennCube.ipynb`: MIP PennCube code with test cases.
- `pennCube/pennCubeSat.ipynb`: SAT PennCube code with test cases.
- `pennCube/pennCube.py`: MIP solver code exported from Jupyter notebook.
- `pennCube/pennCubeSat.py`: SAT solver code exported from Jupyter notebook.

## Usage
To run the web app, run `node app` in the `app` directory and run `flask run` in the `pennCube` directory.
The app will then be live at `http://localhost:8000`.
At the bottom of each Jupyter notebook we have manual test suites for testing outside of the web app.

## App
Our app shows a realistic 3D-rendered Rubik's cube which can be controlled via the mouse.
At any point the user can click the `solve` button to have our solver solve the cube.
The user can select either the `MIP` or `SAT` solver using the buttons on the bottom. 
While the solver is running a timer shows the amount of time elapsed.
Once an optimal solution has been found the app animates the solution on the cube.

The original Rubik's cube animation code was sourced from [here](https://codepen.io/jhourigan8/pen/LYgpLzj).
The rest of the frontend is original work.
Most of the work on the frontend dealt with keeping track of the cube state as the user moves the cube.
To communicate with the solver our app sends a request to a flask server.
The flask server translates from our javascript representation to our python representation and calls one of the solvers.
It then returns the results to the user.

## Solver
We decided to implement a solver using both MIP and SAT to experimentally compare the two.

As a starting point for our solvers we read the following [paper](http://www.m-hikari.com/imf-password2009/45-48-2009/aksopIMF45-48-2009-2.pdf). That described a method to implement a solver using Integer Programing. The main ideas are that we have variables that define the color of each sub cube in
each step in the soltuion, aswell a varaiables that define which move is done at each step in the solution. Then we have contraints making sure the colors match depending on the moves done, and that only move can be done at each time. Initially we had a minimization contraint over the number of moves made, however we found it to be faster to have a max move number, and re run the solver incrementing that.

#### MIP Solver
The main file to open for testing the MIP solver is the `pennCube.ipynb`. If opening run the first 4 code cells, 
which are the imports, two solver sections, and testing helpers. The next secton contain actual test cases which you can run to test the features of our solver. Replace the input array of the first test case with any failing test case to see the output of the solver. Further more our solver has 5 different parameters. 
- Scramble: The starting position of the solver
- debugIn: When true prints runtimes and other information
- oneSideIn: Number from 1-6 that says which one side to solve. If none solves normally
- crossIn: Number from 1-6 that says which cross to solver. If non solves normally
- timeLimit: Time limit for the solver

Bellow all of this was an all in one tester that allows you to take a real-life scramble and input it to be solved. This was helpful for debugging however 
to use one must fully understand our numbering of the cubes as described in the diagrams at the top of the file. 

The last thing to note is that if you wish to modify the constraints one must do that within the solve method (comment out/add the function
calls for the other constraints.) 

If you wish to see the cube in action recomend using the webapp to interface with it, since the code is a bit complex and not fully setup for the 
user to easily interface with it, without knowing how it works.

### Ways We Optimized the Solver
Through the proccess of developing the solver we did some steps to try to make it faster, since intitialy it took an unresonable amount of time even on easy solves.

**Switched Solvers:**
The first thing we did was swap from the `Solver.CBC_MIXED_INTEGER_PROGRAMMING` to the `Solver.SAT_INTEGER_PROGRAMMING`. This new solver requires only bool vars and finite bools vars which matches our situation. This led to speed up from 10's of miniutes to 10's of seconds. We think this is due to the fact that the more complex MIP solver is looking at a much larger search space compared to the SAT version.

**Removed Minimization Contraint:**
One thing we needed was a maxMove contraint on the solver to give a finite number of varaibles to create before calling the solve method. We initially set this to a large number and then just let it run to minimize the number of moves. However we found that it creates a large number of unesseasry varaibales so intead we got rid of the minimization constraint. Then we incremented over the maxMoves values 1, 2, ... until it finds a fesible solution. This decreased runtimes from around 16.0 seconds for a 7 move solve to 1.8 seconds for a 7 move solve. 

**Different Objectives:**
We also tried using different objectives, like just solving one face, or solving the cross on one side. This lead to some speed up in some cases however the main time contraint was due to the actuall minimization value. Since solving one side can take >12 moves this does not lead to much speed up in complex scrambles.

**Change Encodings:**
Lastly we decided to change encodings from MIP to SAT. We thought this might speed things up since the MIP solver might be looking at unessesary search spaces while SAT might be able to ignore some cases. This lead to not much of a different ###(Jack write what it did)



