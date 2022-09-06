import pygame
import random

import editingImage
import functions

class Money(object):
    def __init__(self,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()      

        bill = editingImage.SpriteSheetClass(pygame.image.load('images/game/bill.png').convert_alpha())
        self.billImg, billMask = bill.getImage(0,40,22,self.screenObject)

        coin = editingImage.SpriteSheetClass(pygame.image.load('images/game/coin.png').convert_alpha())
        self.coinImg, coinMask = coin.getImage(0,22,22,self.screenObject)

        self.provabilityList = ["bill","coin","coin","coin","coin","coin","coin","coin","coin","coin"]

        self.howManyBills = 0
        self.howManyCoins = 0

        self.billList = []
        for billCount in range(self.howManyBills):
            pos = {"x": random.randint(self.start["x"],self.end["x"] - 50 * self.scale), 
                   "y": random.randint(self.start["y"],self.end["y"] - 50 * self.scale)}

            bill = Bill(self.screenObject,pos)
            self.billList.append(bill)

        self.coinList = []
        for coinCount in range(self.howManyCoins):
            pos = {"x": random.randint(self.start["x"],self.end["x"] - 50 * self.scale), 
                   "y": random.randint(self.start["y"],self.end["y"] - 50 * self.scale)}

            coin = Coin(self.screenObject,pos)
            self.coinList.append(coin)

        self.coinsCount = 0
        self.billsCount = 0

    def createMoneyObjects(self,enemyPos,enemySize):
        change = random.choice(self.provabilityList)

        pos = {"x": enemyPos["x"] + enemySize["width"] / 2,
               "y": enemyPos["y"] + enemySize["height"] / 2}
        if change == "coin":
            coin = Coin(self.screenObject,pos)
            self.coinList.append(coin)
        elif change == "bill":
            bill = Bill(self.screenObject,pos)
            self.billList.append(bill)
        else:
            print("ERROR || Something is wrong call the technician || ERROR")

    def balancePlayer(self,typeOfMoney):
        if typeOfMoney == "bill":
            self.billsCount += 1
        elif typeOfMoney == "coin":
            self.coinsCount += 1

    def reloadGameData(self,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()   

        self.billList = []
        for billCount in range(self.howManyBills):
            pos = {"x": random.randint(self.start["x"],self.end["x"] - 50 * self.scale), 
                   "y": random.randint(self.start["y"],self.end["y"] - 50 * self.scale)}
            bill = Bill(self.screenObject,pos)
            self.billList.append(bill)

        self.coinList = []
        for coinCount in range(self.howManyCoins):
            pos = {"x": random.randint(self.start["x"],self.end["x"] - 50 * self.scale), 
                   "y": random.randint(self.start["y"],self.end["y"] - 50 * self.scale)}
            coin = Coin(self.screenObject,pos)
            self.coinList.append(coin)

    def moveMoney(self,coinDirectionX, coinDirectionY,billDirectionX, billDirectionY):

        for bill in self.billList:
            bill.moveBill(billDirectionX, billDirectionY)

        for coin in self.coinList:
            coin.moveCoin(coinDirectionX, coinDirectionY)

    def printMoneyAnimations(self):
        for bill in self.billList:
            bill.printBill()

        for coin in self.coinList:
            coin.printCoin()

        self.screen.blit(self.billImg, (self.start["x"],self.start["y"]))       
        self.screen.blit(self.coinImg, (self.start["x"] + 3,25 * self.scale + self.start["y"])) 

        functions.writeText(str(self.billsCount), 30,[self.start["x"] + self.billImg.get_width() + 10,self.start["y"]], self.screenObject)
        functions.writeText(str(self.coinsCount), 30,[self.start["x"] + self.coinImg.get_width() + 10,self.start["y"] + self.billImg.get_height()], self.screenObject)

class Bill(object):
    def __init__(self,screenObject,pos):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()      

        self.pos = pos

        self.billImg = pygame.image.load('images/game/billAnimation.png').convert_alpha()
        self.billSteps = [6] 

        self.billSize = {"width": 38,"height": 20}
        self.billPos = self.pos

        self.ticks = 100
        self.onlyOnce = False

        self.billAnimation = editingImage.AnimationClass((self.billPos["x"], self.billPos["y"]),self.billImg,self.billSteps,(self.billSize["width"], self.billSize["height"]),self.ticks,self.onlyOnce,self.screenObject)

        self.billDirectionX, self.billDirectionY = 0,0
        self.speed = 10

        self.outOfLine = False

    def reloadGameData(self,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()

        self.billPos = self.pos

    def moveBill(self,billDirectionX, billDirectionY):
        self.billDirectionX, self.billDirectionY = billDirectionX, billDirectionY
        
        self.billPos["x"] += (self.speed * self.billDirectionX)
        self.billPos["y"] += (self.speed * self.billDirectionY)

        if self.billPos["x"] > self.end["x"]:
            self.outOfLine = True

        if self.billPos["x"] < self.start["x"] - self.billSize["width"] * self.scale:
            self.outOfLine = True

        if self.billPos["y"] > self.end["y"]:
            self.outOfLine = True

        if self.billPos["y"] < self.start["y"] - self.billSize["height"] * self.scale - 100:
            self.outOfLine = True

        self.billAnimation.pos = (self.billPos["x"], self.billPos["y"])

    def reset(self):
        self.billPos = {"x": random.randint(self.start["x"],self.end["x"] - int(self.billSize["width" ] * self.scale)), 
                        "y": random.randint(self.start["y"],int(self.end["y"] / 4) - int(self.billSize["height"] * self.scale))}

        self.billAnimation.pos = (self.billPos["x"], self.billPos["y"])

    def printBill(self):
        self.mask = self.billAnimation.printAnimation()

class Coin(object):
    def __init__(self,screenObject,pos):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()      

        self.pos = pos

        self.coinImg = pygame.image.load('images/game/coinAnimation.png').convert_alpha()
        self.coinSteps = [7]

        self.coinSize = {"width": 15,"height": 15}
        self.coinPos = self.pos

        self.ticks = 100
        self.onlyOnce = False

        self.coinAnimation = editingImage.AnimationClass((self.coinPos["x"], self.coinPos["y"]),self.coinImg,self.coinSteps,(self.coinSize["width"], self.coinSize["height"]),self.ticks,self.onlyOnce,self.screenObject)

        self.coinDirectionX, self.coinDirectionY = 0,1
        self.speed = 5

        self.outOfLine = False

    def reloadGameData(self,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()

        self.coinPos = self.pos

    def moveCoin(self,coinDirectionX, coinDirectionY):
        self.coinDirectionX, self.coinDirectionY = coinDirectionX, coinDirectionY
        
        self.coinPos["x"] += (self.speed * self.coinDirectionX)
        self.coinPos["y"] += (self.speed * self.coinDirectionY)

        if self.coinPos["x"] > self.end["x"]:
            self.outOfLine = True

        if self.coinPos["x"] < self.start["x"] - self.coinSize["width"] * self.scale:
            self.outOfLine = True

        if self.coinPos["y"] > self.end["y"]:
            self.outOfLine = True

        if self.coinPos["y"] < self.start["y"] - self.coinSize["height"] * self.scale - 100:
            self.outOfLine = True

        self.coinAnimation.pos = (self.coinPos["x"], self.coinPos["y"])


    def reset(self):
        self.coinPos = {"x": random.randint(self.start["x"],self.end["x"] - int(self.coinSize["width" ] * self.scale)), 
                        "y": random.randint(self.start["y"],int(self.end["y"] / 4) - int(self.coinSize["height"] * self.scale))}

        self.coinAnimation.pos = (self.coinPos["x"], self.coinPos["y"])

    def printCoin(self):
        self.mask = self.coinAnimation.printAnimation()
