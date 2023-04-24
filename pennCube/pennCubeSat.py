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
import pycosat
from typing import List, Tuple
import time

# %% [markdown]
# ##### Solver

# %%


class cubeSolver:
    def __init__(self, scramble: List[int], maxMoves):
        self.maxMoves = maxMoves
        self.scramble: List[int] = scramble

    def x(self, c: int, i: int, t: int) -> int:
        # color, square, time
        return 18*self.maxMoves + c + 6*i + 6*54*t + 1
    
    def y(self, k: int, t: int) -> int:
        # move, time
        return k + 18*t + 1

    def gecisTurnContraints(self):
        gecis = self.gecis
        maxMoves = self.maxMoves
        x = self.x
        y = self.y

        # do move => i goes to j
        # add 1 go backwards
        # lots of sub one to undo gecis 1-indexing
        constraints = self.constraints
        for c in range(6):
            for t in range(maxMoves - 1):
                for k, i, j in gecis:
                    constraints.append([-y(k-1, t), x(c, i-1, t), -x(c, j-1, t+1)])
                    constraints.append([-y(k-1, t), -x(c, i-1, t), x(c, j-1, t+1)])   
                    constraints.append([-y(k, t), x(c, j-1, t), -x(c, i-1, t+1)])
                    constraints.append([-y(k, t), -x(c, j-1, t), x(c, i-1, t+1)])  
                    
    def gecisNoTurnContraints(self):
        maxMoves = self.maxMoves
        x = self.x
        y = self.y
        gecis = self.gecis

        # don't move => l stays same
        # add 1 to go backwards
        constraints = self.constraints
        for t in range(maxMoves - 1):
            for l in range(1, 55):
                list = []
                for k, _, j in gecis:
                    if j == l:
                        list.append(y(k-1, t))
                        list.append(y(k, t))
                for c in range(6):
                    constraints.append(list + [x(c, l-1, t), -x(c, l-1, t+1)])
                    constraints.append(list + [-x(c, l-1, t), x(c, l-1, t+1)])      

    def atMostOneMovePerTime(self):
        y = self.y
        maxMoves = self.maxMoves

        constraints = self.constraints
        for t in range(maxMoves - 1):
            for k in range(1,19):
                for l in range(k+1, 19):
                    constraints.append([-y(k-1, t), -y(l-1, t)])

    def atMostOneColorPerTime(self):
        x = self.x
        maxMoves = self.maxMoves

        constraints = self.constraints
        for t in range(maxMoves):
            for i in range(54):
                for c in range(6):
                    for d in range(c+1, 6):
                        constraints.append([-x(c, i, t), -x(d, i, t)])

    def atLeastOneMovePerTime(self):
        y = self.y
        maxMoves = self.maxMoves

        constraints = self.constraints
        for t in range(maxMoves - 1):
            constraints.append([y(k, t) for k in range(18)])

    def atLeastOneColorPerTime(self):
        x = self.x
        maxMoves = self.maxMoves

        constraints = self.constraints
        for t in range(maxMoves):
            for i in range(54):
                constraints.append([x(c, i, t) for c in range(6)])


    def setInitialPositionContraints(self):
        maxMoves = self.maxMoves
        x = self.x
        scramble = self.scramble

        constraints = self.constraints
        for c in range(6):
            for i in range(1, 55):
                assert(i-1 >= 0)
                assert(i-1 <= 53)
                if c == scramble[i-1]:
                    constraints.append([x(c, i-1, 0)])

    def setFinalPosition(self):
        x = self.x
        maxMoves = self.maxMoves
        faces = [[0, 1, 2, 3, 4, 5, 6, 7, 8], 
            [9, 10, 11, 21, 22, 23, 33, 34, 35], 
            [12, 13, 14, 24, 25, 26, 36, 37, 38], 
            [15, 16, 17, 27, 28, 29, 39, 40, 41],
            [18, 19, 20, 30, 31, 32, 42, 43, 44],
            [45, 46, 47, 48, 49, 50, 51, 52, 53]]
        
        constraints = self.constraints
        for f in faces:
            for c in range(6):
                for p in range(9):
                    for q in range(p+1, 9):
                        constraints.append([x(c, f[p], maxMoves - 1), -x(c, f[q], maxMoves - 1)])
                        constraints.append([-x(c, f[p], maxMoves - 1), x(c, f[q], maxMoves - 1)])
        

    def solve(self):
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

        self.constraints = []
        constraints = self.constraints

        self.atMostOneMovePerTime()
        self.atMostOneColorPerTime()
        self.atLeastOneMovePerTime()
        self.atLeastOneColorPerTime()
        self.gecisTurnContraints()
        self.gecisNoTurnContraints()
        self.setInitialPositionContraints()
        self.setFinalPosition()

        solutionTurns = []
        x = self.x
        y = self.y
        maxMoves = self.maxMoves

        print('Starting to solve...')
        ass = pycosat.solve(constraints)

        if ass == "UNSAT":
            raise ValueError('Modeling error!')
        else:
            ass = [((x-1) // 18, (x % 18)) for x in ass if x > 0 and x <= 18*maxMoves]   
        return ass


# %%
def letterToColor(letter):
    if letter == 'r':
        return 4
    elif letter == 'g':
        return 3
    elif letter == 'b':
        return 5
    elif letter == 'w':
        return 1
    elif letter == 'y':
        return 6
    elif letter == 'o':
        return 2
    else:
        raise ValueError(f'enter r, g, b, w, y, o Got {letter} instead')

def inputArrayMaker(printArray = False):
    faces = [[0, 1, 2, 3, 4, 5, 6, 7, 8], 
            [9, 10, 11, 21, 22, 23, 33, 34, 35], 
            [12, 13, 14, 24, 25, 26, 36, 37, 38], 
            [15, 16, 17, 27, 28, 29, 39, 40, 41],
            [18, 19, 20, 30, 31, 32, 42, 43, 44],
            [45, 46, 47, 48, 49, 50, 51, 52, 53]]
    
    colors = ['w', 'o', 'g', 'r', 'b', 'y']
    curr = -1

    outputArray = [0 for i in range(54)]

    for face in faces:
        curr += 1
        for i in face:
            color = input(f'Enter {i + 1}\'th letter for the {colors[curr]} face')
            outputArray[i] = letterToColor(color)
    
    if printArray:
        print(outputArray)
    
    return outputArray

def moveToFaceTurn(move):
    if move == 1:
        return 'B\''
    elif move == 2:
        return 'B'
    elif move ==  3:
        return 'S'
    elif move ==  4:
        return 'S\''
    elif move ==  5:
        return 'F'
    elif move == 6:
        return 'F\''
    elif move == 7:
        return 'U\''
    elif move == 8:
        return 'U'
    elif move == 9:
        return 'E\''
    elif move == 10:
        return 'E'
    elif move == 11:
        return 'D'
    elif move == 12:
        return 'D\''
    elif move == 13:
        return 'L\''
    elif move == 14:
        return 'L'
    elif move == 15:
        return 'M\''
    elif move == 16:
        return 'M'
    elif move == 17:
        return 'R'
    elif move == 18:
        return 'R\''
    else:
        raise ValueError(f'Enter in range 1 to 18, Got {move} instead')

def outputPretty(solutionTurns):
    #solution turns should be in the form [(t, i)] where turn t is i
    if solutionTurns is None:
        print('No solution was found')
        return
    for t, i in solutionTurns:
        print(f'Turn {t + 1} is {moveToFaceTurn(i + 1)}')






# %% [markdown]
# ##### Testing

# %%
#a bunch of test positions

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

threeMove = [5, 5, 5, 
            1, 1, 1, 
            3, 3, 3, 
    1, 3, 6, 4, 4, 4, 1, 5, 6, 2, 2, 2, 
    2, 2, 2, 1, 3, 6, 4, 4, 4, 1, 5, 6, 
    2, 2, 2, 1, 3, 6, 4, 4, 4, 1, 5, 6, 
            3, 6, 5, 
            3, 6, 5, 
            3, 6, 5]

fourMove = [1, 1, 2, 1, 1, 3, 1, 1, 3, 
            5, 2, 2, 3, 3, 6, 4, 4, 1, 
            5, 4, 4, 2, 2, 2, 3, 3, 1, 
            5, 4, 4, 5, 5, 5, 2, 2, 2, 
            3, 3, 3, 1, 4, 4, 5, 5, 5, 
            6, 6, 4, 6, 6, 6, 6, 6, 6]

sevenMove = [1, 2, 1, 
            5, 1, 5, 
            3, 4, 5, 
   5, 6, 1, 2, 3, 4, 6, 1, 3, 4, 1, 4, 
   2, 2, 4, 6, 3, 3, 2, 4, 4, 5, 5, 5, 
   2, 2, 4, 6, 3, 2, 5, 6, 6, 2, 1, 5, 
            3, 1, 1, 
            6, 6, 3, 
            6, 4, 3]

twelveMove = [2, 3, 6, 5, 1, 2, 3, 4, 
2, 5, 6, 1, 2, 3, 6, 3, 3, 2, 5, 1, 
1, 2, 2, 5, 1, 3, 2, 5, 4, 5, 4, 5, 
1, 6, 6, 6, 3, 6, 5, 4, 4, 4, 3, 2, 
5, 4, 3, 1, 4, 6, 1, 4, 6, 1]

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




