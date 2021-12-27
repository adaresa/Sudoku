import sys
from playing import *
from options import *
from achievements import *

class Menu:
    def __init__(self, theme, language):
        pygame.init()
        pygame.display.set_caption('Simple Sudoku')
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_icon(loadImage('images', 'icon.png'))
        
        musicStart()
        self.theme = theme
        self.language = language
        
        self.running = True
        self.state = "main_menu"
        self.loadingScreen()
        self.app = App(self.theme, self.language, self.launchMenu, self.quitGame, self.loadingScreen)
        self.options = Options(self.theme, self.language, self.launchMenu, self.quitGame, self.app.changeDifficulty, self.changeLanguage)
        self.achievements = Achievements(self.theme, self.language, self.launchMenu, self.quitGame, self.changeTheme)
        
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
                self.app.count_time()
            elif self.state == "achievements":
                self.achievements.achievements_events()
                self.achievements.achievements_update()
                self.achievements.achievements_draw()
            elif self.state == "options":
                self.options.options_events()
                self.options.options_update()
                self.options.options_draw()
        closeDB()
        pygame.quit()
        sys.exit()
        
    ###### MAIN MENU FUNCTIONS ######

    def menu_events(self):
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:
                if event.key == 27: # esc
                    self.quitGame()
                                
            if event.type == pygame.QUIT:
                self.quitGame()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.menuButtons:
                    button.activate(self.mousePos)

    def menu_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.menuButtons:
            button.update(self.mousePos)
        
    def menu_draw(self):
        self.window.fill(BG[self.theme])
        self.titleText()
        for button in self.menuButtons:
            button.draw(self.window)
        pygame.display.update()
    
    ###### HELPER FUNCTIONS ######
    
    def titleText(self):
        # title text
        drawText("Simple Sudoku", CENTER, 100, fontTitle, TEXT[self.theme], self.window)
    
    def loadingScreen(self):
        self.window.fill(BG[self.theme])
        drawText(getText(self.language, 'loading'), CENTER, HEIGHT/2, fontTitle, TEXT[self.theme], self.window)
        pygame.display.update()
    
    def changeTheme(self, theme):
        optionsValues("theme", new_value = theme)
        app = Menu(theme, self.language)
        app.run()
    
    def changeLanguage(self, language):
        optionsValues("language", new_value = language)
        app = Menu(self.theme, language)
        app.run()
        
    def launchGame(self):
        self.app.counterStart = None
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
        self.menuButtons.append(Button(CENTER - half_width, 200, width, height, self.theme, 
            renderText(getText(self.language, 'menu_main_1'), fontButton, TEXT[self.theme]), function = self.launchGame))
        
        self.menuButtons.append(Button(CENTER - half_width, 290, width, height, self.theme,
            renderText(getText(self.language, 'menu_main_2'), fontButton, TEXT[self.theme]), function = self.launchAchievements))
        
        self.menuButtons.append(Button(CENTER - half_width, 380, width, height, self.theme,
            renderText(getText(self.language, 'menu_main_3'), fontButton, TEXT[self.theme]), function = self.launchOptions))
        
        self.menuButtons.append(Button(CENTER - half_width, 470, width, height, self.theme,
            renderText(getText(self.language, 'menu_main_4'), fontButton, TEXT[self.theme]), function = self.quitGame))