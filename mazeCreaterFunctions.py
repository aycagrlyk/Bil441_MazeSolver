
from numpy.random import randint
import csv
import sys
import numpy as np
#check the tile coordinates in maze
def inMaze(step, dimension):

    (maxX, maxY) = dimension
    (x, y) = step

    inX = (x <= maxX) & (x >= 0)
    inY = (y <= maxY) & (y >= 0)
    return bool(inX*inY)
#compute the all possible steps for the next step
def allNextSteps(dimension, currentNode):

    stepX, stepY = currentNode

    availableTiles = []
    operation1 = [(0,1), (0,-1), (1,0), (-1,0)]
    operation2 = [(0,2), (0,-2), (2,0), (-2,0)]
    numOperations = len(operation1)

    for i in range(numOperations):
        op1X, op1Y = operation1[i]
        op2X, op2Y = operation2[i]

        if (inMaze((stepX + op1X, stepY + op1Y), dimension)) and (inMaze((stepX + op2X, stepY + op2Y), dimension)):
            availableTiles.append([(stepX + op1X, stepY + op1Y), (stepX + op2X, stepY + op2Y)])
    return availableTiles
#create the maze with dfs
def createMaze(maze, currentNode, seen, backward):

    (x, y) = currentNode
    maze[x][y] = 1
    dimension = (len(maze), len(maze[0]))
    availableTiles = allNextSteps(dimension, currentNode)

    filename = "mazes/new.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        row=0
        column=0
        for row in range(len(maze)):
            for column in range(len(maze[0])):
                if(column == len(maze[0])-1):
                    csvfile.write(str(maze[row][column]))
                else:
                    csvfile.write(str(maze[row][column]) + ",")

            csvfile.write("\n")


    trueSteps = []
    for step in availableTiles:
        (x1, y1) = step[0]
        (x2, y2) = step[1]

        notWhite = (maze[x1][y1] != 1) & (maze[x2][y2] != 1)
        notGreen = (maze[x1][y1] != 2) & (maze[x2][y2] != 2)

        if bool(notWhite * notGreen):
            trueSteps.append(step)



    if (len(trueSteps) == 0):
        currentNode = seen[-2 - backward]
        if currentNode == (0,0):
            print("finished")
            done = True
            return maze, currentNode, backward, done
        backward += 1
        done = False
        return maze, currentNode, backward, done

    else:
        backward = 0

        if (len(trueSteps) == 1):
            currentNode = trueSteps[0]
            (x1, y1) = currentNode[0]
            (x2, y2) = currentNode[1]
            maze[x1][y1] = 1
            maze[x2][y2] = 4
            currentNode = currentNode[1]
            done = False
            return maze, currentNode, backward, done
        else:
            index = randint(0, len(trueSteps))
            currentNode = trueSteps[index]
            (x1, y1) = currentNode[0]
            (x2, y2) = currentNode[1]
            maze[x1][y1] = 1
            maze[x2][y2] = 4
            currentNode = currentNode[1]
            done = False
            return maze, currentNode, backward, done
