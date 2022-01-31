import pygame
import os
import time
from database import *
from languages import *

# INITIALIZE
pygame.init()

# DISPLAY SETUP
WIDTH = 600
CENTER = WIDTH/2
HEIGHT = 600

# COLORS
LINEN = (250,240,230)
SEASHELL = (255,245,238)
ROSE = (255,228,225)
DARKROSE = (245, 200, 215)
ALMOST_DARKROSE = (225, 205, 230)
LIGHTERGRAY = (200, 200, 200)
CYAN = (0, 248, 230)
GREEN = (10, 200, 100)
GREENLIGHTER = (10, 170, 100)
CRIMSON = (220,20,60)
COBALTBLUE = (0, 71, 171)
LIGHTGRAY = (100, 100, 100)
LIMEGREEN = (0, 100, 0)
GRAY = (50,50,50)
DARKGRAY = (22, 22, 22)
ALMOST_DARKGRAY = (35, 45, 40)
ALMOST_BLACK = (10, 10, 10)

# COLOR THEMES      DARK                LIGHT           COLORFUL
BG =                [DARKGRAY,          LINEN,          DARKGRAY]       # Background
TEXT =              [LINEN,             ALMOST_BLACK,   CYAN]           # Text
OUTLINES =          [LINEN,             ALMOST_BLACK,   GREEN]          # Outlines (buttons&grid)
OUTLINES_TIMER =    [SEASHELL,          DARKGRAY,       GREENLIGHTER]   # Outlines (buttons&grid)
BUTTON =            [ALMOST_BLACK,      SEASHELL,       ALMOST_BLACK]   # Button body
BUTTON_HIGHLIGHT =  [DARKGRAY,          ROSE,           DARKGRAY]       # Button body on hover
HOVERED =           [GRAY,              ROSE,           GRAY]           # Cell on hover
SELECTED =          [LIGHTGRAY,         DARKROSE,       LIGHTGRAY]      # Cell on select
DOUBLED =           [ALMOST_DARKGRAY,   ALMOST_DARKROSE,ALMOST_DARKGRAY]      # Cell on select
INSERT_NUMBER =     [COBALTBLUE,        COBALTBLUE,     COBALTBLUE]     # Inserted cell number
SOLVED =            [LIMEGREEN,         LIMEGREEN,      LIMEGREEN]      # Solved cell background (solve button & win)
MISTAKES =          [CRIMSON,           CRIMSON,        CRIMSON]        # Mistake cells background (mistake button)
# GAME INFO         
DIFFICULTY =        [GREEN,             CYAN,           CRIMSON]
SAVABLE =           [GREEN,             CRIMSON,        GREEN]

# POSITIONS AND SIZES
gridPos = (75, 100)
cellSize = 50
gridSize = cellSize * 9

# FONTS
fontTitle = pygame.font.Font('./assets/fonts/maldini/MaldiniNormal2.ttf', 70) # title text
fontCell = pygame.font.SysFont('arial', 50) # cell numbers
fontButton = pygame.font.Font('./assets/fonts/maldini/MaldiniNormal2.ttf', 40) # buttons text
fontButtonPlay = pygame.font.Font('./assets/fonts/maldini/MaldiniNormal2.ttf', 26) # button text in playing
fontStatValue = pygame.font.SysFont('arial', 26) # button text in playing
fontStat = pygame.font.Font('./assets/fonts/maldini/MaldiniNormal2.ttf', 22) # stat title
fontSliderText = pygame.font.Font('./assets/fonts/maldini/MaldiniNormal2.ttf', 20) # text in slider

# GLOBAL FUNCTIONS
def getTime(seconds):
    if seconds >= 3600:
        return time.strftime("%H:%M:%S", time.gmtime(seconds))
    else:
        return time.strftime("%M:%S", time.gmtime(seconds))

def loadImage(folder, file_name):
    return pygame.image.load(os.path.join("./assets", folder, file_name)).convert_alpha()

def loadSound(folder, file_name):
    return pygame.mixer.Sound(os.path.join("./assets", folder, file_name))

def playSound(sound):
    sound.set_volume(optionsValues(1))
    sound.play()
    
def musicStart():
    pygame.mixer.music.set_volume(optionsValues(0)/2)
    pygame.mixer.music.load(os.path.join("./assets", "sounds", "music.mp3"))
    pygame.mixer.music.play(-1)

def renderText(string, font, color):
    return font.render(str(string), True, color)

def drawText(string, x, y, font, color, window):
    text_rendered = renderText(string, font, color)
    rect = text_rendered.get_rect(center=(x, y))
    window.blit(text_rendered, rect)

def getText(language, case):
    language_index = 0 if language == "ENG" else 1
    return texts[case][language_index]

# SOUNDS
MENU_SOUND = loadSound("sounds", "menu.mp3")
INPUT_SOUND = loadSound("sounds", "input.mp3")
WIN_SOUND = loadSound("sounds", "win.mp3")