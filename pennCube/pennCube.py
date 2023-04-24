# %% [markdown]
# # **Penn Cube**
# ### Outline:
# - This file contains main class that will be the backbone to the pennCube implementation
# - Class is borken into several methods that will be used together to initialize all of our contraint variables and then eventualy solve the MIP problem
# - Referencing this [paper](http://www.m-hikari.com/imf-password2009/45-48-2009/aksopIMF45-48-2009-2.pdf) to build the MIP
# - Might also need to reference this [paper](https://cw.fel.cvut.cz/b192/_media/courses/ko/ilp_rubik.pdf) since it has a much smaller set G (gecis)
# 
# 
# ##### Cube Layout:
# ![](RubiksCubeMap.png)
# ##### Move Map:
# ![](moveMap.png)
# 

# %% [markdown]
# ##### Imports

# %%
from ortools.linear_solver.pywraplp import Solver
from typing import List, Tuple


# %%
class cubeSolver:
    def __init__(self, scramble: List[int], maxMoves):
        # List of size 54, that describes the initial positions of all cubes (as from above diagram)
        self.maxMoves = maxMoves
        self.scramble: List[int] = scramble
        self.checkInput()
        self.solved = False

    def checkInput(self):
        # imput checking
        if len(self.scramble) != 54:
            raise ValueError(f'Input scramble not of right size, expected: 54, got: {len(self.scramble)}')
        #should add more in the future to check if the input is a true scramble

    def initializeGecis(self):
        # this is the set of (k, i, j) that means that subcube at position i in the map fo the cube will go to
        # to the position j if a k move is done
        # TODO: depending on if this works go back and adding missing tuples (they might be redundant)

        self.gecis = [
            (1,1,18), (1,2,30), (1,3,42), (1,10,3), (1,22,2),
            (1,34,1), (1,18,54), (1,30,53), (1,42,52), (1,52,10), (1,53,22),
            (1,54,34), (1,19,43), (1,20,31), (1,21,19), (1,31,44), (1,33,20),
            (1,43,45), (1,44,33), (1,45,21), (3,4,17), (3,5,29), (3,6,41), (3,11,6),
            (3,23,5), (3,35,4), (3,17,51), (3,29,50), (3,41,49),
            (3,49,11), (3,50,23), (3,51,35), (5,7,16), (5,8,28), (5,9,40),
            (5,12,9), (5,24,8), (5,36,7), (5,16,48), (5,28,47), (5,40,46),
            (5,46,12), (5,47,24), (5,48,36), (5,13,15), (5,14,27), (5,15,39),
            (5,25,14), (5,27,38), (5,37,13), (5,38,25), (5,39,37), (7,10,13),
            (7,11,14), (7,12,15), (7,13,16), (7,14,17), (7,15,18), (7,16,19),
            (7,17,20), (7,18,21), (7,19,10), (7,20,11), (7,21,12), (7,3,1),
            (7,6,2), (7,9,3), (7,2,4), (7,8,6), (7,1,7), (7,4,8), (7,7,9),
            (9,22,25), (9,23,26), (9,24,27), (9,25,28), (9,26,29), (9,27,30),
            (9,28,31), (9,29,32), (9,30,33), (9,31,22), (9,32,23), (9,33,24),
            (11,34,37), (11,35,38), (11,36,39), (11,37,40), (11,38,41),
            (11,39,42), (11,40,43), (11,41,44), (11,42,45), (11,43,34),
            (11,44,35), (11,45,36), (11,46,48), (11,47,51), (11,48,54),
            (11,49,47), (11,51,53), (11,52,46), (11,53,49), (11,54,52),
            (13,1,45), (13,4,33), (13,7,21), (13,13,1), (13,25,4), (13,37,7),
            (13,21,52), (13,33,49), (13,45,46), (13,46,13), (13,49,25),
            (13,52,37), (13,10,34), (13,11,22), (13,12,10), (13,22,35),
            (13,24,11), (13,34,36), (13,35,24), (13,36,12), (15,2,44), (15,5,32),
            (15,8,20), (15,14,2), (15,26,5), (15,38,8), (15,20,53), (15,32,50),
            (15,44,47), (15,47,14), (15,50,26), (15,53,38), (17,3,43), (17,6,31),
            (17,9,19), (17,15,3), (17,27,6), (17,39,9), (17,19,54), (17,31,51),
            (17,43,48), (17,48,15), (17,51,27), (17,54,39), (17,16,18),
            (17,17,30), (17,18,42), (17,28,17), (17,30,41), (17,40,16),
            (17,41,28), (17,42,40)]

    def create_variables(self):
        model: Solver = self.model
        maxMoves = self.maxMoves

        #x[i][t] = 1 to 6 int var that is the color index of the subcube at i at turn t
        x = [[model.IntVar(1, 6, f'x[{j}][{i}]') for i in range(maxMoves)] for j in range(54)]
        self.x = x

        #y[i][t] = 0 to 1 int var that is 1 if turn t is an i move i = [1..18]
        y = [[model.IntVar(0, 1, f'y[{j}][{i}]') for i in range(maxMoves)] for j in range(18)]
        self.y = y

    def minMoveContraint(self):
        # minimization constraint to minimize total number of moves
        model: Solver = self.model
        maxMoves = self.maxMoves

        totalMoves = 0
        for i in range(18):
            for t in range(maxMoves):
                totalMoves += t * self.y[i][t]
        model.Minimize(totalMoves)


    def gecisTurnContraints(self):
        # adds the turn contraints based on the GECIS set as described in the paper
        # equations 3 and 4 from paper
        model: Solver = self.model
        x: List[int] = self.x
        y: List[int] = self.y
        gecis = self.gecis
        maxMoves = self.maxMoves

        for t in range(maxMoves - 1):
            for k, i, j in gecis:
                #add constraint
                model.Add(x[i - 1][t] - 6 * (1 - y[k - 1][t]) <= x[j - 1][t + 1])
                model.Add(x[j - 1][t + 1] <= x[i - 1][t] + 6 * (1 - y[k - 1][t]))
                
                model.Add(x[j - 1][t] - 6 * (1 - y[k - 1 + 1][t]) <= x[i - 1][t + 1])
                model.Add(x[i - 1][t + 1] <= x[j - 1][t] + 6 * (1 - y[k - 1 + 1][t]))
                        
                        

    def gecisNoTurnContraints(self):
        # add the contraint that x[i][t] = x[i][t + 1] if the i subcube does not move at turn t
        # equation 5 from the paper
        model: Solver = self.model
        x: List[int] = self.x
        y: List[int] = self.y
        gecis = self.gecis
        maxMoves = self.maxMoves

        for t in range(maxMoves - 1):
            for k, i, j in gecis:
                #add constraint
                #TODO: does this add a bunch of repeat constraints
                innerSum = 0
                for l, j, n in gecis:
                    if l != k and i == j:
                        innerSum += y[l - 1][t] 
                        innerSum += y[l - 1 + 1][t]
                    
                model.Add(x[i - 1][t] - 6 * (y[k - 1][t] + y[k - 1 + 1][t] + innerSum) <= x[i - 1][t + 1])
                model.Add(x[i - 1][t + 1] <= x[i - 1][t] + 6 * (y[k - 1][t] + y[k - 1 + 1][t] + innerSum))
        
                        


    def setInitialPositionContraints(self):
        # assigns the variables to the initial posisions of the cube
        model: Solver = self.model
        x: List[int] = self.x
        scramble: List[int] = self.scramble

        for i in range(54):
            model.Add(x[i][0] == scramble[i])



    def atMostOneMovePerTime(self):
        #adds the contraint that at eachtime step at most one face is turned
        model: Solver = self.model
        maxMoves = self.maxMoves

        for t in range(maxMoves):
            #at each time step
            sumOfMoves = 0
            for i in range(18):
                sumOfMoves += self.y[i][t]
            model.Add(sumOfMoves <= 1)

    def setFinalPosition(self):
        model: Solver = self.model
        x: List[int] = self.x
        maxMoves = self.maxMoves

        self.faces = [[0, 1, 2, 3, 4, 5, 6, 7, 8], 
            [9, 10, 11, 21, 22, 23, 33, 34, 35], 
            [12, 13, 14, 24, 25, 26, 36, 37, 38], 
            [15, 16, 17, 27, 28, 29, 39, 40, 41],
            [18, 19, 20, 30, 31, 32, 42, 43, 44],
            [45, 46, 47, 48, 49, 50, 51, 52, 53]]
        
        for face in self.faces:
            for i in range(9):
                model.Add(x[face[i - 1]][maxMoves - 1] == x[face[i]][maxMoves - 1])

        

    def solve(self):
        self.model = Solver('CubeSolver', Solver.CBC_MIXED_INTEGER_PROGRAMMING)
        self.initializeGecis()
        self.create_variables()
        self.atMostOneMovePerTime()
        self.minMoveContraint()
        self.gecisTurnContraints()
        self.gecisNoTurnContraints()
        self.setInitialPositionContraints()
        self.setFinalPosition()

        solutionTurns = []

        print('Starting to solve...')

        if self.model.Solve() == Solver.OPTIMAL:
            self.solved = True
            print(self.model.Objective().Value())
            for t in range(self.maxMoves):
                for i in range(18):
                    if self.y[i][t].solution_value() == 1:
                        print(f'Turn {t} is {i}')
                        solutionTurns.append((t, i))
                
            return solutionTurns
        else:
            raise ValueError('Modeling error!')

    def getSolved(self, debug = False):
        model: Solver = self.model
        if not self.solved:
            print('Call Solve First!')
        elif debug:
            for j in range(self.maxMoves):
                solutionArray = [self.x[i][j].solution_value() for i in range(54)]
                print(solutionArray)
            return solutionArray
        else:
            solutionArray = [self.x[i][self.maxMoves - 1].solution_value() for i in range(54)]
            return solutionArray
                    

    





        


# %%


# %% [markdown]
# ##### Testing

# %%
#basic cube solver

solvedPosition = [
    1, 1, 1, 
    1, 1, 1, 
    1, 1, 1,
2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 
2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5,
2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 
    6, 6, 6,  
    6, 6, 6, 
    6, 6, 6] 

oneTurn = [
    2, 2, 2, 
    1, 1, 1, 
    1, 1, 1,
6, 2, 2, 3, 3, 3, 4, 4, 1, 5, 5, 5, 
6, 2, 2, 3, 3, 3, 4, 4, 1, 5, 5, 5,
6, 2, 2, 3, 3, 3, 4, 4, 1, 5, 5, 5, 
    6, 6, 6,  
    6, 6, 6, 
    4, 4, 4]

twoTurn = [
    6, 6, 6, 
    1, 1, 1, 
    1, 1, 1,
4, 2, 2, 3, 3, 3, 4, 4, 2, 5, 5, 5, 
4, 2, 2, 3, 3, 3, 4, 4, 2, 5, 5, 5,
4, 2, 2, 3, 3, 3, 4, 4, 2, 5, 5, 5, 
    6, 6, 6,  
    6, 6, 6, 
    1, 1, 1]




# %%



