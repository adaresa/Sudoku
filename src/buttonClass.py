import pygame
import PySimpleGUI as sg
from settings import *
from database import *

class Button:
    def __init__(self, x, y, width, height, text=None, color=(10, 10, 10), highlightedColor=(30, 28, 30), function = None, params = None):
        self.font = pygame.font.Font('../assets/fonts/maldini/MaldiniNormal2.ttf', 20) # title text
        self.image = pygame.Surface((width, height))
        self.dims = (width, height)
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.color = color
        self.highlightedColor = highlightedColor
        self.function = function
        self.params = params
        self.highlighted = False
        
        self.rect_selector = None
        self.value = [None, None]
        
        if optionsValues(0):
            self.value[0] = optionsValues(0)
        else:
            self.value[0] = 0.5
        if optionsValues(1):
            self.value[1] = optionsValues(1)
        else:
            self.value[1] = 0.5
        
    def parameter(self, parameter):
        self.params = parameter
    
    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False
            
    def activate(self, mouse):
        if self.rect.collidepoint(mouse):
            playSound(MENU_SOUND)
            if self.params != None:
                self.function(self.params)
            else:
                self.function()
                
    def updateSelector(self, mouse):
        if self.rect_selector is not None:
            if self.rect_selector.collidepoint(mouse):
                self.highlighted = True
            else:
                self.highlighted = False
                
    def onSlider(self, mouse):
        if self.rect.collidepoint(mouse):
            return True
    
    def activateSelector(self, mouse, i):
        if self.rect.collidepoint(mouse):
            output = mouse[0] - self.pos[0] - 12.5
            conversionOutput = (output - 12.5) / (226.5 - 12.5)
            conversionOutput = output / (self.dims[0]-25)

            if conversionOutput < 0:
                conversionOutput = 0
            elif conversionOutput > 1:
                conversionOutput = 1
            conversionOutput = round(conversionOutput, 2)
            self.value[i] = conversionOutput
            

    def draw(self, window):
        # button bg
        size = self.image.get_size()
        pygame.draw.rect(window, (self.highlightedColor if self.highlighted else self.color), (self.pos[0], self.pos[1], *size), border_radius = 3)
        # button border
        pygame.draw.rect(window, SNOW, self.rect, 2, 3)
        # button text
        if self.text:
            a = (self.dims[0] - self.text.get_size()[0]) / 2
            b = (self.dims[1] - self.text.get_size()[1]) / 2
            window.blit(self.text, (self.pos[0]+a, self.pos[1]+b+3))
            
    def drawSlider(self, window, i):
        value = self.value[i]
        # check if music/volume values are already in database 
        if i == 0:    
            pygame.mixer.music.set_volume(optionsValues(i)/2)
        size = self.image.get_size()
        # slider bg
        pygame.draw.rect(window, self.color, (self.pos[0], self.pos[1], *size), border_radius = 12)
        # slider bg border
        pygame.draw.rect(window, SNOW, self.rect, 2, 12)
        # slider text (0 & 100)
        text_0 = self.font.render("0", True, SNOW) # (text, antialias, color)
        text_100 = self.font.render("100", True, SNOW) # (text, antialias, color)
        b = (self.dims[1] - self.text.get_size()[1])
        c = self.pos[0]+self.dims[0]-2
        window.blit(text_0, (self.pos[0]+7, self.pos[1]+b+10))
        window.blit(text_100, (c-29, self.pos[1]+b+10))
        # slider selector width
        width = 25
        # convert range 0-1 to 0-(self.dims[0]-width)
        max = self.dims[0]-width
        conversionOutput = (value - 0) * max
        if conversionOutput > 215:
            conversionOutput = 215
        elif conversionOutput < 0:
            conversionOutput = 0
        # slider selector
        self.rect_selector = pygame.Rect(self.rect[0]+conversionOutput, self.rect[1]-5, width, self.dims[1]+10)
        pygame.draw.rect(window, (SNOW if self.highlighted else LIGHTGRAY), self.rect_selector, border_radius= 16)
        optionsValues(i, new_value = value)
        
        
