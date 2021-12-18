import pygame
import pygame.freetype
import os
from database import *

# INITIALIZE
pygame.init()

# DISPLAY SETUP
WIDTH = 600
HEIGHT = 600

# COLORS
BG = (22, 22, 22)
SNOW = (248, 248, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGRAY = (100, 100, 100)
GRAY = (50,50,50)
COBALTBLUE = (0, 71, 171)
LIMEGREEN = (0, 100, 0)
CRIMSON = (220,20,60)

# POSITIONS AND SIZES
gridPos = (75, 100)
cellSize = 50
gridSize = cellSize * 9

# FUNCTIONS
def loadSound(folder, file_name):
    return pygame.mixer.Sound(os.path.join("../assets", folder, file_name))

def playSound(sound):
    sound.set_volume(optionsValues(1))
    sound.play()
    
def musicControl(change_volume=False):
    if not change_volume:
        pygame.mixer.music.set_volume(optionsValues(0)/2)
        pygame.mixer.music.load(os.path.join("../assets", "sounds", "music.mp3"))
        pygame.mixer.music.play(-1)
    
# SOUNDS
MENU_SOUND = loadSound("sounds", "menu.mp3")
INPUT_SOUND = loadSound("sounds", "input.mp3")
WIN_SOUND = loadSound("sounds", "win.mp3")

