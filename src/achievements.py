import pygame
from settings import *
from buttonClass import *

class Achievements:
    def __init__(self, language, launchMenu):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.Font('../assets/fonts/maldini/MaldiniNormal2.ttf', 70) # title text
        self.font2 = pygame.font.Font('../assets/fonts/maldini/MaldiniNormal2.ttf', 40) # buttons text
        self.font3 = pygame.font.Font('../assets/fonts/maldini/MaldiniNormal2.ttf', 22) # buttons text
        self.font4 = pygame.font.Font('../assets/fonts/maldini/MaldiniNormal2.ttf', 26) # buttons text
        
        self.language = language
        self.state = "achievements_main"
        
        self.launchMenu = launchMenu
        
        self.achievementsButtons = []
        self.statsButtons = []
        self.trophiesButtons = []
        self.themesButtons = []
        
        self.loadButtons() 
        
        ###### ACHIEVEMENTS FUNCTIONS ######
    def achievements_events(self):
            for event in pygame.event.get(): 
                        
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
        text = self.font.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(WIDTH/2, 100))
        self.window.blit(text, text_rect)
        
    def titleStats(self):
        # title text
        string = {'ENG': 'Stats', 'EST': 'Statistika'}
        text = self.font.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(WIDTH/2, 100))
        self.window.blit(text, text_rect)
        # stats box
        pygame.draw.rect(self.window, SNOW, pygame.Rect(WIDTH/2-150, 150, 300, 300), 2, 12)
        # show stats
        self.statsText()
    
    def statsText(self):
        string = {'ENG': 'GAMES COMPLETED', 'EST': 'MÄNGE    LÕPETATUD'}
        text = self.font3.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(WIDTH/2, 190))
        self.window.blit(text, text_rect)
        
        string = {'ENG': 'Easy', 'EST': 'Kerge'}
        text = self.font4.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(248, 230))
        self.window.blit(text, text_rect)
        text = self.font4.render(str(getStat("wins_easy")), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(370, 230))
        self.window.blit(text, text_rect)
        
        string = {'ENG': 'Medium', 'EST': 'Keskmine'}
        text = self.font4.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(262, 280))
        self.window.blit(text, text_rect)
        text = self.font4.render(str(getStat("wins_medium")), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(370, 280))
        self.window.blit(text, text_rect)
        
        string = {'ENG': 'Hard', 'EST': 'Raske'}
        text = self.font4.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(248, 330))
        self.window.blit(text, text_rect)
        text = self.font4.render(str(getStat("wins_hard")), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(370, 330))
        self.window.blit(text, text_rect)
        
        total = getStat("wins_easy") + getStat("wins_medium") + getStat("wins_hard")
        string = {'ENG': 'Total' , 'EST': 'Kokku'}
        text = self.font4.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(248, 380))
        self.window.blit(text, text_rect)
        text = self.font4.render(str(total), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(370, 380))
        self.window.blit(text, text_rect)
        
        text = self.font3.render("1", True, SNOW)
        text_rect = text.get_rect(center=(WIDTH/2, 430))
        self.window.blit(text, text_rect)
        

    def titleTrophies(self):
        # title text
        string = {'ENG': 'Trophies', 'EST': 'Troffeed'}
        text = self.font.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(WIDTH/2, 100))
        self.window.blit(text, text_rect)

    def titleThemes(self):
        # title text
        string = {'ENG': 'Themes', 'EST': 'Teemad'}
        text = self.font.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        text_rect = text.get_rect(center=(WIDTH/2, 100))
        self.window.blit(text, text_rect)
    
    def openAchievementsMain(self):
        self.state = "achievements_main"
    
    def openStats(self):
        self.state = "achievements_stats"
        
    def openTrophies(self):
        self.state = "achievements_trophies"
    
    def openThemes(self):
        self.state = "achievements_themes"
        
    def loadButtons(self):
        width = 240
        half_width = width/2
        # --- Achievements buttons ---
        string = {'ENG': 'STATS', 'EST': 'STATISTIKA'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.achievementsButtons.append(Button(WIDTH/2 - half_width, 200, width, 60, text, function = self.openStats))
        
        string = {'ENG': 'TROPHIES', 'EST': 'TROFFEED'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.achievementsButtons.append(Button(WIDTH/2 - half_width, 290, width, 60, text, function = self.openTrophies))
        
        string = {'ENG': 'THEMES', 'EST': 'TEEMAD'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.achievementsButtons.append(Button(WIDTH/2 - half_width, 380, width, 60, text, function = self.openThemes))
        
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.achievementsButtons.append(Button(WIDTH/2 - half_width, 470, width, 60, text, function = self.launchMenu))
        
        # --- Stats buttons ---
        pages_width = 100
        half_pages_width = pages_width/2
        string = {'ENG': 'PREVIOUS', 'EST': 'EELMINE'}
        text = self.font3.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.statsButtons.append(Button(WIDTH/2 - pages_width - half_pages_width, 410, pages_width, 40, text, function = self.openStats))
        
        string = {'ENG': 'NEXT', 'EST': 'JÄRGMINE'}
        text = self.font3.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.statsButtons.append(Button(WIDTH/2 + half_pages_width, 410, pages_width, 40, text, function = self.openStats))
        
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.statsButtons.append(Button(WIDTH/2 - half_width, 470, width, 60, text, function = self.openAchievementsMain))
        
        # --- Trophies buttons ---
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.trophiesButtons.append(Button(WIDTH/2 - half_width, 470, width, 60, text, function = self.openAchievementsMain))
        
        # --- Themes buttons ---
        string = {'ENG': 'BACK', 'EST': 'TAGASI'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.themesButtons.append(Button(WIDTH/2 - half_width, 470, width, 60, text, function = self.openAchievementsMain))