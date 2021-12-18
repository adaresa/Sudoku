import pygame
from copy import deepcopy
from settings import *
from buttonClass import *
from boardClass import *

class App:
    def __init__(self, language, launchMenu, quitGame, loadingScreen):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font = pygame.font.SysFont('arial', 50) # cell numbers
        self.font2= pygame.font.Font('../assets/fonts/maldini/MaldiniNormal2.ttf', 26) # button text
        self.font3 = pygame.font.Font('../assets/fonts/maldini/MaldiniNormal2.ttf', 20) # buttons text
        
        self.language = language
        self.saveWin = True
        
        self.grid = Board()
        self.difficulty = 0
        self.gridScreen, self.gridResult = self.grid.generateQuestionBoardCode(self.difficulty) # 0-2 difficulty
        self.gridOriginal = deepcopy(self.gridScreen) # original grid to track which values are generated or player inserted
        
        self.solvedCells = []
        self.mistakeCells = []
        self.mistakeCellsIndex = 0
        
        self.mousePos = None # (x, y) for mouse coordinates
        self.selected = None # player selected grid (clicked)
        self.hovered = None # player hovered grid (holding mouse over)
        
        self.launchMenu = launchMenu
        self.quitGame = quitGame
        self.loadingScreen = loadingScreen
        
        self.playingButtons = []
        self.loadButtons()

###### PLAYING STATE FUNCTIONS ######

    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if 0 <= event.key - 48 <= 9:
                    if self.selected:
                        number = event.key - 48
                        if self.gridOriginal[self.selected[1]][self.selected[0]] is 0:
                            self.changeNumber(self.selected, number)
                                
            if event.type == pygame.QUIT:
                self.quitGame()

            if event.type == pygame.MOUSEMOTION:
                hovered = self.mouseOnGrid()
                if hovered:
                    self.hovered = hovered
                else:
                    self.hovered = None

            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    for i, button in enumerate(self.playingButtons):
                        if i is 1:
                            if self.selected:
                                button.parameter(self.selected)
                                button.activate(self.mousePos)
                        else:
                            button.activate(self.mousePos)
                    self.selected = None
                    
    def playing_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingButtons:
            button.update(self.mousePos)
        
    def playing_draw(self):
        self.window.fill(BG)
        self.drawsolvedCells(self.window) # green background for solved grid
        if self.mistakeCells:
            self.drawMistakes(self.window)
        for button in self.playingButtons:
            button.draw(self.window)
        if self.hovered:
            self.drawSelection(self.window, self.hovered, 1)  # 1 -> GRAY
        if self.selected:
            self.drawSelection(self.window, self.selected, 2) # 2 -> LIGHTGRAY
        self.drawGrid(self.window)
        self.drawNumbers()
        
        self.winCheck(self.window)
        pygame.display.update()

