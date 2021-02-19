
import csv
from numpy.random import randint
from time import sleep

#convert mazeFile to mazeGrid
def convertMaze(mazeFile):

    maze = []
    with open(mazeFile, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                maze.append(row)

    # convert to ints
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            maze[i][j] = int(maze[i][j])
    return maze
#check the tile coordinates in maze
def inMaze(step, dimension):
    (maxX, maxY) = dimension
    (x, y) = step

    inX = (x <= maxX) & (x >= 0)
    inY = (y <= maxY) & (y >= 0)
    return bool(inX * inY)
#compute the all possible steps for the next step
def allNextSteps(dimension, currentNode,maze):

    x, y = currentNode
    moves = [(1,0), (-1,0), (0,1), (0,-1)]
    availableTiles = []
    for move in moves:
        dx, dy = move
        nextMove = (x+dx, y+dy)
        if inMaze(nextMove, dimension) and maze[x+dx][y+dy]!=0 :
            availableTiles.append(nextMove)

    return availableTiles
#run the algorithm step by step untill find the goal
def computePath(maze, currentNode, seen, backward,arrGoal):

    x, y = currentNode
    dimension = (len(maze)-1, len(maze[0])-1)
    availableTiles = allNextSteps(dimension, currentNode,maze)

    trueSteps = []
    for tile in availableTiles:
        x, y = tile
        if (maze[x][y] == 3): # if red
            maze[x][y]=5
            trueSteps = []
            trueSteps.append(tile)
            done = True
            return maze, currentNode, backward, done, arrGoal

        elif (maze[x][y] == 1): # if white
            trueSteps.append(tile)



    if len(trueSteps) == 0:
        x, y = currentNode
        maze[x][y] = 4
        x, y = currentNode
        currentNode = seen[-1 - backward]
        backward += 1
       # if (len(arrGoal) != 0):
        #    arrGoal.pop()
        done=False
        return maze, currentNode, backward, done, arrGoal
        #else:
         #   done=True
          #  print("No solution!!!!!!!!!!!!")
           # return grid, last_pos, back_step, done, arrGoal


    elif len(trueSteps) == 1:
        backward = 0
        x, y = trueSteps[0]
        currentNode = (x, y)
        maze[x][y] = 5 # paint blue
        #path.append(last_pos)
        done = False
        return maze, currentNode, backward, done, arrGoal

    else:
        backward = 0
        index = randint(0, len(trueSteps))
        currentNode = trueSteps[index]
        x, y = currentNode
        maze[x][y] = 5 # paint blue
        #path.append(last_pos)
        done = False
        return maze, currentNode, backward, done, arrGoal

