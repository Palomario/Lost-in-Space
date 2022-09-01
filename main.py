import os

import menu
import gameData

os.system('cls')

screenObject = gameData.Screen()
screenObject.calculateGameSize()
menu.mainMenu(screenObject)

