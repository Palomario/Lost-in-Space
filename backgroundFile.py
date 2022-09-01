import pygame
import random 
import os
from colour import Color
import math
import time

import functions

pygame.init()

class StarsClass(object):
    def __init__(self,screenObject):
        self.screenObject = screenObject
        gameData = self.screenObject.returnGameData()
        self.scale = gameData[2]
        self.screen = gameData[3]
        self.start = gameData[4]
        self.end = gameData[5]

        self.x = random.randrange(self.start["x"],self.end["x"])
        self.y = random.randrange(self.start["y"],self.end["y"])

        self.circleRadius = random.randrange(1,4)

        circlesColors = [[179, 201, 212], [209, 235, 248], 
                         [255, 255, 255], [191, 227, 234]]

        self.speed = random.randrange(1,10)
        self.color = random.choice(circlesColors)

    def moveCircle(self,directions):       
        circleDirectionX,circleDirectionY = directions

        self.x += (self.speed * circleDirectionX)
        self.y += (self.speed * circleDirectionY)

        if self.x > (self.end["x"]+10):
            self.x = random.randrange(self.start["x"]-10,self.start["x"]-1)

        if self.x < (self.start["x"]-10):
            self.x = random.randrange(self.end["x"],10+self.end["x"])

        if self.y > (self.end["y"]+10):
            self.y = random.randrange(self.start["y"]-10,self.start["y"]-1)

        if self.y < (self.start["y"]-10):
            self.y = random.randrange(self.end["y"],10+self.end["y"])

        pygame.draw.circle(self.screen,self.color,[self.x,self.y],self.circleRadius,0)

    def reloadGameData(self,screenObject):
        self.screenObject = screenObject
        gameData = self.screenObject.returnGameData()
        self.scale = gameData[2]
        self.screen = gameData[3]
        self.start = gameData[4]
        self.end = gameData[5]

        self.x = random.randrange(self.start["x"],self.end["x"])
        self.y = random.randrange(self.start["y"],self.end["y"])

class BackgroundClass(object):
    def __init__(self,image,screenObject):
        self.screenObject = screenObject
        gameData = self.screenObject.returnGameData()
        self.gameSize = gameData[1]
        self.scale = gameData[2]
        self.screen = gameData[3]
        self.start = gameData[4]
        self.end = gameData[5]

        self.bgHeight = image.get_height()
        self.bgWidth = image.get_width()

        self.green = [0,255,0]

        self.sheet = image
        self.sheet.set_colorkey(self.green)

        self.scroll = 0
        self.tiles = math.ceil(self.gameSize["height"] / self.bgHeight) +1
        
        self.black = Color("black")

    def scrollBackground(self,speed):       

        for i in range(1,self.tiles):
            self.screen.blit(self.sheet,(self.start["x"],(i * (-1) )* self.bgHeight - self.scroll))
            
        functions.transparentRectangle(self.black,pos=(self.start["x"],self.start["y"]),transparency=100,size=(self.gameSize["width"],self.gameSize["height"]),screenObject=self.screenObject)
        self.scroll -= speed

        if abs(self.scroll) > self.bgHeight + self.gameSize["height"]:
            self.scroll = 0

    def reloadGameData(self,screenObject):
        self.screenObject = screenObject
        gameData = self.screenObject.returnGameData()
        self.scale = gameData[2]
        self.screen = gameData[3]
        self.start = gameData[4]
        self.end = gameData[5]
