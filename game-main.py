import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import FPSM

from objloader import *

import math

from numpy import *

class Tower:
    def __init__(self, tLX, tLZ, height, bp, r = 1):
        self.tLX = tLX
        self.tLZ = tLZ
        self.height = height
        self.bp = bp
        self.r = r
        
        self.TABVerts = [
            [(self.tLX - 1)/self.r, self.bp + self.height, self.tLZ/self.r],
            [(self.tLX - 2)/self.r, self.bp + self.height, self.tLZ/self.r],
            [(self.tLX - 3)/self.r, self.bp + self.height, (self.tLZ + 1)/self.r],
            [(self.tLX - 3)/self.r, self.bp + self.height, (self.tLZ + 2)/self.r],
            [(self.tLX - 2)/self.r, self.bp + self.height, (self.tLZ + 3)/self.r],
            [(self.tLX - 1)/self.r, self.bp + self.height, (self.tLZ + 3)/self.r],
            [self.tLX/self.r, self.bp + self.height, (self.tLZ + 2)/self.r],
            [self.tLX/self.r, self.bp + self.height, (self.tLZ + 1)/self.r],
            [(self.tLX - 1)/self.r, self.bp, self.tLZ/self.r],
            [(self.tLX - 2)/self.r, self.bp, self.tLZ/self.r],
            [(self.tLX - 3)/self.r, self.bp, (self.tLZ + 1)/self.r],
            [(self.tLX - 3)/self.r, self.bp, (self.tLZ + 2)/self.r],
            [(self.tLX - 2)/self.r, self.bp, (self.tLZ + 3)/self.r],
            [(self.tLX - 1)/self.r, self.bp, (self.tLZ + 3)/self.r],
            [self.tLX/self.r, self.bp, (self.tLZ + 2)/self.r],
            [self.tLX/self.r, self.bp, (self.tLZ + 1)/self.r]
            ]

        self.towerSurfaces = [
            [0, 1, 2, 3, 4, 5, 6, 7],
            [8, 9, 10, 11, 12, 13, 14, 15]
            ]
        
        self.towerSideSurfaces = [
            [0, 8, 9, 1],
            [1, 9, 10, 2],
            [2, 10, 11, 3],
            [3, 11, 12, 4],
            [4, 12, 13, 5],
            [5, 13, 14, 6],
            [6, 14, 15, 7],
            [7, 15, 8, 0]
            ]
        
    def draw(self):
        ## draw top polygon
        glBegin(GL_POLYGON)
        glColor3fv((1, 0.54, 0.48))
        
        for vertex in self.towerSurfaces[0]:
            glMaterialfv(GL_FRONT,GL_SHININESS,(1,0,1,1));
            glVertex3fv(self.TABVerts[vertex])
            
        glEnd()
        ## draw bottom polygon
        glBegin(GL_POLYGON)
        glColor3fv((0.988, 0.256, 0.404))
        
        for vertex in self.towerSurfaces[1]:
            glVertex3fv(self.TABVerts[vertex])
            
        glEnd()
        ## connect the top and bottom
        glBegin(GL_QUADS)
        glColor3fv((0.55, 0.42, 0.36))
        
        for surface in self.towerSideSurfaces:
            for vertex in surface:
                glVertex3fv(self.TABVerts[vertex])
                
        glEnd()

    def __add__(self, otherTower):
        #priorities of tower connection: 1. left to right 2. top to bottom (seen from birds eye view)
        #dynamically connect two towers, given just their TABVerts
        xDifference = self.TABVerts[0][0] - otherTower.TABVerts[0][0]
        zDifference = self.TABVerts[0][2] - otherTower.TABVerts[0][2]
        
        if xDifference == 0 and zDifference <= 0:
            glBegin(GL_QUADS)
            glColor3fv((0.96, 0.69, 0.42))

            glVertex3fv(self.TABVerts[5])
            glVertex3fv(otherTower.TABVerts[0])
            glVertex3fv(otherTower.TABVerts[1])
            glVertex3fv(self.TABVerts[4])

            glEnd()

        elif xDifference >= 0 and zDifference >= 0:
            glBegin(GL_QUADS)
            glColor3fv((0.96, 0.69, 0.42))

            glVertex3fv(self.TABVerts[3])
            glVertex3fv(otherTower.TABVerts[6])
            glVertex3fv(otherTower.TABVerts[7])
            glVertex3fv(self.TABVerts[2])

            glEnd()

        elif xDifference >= 0 and zDifference <= 0:
            glBegin(GL_QUADS)
            glColor3fv((0.96, 0.69, 0.42))

            glVertex3fv(self.TABVerts[4])
            glVertex3fv(otherTower.TABVerts[7])
            glVertex3fv(otherTower.TABVerts[0])
            glVertex3fv(self.TABVerts[3])

            glEnd()

        elif xDifference <= 0 and zDifference <= 0:
            glBegin(GL_QUADS)
            glColor3fv((0.96, 0.69, 0.42))

            glVertex3fv(self.TABVerts[6])
            glVertex3fv(otherTower.TABVerts[1])
            glVertex3fv(otherTower.TABVerts[2])
            glVertex3fv(self.TABVerts[5])

            glEnd()

    def collHandle(self, cx, cz, ms):
        if cz > self.TABVerts[0][2] and cz < self.TABVerts[0][2] + .5 and cx < self.TABVerts[0][0] and cx > self.TABVerts[1][0]:
            ##print("LEFT")
            glTranslatef(0,0,ms)
        elif cz < self.TABVerts[5][2] and cz > self.TABVerts[5][2] - .5 and cx < self.TABVerts[0][0] and cx > self.TABVerts[1][0]:
            ##print("RIGHT")
            glTranslatef(0,0,-ms)
        elif cz > self.TABVerts[7][2] and cz < self.TABVerts[6][2] and cx < self.TABVerts[7][0] and cx > self.TABVerts[7][0] - .5:
            ##print("TOP")
            glTranslatef(-ms,0,0)
        elif cz > self.TABVerts[7][2] and cz < self.TABVerts[6][2] and cx > self.TABVerts[3][0] and cx < self.TABVerts[3][0] + .5:
            ##print("BOTTOM")
            glTranslatef(ms,0,0)
            
        ## TODO: IMPROVE AND UNCOMMENT THE COLLISION HANDLING BELOW (DIAGONAL TOWER SIDES)
        
