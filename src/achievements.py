from buttonClass import *
from statsPages import *

class Achievements:
    def __init__(self, theme, language, launchMenu, quitGame, changeTheme):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        
        self.theme = theme
        self.language = language
        self.state = "achievements_main"
        
        self.changeTheme = changeTheme
        self.launchMenu = launchMenu
        self.quitGame = quitGame
        
        self.achievementsButtons = []
        self.statsButtons = []
        self.page = 1 # stats page
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
        self.window.fill(BG[self.theme])
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
        drawText(getText(self.language, 'menu_achievements_title'), CENTER, 100, fontTitle, TEXT[self.theme], self.window)
        
    def titleStats(self):
        # title text
        drawText(getText(self.language, 'menu_stats_title'), CENTER, 100, fontTitle, TEXT[self.theme], self.window)
        # stats box
        pygame.draw.rect(self.window, OUTLINES[self.theme], pygame.Rect(CENTER-150, 150, 300, 300), 2, 12)
        # show stats
        self.statsText()
    
    def statsText(self):
        stats = getStatsPages(self.language)
        drawText(stats[self.page][0], CENTER, 190, fontStat, TEXT[self.theme], self.window)
        
        drawText(stats[self.page][1], 248, 230, fontButtonPlay, TEXT[self.theme], self.window)
        drawText(stats[self.page][2], 370, 230, fontStatValue, TEXT[self.theme], self.window)    
        
        drawText(stats[self.page][3], 248, 280, fontButtonPlay, TEXT[self.theme], self.window)
        drawText(stats[self.page][4], 370, 280, fontStatValue, TEXT[self.theme], self.window)
        
        drawText(stats[self.page][5], 248, 330, fontButtonPlay, TEXT[self.theme], self.window)
        drawText(stats[self.page][6], 370, 330, fontStatValue, TEXT[self.theme], self.window)

        drawText(stats[self.page][7], 248, 380, fontButtonPlay, TEXT[self.theme], self.window)
        drawText(stats[self.page][8], 370, 380, fontStatValue, TEXT[self.theme], self.window)
        
        drawText(str(self.page), CENTER, 430, fontButtonPlay, TEXT[self.theme], self.window)
        
    def previousPage(self):
        if self.page > 1:
            self.page -= 1
    
    def nextPage(self):
        stats = getStatsPages(self.language)
        if self.page < len(stats):
            self.page += 1
        
    def titleTrophies(self):
        # title text
        drawText(getText(self.language, 'menu_trophies_title'), CENTER, 100, fontTitle, TEXT[self.theme], self.window)

    def titleThemes(self):
        # title text
        drawText(getText(self.language, 'menu_themes_title'), CENTER, 100, fontTitle, TEXT[self.theme], self.window)
    
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
        self.achievementsButtons.append(Button(CENTER - half_width, 200, width, height, self.theme, 
            renderText(getText(self.language, 'menu_achievements_1'), fontButton, TEXT[self.theme]), function = self.openStats))
        
        self.achievementsButtons.append(Button(CENTER - half_width, 290, width, height, self.theme,
            renderText(getText(self.language, 'menu_achievements_2'), fontButton, TEXT[self.theme]), function = self.openTrophies))
        
        self.achievementsButtons.append(Button(CENTER - half_width, 380, width, height, self.theme, 
            renderText(getText(self.language, 'menu_achievements_3'), fontButton, TEXT[self.theme]), function = self.openThemes))
        
        self.achievementsButtons.append(Button(CENTER - half_width, 470, width, height, self.theme,
            renderText(getText(self.language, 'back_button'), fontButton, TEXT[self.theme]), function = self.launchMenu))
        
        # --- Stats buttons ---
        self.statsButtons.append(Button(CENTER - pages_width - half_pages_width, 410, pages_width, pages_height, self.theme,
            renderText(getText(self.language, 'menu_stats_1'), fontSliderText, TEXT[self.theme]), function = self.previousPage))
        
        self.statsButtons.append(Button(CENTER + half_pages_width, 410, pages_width, pages_height, self.theme,
            renderText(getText(self.language, 'menu_stats_2'), fontSliderText, TEXT[self.theme]), function = self.nextPage))
        
        self.statsButtons.append(Button(CENTER - half_width, 470, width, height, self.theme,
            renderText(getText(self.language, 'back_button'), fontButton, TEXT[self.theme]), function = self.openAchievementsMain))
        
        # --- Trophies buttons ---
        self.trophiesButtons.append(Button(CENTER - half_width, 470, width, height, self.theme,
            renderText(getText(self.language, 'back_button'), fontButton, TEXT[self.theme]), function = self.openAchievementsMain))
        
        # --- Themes buttons ---
        self.themesButtons.append(Button(CENTER - half_width, 200, width, height, self.theme,
            renderText(getText(self.language, 'menu_themes_1'), fontButton, TEXT[self.theme]), function = self.changeTheme, params=0))
        
        self.themesButtons.append(Button(CENTER - half_width, 290, width, height, self.theme,
            renderText(getText(self.language, 'menu_themes_2'), fontButton, TEXT[self.theme]), function = self.changeTheme, params=1))
        
        self.themesButtons.append(Button(CENTER - half_width, 380, width, height, self.theme,
            renderText(getText(self.language, 'menu_themes_3'), fontButton, TEXT[self.theme]), function = self.changeTheme, params=2))
        
        self.themesButtons.append(Button(CENTER - half_width, 470, width, height, self.theme,
            renderText(getText(self.language, 'back_button'), fontButton, TEXT[self.theme]), function = self.openAchievementsMain))