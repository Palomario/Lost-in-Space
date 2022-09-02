import pygame
import random
import os
from colour import Color
import time

import functions
import playerFile
import backgroundFile
import editingImage
import enemyFile
import gameData

pygame.init()

def mainMenu(screenObject):
    objectList = functions.buildObjects(screenObject)
    enemyList,enemyObjectList,playerList,player,planets,stars,money = objectList

    particles = []
    for a in range(200):
        particle = editingImage.Particles(screenObject)
        particles.append(particle)
        particle.printParticles()

    clock = pygame.time.Clock()

    playImg = pygame.image.load('images/mainMenu/play.png').convert_alpha()
    playImg.set_colorkey([0,255,0])

    optionsImg = pygame.image.load('images/mainMenu/options.png').convert_alpha()
    optionsImg.set_colorkey([0,255,0])

    exitImg = pygame.image.load('images/mainMenu/exit.png').convert_alpha()
    exitImg.set_colorkey([0,255,0])

    shopImg = pygame.image.load('images/mainMenu/shop.png').convert_alpha()
    shopImg.set_colorkey([0,255,0])

    mainMenu = pygame.image.load('images/mainMenu/mainMenu.png').convert_alpha()

    while True:
        if screenObject.runGame == True:
            theGame(screenObject)

        screenSize,gameSize,scale,screen,start,end,runGame = screenObject.returnGameData()

        specialEfect,mauseEvent = functions.checkEvents(screenObject,objectList,specialEfect=False)

        screen.blit(mainMenu,(start["x"],start["y"]))

        mauseCor = pygame.mouse.get_pos()
        mausePos = {"x": mauseCor[0], "y": mauseCor[1]}

        if 240+start["x"] <= mausePos["x"] <= 558+start["x"]:
            if 375+start["y"] <= mausePos["y"] <= 480+start["y"]:
                screen.blit(playImg,(240+start["x"],375+start["y"]))
                if mauseEvent:
                    screenObject.runGame = True
                    theGame(screenObject)

        if 48+start["x"] <= mausePos["x"] <= 281+start["x"]:
            if 618+start["y"] <= mausePos["y"] <= 718+start["y"]:
                screen.blit(exitImg,(48+start["x"],618+start["y"]))
                if mauseEvent:
                    os.system('cls')
                    quit()

        if 246+start["x"] <= mausePos["x"] <= 553+start["x"]:
            if 507+start["y"] <= mausePos["y"] <= 600+start["y"]:
                screen.blit(optionsImg,(246+start["x"],507+start["y"]))
                if mauseEvent:
                    os.system('cls')
                    print("THE OPTIONS ARE IN PROGRESS")

        if 524+start["x"] <= mausePos["x"] <= 757+start["x"]:
            if 618+start["y"] <= mausePos["y"] <= 718+start["y"]:
                screen.blit(shopImg,(524+start["x"],618+start["y"]))
                if mauseEvent:
                    os.system('cls')
                    print("THE SHOP ARE IN PROGRESS")

        if start["x"] <= mausePos["x"] <= end["x"]:
            if start["y"] <= mausePos["y"] <= end["y"]:
                for particle in particles:
                    particle.printParticles()
                    particle.reloadGameData(screenObject)
                            
        functions.frameworkScreen(screenObject)

        pygame.display.update()
        clock.tick(70)

def pauseMenu(screenObject,objectList):
    screenSize,gameSize,scale,screen,start,end,runGame = screenObject.returnGameData()

    particles = []
    for a in range(200):
        particle = editingImage.Particles(screenObject)
        particles.append(particle)
        particle.printParticles()

    clock = pygame.time.Clock()

    resumeImg = pygame.image.load('images/pauseMenu/resume.png').convert_alpha()
    resumeImg.set_colorkey([0,255,0])

    optionsImg = pygame.image.load('images/pauseMenu/options.png').convert_alpha()
    optionsImg.set_colorkey([0,255,0])

    quitImg = pygame.image.load('images/pauseMenu/quit.png').convert_alpha()
    quitImg.set_colorkey([0,255,0])

    pauseImage = pygame.image.load('images/pauseMenu/pause.png').convert_alpha()

    while screenObject.paused:
        screenSize,gameSize,scale,screen,start,end,runGame = screenObject.returnGameData()
        if screenObject.runGame == False:
            screenObject.paused = not screenObject.paused

        specialEfect,mauseEvent = functions.checkEvents(screenObject,objectList,specialEfect=False)

        screen.blit(pauseImage,(start["x"],start["y"]))

        mauseCor = pygame.mouse.get_pos()
        mausePos = {"x": mauseCor[0], "y": mauseCor[1]}

        if 164+start["x"] <= mausePos["x"] <= 636+start["x"]:
            if 399+start["y"] <= mausePos["y"] <= 525+start["y"]:
                screen.blit(resumeImg,(164+start["x"],399+start["y"]))
                if mauseEvent:
                    screenObject.paused = not screenObject.paused

        if 32+start["x"] <= mausePos["x"] <= 295+start["x"]:
            if 579+start["y"] <= mausePos["y"] <= 679+start["y"]:
                screen.blit(quitImg,(32+start["x"],579+start["y"]))
                if mauseEvent:
                    print("QUIT")
                    screenObject.runGame = False

        if 504+start["x"] <= mausePos["x"] <= 767+start["x"]:
            if 581+start["y"] <= mausePos["y"] <= 677+start["y"]:
                screen.blit(optionsImg,(504+start["x"],579+start["y"]))
                if mauseEvent:
                    print("THE OPTIONS ARE IN PROGRESS")

        if start["x"] <= mausePos["x"] <= end["x"]:
            if start["y"] <= mausePos["y"] <= end["y"]:
                for particle in particles:
                    particle.printParticles()
                    particle.reloadGameData(screenObject)
                            
        functions.frameworkScreen(screenObject)

        pygame.display.update()
        clock.tick(70)

