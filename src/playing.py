import time
from buttonClass import *
from boardClass import *

class App:
    def __init__(self, theme, language, launchMenu, quitGame, loadingScreen):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        
        self.theme = theme
        self.language = language
        self.counterStart = None
        self.timer = 0
        self.saveWin = True
        
        self.grid = Board()
        self.difficulty = 0
        self.gridScreen, self.gridResult = self.grid.generateQuestionBoardCode(self.difficulty) # 0-2 difficulty
        self.gridOriginal = copy.deepcopy(self.gridScreen) # original grid to track which values are generated or player inserted
        
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
                if 0 <= event.key - 48 <= 9: # 0-9
                    if self.selected:
                        number = event.key - 48
                        if self.gridOriginal[self.selected[1]][self.selected[0]] == 0:
                            self.changeNumber(self.selected, number)
                elif event.key == 27: # esc
                    self.goToMenu()
                                
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
                    for button in self.playingButtons:
                            button.activate(self.mousePos)
                    self.selected = None
                    
    def playing_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingButtons:
            button.update(self.mousePos)
        
    def playing_draw(self):
        self.window.fill(BG[self.theme])
        self.drawsolvedCells(self.window) # green background for solved grid
        if self.mistakeCells:
            self.drawMistakes(self.window)
        for button in self.playingButtons:
            button.draw(self.window)
        if self.hovered:
            self.drawSelection(self.window, self.hovered, 1)
        if self.selected:
            self.drawSelection(self.window, self.selected, 2)
        self.drawGrid(self.window)
        self.drawNumbers()
        self.drawTime()
        
        self.winCheck(self.window)
        pygame.display.update()
    
    def count_time(self):
        if self.counterStart is None:
            self.counterStart = time.perf_counter()
        else:
            elapsed = time.perf_counter() - self.counterStart
            if elapsed >= 1:
                self.timer += 1
                self.counterStart = None
            

