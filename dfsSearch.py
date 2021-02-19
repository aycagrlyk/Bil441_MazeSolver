
import os
import pygame
from time import sleep
from dfsSearchFunctions import convertMaze, computePath

def dfs() :

    numOfTile = 0
    arrGoal = []
    check = 0

    if check == 0:
        arr = os.listdir("mazes")
        for i in range(0, len(arr)):
            arr[i] = "mazes/" + arr[i]
        print(arr)
        select = input("Select one of them mazes 0-21\n")
        num = int(select)
        print(arr[num])
        numGoalStr = input("Select number of goal point \n")
        numGoal = int(numGoalStr)


    mazeFile = str(arr[num])
    gridMaze = convertMaze(mazeFile)
    numOfRows = len(gridMaze)
    numOfColumns = len(gridMaze[0])

    startPoint = False
    goalPoint = False
    seen = []
    backward = 0
    path = []

    # define the colors
    black = (0, 0, 0)  # grid == 0 for wall
    white = (255, 255, 255)  # grid == 1 for available tile
    green = (50, 205, 50)  # grid == 2 for start point
    red = (255, 99, 71)  # grid == 3 for goal points
    grey = (211, 211, 211)  # for background
    blue = (153, 255, 255)  # grid[x][y] == 4 for current position
    magenta = (255, 0, 255)  # grid[x][y] == 5 for solution
    orange = (255, 140, 0)  # grid == 6 for barrier

    # set the height/width of each location on the grid
    height = 15
    width = height  # i want the grid square
    margin = 1  # sets margin between grid locations

    # initialize pygame
    pygame.init()

    # congiguration of the window
    screen = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
    # screen title
    pygame.display.set_caption(f"DFS for. {mazeFile,}")

    # while running
    done = False
    run = False
    close = False

    # to manage how fast the screen updates
    clock = pygame.time.Clock()

    yol = []

    # program running
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN and run == False:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (width + margin)
                row = pos[1] // (height + margin)
                # Set that location to one
                if startPoint == False:
                    if gridMaze[row][column] == 1:
                        gridMaze[row][column] = 2
                        start = (row, column)
                        startPoint = True
                        currentNode = start
                        seen.append(currentNode)
                elif goalPoint == False:
                    if (numGoal == 0):
                        goalPoint = True
                    else:
                        if gridMaze[row][column] == 1:
                            gridMaze[row][column] = 3
                            goal = (row, column)
                            arrGoal.append(goal)
                            numGoal = numGoal - 1
                elif gridMaze[row][column] == 1 and startPoint == True and goalPoint == True:
                    gridMaze[row][column] = 6
                elif (gridMaze[row][column] == 0 or gridMaze[row][column] == 6) and startPoint == True and goalPoint == True:
                    gridMaze[row][column] = 1
            # wait for user to press any key to start
            elif event.type == pygame.KEYDOWN:
                run = True

        # color background  grey
        screen.fill(grey)

        for row in range(numOfRows):
            for column in range(numOfColumns):

                if gridMaze[row][column] == 1:
                    color = white
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin,(margin + height) * row + margin,width,height])

                elif gridMaze[row][column] == 2:
                    color = green
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin,(margin + height) * row + margin,width,height])

                elif gridMaze[row][column] == 3:
                    color = red
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin,(margin + height) * row + margin,width,height])

                elif gridMaze[row][column] == 4:
                    color = white
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin,(margin + height) * row + margin,width,height])

                elif gridMaze[row][column] == 5:
                    color = white
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin,(margin + height) * row + margin,width,height])

                else:
                    color = black
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin,(margin + height) * row + margin,width,height])

        # set limit to 60 frames per second
        clock.tick(60)

        # update screen
        pygame.display.flip()

        if run == True:
            # feed the algorithm the last updated position and the grid
            gridMaze, currentNode, backward, done, arrGoal = computePath(gridMaze, currentNode, seen, backward, arrGoal)
            if currentNode not in seen:
                seen.append(currentNode)



        sleep(0.01)
    #if (done == None):
     #       print("No solution!!!!!!!!")
      #      numOfTile=0
       #     done == True
    if (done == True):
        for row in range(numOfRows):
            for column in range(numOfColumns):
                if (gridMaze[row][column] == 5):
                    color = magenta
                    numOfTile = numOfTile + 1
                    pygame.draw.rect(screen, color,[(margin + width) * column + margin,(margin + height) * row + margin,width,height])

        # update screen
        pygame.display.flip()

        print("NUMBER OF TİLES TO TARGET -----> ", numOfTile)
        print("NUMBER OF TİLES TO EXPAND  -----> ", len(seen))

    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
            # wait for user to press any key to start
            elif event.type == pygame.KEYDOWN:
                close = True

    pygame.quit()

    return gridMaze,numOfTile,len(seen)