def gameOverMenu(screenObject,objectList):
    screenSize,gameSize,scale,screen,start,end,runGame = screenObject.returnGameData()

    particles = []
    for a in range(200):
        particle = editingImage.Particles(screenObject)
        particles.append(particle)
        particle.printParticles()

    clock = pygame.time.Clock()

    tryAgainImg = pygame.image.load('images/gameOverMenu/tryAgain.png').convert_alpha()
    tryAgainImg.set_colorkey([0,255,0])

    menuImg = pygame.image.load('images/gameOverMenu/menu.png').convert_alpha()
    menuImg.set_colorkey([0,255,0])

    gameOverMenuImage = pygame.image.load('images/gameOverMenu/gameOverMenu.png').convert_alpha()

    while screenObject.gameOver:
        screenSize,gameSize,scale,screen,start,end,runGame = screenObject.returnGameData()

        specialEfect,mauseEvent = functions.checkEvents(screenObject,objectList,specialEfect=False)

        screen.blit(gameOverMenuImage,(start["x"],start["y"]))

        mauseCor = pygame.mouse.get_pos()
        mausePos = {"x": mauseCor[0], "y": mauseCor[1]}

        if 36+start["x"] <= mausePos["x"] <= 461+start["x"]:
            if 628+start["y"] <= mausePos["y"] <= 716+start["y"]:
                screen.blit(tryAgainImg,(36+start["x"],628+start["y"]))
                if mauseEvent:
                    screenObject.runGame = True
                    screenObject.gameOver = False

        if 531+start["x"] <= mausePos["x"] <= 766+start["x"]:
            if 628+start["y"] <= mausePos["y"] <= 716+start["y"]:
                screen.blit(menuImg,(531+start["x"],628+start["y"]))
                if mauseEvent:
                    screenObject.runGame = False
                    screenObject.gameOver = False

        if start["x"] <= mausePos["x"] <= end["x"]:
            if start["y"] <= mausePos["y"] <= end["y"]:
                for particle in particles:
                    particle.printParticles()
                    particle.reloadGameData(screenObject)
                            
        functions.frameworkScreen(screenObject)

        pygame.display.update()
        clock.tick(70)


def theGame(screenObject):
    objectList = functions.buildObjects(screenObject)
    enemyList,enemyObjectList,playerList,player,planets,stars,money = objectList
    
    screenSize,gameSize,scale,screen,start,end,runGame = screenObject.returnGameData()

    specialEfect = False
    clock = pygame.time.Clock()
    pygame.display.set_caption("Spaceships Game")
    while screenObject.runGame:
        specialEfect,mauseEvent = functions.checkEvents(screenObject,objectList,specialEfect)

        if not specialEfect:
            screen.fill([0,0,0])

        planets.scrollBackground(player.returnBackgroundSpeed())
        
        for i in range(0,600):
            stars[i].moveCircle(player.returnStarsSpeed())

        money.printMoneyAnimations()

        player.getAllObjectList(playerList,enemyList,enemyObjectList,money)
        player.movePlayer()
        player.printPlayer()
        player.colisionsEnemys()
        player.colisionsBullet()
        player.colisionsMoney()

        destroyAnimationList = []
        for enemy in enemyObjectList:
            enemy.getEnemyDirections(player.returnEnemySpeed())
            enemy.moveEnemy()
            enemy.printEnemy(enemyList)

            if bool(enemy.destroyAnimationList):
                for explotion in enemy.destroyAnimationList:
                    if explotion.done == True:
                        enemy.destroyAnimationList.remove(explotion)
                    else:
                        explotion.printAnimation()

        functions.frameworkScreen(screenObject)    

        clock.tick(30)
        pygame.display.update()

    gameOverMenu(screenObject,objectList)