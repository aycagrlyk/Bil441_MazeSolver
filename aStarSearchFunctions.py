
import csv
import numpy as np
from time import sleep


class Node:
    def __init__(self, parent, cost, position):
        self.parent = parent
        self.cost = cost
        self.position = position
#convert mazeFile to mazeGrid
def convertMaze(mazeFile):
    maze = []
    with open(mazeFile, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                #row.pop()
                maze.append(row)
                
    # convert to ints
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            maze[i][j] = int(maze[i][j])
    return maze
#delete the node from the frontier
def deleteNodeFrontier(node, frontier):

    pos = node.position
    newFrontier = []
    for tile in frontier:
        if tile.position != pos:
            newFrontier.append(tile)
    return newFrontier

#compute the node cost with euclidean heuristic
def nodeCost(position, goal):

    x, y = position
    xGoal, yGoal = goal
    cost = np.sqrt((xGoal-x)**2 + (yGoal-y)**2)
    return cost
#check the tile coordinates in maze
def inMaze(step, dimension):
    (maxX, maxY) = dimension
    (x, y) = step

    inX = (x <= maxX) & (x >= 0)
    inY = (y <= maxY) & (y >= 0)
    return bool(inX * inY)

#find possible current successors
def findSuccessors(currentNode, maze, seen):

    moves = [(1,0), (-1,0), (0,1), (0,-1)]
    x0, y0 = currentNode.position
    dimension = (len(maze)-1, len(maze[0])-1)
    successors = []
    finalCost=0

    for move in moves:
        dx, dy = (move[0], move[1])
        nextStep = (x0 + dx, y0 + dy)
        cond1 = inMaze(nextStep, dimension) # if is in maze
        if cond1:
            cond2 = maze[nextStep[0]][nextStep[1]] != 0 # if not wall
            cond3 = nextStep not in [tile.position for tile in seen] # dont go to any already seen
            cond4 = maze[nextStep[0]][nextStep[1]] != 6  # if not barrier
            if bool(cond2*cond3*cond4):
                cost = nodeCost(nextStep, dimension)
                finalCost=finalCost+cost
                newNode = Node(currentNode, cost, nextStep)
                successors.append(newNode)

    print ("Current cost is: ",finalCost)
    if(finalCost==0):
        count=1
    return successors

#select the min cost node for the next step
def selectNode(nodeList):

    if len(nodeList) == 1:
        currentNode = nodeList[0]
        return currentNode
    
    currentNode = Node(None, np.inf, (0,0))
    for node in nodeList:
        if node.cost <= currentNode.cost: # select least cost
            currentNode = node

    return currentNode
#run the algorithm step by step untill find the goal
def computePath(maze, frontier, seen, currentNode,arrGoal,detect):

    # add parent to seen list
    seen.append(currentNode)
    
    # remove parent from frontier
    frontier = deleteNodeFrontier(currentNode, frontier)
    #temp=currentNode
    # given the node compute the successors
    successors = findSuccessors(currentNode, maze, seen)

    # add successors to the frontier
    for son in successors:
        frontier.append(son)


    # pick one of the successors
    currentCheck = {currentNode.position}
    currentNode = selectNode(successors)

    if currentCheck == {currentNode.position}:
    #if len(frontier) == 0:
        #print("NO SOLUTION!!!!!!!")
        #sleep(120)
        #exit()
        detect=False
        x, y = currentNode.position
        return maze, frontier, seen, currentNode,detect


    # paint the grid with the new node position
    x, y = currentNode.position
   # grid[x][y] = 4 # paint blue
    #if(count==0):
     #   detect=False
    #else:
    detect = True

    return maze, frontier, seen, currentNode,detect