###### HELPER FUNCTIONS ######

    def winCheck(self, window):
        if self.gridScreen == self.gridResult:
            if self.saveWin:
                if self.difficulty == 0:
                    saveStat("wins_easy", 1)
                elif self.difficulty == 1:
                    saveStat("wins_medium", 1)
                elif self.difficulty == 2:
                    saveStat("wins_hard", 1)
            playSound(WIN_SOUND)
            for x in range(9):
                for y in range(9):
                    pygame.draw.rect(window, LIMEGREEN, ((
                        x * cellSize) + gridPos[0], (y * cellSize) + gridPos[1], cellSize, cellSize))
            self.drawNumbers()
            self.drawGrid(self.window)
            pygame.display.update()
            pygame.time.delay(5000)
            self.resetGame()
            
    def resetGame(self):
        self.loadingScreen()
        self.gridScreen, self.gridResult = self.grid.generateQuestionBoardCode(self.difficulty) # 0-2 difficulty
        self.gridOriginal = deepcopy(self.gridScreen) # original grid to track which values are generated or player inserted
        self.solvedCells = []
        self.selected = None
        self.saveWin = True
        
    def changeDifficulty(self, difficulty):
        self.difficulty = difficulty
        self.resetGame()

    # Colors selected and hovered grid
    def drawSelection(self, window, pos, color):
        if color is 2:
            pygame.draw.rect(window, LIGHTGRAY, ((
                pos[0] * cellSize) + gridPos[0], (pos[1] * cellSize) + gridPos[1], cellSize, cellSize))
        elif color is 1:
            pygame.draw.rect(window, GRAY, ((
                pos[0] * cellSize) + gridPos[0], (pos[1] * cellSize) + gridPos[1], cellSize, cellSize))
    
    # Draw numbers on all grids 
    def drawNumbers(self):
        for x in range(9):
            for y in range(9):
                if self.gridScreen[y][x] is not 0:
                    # text style for generated number
                    if self.gridOriginal[y][x] is not 0:
                        self.text = self.font.render(str(self.gridScreen[y][x]), True, SNOW) # (text, antialias, color)
                        
                    # text style for user inserted number
                    else:
                        self.text = self.font.render(str(self.gridScreen[y][x]), True, COBALTBLUE) # (text, antialias, color)
                        
                    self.window.blit(self.text, (13 + gridPos[0] + (x * cellSize), 
                                                gridPos[1] - 3 + (y * cellSize))) # (text, (x,y))
                    
    def changeNumber(self, pos, number):
        playSound(INPUT_SOUND)
        self.gridScreen[pos[1]][pos[0]] = number
        
    def solveCell(self, pos):
        self.saveWin = False
        playSound(MENU_SOUND)
        if self.gridOriginal[pos[1]][pos[0]] is not self.gridResult[pos[1]][pos[0]]:
            self.gridScreen[pos[1]][pos[0]] = self.gridResult[pos[1]][pos[0]]
            self.gridOriginal[pos[1]][pos[0]] = self.gridResult[pos[1]][pos[0]]
            self.solvedCells.append((pos[1], pos[0]))
            
    def drawsolvedCells(self, window):
        for cell in self.solvedCells:
            pygame.draw.rect(window, LIMEGREEN, ((
                cell[1] * cellSize) + gridPos[0], (cell[0] * cellSize) + gridPos[1], cellSize, cellSize))
            
    def showMistakes(self):
        self.saveWin = False
        playSound(MENU_SOUND)
        self.mistakeCells = []
        for x in range(9):
            for y in range(9):
                if self.gridScreen[y][x] != 0:
                    if self.gridScreen[y][x] != self.gridResult[y][x]:
                        self.mistakeCells.append((y, x))
        self.mistakeCellsIndex = 0
    
    def drawMistakes(self, window):
        if self.mistakeCellsIndex < 1000:
            for cell in self.mistakeCells:
                pygame.draw.rect(window, CRIMSON, ((
                    cell[1] * cellSize) + gridPos[0], (cell[0] * cellSize) + gridPos[1], cellSize, cellSize))
        else:
            for cell in self.mistakeCells:
                pygame.draw.rect(window, BG, ((
                        cell[1] * cellSize) + gridPos[0], (cell[0] * cellSize) + gridPos[1], cellSize, cellSize))
            self.mistakeCells = []
            self.mistakeCellsIndex = 0
        self.mistakeCellsIndex += 1

    # Draw the gridlines
    def drawGrid(self, window):
        pygame.draw.rect(
            window, SNOW, (gridPos[0], gridPos[1], WIDTH-150, HEIGHT-150), 3)
        for x in range(9):
            if x % 3 == 0:
                # Fat line vertical
                pygame.draw.line(window, SNOW, (gridPos[0] + (
                    x * cellSize), gridPos[1]), (gridPos[0] + (x * cellSize), gridPos[1] + 450), 3)
                # Fat line horizontal
                pygame.draw.line(window, SNOW, (gridPos[0], gridPos[1] + (
                    x * cellSize)), (gridPos[0] + 450, gridPos[1] + (x * cellSize)), 3)
            else:
                pygame.draw.line(window, SNOW, (gridPos[0] + (
                    x * cellSize), gridPos[1]), (gridPos[0] + (x * cellSize), gridPos[1] + 450))
                pygame.draw.line(window, SNOW, (gridPos[0], gridPos[1] + (
                    x * cellSize)), (gridPos[0] + 450, gridPos[1] + (x * cellSize)))

    # Check if mouse is on grid
    def mouseOnGrid(self):
        if self.mousePos:
            inGridHorizontal = (self.mousePos[0] > gridPos[0] and self.mousePos[0] < gridPos[0]+gridSize)
            inGridVertical = (self.mousePos[1] > gridPos[1] and self.mousePos[1] < gridPos[1]+gridSize)
            if inGridHorizontal and inGridVertical:
                return ((self.mousePos[0] - gridPos[0]) // cellSize, (self.mousePos[1] - gridPos[1]) // cellSize)
            return False

    # Check if mouse on a button
    def mouseOnButton(self):
        if self.mousePos:
            for button in self.playingButtons:
                inBtnHorizontal = (self.mousePos[0] > button.pos[0] and self.mousePos[0] < button.pos[0]+button.dims[0])
                inBtnVertical = (self.mousePos[1] > button.pos[1] and self.mousePos[1] < button.pos[1]+button.dims[1])
                if inBtnHorizontal and inBtnVertical:
                    return True
        return False
    
    def goToMenu(self):
        self.launchMenu()
    
    # Load all buttons on screen
    def loadButtons(self):
        string = {'ENG': 'Back', 'EST': 'Tagasi'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.playingButtons.append(Button(gridPos[0], 40, 100, 40, text, function = self.goToMenu))
        
        string = {'ENG': 'Solve cell', 'EST': 'Lahenda'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.playingButtons.append(Button(WIDTH/2 - 108, 40, 100, 40, text, function = self.solveCell))
        
        string = {'ENG': 'Mistakes', 'EST': 'Vead'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.playingButtons.append(Button(WIDTH/2 + 8, 40, 100, 40, text, function = self.showMistakes))
        
        string = {'ENG': 'New', 'EST': 'Uus'}
        text = self.font2.render(string.get(self.language), True, SNOW) # (text, antialias, color)
        self.playingButtons.append(Button(gridPos[0]+gridSize - 100, 40, 100, 40, text, function = self.resetGame))

