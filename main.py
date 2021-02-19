import pygame
def main():
    from aStarSearch import aStar
    from dfsSearch import dfs
    from mazeCreater import mazeCreater
    select = input("Press 1 for create new maze or press 2 use old ones \n")
    if select==str(1):
        result=mazeCreater()
    else:

        grid, num , total= aStar()
        grid2,num2, total2 = dfs()

        if grid != None and grid2 != None :

            pygame.init()
            white = (255, 255, 255)
            green = (0, 255, 0)
            blue = (0, 0, 128)
            X = 800
            Y = 800
            display_surface = pygame.display.set_mode((X, Y))
            pygame.display.set_caption('path length')
            font = pygame.font.Font('freesansbold.ttf', 32)
            mesaj = "A* path: "+str(num)+" and expands node :"+ str(total)
            mesaj2= "DFS min path: "+str(num2)+" and expands node :"+ str(total2)
            text1 = font.render(mesaj, True, green, white)
            text2 = font.render(mesaj2,True,green,white)
            textRect1 = text1.get_rect()
            textRect1.center = (X//2, Y//2)
            textRect2 = text2.get_rect()
            textRect2.center = (X//2,Y//2 + 50)
            finish=False
            while not finish:
                display_surface.fill(white)
                display_surface.blit(text1, textRect1)
                display_surface.blit(text2, textRect2)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        finish = True
                    elif event.type == pygame.KEYDOWN:
                        finish = True
                    pygame.display.update()
            pygame.quit()

if __name__ == "__main__":
    main()