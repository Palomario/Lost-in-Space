import pygame
import random

import editingImage

class Money(object):
    def __init__(self,howManyCoins,howManyBills,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()      

        self.howManyBills = howManyBills
        self.howManyCoins = howManyCoins

        self.billList = []
        for billCount in range(self.howManyBills):
            bill = Bill(self.screenObject)
            self.billList.append(bill)

        self.coinList = []
        for coinCount in range(self.howManyCoins):
            coin = Coin(self.screenObject)
            self.coinList.append(coin)

    def reloadGameData(self,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()   

        self.billList = []
        for billCount in range(self.howManyBills):
            bill = Bill(self.screenObject)
            self.billList.append(bill)

        self.coinList = []
        for coinCount in range(self.howManyCoins):
            coin = Coin(self.screenObject)
            self.coinList.append(coin)

    def printMoneyAnimations(self):
        for bill in self.billList:
            bill.printBill()

        for coin in self.coinList:
            coin.printCoin()

class Bill(object):
    def __init__(self,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()      

        self.billImg = pygame.image.load('images/game/billAnimation.png').convert_alpha()
        self.billSteps = [6] 

        self.billSize = {"width": 38,"height": 20}
        self.billPos = {"x": random.randint(self.start["x"],self.end["x"] - int(self.billSize["width" ] * self.scale)), 
                        "y": random.randint(self.start["y"],int(self.end["y"] / 4) - int(self.billSize["height"] * self.scale))}

        self.ticks = 100
        self.onlyOnce = False

        self.billAnimation = editingImage.AnimationClass((self.billPos["x"], self.billPos["y"]),self.billImg,self.billSteps,(self.billSize["width"], self.billSize["height"]),self.ticks,self.onlyOnce,self.screenObject)

        self.directionX, self.directionY = 0,0
        self.speed = 2

    def reloadGameData(self,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()

        self.billPos = {"x": random.randint(self.start["x"],self.end["x"] - int(self.billSize["width" ] * self.scale)), 
                        "y": random.randint(self.start["y"],self.end["y"] - int(self.billSize["height"] * self.scale))}

    def reset(self):
        self.billPos = {"x": random.randint(self.start["x"],self.end["x"] - int(self.billSize["width" ] * self.scale)), 
                        "y": random.randint(self.start["y"],int(self.end["y"] / 4) - int(self.billSize["height"] * self.scale))}

        self.billAnimation.pos = (self.billPos["x"], self.billPos["y"])

    def printBill(self):
        self.mask = self.billAnimation.printAnimation()

class Coin(object):
    def __init__(self,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()      

        self.coinImg = pygame.image.load('images/game/coinAnimation.png').convert_alpha()
        self.coinSteps = [7]

        self.coinSize = {"width": 15,"height": 15}
        self.coinPos = {"x": random.randint(self.start["x"],self.end["x"] - int(self.coinSize["width" ] * self.scale)), 
                        "y": random.randint(self.start["y"],self.end["y"] - int(self.coinSize["height"] * self.scale))}

        self.ticks = 100
        self.onlyOnce = False

        self.coinAnimation = editingImage.AnimationClass((self.coinPos["x"], self.coinPos["y"]),self.coinImg,self.coinSteps,(self.coinSize["width"], self.coinSize["height"]),self.ticks,self.onlyOnce,self.screenObject)

        self.directionX, self.directionY = 0,0
        self.speed = 5

    def reloadGameData(self,screenObject):
        self.screenObject = screenObject
        self.screenSize,self.gameSize,self.scale,self.screen,self.start,self.end,self.runGame = self.screenObject.returnGameData()

        self.coinPos = {"x": random.randint(self.start["x"],self.end["x"] - int(self.coinSize["width" ] * self.scale)), 
                        "y": random.randint(self.start["y"],self.end["y"] - int(self.coinSize["height"] * self.scale))}

    def reset(self):
        self.coinPos = {"x": random.randint(self.start["x"],self.end["x"] - int(self.coinSize["width" ] * self.scale)), 
                        "y": random.randint(self.start["y"],self.end["y"] - int(self.coinSize["height"] * self.scale))}

        self.coinAnimation.pos = (self.coinPos["x"], self.coinPos["y"])

    def printCoin(self):
        self.mask = self.coinAnimation.printAnimation()
