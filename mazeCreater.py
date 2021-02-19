
import pygame
from time import sleep
from mazeCreaterFunctions import createMaze

def mazeCreater():

    black = (0, 0, 0) # grid == 0 for walls
    white = (255, 255, 255) # grid == 1 for available tiles
    green = (50,205,50) # grid == 2 for start point
    red = (255,99,71) # grid == 3 for goal points
    grey = (211,211,211) # for background
    blue = (153,255,255) # grid[x][y] == 4 for current position

    height = 15
    width = height
    margin = 1

    # initialize the maze array
    maze = []
    numOfRows = 41
    numOfColumns = numOfRows
    for row in range(numOfRows):
        maze.append([])
        for column in range(numOfColumns):
            maze[row].append(0)

    done = False
    currentNode = (0, 0)
    seen = []
    seen.append(currentNode)
    backward = 0
    maze[0][0] = 1
    maze[-1][-1] = 1


    while not done:

        run = True

        if run == True:

            maze, currentNode, backward, done = createMaze(maze, currentNode, seen, backward)

            if currentNode not in seen:
                seen.append(currentNode)
            sleep(0.01)

            if (done == True):

                pygame.init()
                screen = pygame.display.set_mode((700, 700), pygame.RESIZABLE)
                pygame.display.set_caption("Generated Maze")
                clock = pygame.time.Clock()
                print("*************** MAZE CREATED ****************")
                screen.fill(grey)

                for row in range(numOfRows):
                    for column in range(numOfColumns):

                        if maze[row][column] == 1:
                            color = white
                            pygame.draw.rect(screen, color,
                                             [(margin + width) * column + margin,
                                              (margin + height) * row + margin,
                                              width,
                                              height])
                        elif maze[row][column] == 2:
                            color = green
                            pygame.draw.rect(screen, color,
                                             [(margin + width) * column + margin,
                                              (margin + height) * row + margin,
                                              width,
                                              height])
                        elif maze[row][column] == 3:
                            color = red
                            pygame.draw.rect(screen, color,
                                             [(margin + width) * column + margin,
                                              (margin + height) * row + margin,
                                              width,
                                              height])
                        elif maze[row][column] == 4:
                            color = blue
                            pygame.draw.rect(screen, color,
                                             [(margin + width) * column + margin,
                                              (margin + height) * row + margin,
                                              width,
                                              height])
                        else:
                            color = black
                            pygame.draw.rect(screen, color,
                                             [(margin + width) * column + margin,
                                              (margin + height) * row + margin,
                                              width,
                                              height])


                clock.tick(60)
                pygame.display.flip()
            else:
                print("CREATING...")

    close = False
    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
            if event.type == pygame.KEYDOWN:
                close = True
    pygame.quit()

    return 0