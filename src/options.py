import pygame
from settings import *
from buttonClass import *

class Options:
    def __init__(self, language, launchMenu, quitGame, changeDifficulty, changeLanguage):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font('../assets/fonts/maldini/MaldiniNormal2.ttf', 70) # title text
        self.font2 = pygame.font.Font('../assets/fonts/maldini/MaldiniNormal2.ttf', 40) # buttons text
        self.font3 = pygame.font.Font('../assets/fonts/maldini/MaldiniNormal2.ttf', 26) #  slider titletext
        
        self.language = language
        self.state = "options_main"
        
        self.launchMenu = launchMenu
        self.quitGame = quitGame
        self.changeDifficulty = changeDifficulty
        self.changeLanguage = changeLanguage
        
        self.optionsButtons = []
        self.difficultyButtons = []
        self.soundButtons = []
        self.soundSliders = []
        self.soundQueued = False
        self.languageButtons = []
        
        self.held = False
        self.loadButtons()        
        
    ###### OPTIONS FUNCTIONS ######
    def options_events(self):
            for event in pygame.event.get(): 
                        
                if event.type == pygame.QUIT:
                    self.quitGame()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "options_main":
                        for button in self.optionsButtons:
                            button.activate(self.mousePos)
                    elif self.state == "options_difficulty":
                        for button in self.difficultyButtons:
                            button.activate(self.mousePos)
                    elif self.state == "options_sound":
                        for button in self.soundButtons:
                            button.activate(self.mousePos)
                        for i, slider in enumerate(self.soundSliders):
                            if slider.onSlider(self.mousePos):
                                self.held = True
                                if i == 1:
                                    self.soundQueued = True
                    elif self.state == "options_language":
                        for button in self. languageButtons:
                            button.activate(self.mousePos)
                            
                if event.type == pygame.MOUSEBUTTONUP:
                    self.held = False
                    if self.state == "options_sound":
                        if self.soundQueued:
                            playSound(INPUT_SOUND)
                            self.soundQueued = False
    
            if self.state == "options_sound":
                if self.held:
                    for i, slider in enumerate(self.soundSliders):
                            slider.activateSelector(self.mousePos, i)

    def options_update(self):
        self.mousePos = pygame.mouse.get_pos()
        
        if self.state == "options_main":
            for button in self.optionsButtons:
                button.update(self.mousePos)
        elif self.state == "options_difficulty":
            for button in self.difficultyButtons:
                button.update(self.mousePos)
        elif self.state == "options_sound":
            for button in self.soundButtons:
                button.update(self.mousePos)
            for slider in self.soundSliders:
                slider.updateSelector(self.mousePos)
        elif self.state == "options_language":
            for button in self.languageButtons:
                button.update(self.mousePos)
            
            
        
    def options_draw(self):
        self.window.fill(BG)
        if self.state == "options_main":
            self.titleOptions()
            for button in self.optionsButtons:
                button.draw(self.window)
        elif self.state == "options_difficulty":
            self.titleDifficulty()
            for button in self.difficultyButtons:
                button.draw(self.window)
        elif self.state == "options_sound":
            self.titleSound()
            for button in self.soundButtons:
                button.draw(self.window)
            for i, slider in enumerate(self.soundSliders):
                slider.drawSlider(self.window, i)
        elif self.state == "options_language":
            self.titleLanguage()
            for button in self.languageButtons:
                button.draw(self.window)
            
        pygame.display.update()
        
    
        
    ###### HELPER FUNCTIONS ######
    
    def titleOptions(self):
        # title text
        string = {'ENG': 'Options', 'EST': 'Seaded'}
        text = self.font.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(WIDTH/2, 100))
        self.window.blit(text, text_rect)
        
        
    def titleDifficulty(self):
        # title text
        string = {'ENG': 'Difficulty', 'EST': 'Raskusaste'}
        text = self.font.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(WIDTH/2, 100))
        self.window.blit(text, text_rect)
        
    def titleSound(self):
        # title text
        string = {'ENG': 'Sound', 'EST': 'Heli'}
        text = self.font.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(WIDTH/2, 100))
        self.window.blit(text, text_rect)
        # music volume slider text
        string = {'ENG': 'Music', 'EST': 'Muusika'}
        text = self.font3.render(string.get(self.language), True, SNOW)
        text_rect = text.get_rect(center=(WIDTH/2, 190))
        self.window.blit(text, text_rect)
        # sound effects volume slider text
        string = {'ENG': 'Sound effects', 'EST': 'Heliefektid'}
        text = self.font3.render(string.get(self.language), True, SNOW)
        text_rect = text.get_rect(center=(WIDTH/2, 325))
        self.window.blit(text, text_rect)
        
    def titleLanguage(self):
        # title text
        string = {'ENG': 'Language', 'EST': 'Keel'}
        text = self.font.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(WIDTH/2, 100))
        self.window.blit(text, text_rect)
    
    def openMainOptions(self):
        self.state = "options_main"
    
    def openDifficulty(self):
        self.state = "options_difficulty"
        
    def openSound(self):
        self.state = "options_sound"
        
    def openLanguage(self):
        self.state = "options_language"
    
    def loadButtons(self):
        width = 240
        half_width = width/2
        # --- Options buttons ---
        string = {'ENG': 'DIFFICULTY', 'EST': 'RASKUSASTE'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.optionsButtons.append(Button(WIDTH/2 - half_width, 200, width, 60, text, function = self.openDifficulty))
        
        string = {'ENG': 'SOUND', 'EST': 'HELI'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.optionsButtons.append(Button(WIDTH/2 - half_width, 290, width, 60, text, function = self.openSound))
        
        string = {'ENG': 'LANGUAGE', 'EST': 'KEEL'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.optionsButtons.append(Button(WIDTH/2 - half_width, 380, width, 60, text, function = self.openLanguage))
        
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.optionsButtons.append(Button(WIDTH/2 - half_width, 470, width, 60, text, function = self.launchMenu))
        
        # --- Difficulty buttons ---
        string = {'ENG': 'EASY', 'EST': 'KERGE'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.difficultyButtons.append(Button(WIDTH/2 - half_width, 200, width, 60, text, function = self.changeDifficulty, params = 0))
        
        string = {'ENG': 'MEDIUM', 'EST': 'KESKMINE'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.difficultyButtons.append(Button(WIDTH/2 - half_width, 290, width, 60, text, function = self.changeDifficulty, params = 1))
        
        string = {'ENG': 'HARD', 'EST': 'RASKE'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.difficultyButtons.append(Button(WIDTH/2 - half_width, 380, width, 60, text, function = self.changeDifficulty, params = 2))
        
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.difficultyButtons.append(Button(WIDTH/2 - half_width, 470, width, 60, text, function = self.openMainOptions))
        
        # --- Sound buttons ---
        string = {'ENG': 'MUSIC', 'EST': 'MUUSIKA'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.soundSliders.append(Button(WIDTH/2 - half_width, 210, width, 40, text))
        
        string = {'ENG': 'SOUND', 'EST': 'HELI'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.soundSliders.append(Button(WIDTH/2 - half_width, 345, width, 40, text))
        
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.soundButtons.append(Button(WIDTH/2 - half_width, 470, width, 60, text, function = self.openMainOptions))
        
        # --- Language buttons ---
        text = self.font2.render("ENGLISH", True, SNOW) # (text, antialias, color)
        self.languageButtons.append(Button(WIDTH/2 - half_width, 200, width, 60, text, function = self.changeLanguage, params = "ENG"))
        
        text = self.font2.render("EESTI", True, SNOW) # (text, antialias, color)
        self.languageButtons.append(Button(WIDTH/2 - half_width, 290, width, 60, text, function = self.changeLanguage, params = "EST"))
        
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.languageButtons.append(Button(WIDTH/2 - half_width, 380, width, 60, text, function = self.openMainOptions))
        
        