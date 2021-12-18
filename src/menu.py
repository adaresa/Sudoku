import sys
import pygame
from settings import *
from buttonClass import *
from playing import *
from options import *
from achievements import *

class Menu:
    def __init__(self, language):
        pygame.init()
        musicControl()
        self.language = language
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font('../assets/fonts/maldini/MaldiniNormal2.ttf', 70) # title text
        self.font2 = pygame.font.Font('../assets/fonts/maldini/MaldiniNormal2.ttf', 40) # buttons text
        
        self.running = True
        self.state = "main_menu"
        self.loadingScreen()
        self.app = App(self.language, self.launchMenu, self.quitGame, self.loadingScreen)
        self.options = Options(self.language, self.launchMenu, self.quitGame, self.app.changeDifficulty, self.changeLanguage)
        self.achievements = Achievements(self.language, self.launchMenu)
        
        self.menuButtons = []
        self.loadButtons()
    
    def run(self):
        while self.running:
            if self.state == "main_menu":
                self.menu_events()
                self.menu_update()
                self.menu_draw()
            elif self.state == "playing":
                self.app.playing_events()
                self.app.playing_update()
                self.app.playing_draw()
            elif self.state == "achievements":
                self.achievements.achievements_events()
                self.achievements.achievements_update()
                self.achievements.achievements_draw()
            elif self.state == "options":
                self.options.options_events()
                self.options.options_update()
                self.options.options_draw()
        pygame.quit()
        sys.exit()
        
    ###### MAIN MENU FUNCTIONS ######

    def menu_events(self):
        for event in pygame.event.get():
                                
            if event.type == pygame.QUIT:
                self.running = False

            #if event.type == pygame.MOUSEMOTION:

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.menuButtons:
                    button.activate(self.mousePos)

    def menu_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.menuButtons:
            button.update(self.mousePos)
        
    def menu_draw(self):
        self.window.fill(BG)
        self.titleText()
        for button in self.menuButtons:
            button.draw(self.window)
        pygame.display.update()
    
    ###### HELPER FUNCTIONS ######
    
    def titleText(self):
        # title text
        text = self.font.render("Simple Sudoku", True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(WIDTH/2, 100))
        self.window.blit(text, text_rect)
    
    def loadingScreen(self):
        self.window.fill(BG)
        string = {'ENG': 'LOADING ...', 'EST': 'LAADIMINE ...'}
        text = self.font.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.window.blit(text, text_rect)
        pygame.display.update()
        
    def changeLanguage(self, language):
        optionsValues("language", new_value = language)
        app = Menu(language)
        app.run()
        
    def launchGame(self): 
        self.state = "playing"
        
    def launchAchievements(self):
        self.state = "achievements"
        
    def launchOptions(self):
        self.state = "options"
        
    def launchMenu(self):
        self.state = "main_menu"
        
    def quitGame(self):
        self.running = False
        
    def loadButtons(self):
        width = 240
        half_width = width/2
        string = {'ENG': 'PLAY GAME', 'EST': 'MÄNGI'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.menuButtons.append(Button(WIDTH/2 - half_width, 200, width, 60, text, function = self.launchGame))
        
        string = {'ENG': 'ACHIEVEMENTS', 'EST': 'SAAVUTUSED'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.menuButtons.append(Button(WIDTH/2 - half_width, 290, width, 60, text, function = self.launchAchievements))
        
        string = {'ENG': 'OPTIONS', 'EST': 'SEADED'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.menuButtons.append(Button(WIDTH/2 - half_width, 380, width, 60, text, function = self.launchOptions))
        
        string = {'ENG': 'EXIT GAME', 'EST': 'SULGE MÄNG'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.menuButtons.append(Button(WIDTH/2 - half_width, 470, width, 60, text, function = self.quitGame))