###### HELPER FUNCTIONS ######
    def drawTime(self):
        drawText(time.strftime("%M:%S", time.gmtime(self.timer)), CENTER+(3*cellSize), 568, fontStatValue, TEXT[self.theme], self.window)
        pygame.draw.line(self.window, OUTLINES_TIMER[self.theme], (gridPos[0] + (
                    6 * cellSize), gridPos[1]+gridSize), (gridPos[0] + (6 * cellSize), gridPos[1]+gridSize + 35), 3)
        pygame.draw.line(self.window, OUTLINES_TIMER[self.theme], (gridPos[0] + (
                    9 * cellSize)-1, gridPos[1]+gridSize), (gridPos[0]-1 + (9 * cellSize), gridPos[1]+gridSize + 35), 3)
        pygame.draw.line(self.window, OUTLINES_TIMER[self.theme], (gridPos[0] + (
                    6*cellSize), gridPos[1]+gridSize + 35), (gridPos[0] + (9*cellSize), gridPos[1] + gridSize + 35), 3)

    def winCheck(self, window):
        if self.gridScreen == self.gridResult:
            if self.saveWin:
                if self.difficulty == 0:
                    saveStat("wins_easy", 1)
                    saveStat("time_easy", self.timer, compare=-1)
                elif self.difficulty == 1:
                    saveStat("wins_medium", 1)
                    saveStat("time_medium", self.timer, compare=-1)
                elif self.difficulty == 2:
                    saveStat("wins_hard", 1)
                    saveStat("time_hard", self.timer, compare=-1)
                saveStat("time_total", self.timer)
            playSound(WIN_SOUND)
            for x in range(9):
                for y in range(9):
                    pygame.draw.rect(window, SOLVED[self.theme], ((
                        x * cellSize) + gridPos[0], (y * cellSize) + gridPos[1], cellSize, cellSize))
            self.drawNumbers()
            self.drawGrid(self.window)
            pygame.display.update()
            pygame.time.delay(5000)
            self.resetGame()
            
    def resetGame(self):
        self.loadingScreen()
        self.gridScreen, self.gridResult = self.grid.generateQuestionBoardCode(self.difficulty) # 0-2 difficulty
        self.gridOriginal = copy.deepcopy(self.gridScreen) # original grid to track which values are generated or player inserted
        self.solvedCells = []
        self.selected = None
        self.saveWin = True
        self.timer = 0
        self.counterStart = None
        
    def changeDifficulty(self, difficulty):
        self.difficulty = difficulty
        self.resetGame()

    # Colors selected and hovered grid
    def drawSelection(self, window, pos, color):
        if color == 2:
            pygame.draw.rect(window, SELECTED[self.theme], ((
                pos[0] * cellSize) + gridPos[0], (pos[1] * cellSize) + gridPos[1], cellSize, cellSize))
        elif color == 1:
            pygame.draw.rect(window, HOVERED[self.theme], ((
                pos[0] * cellSize) + gridPos[0], (pos[1] * cellSize) + gridPos[1], cellSize, cellSize))
    
    # Draw numbers on all grids 
    def drawNumbers(self):
        for x in range(9):
            for y in range(9):
                if self.gridScreen[y][x] != 0:
                    # text style for generated number
                    if self.gridOriginal[y][x] != 0:
                        self.text = fontCell.render(str(self.gridScreen[y][x]), True, TEXT[self.theme]) # (text, antialias, color)
                        
                    # text style for user inserted number
                    else:
                        self.text = fontCell.render(str(self.gridScreen[y][x]), True, INSERT_NUMBER[self.theme]) # (text, antialias, color)
                        
                    self.window.blit(self.text, (13 + gridPos[0] + (x * cellSize), 
                                                gridPos[1] - 3 + (y * cellSize))) # (text, (x,y))
                    
    def changeNumber(self, pos, number):
        playSound(INPUT_SOUND)
        self.gridScreen[pos[1]][pos[0]] = number
        
    def solveCell(self):
        if self.selected:
            pos = self.selected
            if self.gridOriginal[pos[1]][pos[0]] is not self.gridResult[pos[1]][pos[0]]:
                self.saveWin = False
                self.gridScreen[pos[1]][pos[0]] = self.gridResult[pos[1]][pos[0]]
                self.gridOriginal[pos[1]][pos[0]] = self.gridResult[pos[1]][pos[0]]
                self.solvedCells.append((pos[1], pos[0]))
            
    def drawsolvedCells(self, window):
        for cell in self.solvedCells:
            pygame.draw.rect(window, SOLVED[self.theme], ((
                cell[1] * cellSize) + gridPos[0], (cell[0] * cellSize) + gridPos[1], cellSize, cellSize))
            
    def showMistakes(self):
        self.saveWin = False
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
                pygame.draw.rect(window, MISTAKES[self.theme], ((
                    cell[1] * cellSize) + gridPos[0], (cell[0] * cellSize) + gridPos[1], cellSize, cellSize))
        else:
            for cell in self.mistakeCells:
                pygame.draw.rect(window, BG[self.theme], ((
                        cell[1] * cellSize) + gridPos[0], (cell[0] * cellSize) + gridPos[1], cellSize, cellSize))
            self.mistakeCells = []
            self.mistakeCellsIndex = 0
        self.mistakeCellsIndex += 1

    # Draw the gridlines
    def drawGrid(self, window):
        pygame.draw.rect(
            window, OUTLINES[self.theme], (gridPos[0], gridPos[1], WIDTH-150, HEIGHT-150), 3)
        for x in range(9):
            if x % 3 == 0:
                # Fat line vertical
                pygame.draw.line(window, OUTLINES[self.theme], (gridPos[0] + (
                    x * cellSize), gridPos[1]), (gridPos[0] + (x * cellSize), gridPos[1] + 450), 3)
                # Fat line horizontal
                pygame.draw.line(window, OUTLINES[self.theme], (gridPos[0], gridPos[1] + (
                    x * cellSize)), (gridPos[0] + 450, gridPos[1] + (x * cellSize)), 3)
            else:
                pygame.draw.line(window, OUTLINES[self.theme], (gridPos[0] + (
                    x * cellSize), gridPos[1]), (gridPos[0] + (x * cellSize), gridPos[1] + 450))
                pygame.draw.line(window, OUTLINES[self.theme], (gridPos[0], gridPos[1] + (
                    x * cellSize)), (gridPos[0] + 450, gridPos[1] + (x * cellSize)))

    # Check if mouse is on grid
    def mouseOnGrid(self):
        if self.mousePos:
            inGridHorizontal = (self.mousePos[0] > gridPos[0] and self.mousePos[0] < gridPos[0]+gridSize)
            inGridVertical = (self.mousePos[1] > gridPos[1] and self.mousePos[1] < gridPos[1]+gridSize)
            if inGridHorizontal and inGridVertical:
                return ((self.mousePos[0] - gridPos[0]) // cellSize, (self.mousePos[1] - gridPos[1]) // cellSize)
            return False
    
    def goToMenu(self):
        self.launchMenu()
    
    # Load all buttons on screen
    def loadButtons(self):
        self.playingButtons.append(Button(gridPos[0], 40, 100, 40, self.theme,
            renderText(getText(self.language, 'back_button_lower'), fontButtonPlay, TEXT[self.theme]), function = self.goToMenu))
        
        self.playingButtons.append(Button(WIDTH/2 - 108, 40, 100, 40, self.theme,
            renderText(getText(self.language, 'game_solve'), fontButtonPlay, TEXT[self.theme]), function = self.solveCell))
        
        self.playingButtons.append(Button(WIDTH/2 + 8, 40, 100, 40, self.theme,
            renderText(getText(self.language, 'game_mistakes'), fontButtonPlay, TEXT[self.theme]), function = self.showMistakes))
        
        self.playingButtons.append(Button(gridPos[0]+gridSize - 100, 40, 100, 40, self.theme,
            renderText(getText(self.language, 'game_new'), fontButtonPlay, TEXT[self.theme]), function = self.resetGame))

