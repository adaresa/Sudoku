from buttonClass import *
from statsPages import getStatsPages
from trophiesPages import getTrophiesPages

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
        self.pageStats = 1 # stats page
        self.pageTrophies = 1 # trophies page
        self.trophiesButtons = []
        self.themesButtons = []
        
        self.trophy = loadImage('images', 'trophy.png')
        self.trophy = pygame.transform.smoothscale(self.trophy, (50, 50))
        self.trophyBackup = self.trophy
        
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
        # title 
        drawText(stats[self.pageStats][0], CENTER, 190, fontStat, TEXT[self.theme], self.window)
        
        # 1. row
        drawText(stats[self.pageStats][1], 248, 230, fontButtonPlay, TEXT[self.theme], self.window)
        drawText(stats[self.pageStats][2], 370, 230, fontStatValue, TEXT[self.theme], self.window)    
        
        # 2. row
        drawText(stats[self.pageStats][3], 248, 280, fontButtonPlay, TEXT[self.theme], self.window)
        drawText(stats[self.pageStats][4], 370, 280, fontStatValue, TEXT[self.theme], self.window)
        
        # 3. row
        drawText(stats[self.pageStats][5], 248, 330, fontButtonPlay, TEXT[self.theme], self.window)
        drawText(stats[self.pageStats][6], 370, 330, fontStatValue, TEXT[self.theme], self.window)

        # 4. row
        drawText(stats[self.pageStats][7], 248, 380, fontButtonPlay, TEXT[self.theme], self.window)
        drawText(stats[self.pageStats][8], 370, 380, fontStatValue, TEXT[self.theme], self.window)
        
        # current page
        drawText(str(self.pageStats), CENTER, 430, fontButtonPlay, TEXT[self.theme], self.window)
        
    def previousStatsPage(self):
        if self.pageStats > 1:
            self.pageStats -= 1
    
    def nextStatsPage(self):
        stats = getStatsPages(self.language)
        if self.pageStats < len(stats):
            self.pageStats += 1
        
    def titleTrophies(self):
        # title text
        drawText(getText(self.language, 'menu_trophies_title'), CENTER, 100, fontTitle, TEXT[self.theme], self.window)
        # stats box
        pygame.draw.rect(self.window, OUTLINES[self.theme], pygame.Rect(CENTER-150, 150, 300, 300), 2, 12)
        # show trophies
        self.trophiesText()
        
    def trophiesText(self):
        trophies = getTrophiesPages(self.language)
        height = 180
        for page, info in trophies.items():
            if page == self.pageTrophies:
                for combo in info:
                    if combo[0] == 'GIGACHAD':
                        self.trophy = loadImage('images', 'gigachad.png')
                        self.trophy = pygame.transform.smoothscale(self.trophy, (50, 50))
                    else:
                        self.trophy = self.trophyBackup
                    # trophy box
                    pygame.draw.rect(self.window, OUTLINES[self.theme], pygame.Rect(CENTER-125, height, 250, 50), 2, 4)
                    # trophy icon box
                    pygame.draw.rect(self.window, OUTLINES[self.theme], pygame.Rect(CENTER-125, height, 50, 50), 2, 4)
                    # name, description separator
                    pygame.draw.line(self.window, OUTLINES[self.theme], (CENTER-75, height+28), (CENTER+123, height+28), 1)
                    # tropy name
                    drawText(combo[0], CENTER+20, height+14, fontTrophyTitle, TEXT[self.theme], self.window)
                    # trophy description
                    drawText(f"{combo[1]}", CENTER+23, height+38, fontTrophyDescription, TEXT[self.theme], self.window)
                    # trophy icon
                    if combo[2]:
                        self.window.blit(colorize(self.trophy, TEXT[self.theme]), (CENTER-125, height))
                    else:
                        self.window.blit(self.trophy, (CENTER-125, height))
                    # current page
                    drawText(str(self.pageTrophies), CENTER, 430, fontButtonPlay, TEXT[self.theme], self.window)
                    
                    height += 75
                    
    def previousTrophiesPage(self):
        if self.pageTrophies > 1:
            self.pageTrophies -= 1
    
    def nextTrophiesPage(self):
        trophies = getTrophiesPages(self.language)
        if self.pageTrophies < len(trophies):
            self.pageTrophies += 1

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
            renderText(getText(self.language, 'menu_stats_1'), fontSliderText, TEXT[self.theme]), function = self.previousStatsPage))
        
        self.statsButtons.append(Button(CENTER + half_pages_width, 410, pages_width, pages_height, self.theme,
            renderText(getText(self.language, 'menu_stats_2'), fontSliderText, TEXT[self.theme]), function = self.nextStatsPage))
        
        self.statsButtons.append(Button(CENTER - half_width, 470, width, height, self.theme,
            renderText(getText(self.language, 'back_button'), fontButton, TEXT[self.theme]), function = self.openAchievementsMain))
        
        # --- Trophies buttons ---
        self.trophiesButtons.append(Button(CENTER - pages_width - half_pages_width, 410, pages_width, pages_height, self.theme,
            renderText(getText(self.language, 'menu_trophies_1'), fontSliderText, TEXT[self.theme]), function = self.previousTrophiesPage))
        
        self.trophiesButtons.append(Button(CENTER + half_pages_width, 410, pages_width, pages_height, self.theme,
            renderText(getText(self.language, 'menu_trophies_2'), fontSliderText, TEXT[self.theme]), function = self.nextTrophiesPage))
        
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