import pygame
import random
import os
import math
from colour import Color
import time

import editingImage
import functions

class playerClass(editingImage.SpriteSheetClass):
    def __init__(self,screenObject):
        self.sheet = pygame.image.load('images/game/spaceship.png').convert_alpha()
        self.steps = [5,5,5]

        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()
        
        self.playerSize = {"width": 40, "height": 60}
        self.speed = 10
        self.health = 0

        self.balance = 0.00

        self.playerPos = {"x": int(self.screen.get_width() / 2),
                          "y": self.gameSize["height"] - self.playerSize["height"] * self.scale}

        self.sprite = 0

        self.bullets = []
        self.hits = 0
        self.enemiesDown = 0
        self.bulletDamage = 1

        self.cooldown = 5
        self.coolDownCount = 0

        self.playerDirection = ""
        self.starsDirectionX,self.starsDirectionY = 0,1
        self.enemyDirectionX,self.enemyDirectionY = 0,1
        self.backgroundSpeed = 0.5
        self.coinDirectionX, self.coinDirectionY = 0,1
        self.billDirectionX, self.billDirectionY = 0,1

        self.coinsCount = 0
        self.billsCount = 0

        self.score = 0
        self.lastUpdateScore = pygame.time.get_ticks()
        self.ticksScore = 1000
        self.dificultyCount = 0
        self.dificulty = 30

    def reloadGameData(self,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()

        self.playerPos = {"x": int(self.screen.get_width() / 2),
                          "y": self.gameSize["height"] - self.playerSize["height"] * self.scale}

    def getAllObjectList(self,playerList,enemyList,enemyObjectList,moneyObject):
        self.playerList = playerList
        self.enemyList = enemyList
        self.enemyObjectList = enemyObjectList

        self.moneyObject = moneyObject
        self.billList = moneyObject.billList
        self.coinList = moneyObject.coinList

    def returnBackgroundSpeed(self):
        return self.backgroundSpeed

    def returnEnemySpeed(self):
        return self.enemyDirectionX,self.enemyDirectionY

    def returnStarsSpeed(self):
        return self.starsDirectionX,self.starsDirectionY

    def returnCoinSpeed(self):
        return self.coinDirectionX, self.coinDirectionY

    def returnBillSpeed(self):
        return self.billDirectionX, self.billDirectionY

    def calculateEnemiesDown(self):
        for enemy in self.enemyObjectList:
            self.enemiesDown += enemy.enemiesDown

    def playerScore(self):
        if functions.timeCooldown(self.ticksScore,self.lastUpdateScore):
            self.lastUpdateScore = pygame.time.get_ticks()
            self.score += 1
            self.dificultyCount += 1

            if self.dificultyCount >= 20:
                self.dificulty += 1
                self.dificultyCount = 0


    def playerHealth(self):
        if self.health == 1:
            self.speed = 7.5
        elif self.health == 2:
            self.speed = 5

    def checkEventPlayer(self):
        self.playerHealth()

        if self.playerDirection == "right":
            self.playerPos["x"] += self.speed
            self.starsDirectionX = -1
            self.enemyDirectionX = -0.25
            self.coinDirectionX = -1
            self.billDirectionX = -1
            
            self.sprite = 1
        elif self.playerDirection == "left":
            self.playerPos["x"] -= self.speed
            self.starsDirectionX = 1
            self.enemyDirectionX = 0.25
            self.coinDirectionX = 1
            self.billDirectionX = 1

            self.sprite = 2
        elif self.playerDirection == "up":
            self.playerPos["y"] -= self.speed
            self.starsDirectionY = 1.5  
            self.enemyDirectionY = 1.5
            self.backgroundSpeed = 1
            self.coinDirectionY = 1.5
            self.billDirectionY = 1.5

            self.sprite = 3 
        elif self.playerDirection == "down":
            self.playerPos["y"] += self.speed
            self.starsDirectionY = 0.5
            self.enemyDirectionY = 0.5
            self.backgroundSpeed = 0.2
            self.coinDirectionY = 0.5
            self.billDirectionY = 0.5

            self.sprite = 4  
        elif self.playerDirection == "":
            self.starsDirectionX,self.starsDirectionY = 0,1
            self.enemyDirectionX,self.enemyDirectionY = 0,1
            self.backgroundSpeed = 0.5
            self.coinDirectionX, self.coinDirectionY = 0,1
            self.billDirectionX, self.billDirectionY = 0,1

            self.sprite = 0

    def movePlayer(self):
        keys = pygame.key.get_pressed()

        self.shooting(keys)
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.playerPos["x"] <= self.end["x"] - self.playerSize["width"] * self.scale:
            self.playerDirection = "right"

            self.checkEventPlayer()
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.playerPos["x"] >= self.start["x"]:
            self.playerDirection = "left"
            
            self.checkEventPlayer()
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.playerPos["y"] >= self.start["y"]:
            self.playerDirection = "up"

            self.checkEventPlayer()
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.playerPos["y"] <= self.end["y"] - self.playerSize["height"] * self.scale:
            self.playerDirection = "down"
            
            self.checkEventPlayer()
        else:
            self.playerDirection = ""

            self.checkEventPlayer()

    def colisionsEnemys(self):
        playerMask = self.playerList[self.health][self.sprite][1]
        for enemy in self.enemyObjectList:
            enemyMask = self.enemyList[enemy.typeOfenemy][enemy.health][1]
            colisions = functions.detectColision(enemyMask,(enemy.enemyPos["x"],enemy.enemyPos["y"]),playerMask,(self.playerPos["x"],self.playerPos["y"]))

            if colisions:
                enemy.destruccionAnimation()
                enemy.reset()
                
                self.playerPos = {"x": int(self.screen.get_width() / 2),
                                  "y": self.gameSize["height"] - self.playerSize["height"] * self.scale}

                if  not self.health >= 2:
                    self.health += 1
                else:
                    self.screenObject.runGame = False
                    self.screenObject.gameOver = True
                    self.health = 0
                    self.reloadGameData(self.screenObject)

    def sameXCor(self,enemy,bulletsList):
        ValidA,ValidB = False, False
        for bullet in bulletsList:
            if bulletsList.index(bullet) == 0:
                if bullet.x >= enemy.enemyPos["x"] and bullet.x <= enemy.enemyPos["x"] + enemy.enemySize["width"]* self.scale:
                    ValidA = True
            elif bulletsList.index(bullet) == 1:
                if bullet.x >= enemy.enemyPos["x"] and bullet.x <= enemy.enemyPos["x"] + enemy.enemySize["width"]* self.scale:
                    ValidB = True

        if ValidA and ValidB:
            return True
        else:
            return False

    def colisionsBullet(self):
        for enemy in self.enemyObjectList:
            enemyMask = self.enemyList[enemy.typeOfenemy][enemy.health][1]
            for bulletsList in self.bullets:

                sameColision = self.sameXCor(enemy,bulletsList)
                for bullet in bulletsList:

                    bulletMask = bullet.mask
                    
                    colisions = functions.detectColision(enemyMask,(enemy.enemyPos["x"],enemy.enemyPos["y"]),bulletMask,(bullet.x, bullet.y)) 

                    if colisions:

                        if enemy.health == 2:
                            self.moneyObject.createMoneyObjects(enemy.enemyPos, enemy.enemySize)

                            self.score += 10
                            self.dificultyCount += 200

                        if not sameColision:
                            a = self.bullets.index(bulletsList)
                            b = bulletsList.index(bullet)
                            self.bullets[a].remove(self.bullets[a][b])
                            self.hits += 1
                            enemy.loseHealth(self.bulletDamage)
                        else:
                            if enemy.health == 2:
                                a = self.bullets.index(bulletsList)
                                self.bullets.remove(self.bullets[a])
                                self.hits += 1
                                enemy.loseHealth(self.bulletDamage)
                                break
                            else:
                                a = self.bullets.index(bulletsList)
                                b = bulletsList.index(bullet)
                                self.bullets[a].remove(self.bullets[a][b])
                                self.hits += 1
                                enemy.loseHealth(self.bulletDamage)

    def colisionsMoney(self):
        playerMask = self.playerList[self.health][self.sprite][1]
        for bill in self.billList:
            if bill.outOfLine == True:
                self.billList.remove(bill)
                break
            billMask = bill.mask 
            
            colisions = functions.detectColision(billMask,(bill.billPos["x"],bill.billPos["y"]),playerMask,(self.playerPos["x"],self.playerPos["y"])) 

            if colisions:
                self.billsCount += 1
                self.billList.remove(bill)

        for coin in self.coinList:
            if coin.outOfLine == True:
                self.coinList.remove(coin)
                break
            coinMask = coin.mask 
            
            colisions = functions.detectColision(coinMask,(coin.coinPos["x"],coin.coinPos["y"]),playerMask,(self.playerPos["x"],self.playerPos["y"])) 

            if colisions:
                self.coinsCount += 1
                self.coinList.remove(coin)

        if self.coinsCount == 10:
            self.billsCount += 1
            self.coinsCount = 0

        self.moneyObject.coinsCount = self.coinsCount
        self.moneyObject.billsCount = self.billsCount

        self.moneyObject.playerScore = self.score

    def shooting(self,keys):
        self.coolDownCount = functions.cooldown(self.coolDownCount,self.cooldown)
        if keys[pygame.K_SPACE] and self.coolDownCount == 0:
            bullet1Pos = [self.playerPos["x"]+4*self.scale,self.playerPos["y"]+6]
            bullet2Pos = [self.playerPos["x"]+29*self.scale,self.playerPos["y"]+6]

            bullet1 = Bullet(bullet1Pos[0], bullet1Pos[1],self.screenObject)
            bullet2 = Bullet(bullet2Pos[0], bullet2Pos[1],self.screenObject)

            tempList = []

            tempList.append(bullet1)
            tempList.append(bullet2)

            self.bullets.append(tempList)
            
            self.coolDownCount = 1

        for bulletsList in self.bullets:
            for bullet in bulletsList:
                bullet.draw()
                bullet.move()

                if bullet.off_screen():
                    a = self.bullets.index(bulletsList)
                    b = bulletsList.index(bullet)
                    self.bullets[a].remove(self.bullets[a][b])

    def printPlayer(self):
        self.screen.blit(self.playerList[self.health][self.sprite][0],(self.playerPos["x"],self.playerPos["y"]))

class Bullet(object):
    def __init__(self,x, y,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()

        self.x = x
        self.y = y

        self.speed = 30

        self.directionX, self.directionY = 0,-1

        bulletImg = pygame.image.load('images/game/bullet.png')
        bullet = editingImage.SpriteSheetClass(bulletImg)
        self.sheet, self.mask = bullet.getImage(0,bulletImg.get_width(),bulletImg.get_height(),self.screenObject)

    def move(self):
        self.y += (self.speed * self.directionY)
        self.x += (self.speed * self.directionX)

    def draw(self):
        self.screen.blit(self.sheet,(self.x,self.y))

    def off_screen(self):
        return not(self.end["y"] >= self.y >= self.start["y"])

    def reloadGameData(self,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()
