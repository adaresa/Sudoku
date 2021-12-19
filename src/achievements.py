from buttonClass import *

class Achievements:
    def __init__(self, language, launchMenu, quitGame):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        
        self.language = language
        self.state = "achievements_main"
        
        self.launchMenu = launchMenu
        self.quitGame = quitGame
        
        self.achievementsButtons = []
        self.statsButtons = []
        self.trophiesButtons = []
        self.themesButtons = []
        
        self.loadButtons() 
        
        ###### ACHIEVEMENTS FUNCTIONS ######
    def achievements_events(self):
            for event in pygame.event.get(): 
                
                if event.type == pygame.KEYDOWN:
                    if event.key == 27: # esc
                        if self.state == "achievements_main":
                            self.launchMenu()
                        else:
                            self.openAchievementsMain()
                        
                if event.type == pygame.QUIT:
                    self.quitGame()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "achievements_main":
                        for button in self.achievementsButtons:
                            button.activate(self.mousePos)
                    elif self.state == "achievements_stats":
                        for button in self.statsButtons:
                            button.activate(self.mousePos)
                    elif self.state == "achievements_trophies":
                        for button in self.trophiesButtons:
                            button.activate(self.mousePos)
                    elif self.state == "achievements_themes":
                        for button in self.themesButtons:
                            button.activate(self.mousePos)

    def achievements_update(self):
        self.mousePos = pygame.mouse.get_pos()
        
        if self.state == "achievements_main":
            for button in self.achievementsButtons:
                button.update(self.mousePos)
        elif self.state == "achievements_stats":
            for button in self.statsButtons:
                button.update(self.mousePos)
        elif self.state == "achievements_trophies":
            for button in self.trophiesButtons:
                button.update(self.mousePos)
        elif self.state == "achievements_themes":
            for button in self.themesButtons:
                button.update(self.mousePos)
          
    def achievements_draw(self):
        self.window.fill(BG)
        if self.state == "achievements_main":
            self.titleAchievements()
            for button in self.achievementsButtons:
                button.draw(self.window)
        elif self.state == "achievements_stats":
            self.titleStats()
            for button in self.statsButtons:
                button.draw(self.window)
        elif self.state == "achievements_trophies":
            self.titleTrophies()
            for button in self.trophiesButtons:
                button.draw(self.window)
        elif self.state =="achievements_themes":
            self.titleThemes()
            for button in self.themesButtons:
                button.draw(self.window)
            
        pygame.display.update()
        
    ###### HELPER FUNCTIONS ######
    
    def titleAchievements(self):
        # title text
        string = {'ENG': 'Achievements', 'EST': 'Saavutused'}
        drawText(string.get(self.language), CENTER, 100, fontTitle, SNOW, self.window)
        
    def titleStats(self):
        # title text
        string = {'ENG': 'Stats', 'EST': 'Statistika'}
        drawText(string.get(self.language), CENTER, 100, fontTitle, SNOW, self.window)
        # stats box
        pygame.draw.rect(self.window, SNOW, pygame.Rect(CENTER-150, 150, 300, 300), 2, 12)
        # show stats
        self.statsText()
    
    def statsText(self):
        string = {'ENG': 'GAMES COMPLETED', 'EST': 'MÄNGE    LÕPETATUD'}
        drawText(string.get(self.language), CENTER, 190, fontStat, SNOW, self.window)
        
        string = {'ENG': 'Easy', 'EST': 'Kerge'}
        drawText(string.get(self.language), 248, 230, fontButtonPlay, SNOW, self.window)
        drawText(str(getStat("wins_easy")), 370, 230, fontButtonPlay, SNOW, self.window)    
        
        string = {'ENG': 'Medium', 'EST': 'Keskmine'}
        drawText(string.get(self.language), 262, 280, fontButtonPlay, SNOW, self.window)
        drawText(str(getStat("wins_medium")), 370, 280, fontButtonPlay, SNOW, self.window)
        
        string = {'ENG': 'Hard', 'EST': 'Raske'}
        drawText(string.get(self.language), 248, 330, fontButtonPlay, SNOW, self.window)
        drawText(str(getStat("wins_hard")), 370, 330, fontButtonPlay, SNOW, self.window)
        
        total = getStat("wins_easy") + getStat("wins_medium") + getStat("wins_hard")
        string = {'ENG': 'Total' , 'EST': 'Kokku'}
        drawText(string.get(self.language), 248, 380, fontButtonPlay, SNOW, self.window)
        drawText(str(total), 370, 380, fontButtonPlay, SNOW, self.window)
        
        page = 1
        drawText(str(page), CENTER, 430, fontButtonPlay, SNOW, self.window)
        
    def titleTrophies(self):
        # title text
        string = {'ENG': 'Trophies', 'EST': 'Troffeed'}
        drawText(string.get(self.language), CENTER, 100, fontTitle, SNOW, self.window)

    def titleThemes(self):
        # title text
        string = {'ENG': 'Themes', 'EST': 'Teemad'}
        drawText(string.get(self.language), CENTER, 100, fontTitle, SNOW, self.window)
    
    def openAchievementsMain(self):
        self.state = "achievements_main"
    
    def openStats(self):
        self.state = "achievements_stats"
        
    def openTrophies(self):
        self.state = "achievements_trophies"
    
    def openThemes(self):
        self.state = "achievements_themes"
        
    def loadButtons(self):
        # --- Button sizes ---
        width = 240 # button width
        half_width = width / 2
        height = 60
        pages_width = 100 # button width of previous/next page
        pages_height = 40
        half_pages_width = pages_width / 2
        
        # --- Achievements buttons ---
        string = {'ENG': 'STATS', 'EST': 'STATISTIKA'}
        self.achievementsButtons.append(Button(CENTER - half_width, 200, width, height, 
            renderText(string.get(self.language), fontButton, SNOW), function = self.openStats))
        
        string = {'ENG': 'TROPHIES', 'EST': 'TROFFEED'}
        self.achievementsButtons.append(Button(CENTER - half_width, 290, width, height,
            renderText(string.get(self.language), fontButton, SNOW), function = self.openTrophies))
        
        string = {'ENG': 'THEMES', 'EST': 'TEEMAD'}
        self.achievementsButtons.append(Button(CENTER - half_width, 380, width, height, 
            renderText(string.get(self.language), fontButton, SNOW), function = self.openThemes))
        
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        self.achievementsButtons.append(Button(CENTER - half_width, 470, width, height,
            renderText(string.get(self.language), fontButton, SNOW), function = self.launchMenu))
        
        # --- Stats buttons ---
        string = {'ENG': 'PREVIOUS', 'EST': 'EELMINE'}
        self.statsButtons.append(Button(CENTER - pages_width - half_pages_width, 410, pages_width, pages_height,
            renderText(string.get(self.language), fontSliderText, SNOW), function = self.openStats))
        
        string = {'ENG': 'NEXT', 'EST': 'JÄRGMINE'}
        self.statsButtons.append(Button(CENTER + half_pages_width, 410, pages_width, pages_height,
            renderText(string.get(self.language), fontSliderText, SNOW), function = self.openStats))
        
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        self.statsButtons.append(Button(CENTER - half_width, 470, width, height,
            renderText(string.get(self.language), fontButton, SNOW), function = self.openAchievementsMain))
        
        # --- Trophies buttons ---
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        self.trophiesButtons.append(Button(CENTER - half_width, 470, width, height,
            renderText(string.get(self.language), fontButton, SNOW), function = self.openAchievementsMain))
        
        # --- Themes buttons ---
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        self.themesButtons.append(Button(CENTER - half_width, 470, width, height,
            renderText(string.get(self.language), fontButton, SNOW), function = self.openAchievementsMain))