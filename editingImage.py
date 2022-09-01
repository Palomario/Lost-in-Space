import pygame
import random 
import os
from colour import Color
import math
import time

import functions

pygame.init()

class SpriteSheetClass(object):
    def __init__(self,image):
        self.sheet = image

    def getImage(self,frame,width,height,screenObject):
        green = [0,255,0]

        gameData = screenObject.returnGameData()
        scale = gameData[2]

        image = pygame.Surface((width,height)).convert_alpha()

        image.blit(self.sheet, (0,0), ((frame*width),0, width, height))

        image = pygame.transform.scale(image, (width * scale, height * scale))

        image.set_colorkey(green)

        mask = pygame.mask.from_surface(image)

        return image,mask

class Particles(object):
    def __init__(self,screenObject):
        self.screenObject = screenObject
        gameData = self.screenObject.returnGameData()
        self.screen = gameData[3]
        self.start = gameData[4]

        mauseCor = pygame.mouse.get_pos()
        self.localitation = [mauseCor[0],mauseCor[1]]

        self.velocity = [random.randint(0,20) / 10 - 1.0, -2.0]

        self.timer = random.randint(4,6)

        self.colorsParticles = [[179, 201, 212], [209, 235, 248], 
                         [255, 255, 255], [191, 227, 234]]

        self.color = random.choice(self.colorsParticles)

    def reloadGameData(self,screenObject):
        self.screenObject = screenObject
        gameData = self.screenObject.returnGameData()
        self.gameSize = gameData[1]
        self.scale = gameData[2]
        self.screen = gameData[3]
        self.start = gameData[4]
        self.end = gameData[5]


    def printParticles(self):
        self.localitation[0] += self.velocity[0]
        self.localitation[1] += self.velocity[1]
        self.velocity[1] += 0.1
        self.timer -= 0.1

        pygame.draw.circle(self.screen, self.color, self.localitation, int(self.timer))

        if self.timer <= 0:
            self.timer = random.randint(4,6)
            self.velocity = [random.randint(0,20) / 10 - 1, -2]
            mauseCor = pygame.mouse.get_pos()
            self.localitation = [mauseCor[0],mauseCor[1]]
            self.color = random.choice(self.colorsParticles)

class AnimationClass(object):
    def __init__(self,pos,image,animationSteps,animationSize,ticks,screenObject):
        self.screenObject = screenObject
        gameData = self.screenObject.returnGameData()
        self.gameSize = gameData[1]
        self.scale = gameData[2]
        self.screen = gameData[3]
        self.start = gameData[4]
        self.end = gameData[5]

        self.animationSize = animationSize

        self.lastUpdate = pygame.time.get_ticks()

        self.sheet = image
        self.pos = pos

        self.ticks = ticks

        self.frame = 0
        self.animationSteps = animationSteps

        self.animation = SpriteSheetClass(image)
        self.animationList = functions.listCreator(self.animationSteps,self.animation,self.animationSize[0],self.animationSize[1],self.screenObject)

        self.done = False

    def printAnimation(self):
        if functions.timeCooldown(self.ticks,self.lastUpdate):

            self.lastUpdate = pygame.time.get_ticks()
            self.frame += 1
            self.done = False
            if self.frame >= len(self.animationList):
                self.frame = 0
                self.done = True

        if not self.done:
            self.screen.blit(self.animationList[self.frame][0], self.pos)

