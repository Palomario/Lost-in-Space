import pygame

class Screen(object):
    def __init__(self):
        self.screenSize = {"width": 800, "height": 750}

        self.gameSize =   {"width": 800, "height": 750}
        self.scale = 1.5

        self.runGame = False
        self.paused = False
        self.gameOver = False
        
        self.startingPoint = {"x": int(self.screenSize["width" ] / 2) - int(self.gameSize["width" ] / 2),
                              "y": int(self.screenSize["height"] / 2) - int(self.gameSize["height"] / 2)}
        self.endPoint =      {"x": int(self.startingPoint["x"] + self.gameSize["width" ]),
                              "y": int(self.startingPoint["y"] + self.gameSize["height"])}
        self.screen = pygame.display.set_mode((self.screenSize["width"],self.screenSize["height"]), pygame.RESIZABLE)   

    def calculateGameSize(self):
        self.startingPoint = {"x": int(self.screenSize["width" ] / 2) - int(self.gameSize["width" ] / 2),
                              "y": int(self.screenSize["height"] / 2) - int(self.gameSize["height"] / 2)}
        self.endPoint =      {"x": int(self.startingPoint["x"] + self.gameSize["width" ]),
                              "y": int(self.startingPoint["y"] + self.gameSize["height"])}
        self.screen = pygame.display.set_mode((self.screenSize["width"],self.screenSize["height"]), pygame.RESIZABLE)

    def returnGameData(self):
        return self.screenSize, self.gameSize, self.scale, self.screen, self.startingPoint, self.endPoint, self.runGame

    def getGameData(self,screenSize):
        self.screenSize = screenSize
