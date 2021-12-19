from buttonClass import *

class Options:
    def __init__(self, language, launchMenu, quitGame, changeDifficulty, changeLanguage):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        
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
                
                if event.type == pygame.KEYDOWN:
                    if event.key == 27: # esc
                        if self.state == "options_main":
                            self.launchMenu()
                        else:
                            self.openMainOptions()
                        
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
        drawText(string.get(self.language), CENTER, 100, fontTitle, SNOW, self.window)        
        
    def titleDifficulty(self):
        # title text
        string = {'ENG': 'Difficulty', 'EST': 'Raskusaste'}
        drawText(string.get(self.language), CENTER, 100, fontTitle, SNOW, self.window)   
        
    def titleSound(self):
        # title text
        string = {'ENG': 'Sound', 'EST': 'Heli'}
        drawText(string.get(self.language), CENTER, 100, fontTitle, SNOW, self.window)   
        # music volume slider text
        string = {'ENG': 'Music', 'EST': 'Muusika'}
        drawText(string.get(self.language), CENTER, 190, fontButtonPlay, SNOW, self.window)   
        # sound effects volume slider text
        string = {'ENG': 'Sound effects', 'EST': 'Heliefektid'}
        drawText(string.get(self.language), CENTER, 325, fontButtonPlay, SNOW, self.window)   
        
    def titleLanguage(self):
        # title text
        string = {'ENG': 'Language', 'EST': 'Keel'}
        drawText(string.get(self.language), CENTER, 100, fontTitle, SNOW, self.window)   
    
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
        half_width = width / 2
        # --- Options buttons ---
        string = {'ENG': 'DIFFICULTY', 'EST': 'RASKUSASTE'}
        self.optionsButtons.append(Button(WIDTH/2 - half_width, 200, width, 60,
            renderText(string.get(self.language), fontButton, SNOW), function = self.openDifficulty))
        
        string = {'ENG': 'SOUND', 'EST': 'HELI'}
        self.optionsButtons.append(Button(WIDTH/2 - half_width, 290, width, 60,
            renderText(string.get(self.language), fontButton, SNOW), function = self.openSound))
        
        string = {'ENG': 'LANGUAGE', 'EST': 'KEEL'}
        self.optionsButtons.append(Button(WIDTH/2 - half_width, 380, width, 60,
            renderText(string.get(self.language), fontButton, SNOW), function = self.openLanguage))
        
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        self.optionsButtons.append(Button(WIDTH/2 - half_width, 470, width, 60,
            renderText(string.get(self.language), fontButton, SNOW), function = self.launchMenu))
        
        # --- Difficulty buttons ---
        string = {'ENG': 'EASY', 'EST': 'KERGE'}
        self.difficultyButtons.append(Button(WIDTH/2 - half_width, 200, width, 60,
            renderText(string.get(self.language), fontButton, SNOW), function = self.changeDifficulty, params = 0))
        
        string = {'ENG': 'MEDIUM', 'EST': 'KESKMINE'}
        self.difficultyButtons.append(Button(WIDTH/2 - half_width, 290, width, 60,
            renderText(string.get(self.language), fontButton, SNOW), function = self.changeDifficulty, params = 1))
        
        string = {'ENG': 'HARD', 'EST': 'RASKE'}
        self.difficultyButtons.append(Button(WIDTH/2 - half_width, 380, width, 60,
            renderText(string.get(self.language), fontButton, SNOW), function = self.changeDifficulty, params = 2))
        
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        self.difficultyButtons.append(Button(WIDTH/2 - half_width, 470, width, 60,
            renderText(string.get(self.language), fontButton, SNOW), function = self.openMainOptions))
        
        # --- Sound buttons ---
        string = {'ENG': 'MUSIC', 'EST': 'MUUSIKA'}
        self.soundSliders.append(Button(WIDTH/2 - half_width, 210, width, 40,
            renderText(string.get(self.language), fontButton, SNOW)))
        
        string = {'ENG': 'SOUND', 'EST': 'HELI'}
        self.soundSliders.append(Button(WIDTH/2 - half_width, 345, width, 40,
            renderText(string.get(self.language), fontButton, SNOW)))
        
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        self.soundButtons.append(Button(WIDTH/2 - half_width, 470, width, 60,
            renderText(string.get(self.language), fontButton, SNOW), function = self.openMainOptions))
        
        # --- Language buttons ---
        self.languageButtons.append(Button(WIDTH/2 - half_width, 200, width, 60,
            renderText("ENGLISH", fontButton, SNOW), function = self.changeLanguage, params = "ENG"))
        
        self.languageButtons.append(Button(WIDTH/2 - half_width, 290, width, 60,
            renderText("EESTI", fontButton, SNOW), function = self.changeLanguage, params = "EST"))
        
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        self.languageButtons.append(Button(WIDTH/2 - half_width, 380, width, 60,
            renderText(string.get(self.language), fontButton, SNOW), function = self.openMainOptions))
        
        