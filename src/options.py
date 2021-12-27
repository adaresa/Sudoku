from buttonClass import *

class Options:
    def __init__(self, theme, language, launchMenu, quitGame, changeDifficulty, changeLanguage):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        
        self.theme = theme
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
        self.window.fill(BG[self.theme])
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
        drawText(getText(self.language, 'menu_options_title'), CENTER, 100, fontTitle, TEXT[self.theme], self.window)        
        
    def titleDifficulty(self):
        # title text
        drawText(getText(self.language, 'menu_difficulty_title'), CENTER, 100, fontTitle, TEXT[self.theme], self.window)   
        
    def titleSound(self):
        # title text
        drawText(getText(self.language, 'menu_sound_title'), CENTER, 100, fontTitle, TEXT[self.theme], self.window)   
        # music volume slider text
        drawText(getText(self.language, 'menu_sound_1'), CENTER, 190, fontButtonPlay, TEXT[self.theme], self.window)   
        # sound effects volume slider text
        drawText(getText(self.language, 'menu_sound_2'), CENTER, 325, fontButtonPlay, TEXT[self.theme], self.window)   
        
    def titleLanguage(self):
        # title text
        drawText(getText(self.language, 'menu_language_title'), CENTER, 100, fontTitle, TEXT[self.theme], self.window)   
    
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
        self.optionsButtons.append(Button(WIDTH/2 - half_width, 200, width, 60, self.theme,
            renderText(getText(self.language, 'menu_options_1'), fontButton, TEXT[self.theme]), function = self.openDifficulty))

        self.optionsButtons.append(Button(WIDTH/2 - half_width, 290, width, 60, self.theme,
            renderText(getText(self.language, 'menu_options_2'), fontButton, TEXT[self.theme]), function = self.openSound))
        
        self.optionsButtons.append(Button(WIDTH/2 - half_width, 380, width, 60, self.theme,
            renderText(getText(self.language, 'menu_options_3'), fontButton, TEXT[self.theme]), function = self.openLanguage))
        
        self.optionsButtons.append(Button(WIDTH/2 - half_width, 470, width, 60, self.theme,
            renderText(getText(self.language, 'back_button'), fontButton, TEXT[self.theme]), function = self.launchMenu))
        
        # --- Difficulty buttons ---
        self.difficultyButtons.append(Button(WIDTH/2 - half_width, 200, width, 60, self.theme,
            renderText(getText(self.language, 'menu_difficulty_1'), fontButton, TEXT[self.theme]), function = self.changeDifficulty, params = 0))
        
        self.difficultyButtons.append(Button(WIDTH/2 - half_width, 290, width, 60, self.theme,
            renderText(getText(self.language, 'menu_difficulty_2'), fontButton, TEXT[self.theme]), function = self.changeDifficulty, params = 1))
        
        self.difficultyButtons.append(Button(WIDTH/2 - half_width, 380, width, 60, self.theme,
            renderText(getText(self.language, 'menu_difficulty_3'), fontButton, TEXT[self.theme]), function = self.changeDifficulty, params = 2))
        
        self.difficultyButtons.append(Button(WIDTH/2 - half_width, 470, width, 60, self.theme,
            renderText(getText(self.language, 'back_button'), fontButton, TEXT[self.theme]), function = self.openMainOptions))
        
        # --- Sound buttons ---
        self.soundSliders.append(Button(WIDTH/2 - half_width, 210, width, 40, self.theme,
            renderText(getText(self.language, 'menu_sound_1'), fontButton, TEXT[self.theme])))
        
        self.soundSliders.append(Button(WIDTH/2 - half_width, 345, width, 40, self.theme,
            renderText(getText(self.language, 'menu_sound_2'), fontButton, TEXT[self.theme])))
        
        self.soundButtons.append(Button(WIDTH/2 - half_width, 470, width, 60, self.theme,
            renderText(getText(self.language, 'back_button'), fontButton, TEXT[self.theme]), function = self.openMainOptions))
        
        # --- Language buttons ---
        self.languageButtons.append(Button(WIDTH/2 - half_width, 200, width, 60, self.theme,
            renderText("ENGLISH", fontButton, TEXT[self.theme]), function = self.changeLanguage, params = "ENG"))
        
        self.languageButtons.append(Button(WIDTH/2 - half_width, 290, width, 60, self.theme,
            renderText("EESTI", fontButton, TEXT[self.theme]), function = self.changeLanguage, params = "EST"))
        
        self.languageButtons.append(Button(WIDTH/2 - half_width, 380, width, 60, self.theme,
            renderText(getText(self.language, 'back_button'), fontButton, TEXT[self.theme]), function = self.openMainOptions))
        
        