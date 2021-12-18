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
        pygame.display.set_caption('Simple Sudoku')
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_icon(loadImage('images', 'icon.png'))
        
        musicControl()
        self.language = language
        
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
        drawText("Simple Sudoku", CENTER, 100, fontTitle, SNOW, self.window)
    
    def loadingScreen(self):
        self.window.fill(BG)
        string = {'ENG': 'LOADING ...', 'EST': 'LAADIMINE ...'}
        drawText(string.get(self.language), CENTER, HEIGHT/2, fontTitle, SNOW, self.window)
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
        # --- Button sizes ---
        width = 240
        half_width = width / 2
        height = 60
        
        # --- Main menu ---
        string = {'ENG': 'PLAY GAME', 'EST': 'MÄNGI'}
        self.menuButtons.append(Button(CENTER - half_width, 200, width, height, 
            renderText(string.get(self.language), fontButton, SNOW), function = self.launchGame))
        
        string = {'ENG': 'ACHIEVEMENTS', 'EST': 'SAAVUTUSED'}
        self.menuButtons.append(Button(CENTER - half_width, 290, width, height,
            renderText(string.get(self.language), fontButton, SNOW), function = self.launchAchievements))
        
        string = {'ENG': 'OPTIONS', 'EST': 'SEADED'}
        self.menuButtons.append(Button(CENTER - half_width, 380, width, height,
            renderText(string.get(self.language), fontButton, SNOW), function = self.launchOptions))
        
        string = {'ENG': 'EXIT GAME', 'EST': 'SULGE MÄNG'}
        self.menuButtons.append(Button(CENTER - half_width, 470, width, height,
            renderText(string.get(self.language), fontButton, SNOW), function = self.quitGame))