##        elif cx > self.TABVerts[0][0] and cx < self.TABVerts[0][0] + (0.5/self.r) and cz > self.TABVerts[0][2] + (0.5/self.r) and cz < self.TABVerts[7][2]:
##            print("TOPLEFT")
##            glTranslatef(-ms*2,0,ms*2)
##        elif cx > self.TABVerts[0][0] and cx < self.TABVerts[0][0] + (0.5/self.r) and cz > self.TABVerts[6][2] and cz < self.TABVerts[6][2] + (0.5/self.r):
##            print("TOPRIGHT")
##            glTranslatef(-ms*2,0,-ms*2)
##        elif cx > self.TABVerts[2][0] + (0.5/self.r) and cx < self.TABVerts[1][0] and cz > self.TABVerts[0][2] + (0.5/self.r) and cz < self.TABVerts[7][2]:
##            print("BOTLEFT")
##            glTranslatef(ms*2,0,ms*2)
##        elif cx > self.TABVerts[2][0] + (0.5/self.r) and cx < self.TABVerts[1][0] and cz > self.TABVerts[6][2] and cz < self.TABVerts[6][2] + (0.5/self.r):
##            print("BOTRIGHT")
##            glTranslatef(ms*2,0,-ms*2)

def main():
    pygame.init()

    wWidth = 1200
    wHeight = 800

    clock = pygame.time.Clock()

    window = pygame.display.set_mode((wWidth, wHeight), DOUBLEBUF|OPENGL)
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(90, wWidth/wHeight, 0.001, 100000.0)
    glMatrixMode(GL_MODELVIEW)

    glTranslatef(-8,-15,8)

    onBridges = True
    inAir = True
    rise = False
    moon = False
    fall = False
    landable = True
    inMoon = False
    
    obj = OBJ("moon.obj", swapyz=False)

    h = 0.1
    bp = 0
    hits = 0

    gameOn = True
    
    while gameOn:

        ms = .04
        tx = 0
        ty = 0
        tz = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    pass
                if event.key == pygame.K_1:
                    moon = True
                if event.key == pygame.K_2:
                    rise = True
                if event.key == pygame.K_3:
                    rise = False
                    fall = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inMoon:
                    pygame.mixer.music.load("hit.mp3")
                    pygame.mixer.music.play()
                    hits += 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            if inAir == False:
                if cy < (h + .5):
                    glTranslatef(0, -0.75, 0)
                if cy > (h + .5) and cy < (h + 1):
                    glTranslatef(0, -0.5, 0)
                if cy > (h + 1) and cy < (h + 1.5):
                    glTranslatef(0, -0.25, 0)
                if cy > (h + 1.5) and cy < (h + 2):
                    glTranslatef(0, -0.175, 0)
                    
        if keys[pygame.K_f]:
            if moon and fall:
                glTranslatef(0,-0.15,0)
                
        if keys[pygame.K_g]:
            ## NO GRAVITY (HIDDEN FEATURE)
            glTranslatef(0,-0.1,0)
            ## ms = .2
            
        if keys[pygame.K_LSHIFT]:
            ## SPRINT (HIDDEN FEATURE)
            ms = .06

        if rise:
            if h <= 6:
                h += 0.01
        if fall:
            if h >= 0.1:
                h -= 0.01

        if hits == 10:
            gameOn = False

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        t1 = Tower(9, -9, h, bp)
        t2 = Tower(9, 6, h, bp)
        t3 = Tower(-6, 6, h, bp)
        t4 = Tower(-6, -9, h, bp)
        t5 = Tower(4, -4, h, bp, 2)
        t6 = Tower(4, 1, h, bp, 2)
        t7 = Tower(-1, 1, h, bp, 2)
        t8 = Tower(-1, -4, h, bp, 2)
        
        towerList = [t1, t2, t3, t4, t5, t6, t7, t8]

        for tower in towerList:
            tower.draw()

        t1 + t5
        t6 + t2
        t7 + t3
        t4 + t8
        t5 + t6
        t6 + t7
        t8 + t7
        t5 + t8

        if moon:
            glCallList(obj.gl_list)

        if h >= 1.8:
            moon = False

        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 0.8, 0.8, 1.0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 0.8, 0.8, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.15, 0, 0, 1.0))
        glLightfv(GL_LIGHT0, GL_POSITION, (200.0, 30.0, 200.0, 8.0))
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)


        ## FIRST PERSON MOVEMENT
        mov = FPSM.Spectator()
        mov.get_keys()
        mov.controls_3d(0,'w','s','a','d')
        
        matrix = mov.controls_3d(ms)
        cx = matrix[0]
        cy = matrix[1]
        cz = matrix[2]

        towerTouch = None

        for t in towerList:

            ## UNCOMMENT THE FOLLOWING IF YOU WISH TO KNOW WHICH PART OF THE "TOWER" YOU ARE ON
            
