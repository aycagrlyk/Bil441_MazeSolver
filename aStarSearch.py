import pygame
import os
from time import sleep
from aStarSearchFunctions import convertMaze, computePath, selectNode

def aStar():

    # path solution
    numOfTile=0
    # keep all goal points
    arrGoal=[]

    # using to find shorthest path
    class Shortest:
        def __init__(self, yol):
            self.yol = yol
    # class node
    class Node:
        def __init__(self, parent, cost, position):
            self.parent = parent
            self.cost = cost
            self.position = position

    # path nodes
    check=0
    # list all mazes and ask the user to select one of them,number of goal point
    if check==0:
        arr = os.listdir("mazes")
        for i in range (0,len(arr)):
            arr[i]="mazes/"+arr[i]
        print(arr)
        select=input("Select one of them mazes \n")
        num=int(select)
        print(arr[num])
        numGoalStr = input("Select number of goal point \n")
        numGoal=int(numGoalStr)

    # keep all possible path to goals
    paths = []

    # selected maze are read from the file
    mazeFile =str(arr[num])
    gridMaze = convertMaze(mazeFile)

    # define maze size nxn
    numOfRows = len(gridMaze)
    numOfColumns = len(gridMaze[0])

    # define colors for maze
    black = (0, 0, 0) # grid == 0 for wall
    white = (255, 255, 255) # grid == 1 for available
    green = (50,205,50) # grid == 2 for starting point
    red = (255,99,71) # grid == 3 for goal point
    grey = (211,211,211) # for background
    blue = (153,255,255) # grid[x][y] == 4 for current position
    magenta = (255,0,255) # grid[x][y] == 5 for solution
    orange = (255,140,0) # grid == 6 for barrier

    # set the height/width of each location on the grid
    height = 15
    # nxn size
    width = height
    # sets margin between grid tiles
    margin = 1
    gridMaze[0][0]=1
    gridMaze[numOfRows-1][numOfColumns-1]=1

    # initialize pygame
    pygame.init()
    # congiguration of the window
    screen = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
    # screen title
    pygame.display.set_caption(f"A* for. {mazeFile}")
    # to manage how fast the screen updates
    clock = pygame.time.Clock()

    # while runnig
    # when user clicks exit
    interrupt = False
    # when algorithm starts
    run = False
    finish = False
    finalStep = False
    startPoint = False
    goalPoint = False


    # maze coloring and changing
    while not interrupt:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                interrupt = True

            elif event.type == pygame.MOUSEBUTTONDOWN and run == False:
                # user clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # change the x/y screen coordinates to gridMaze coordinates
                column = pos[0] // (width + margin)
                row = pos[1] // (height + margin)
                # set that location to start point
                if startPoint == False:
                    if gridMaze[row][column] == 1:
                        gridMaze[row][column] = 2
                        start = (row,column)
                        startPoint=True
                # set that location to goal points
                elif goalPoint == False:
                     # all goal points are selected
                     if (numGoal == 0):
                         goalPoint = True
                     else:
                        if gridMaze[row][column] == 1:
                            gridMaze[row][column] =3
                            goal=(row,column)
                            arrGoal.append(goal)
                            numGoal=numGoal-1
                # start point and goal points are selected then select barriers
                elif gridMaze[row][column] == 1 and startPoint== True and goalPoint==True:
                    gridMaze[row][column] = 6
                # return the tile available
                elif (gridMaze[row][column] == 0 or gridMaze[row][column] == 6) and startPoint== True and goalPoint==True:
                    gridMaze[row][column] = 1

             # wait for user to press any key to start
            elif event.type == pygame.KEYDOWN:
                # define start node
                startNode = Node(None, 0, start)

                # initialize seen, frontier list
                seen = []
                frontier = [startNode]
                run = True

        # color background grey
        screen.fill(grey)

        for row in range(numOfRows):
            for column in range(numOfColumns):

                if gridMaze[row][column] == 1:
                    color = white
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin,(margin + height) * row + margin,width,height])

                elif gridMaze[row][column] == 2:
                    color = green
                    pygame.draw.rect(screen, color, [(margin + width) * column + margin,(margin + height) * row + margin,width,height])

                elif gridMaze[row][column] == 3:
                    color = red
                    pygame.draw.rect(screen, color, [(margin + width) * column + margin, (margin + height) * row + margin,width,height])

                elif gridMaze[row][column] == 4:
                    color = blue
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin,(margin + height) * row + margin,width,height])

                elif gridMaze[row][column] == 5:
                    color = magenta
                    # compute solution path cost
                    numOfTile=numOfTile+1
                    pygame.draw.rect(screen, color, [(margin + width) * column + margin,(margin + height) * row + margin,width,height])

                elif gridMaze[row][column] == 6:
                    color = orange
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin,(margin + height) * row + margin,width,height])

                else:
                    color = black
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin, (margin + height) * row + margin,width,height])

        # set limit to 60 frames per second
        clock.tick(60)

        # update screen
        pygame.display.flip()

        if finalStep == True:

            interrupt = True
            run = False

        elif run == True:

            detect=True
            # pick a node from the frontier
            currentNode = selectNode(frontier)
            gridMaze, frontier, seen, currentNode, detect = computePath(gridMaze, frontier, seen, currentNode,arrGoal,detect)


            if detect==False:
                    arrGoal.pop()
                    detect=True
            elif currentNode.position in arrGoal and detect==True: # if a* is at goal then finish
                    a,b=currentNode.position
                    temp=currentNode.position
                    count=0
                    liste=[]
                    liste.append(temp)
                    while currentNode.parent != None:
                        x, y = currentNode.position
                        liste.append(currentNode.position)
                        count=count+1
                        currentNode = currentNode.parent
                    paths.append(Shortest(liste))
                    arrGoal.remove(temp)


            if len(arrGoal) <= 0:
                min=16000
                if len(paths)== 0:
                    finalStep=True
                else:
                    for sol in paths:
                        if len(sol.yol) < min:
                            min=len(sol.yol)
                            print(len(sol.yol))
                            obj=Shortest(sol.yol)
                    finalStep=True
                    # Show the shortest path
                    for s in obj.yol:
                        x,y=s
                        gridMaze[x][y]=5

            # control speed of the update
            sleep(0.01)

    print("NUMBER OF TİLES TO TARGET -----> ",numOfTile)
    print("NUMBER OF TİLES TO EXPAND  -----> ", len(seen))

    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            # wait for user to press any key to start
            elif event.type == pygame.KEYDOWN:
                finish = True
    # so that it doesnt "hang" on exit
    pygame.quit()

    return gridMaze,numOfTile,len(seen)
