import pygame
import os
from database import *

# INITIALIZE
pygame.init()

# DISPLAY SETUP
WIDTH = 600
CENTER = WIDTH/2
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

# FONTS
fontTitle = pygame.font.Font('./assets/fonts/maldini/MaldiniNormal2.ttf', 70) # title text
fontCell = pygame.font.SysFont('arial', 50) # cell numbers
fontButton = pygame.font.Font('./assets/fonts/maldini/MaldiniNormal2.ttf', 40) # buttons text
fontButtonPlay = pygame.font.Font('./assets/fonts/maldini/MaldiniNormal2.ttf', 26) # button text in playing
fontStat = pygame.font.Font('./assets/fonts/maldini/MaldiniNormal2.ttf', 22) # stat text
fontSliderText = pygame.font.Font('./assets/fonts/maldini/MaldiniNormal2.ttf', 20) # text in slider

# FUNCTIONS
def loadImage(folder, file_name):
    return pygame.image.load(os.path.join("./assets", folder, file_name)).convert_alpha()

def loadSound(folder, file_name):
    return pygame.mixer.Sound(os.path.join("./assets", folder, file_name))

def playSound(sound):
    sound.set_volume(optionsValues(1))
    sound.play()
    
def musicControl(change_volume=False):
    if not change_volume:
        pygame.mixer.music.set_volume(optionsValues(0)/2)
        pygame.mixer.music.load(os.path.join("./assets", "sounds", "music.mp3"))
        pygame.mixer.music.play(-1)

def renderText(string, font, color):
    return font.render(str(string), True, color)

def drawText(string, x, y, font, color, window):
    text_rendered = renderText(string, font, color)
    rect = text_rendered.get_rect(center=(x, y))
    window.blit(text_rendered, rect)

    
# SOUNDS
MENU_SOUND = loadSound("sounds", "menu.mp3")
INPUT_SOUND = loadSound("sounds", "input.mp3")
WIN_SOUND = loadSound("sounds", "win.mp3")

