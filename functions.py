import pygame
import random
import os
from colour import Color
import time

import backgroundFile
import editingImage
import playerFile
import enemyFile
import gameData
import menu
import moneyFile

pygame.init()
pygame.font.init()

def frameworkScreen(screenObject):
    gameData = screenObject.returnGameData()

    screenSize = gameData[0]
    gameSize = gameData[1]
    screen = gameData[3]
    start = gameData[4]
    end = gameData[5]

    frameworkSize = 25

    colorA = [0, 90, 112]
    colorB = [36,121,142]
    if not screenSize["height"] == gameSize["height"]:
        pygame.draw.rect(screen, colorA,(0, 0, screenSize["width"], (screenSize["height"] - gameSize["height"]) / 2))
        pygame.draw.rect(screen, colorA,(0, ((screenSize["height"] - gameSize["height"]) / 2) + gameSize["height"] , screenSize["width"], screenSize["height"]))

        pygame.draw.rect(screen, colorB,(start["x"]-frameworkSize, start["y"]-frameworkSize, gameSize["width"]+frameworkSize, frameworkSize))
        pygame.draw.rect(screen, colorB,(start["x"], end["y"], gameSize["width"]+frameworkSize, frameworkSize))

    if not screenSize["width"] == gameSize["width"]:
        pygame.draw.rect(screen, colorA,(end["x"], start["y"], (screenSize["width"] - gameSize["width"]) / 2,gameSize["height"]))
        pygame.draw.rect(screen, colorA,(0, start["y"], (screenSize["width"] - gameSize["width"]) / 2,gameSize["height"]))

        pygame.draw.rect(screen, colorB,(end["x"], start["y"]-frameworkSize, frameworkSize, gameSize["height"]+frameworkSize))
        pygame.draw.rect(screen, colorB,(start["x"]-frameworkSize, start["y"], frameworkSize, gameSize["height"]+frameworkSize))

def listCreator(steps,object,width,height,screenObject) :
    stepCounter = 0
    if not len(steps) == 1:
        list = []
        
        for a in steps:
            tempImgList = []
            for _ in range(a):
                tempImgList.append(object.getImage(stepCounter,width,height,screenObject))
                
                stepCounter += 1
            list.append(tempImgList)

        return list
    else:
        
        for a in steps:
            tempImgList = []
            for _ in range(a):
                tempImgList.append(object.getImage(stepCounter,width,height,screenObject))
                
                stepCounter += 1
        return tempImgList

def cooldown(coolDownCount,number):
    if coolDownCount >= number:
        coolDownCount = 0
    elif coolDownCount > 0:
        coolDownCount += 1

    return coolDownCount

def timeCooldown(ticks,lastUpdate):
    currentTime = pygame.time.get_ticks()
    if currentTime - lastUpdate >= ticks:
        return True
    else:
        return False

def detectColision(mask1,pos1,mask2,pos2):
    overlaping = (pos1[0] - pos2[0], pos1[1] - pos2[1])
    result = mask2.overlap_area(mask1,overlaping)

    if result:
        return True

def transparentRectangle(colour,pos,size,transparency,screenObject):
    gameData = screenObject.returnGameData()
    screen = gameData[3]

    color = Color(colour)
    colorRGB = color.rgb

    rect = pygame.Surface(size)
    rect.fill(colorRGB)
    rect.set_alpha(transparency)
    screen.blit(rect, pos) 

def buildObjects(screenObject):
    stars = []
    for i in range(0,600):
        star = backgroundFile.StarsClass(screenObject)
        stars.append(star)

    money = moneyFile.Money(screenObject=screenObject)

    bg = pygame.image.load('images/game/bg.png').convert_alpha()
    planets = backgroundFile.BackgroundClass(bg,screenObject)
 
    player = playerFile.playerClass(screenObject)
    playerList = listCreator(player.steps,player,player.playerSize["width"],player.playerSize["height"],screenObject)

    enemyObjectList = []
    enemy = enemyFile.enemyClass(0,screenObject)
    for b in range(len(enemy.steps)):
        enemy = enemyFile.enemyClass(b,screenObject)
        enemyObjectList.append(enemy)

    enemyList = listCreator(enemyObjectList[0].steps,enemyObjectList[0],enemyObjectList[0].enemySize["width"],enemyObjectList[0].enemySize["height"],screenObject)

    return enemyList,enemyObjectList,playerList,player,planets,stars,money

