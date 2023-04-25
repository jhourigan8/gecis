# MIP Rubics Cube Solver
The main file to open for testing the MIP solver is the pennCube.ipynb. If opening run the first 3 code cells, 
which are the imports, solver, and testing helpers. The next cell is a tool used to take a real-life scramble and get the array representation for testing
and thus can be ignored. Then follows some test arrays. Then comes the next section in which you have the ability to run a test as it would run on the front end. 
Replace the input array with any failing test case to see the output of the solver. 

Bellow all of this was an all in one tester that allows you to take a real-life scramble and input it to be solved. This was helpful for debugging however 
to use one must fully understand our numbering of the cubes as described in the diagrams at the top of the file. 

The last thing to note is that if you wish to modify the constraints one must do that within the solve method (comment out/add the function
calls for the other constraints.) 

If you wish to see the cube in action recomend using the webapp to interface with it, since the code is a bit complex and not fully setup for the 
user to easily interface with it, without knowing how it works.