##            if cx > t.TABVerts[2][0] and cx < t.TABVerts[7][0] and cz > t.TABVerts[7][2] and cz < t.TABVerts[6][2]:
##                print("MIDDLE")
##            elif cx > t.TABVerts[1][0] and cx < t.TABVerts[0][0] and cz > t.TABVerts[0][2] and cz < t.TABVerts[7][2]:
##                print("LEFT")
##            elif cx > t.TABVerts[4][0] and cx < t.TABVerts[5][0] and cz > t.TABVerts[6][2] and cz < t.TABVerts[5][2]:
##                print("RIGHT")
##            elif cx > t.TABVerts[0][0] and cx < t.TABVerts[0][0] + (0.5/t.r) and cz > t.TABVerts[0][2] + (0.5/t.r) and cz < t.TABVerts[7][2]:
##                print("TOPLEFT")
##            elif cx > t.TABVerts[0][0] and cx < t.TABVerts[0][0] + (0.5/t.r) and cz > t.TABVerts[6][2] and cz < t.TABVerts[6][2] + (0.5/t.r):
##                print("TOPRIGHT")
##            elif cx > t.TABVerts[2][0] + (0.5/t.r) and cx < t.TABVerts[1][0] and cz > t.TABVerts[0][2] + (0.5/t.r) and cz < t.TABVerts[7][2]:
##                print("BOTLEFT")
##            elif cx > t.TABVerts[2][0] + (0.5/t.r) and cx < t.TABVerts[1][0] and cz > t.TABVerts[6][2] and cz < t.TABVerts[6][2] + (0.5/t.r):
##                print("BOTRIGHT")
            
            if cy < (h + bp):
                t.collHandle(cx, cz, ms)
                    
        if cx <= 9 and cx >= 6 and cz >= -9 and cz <= -6 and cx <= cz + 17 and cx <= -cz + 2 and cx >= cz + 13 and cx >= -cz - 2:
            ## T1
            towerTouch = t1
        elif cx <= 9 and cx >= 6 and cz <= 9 and cz >= 6 and cx <= -cz + 17 and cx <= cz + 2 and cx >= -cz + 13 and cx >= cz - 2:
            ## T2
            if fall:
                moon = True
                pygame.mixer.music.load("press_f.mp3")
                pygame.mixer.music.play()
                landable = True
            towerTouch = t2
        elif cx >= -9 and cx <= -6 and cz <= 9 and cz >= 6 and cx >= cz - 17 and cx <= -cz + 2 and cx <= cz - 13 and cx >= -cz - 2:
            ## T3
            if h > 5.9:
                rise = False
                fall = True
            towerTouch = t3
        elif cx >= -9 and cx <= -6 and cz >= -9 and cz <= -6 and cx >= -cz - 17 and cx <= cz + 2 and cx <= -cz - 13 and cx >= cz - 2:
            ## T4
            moon = True
            towerTouch = t4
        elif cz >= -2 and cz <= -0.5 and cx >= 0.5 and cx <= 2 and cx <= cz + 3.5 and cx <= -cz + 1 and cx >= cz + 1.5 and cx >= -cz - 1:
            ## T5
            towerTouch = t5
        elif cz <= 2 and cz >= 0.5 and cx >= 0.5 and cx <= 2 and cx <= -cz + 3.5 and cx <= cz + 1 and cx >= -cz + 1.5 and cx >= cz -1:
            ## T6
            towerTouch = t6
        elif cz <= 2 and cz >= 0.5 and cx <= -0.5 and cx >= -2 and cx >= cz - 3.5 and cx >= -cz - 1 and cx <= cz - 1.5 and cx <= -cz + 1:
            ## T7
            towerTouch = t7
        elif cz >= -2 and cz <= -0.5 and cx <= -0.5 and cx >= -2 and cx >= -cz - 3.5 and cx >= cz - 1 and cx <= -cz - 1.5 and cx <= cz + 1:
            ## T8
            towerTouch = t8

        if cx >= t5.TABVerts[4][0] and cx <= t5.TABVerts[5][0] and cz >= t5.TABVerts[5][2]and cz <= t6.TABVerts[0][2]:
            ## TOPLITBRIDGE
            onBridges = True
        elif cx >= t7.TABVerts[7][0] and cx <= t6.TABVerts[2][0] and cz >= t6.TABVerts[2][2]and cz <= t6.TABVerts[3][2]:
            ## RIGHTLITBRIDGE
            onBridges = True
        elif cx >= t8.TABVerts[4][0] and cx <= t8.TABVerts[5][0] and cz >= t8.TABVerts[1][2]and cz <= t7.TABVerts[0][2]:
            ## BOTTOMLITBRIDGE
            onBridges = True
        elif cx >= t8.TABVerts[7][0] and cx <= t5.TABVerts[2][0] and cz >= t5.TABVerts[2][2]and cz <= t5.TABVerts[3][2]:
            ## LEFTLITBRIDGE
            onBridges = True
        elif cx <= cz + 13 and cx >= (-0.9)*cz - 0.3 and cx <= (-10/9)*cz + (1/3) and cx >= cz + 3.5:
            ## TOPLEFTBIGBRIDGE
            onBridges = True
        elif cx <= -cz + 13 and cx >= (0.9)*cz - 0.3 and cx <= (10/9)*cz + (1/3) and cx >= -cz + 3.5:
            ## TOPRIGHTBIGBRIDGE
            onBridges = True
        elif cx >= cz - 13 and cx <= (-0.9)*cz + 0.3 and cx >= (-10/9)*cz - (1/3) and cx <= cz - 3.5:
            ## BOTRIGHTBRIDGE
            onBridges = True
        elif cx >= -cz - 13 and cx <= (0.9)*cz + 0.3 and cx >= (10/9)*cz - (1/3) and cx <= -cz - 3.5:
            ## BOTLEFTBRIDGE
            if moon:
                rise = True
            onBridges = True
        elif cx <= 0.5 and cx >= -0.5 and cz >= -0.5 and cz <= 0.5:
            if landable:
                if cy >= 0 and cy <= 3:
                    inMoon = True
                onBridges = True
        else:
            onBridges = False

        if towerTouch != None and cy > (h + bp + .2) and cy < (h + bp + .4) or onBridges == True and cy > (h + bp + .2) and cy < (h + bp + .4):
            if cy > (h + bp + .31):
                ty = .01
                if cy > (h + bp + .32):
                    ty = .02
                    if cy > (h + bp + .4):
                        ty = .1
                        if cy > (h + bp + .5):
                            ty = .2
                            if cy > (h + bp + 1):
                                ty = .5

            if cy < (h + bp + .29):
                glTranslatef(0, -((h + bp + .3) - cy), 0)

            if cy > (h + bp + .29) and cy < (h + bp + .31):
                inAir = False
            
        else:
            glTranslatef(0, 0.1, 0)

        if towerTouch != None or onBridges == True:
            if cy > (h + bp + 2):
                inAir = True

        if towerTouch == None and onBridges != True:
            inAir = True
        glTranslatef(tx,ty,tz)
        pygame.display.flip()
        clock.tick(100)

main()

pygame.mixer.music.load("scream_game_over.mp3")
pygame.mixer.music.play()

while True:
    if not pygame.mixer.music.get_busy():
        pygame.quit()
        quit()


