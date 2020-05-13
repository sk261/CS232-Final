import pygame
import requests
import math
from pygame import mixer, time

def runGame(serverID, un, pw):

    WINDOW_SIZE = [500, 500]
    INCOMING_SIZE = [100, 100]
    DRAW_SIZE = [WINDOW_SIZE[0]/INCOMING_SIZE[0], WINDOW_SIZE[1]/INCOMING_SIZE[1]]

    # Intialize the pygame
    pygame.init()

    # create the screen
    screen = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]))

    # Framerate
    clock = pygame.time.Clock()

    # Caption and Icon
    pygame.display.set_caption("Shay's Pixel Game")

    # Joystick initialization
    pygame.joystick.init()

    # Game Loop
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        joystick_count = pygame.joystick.get_count()
        actions = {}
        actions['un'] = un
        actions['pw'] = pw
        actions['moveX'] = 0
        actions['moveY'] = 0
        actions['controlX'] = 0
        actions['controlY'] = 0
        actions['breaking'] = 0
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            axes = joystick.get_numaxes()
            buttons = joystick.get_numbuttons()
            print("-------")
            for i in range(axes):
                a = joystick.get_axis(i)
                # 0 and 1 are movement horizontal and vertical
                # 4 and 3 are force bubble horizontal and vertical
                if i == 0:
                    actions['moveX'] = a
                elif i == 1:
                    actions['moveY'] = a
                elif i == 4:
                    actions['controlX'] = a
                elif i == 3:
                    actions['controlY'] = a
            for i in range(buttons):
                # Button 5 is mine
                b = joystick.get_button(i)
                if i == 5 and b:
                    actions['breaking'] = True

    
        x = requests.post(serverID + 'act', actions)

        try:
            x = requests.get(serverID + 'view', {'un':un, 'pw':pw})
            x = x.json()
        except:
            x = {}
            print("err")
            running = False

        if 'err' in x:
            if x['err'] == 1:
                running = False

        if 'pixelX' in x:
            screen.fill((0,0,0))
            p_X = x['pixelX'].split(',')
            p_Y = x['pixelY'].split(',')
            p_RGB = x['pixelRGB'].split(',')
            for p in range(len(p_X)):
                p_RGB[p] = p_RGB[p].split('|')
                p_RGB[p] = (int(p_RGB[p][0]), int(p_RGB[p][1]), int(p_RGB[p][2]))
                p_X[p] = float(p_X[p])
                p_Y[p] = float(p_Y[p])
                pygame.draw.rect(screen, p_RGB[p], pygame.Rect(
                    int(math.floor((INCOMING_SIZE[0]/2+p_X[p])*DRAW_SIZE[0])), 
                    int(math.floor((INCOMING_SIZE[1]/2+p_Y[p])*DRAW_SIZE[1])), 
                    DRAW_SIZE[0], DRAW_SIZE[1]))
            # Draw player
            pygame.draw.rect(screen, (255,255,255), pygame.Rect(WINDOW_SIZE[0]/2-DRAW_SIZE[0]/2, WINDOW_SIZE[0]/2-DRAW_SIZE[0]/2, DRAW_SIZE[0], DRAW_SIZE[1]))
            pygame.display.update()





        clock.tick(60)
