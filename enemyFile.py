import pygame
import random 
import os
import math
import time

import functions
import editingImage

pygame.init()

class enemyClass(editingImage.SpriteSheetClass):
    def __init__(self,typeOfenemy,screenObject):  
        self.sheet = pygame.image.load('images/game/enemies.png').convert_alpha()  
        self.steps = [3,3,3,3]

        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()

        self.enemySize = {"width": 50, "height": 50}
        self.speedFactor = (10,15)
        self.speed = random.randrange(self.speedFactor[0],self.speedFactor[1])
        self.typeOfenemy = typeOfenemy
        self.health = 0

        self.enemyPos = {"x": random.randint(self.start["x"], self.end["x"] - self.enemySize["width"] * self.scale),
                         "y": int(self.start["y"] - self.enemySize["height"] * self.scale)}
        self.enemiesDown = 0

        self.animationImg = pygame.image.load('images/game/explotion.png')
        self.explotionSteps = [8]
        self.destroyAnimationList = []
        self.ticks = 100
        self.onlyOnce = True

    def reloadGameData(self,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()

    def getEnemyDirections(self,directions):
        self.enemyDirectionX,self.enemyDirectionY = directions

    def outOfLine(self):
        self.enemyPos = {"x": random.randint(self.start["x"], self.end["x"] - self.enemySize["width"] * self.scale),
                         "y": int(self.start["y"] - self.enemySize["height"] * self.scale)}

        self.speed = random.randrange(self.speedFactor[0],self.speedFactor[1])
        self.health = 0
        self.enemyDirectionX,self.enemyDirectionY = 0,1

    def reset(self):
        self.health = 0
        self.speed = random.randrange(self.speedFactor[0],self.speedFactor[1])

        self.enemyPos = {"x": random.randint(self.start["x"], self.end["x"] - self.enemySize["width"] * self.scale),
                         "y": int(self.start["y"] - self.enemySize["height"] * self.scale)}

    def destruccionAnimation(self):
        self.exploutingAnimation = editingImage.AnimationClass((self.enemyPos["x"],self.enemyPos["y"]),self.animationImg,self.explotionSteps,(self.enemySize["width"], self.enemySize["height"]),self.ticks,self.onlyOnce,self.screenObject)
        self.destroyAnimationList.append(self.exploutingAnimation)

    def loseHealth(self,bulletDamage):
        self.health += 1

        if self.health > 2:
            self.health = int(bulletDamage)
            self.enemiesDown += 1

            self.destruccionAnimation()

            self.reset()

    def moveEnemy(self):
        self.enemyPos["y"] += (self.speed * self.enemyDirectionY)
        self.enemyPos["x"] += (self.speed * self.enemyDirectionX)

        if self.enemyPos["x"] > self.end["x"]:
            self.outOfLine()

        if self.enemyPos["x"] < self.start["x"] - self.enemySize["width"] * self.scale:
            self.outOfLine()

        if self.enemyPos["y"] > self.end["y"]:
            self.outOfLine()

        if self.enemyPos["y"] < self.start["y"] - self.enemySize["height"] * self.scale - 100:
            self.outOfLine()

    def printEnemy(self,enemyList):
        self.screen.blit(enemyList[self.typeOfenemy][self.health][0],(self.enemyPos["x"],self.enemyPos["y"]))