def checkEvents(screenObject,objectList,specialEfect):
    gameData = screenObject.returnGameData()
    gameSize = gameData[1]
    runGame = gameData[6]

    mauseEvent = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.VIDEORESIZE:
            if event.w < gameSize["width"]:
                event.w = gameSize["width"]
            elif event.h < gameSize["height"]:
                event.h = gameSize["height"]

            screenSize = {"width": event.w, "height": event.h}
            screenObject.getGameData(screenSize)
            screenObject.calculateGameSize()

            enemyList,enemyObjectList,playerList,player,planets,stars,money = objectList

            for enemy in enemyObjectList:
                enemy.reloadGameData(screenObject)

            player.reloadGameData(screenObject)

            for bulletsList in player.bullets:
                for bullet in bulletsList:
                    bullet.reloadGameData(screenObject)

            planets.reloadGameData(screenObject)

            for i in range(0,600):
                stars[i].reloadGameData(screenObject)

            money.reloadGameData(screenObject)

            screenObject.paused = True

            mauseEvent = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if screenObject.runGame:
                    screenObject.gameOver = False
                    screenObject.runGame = False 
                    
                elif screenObject.gameOver:
                    screenObject.gameOver = False
                else: 
                    quit()
            elif event.key == pygame.K_p:
                screenObject.paused = not screenObject.paused
                menu.pauseMenu(screenObject,objectList)
            elif event.key == pygame.K_t:
                specialEfect = not specialEfect

        if event.type == pygame.MOUSEBUTTONDOWN:
            mauseEvent = True
            
    return specialEfect,mauseEvent
     

def writeText(text,fontSize,position,screenObject,color):
    screenSize,gameSize,scale,screen,start,end,runGame = screenObject.returnGameData()

    text = [word.split(' ') for word in text.splitlines()]

    pathFont = os.path.abspath('images/britannic-becker-bold.ttf')
    font = pygame.font.Font(pathFont, fontSize) 
    space = font.size(' ')[0]

    x, y = position
    for lines in text:

        for word in lines:

            newText = ""
            text = font.render(newText, True, color)
            textWidth, textHeight = text.get_size()

            otherText = newText
            for letter in word:
                screenSize,gameSize,scale,screen,start,end,runGame = screenObject.returnGameData()
                otherText += str(letter)
                
                text = font.render(otherText, True, color)
                textWidth, textHeight = text.get_size()

                if x + textWidth >= end["x"]:
                    x = position[0]
                    y += textHeight

                textRect = text.get_rect()
                textRect.topleft = (x, y)

            for letter in word:
                screenSize,gameSize,scale,screen,start,end,runGame = screenObject.returnGameData()

                newText += str(letter)                    
                
                text = font.render(newText, True, color)
                textWidth, textHeight = text.get_size()

                textRect = text.get_rect()
                textRect.topleft = (x, y)

                screen.blit(text, textRect)

                frameworkScreen(screenObject)

            x += textWidth + space
        x = position[0]
        y += 50

def writeTextWithAnimation(text,fontSize,position,screenObject,objectList,image,color):
    screenSize,gameSize,scale,screen,start,end,runGame = screenObject.returnGameData()

    text = [word.split(' ') for word in text.splitlines()]

    clock = pygame.time.Clock()

    pathFont = os.path.abspath('images/britannic-becker-bold.ttf')
    font = pygame.font.Font(pathFont, fontSize) 
    space = font.size(' ')[0]
    
    screen.blit(image,(start["x"],start["y"]))

    x, y = position
    for lines in text:

        for word in lines:

            newText = ""
            text = font.render(newText, True, color)
            textWidth, textHeight = text.get_size()

            otherText = newText
            for letter in word:
                specialEfect, mauseEvent = checkEvents(screenObject,objectList,specialEfect=False)
                screenSize,gameSize,scale,screen,start,end,runGame = screenObject.returnGameData()

                if mauseEvent:
                    break

                otherText += str(letter)                    
                
                text = font.render(otherText, True, color)
                textWidth, textHeight = text.get_size()

                if x + textWidth >= end["x"]:
                    x = position[0]
                    y += textHeight

                textRect = text.get_rect()
                textRect.topleft = (x, y)

            for letter in word:
                specialEfect, mauseEvent = checkEvents(screenObject,objectList,specialEfect=False)
                screenSize,gameSize,scale,screen,start,end,runGame = screenObject.returnGameData()

                if mauseEvent:
                    break

                newText += str(letter)                    
                
                text = font.render(newText, True, color)
                textWidth, textHeight = text.get_size()

                textRect = text.get_rect()
                textRect.topleft = (x, y)

                screen.blit(text, textRect)
                time.sleep(0.05)

                frameworkScreen(screenObject)

                pygame.display.update()
            if mauseEvent:
                break
            x += textWidth + space
            time.sleep(0.1)
        if mauseEvent:
            break
        x = position[0]
        y += 50

    if mauseEvent:
        pygame.display.update()
