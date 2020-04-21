import pygame
import numpy as np
import time

pygame.init()

width, height = 600, 600

screen = pygame.display.set_mode((width, height))

bg = 25, 25, 25

screen.fill(bg)

nxC, nyC = 50, 50

dimCW = (width-1) / nxC
dimCH = (height-1) / nyC

gameState = np.zeros((nxC, nyC))

# automata que se mueve
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

pauseExect = False
endGame = False

clock = pygame.time.Clock()


def dibujar(x, y):

    poly = [
        ((x)   * dimCW,  y    * dimCH),
        ((x+1) * dimCW,  y    * dimCH),
        ((x+1) * dimCW, (y+1) * dimCH),
        ((x)   * dimCW, (y+1) * dimCH)
    ]

    if newGameState[x, y] == 0:
        pygame.draw.polygon(screen, (25, 25, 25), poly, 0)
        pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
    else:
        pygame.draw.polygon(screen, (255, 255, 255), poly, 0)


while not endGame:

    newGameState = np.copy(gameState)

    time.sleep(0.1)
    #clock.tick(20)

    # Eventos
    ev = pygame.event.get()

    for event in ev:

        if event.type == pygame.QUIT:
            endGame = True

        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:

            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))

            newGameState[celX, celY] = not gameState[celX, celY]

            dibujar(celX, celY)

    if not pauseExect:

        for y in range(0, nyC):
            for x in range(0, nxC):

                # Calculo de vecinos
                n_neigh = gameState[(x-1) % nxC, (y-1) % nyC] + \
                        gameState[(x)   % nxC, (y-1) % nyC] + \
                        gameState[(x+1) % nxC, (y-1) % nyC] + \
                        gameState[(x-1) % nxC, (y)   % nyC] + \
                        gameState[(x+1) % nxC, (y)   % nyC] + \
                        gameState[(x-1) % nxC, (y+1) % nyC] + \
                        gameState[(x)   % nxC, (y+1) % nyC] + \
                        gameState[(x+1) % nxC, (y+1) % nyC]

                # Reglas
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                if gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

                dibujar(x, y)

    gameState = np.copy(newGameState)
            
    pygame.display.flip()
