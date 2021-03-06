import time
import collections
from buttonClass import *
from boardClass import *

class App:
    def __init__(self, theme, language, launchMenu, quitGame, loadingScreen):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.theme = theme
        self.language = language
        self.counterStart = None
        self.timer = 0
        self.timerClick = 0
        self.saveWin = True
        
        self.grid = Board()
        self.difficulty = 0
        self.gridScreen, self.gridResult = self.grid.generateQuestionBoardCode(self.difficulty) # 0-2 difficulty
        self.gridOriginal = copy.deepcopy(self.gridScreen) # original grid to track which values are generated or player inserted
        self.gridSmall = [[[0] for m in range(9)] for n in range(9)] # to track small numbers in a cell
        
        self.solvedCells = []
        self.mistakeCells = []
        self.mistakeCellsIndex = 0
        
        self.mousePos = None # (x, y) for mouse coordinates
        self.selected = None # player selected grid (clicked)
        self.hovered = None # player hovered grid (holding mouse over)
        self.doubled = None # player doubleclicked grid
        self.doubled_space = None # make sure player doubleclicks same spot
        
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
                        # if pressed number is in a replacable cell
                        if self.gridOriginal[self.selected[1]][self.selected[0]] == 0:
                            # if pressed number is already in that cell
                            if number == self.gridScreen[self.selected[1]][self.selected[0]]:
                                # if pressed 0 on empty cell, clear all small numbers
                                if number == 0:
                                    self.changeSmallNumber(self.selected, number, 'clear')
                                else:
                                    # add small number to cell, clear big number
                                    self.changeSmallNumber(self.selected, number, 'add')
                                    self.changeNumber(self.selected, 0)
                                    continue
                            # set big number to pressed number
                            self.changeNumber(self.selected, number)
                elif event.key == 27: # esc
                    self.goToMenu()
                                
            if event.type == pygame.QUIT:
                self.quitGame()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.doubled = None
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                    if self.timerClick == 0:
                        self.timerClick = 0.001
                        self.doubled_space = self.selected
                    elif self.timerClick <= 0.5:
                        if self.selected == self.doubled_space:
                            self.doubled = True
                else:
                    for button in self.playingButtons:
                            button.activate(self.mousePos)
                    self.selected = None
                    
    def playing_update(self):
        self.click_timer_update()
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingButtons:
            button.update(self.mousePos)
        hovered = self.mouseOnGrid()
        if hovered:
            self.hovered = hovered
        else:
            self.hovered = None
        
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
            if self.doubled:
                self.double_click_highlight(self.gridScreen[self.selected[1]][self.selected[0]])
                self.doubled_space = None
        self.drawGrid(self.window)
        self.drawNumbers()
        self.drawSmallNumbers()
        self.drawInfo()
        self.showCompleted(self.getFrequency())
        
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
                
    def click_timer_update(self):
        dt = self.clock.tick(30) / 1000
        if self.timerClick != 0:
            self.timerClick += dt
            if self.timerClick >= 0.5:
                self.timerClick = 0
            

###### HELPER FUNCTIONS ######
    def changeSmallNumber(self, pos, number, action):
        '''
        add/clear small numbers in a cell
        '''
        if action == 'add':
            # if 0, set first value
            if self.gridSmall[pos[1]][pos[0]] == [0]:
                self.gridSmall[pos[1]][pos[0]] = [number]
            else:
                # add new value if less than 3 values, value not already in cell
                if len(self.gridSmall[pos[1]][pos[0]]) < 3 and number not in self.gridSmall[pos[1]][pos[0]]:
                    self.gridSmall[pos[1]][pos[0]].append(number)
        elif action == 'clear':
            # clear all values, set back 0
            self.gridSmall[pos[1]][pos[0]] = [0]
                
    def drawSmallNumbers(self):
        '''
        draw small numbers in a cell
        '''
        for x in range(9):
            for y in range(9):
                if 0 not in self.gridSmall[y][x]:
                    height = 0
                    for num in self.gridSmall[y][x]:
                        self.text = fontSmallCell.render(str(num), True, TEXT[self.theme]) # (text, antialias, color)
                        self.window.blit(self.text, (39 + gridPos[0] + (x * cellSize), 
                                                gridPos[1] + height + (y * cellSize))) # (text, (x,y))
                        height += 15

    def changeNumber(self, pos, number):
        playSound(INPUT_SOUND)
        self.gridScreen[pos[1]][pos[0]] = number
        
    def drawNumbers(self):
        '''
        Draw numbers on all grids 
        '''
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

    def showCompleted(self, total):
        '''
        draw next to board of which numbers player has 9 or more of
        input: dict of {num: frequency}
        '''
        od = collections.OrderedDict(sorted(total.items()))
        header = False
        x, y = gridPos[0] // 2, gridPos[1] + 8
        for key, val in od.items():
            if val >= 9:
                if not header:
                   txt = [getText(self.language, 'game_all_nine'), SAVABLE[0]]
                   drawText(txt[0], x, y, fontButtonPlay, txt[1], self.window)
                   header = True
                   y += 30
                drawText(str(key), x, y, fontButtonPlay, txt[1], self.window)
                y += 30
                
    def getFrequency(self):
        '''
        return dict of number frequencies
        output: dict of {num: frequency}
        '''
        total = {}
        for lst in self.gridScreen:
            for num in lst:
                if num != 0:
                    if num not in total:
                        total[num] = 1
                    else:
                        total[num] += 1
        return(total)

    def double_click_highlight(self, num):
        draw_x = set()
        draw_y = set()
        if num > 0:
            for x in range(9):
                for y in range(9):                    
                    if self.gridScreen[y][x] == num:
                        draw_x.add(x)
                        draw_y.add(y)
        for x in draw_x:
            for y in range(9):
                if self.gridScreen[y][x] == num:
                    self.drawSelection(self.window, (x, y), 2)
                else:
                    self.drawSelection(self.window, (x, y), 3)
        for y in draw_y:
            for x in range(9):
                if self.gridScreen[y][x] == num:
                    self.drawSelection(self.window, (x, y), 2)
                else:
                    self.drawSelection(self.window, (x, y), 3)

    def drawInfo(self):
        '''
        draw self.saveWin, 
        self.difficulty, 
        self.timer 
        under board
        '''
        # 4 vertical lines
        pygame.draw.line(self.window, OUTLINES_TIMER[self.theme], (gridPos[0] + (
                    0 * cellSize), gridPos[1]+gridSize), (gridPos[0] + (0 * cellSize), gridPos[1]+gridSize + 35), 3)
        pygame.draw.line(self.window, OUTLINES_TIMER[self.theme], (gridPos[0] + (
                    3 * cellSize), gridPos[1]+gridSize), (gridPos[0] + (3 * cellSize), gridPos[1]+gridSize + 35), 3)
        pygame.draw.line(self.window, OUTLINES_TIMER[self.theme], (gridPos[0] + (
                    6 * cellSize), gridPos[1]+gridSize), (gridPos[0] + (6 * cellSize), gridPos[1]+gridSize + 35), 3)
        pygame.draw.line(self.window, OUTLINES_TIMER[self.theme], (gridPos[0] + (
                    9 * cellSize)-1, gridPos[1]+gridSize), (gridPos[0]-1 + (9 * cellSize), gridPos[1]+gridSize + 35), 3)
        # 1 horizontal line
        pygame.draw.line(self.window, OUTLINES_TIMER[self.theme], (gridPos[0], 
                    gridPos[1]+gridSize + 35), (gridPos[0] + (9*cellSize), gridPos[1] + gridSize + 35), 3)

        to_save = [getText(self.language, 'game_savable_yes'), SAVABLE[0]] if self.saveWin == True else [getText(self.language, 'game_savable_no'), SAVABLE[1]]
        difficulty = [
            [getText(self.language, 'stat_1_1'), DIFFICULTY[0]], 
            [getText(self.language, 'stat_1_2'), DIFFICULTY[1]],
            [getText(self.language, 'stat_1_3'), DIFFICULTY[2]]
            ]

        drawText(to_save[0], CENTER-(3*cellSize), 568, fontButtonPlay, to_save[1], self.window)
        drawText(difficulty[self.difficulty][0], CENTER, 568, fontButtonPlay, difficulty[self.difficulty][1], self.window)
        drawText(getTime(self.timer), CENTER+(3*cellSize), 568, fontStatValue, TEXT[self.theme], self.window)

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
        self.gridSmall = [[[0] for m in range(9)] for n in range(9)]
        self.selected = None
        self.saveWin = True
        self.timer = 0
        self.counterStart = None
        
    def changeDifficulty(self, difficulty):
        self.difficulty = difficulty
        self.resetGame()

    def drawSelection(self, window, pos, color):
        '''
        Colors selected and hovered grid
        '''
        if color == 3: # TODO change this for doubleclick rows
            pygame.draw.rect(window, DOUBLED[self.theme], ((
                pos[0] * cellSize) + gridPos[0], (pos[1] * cellSize) + gridPos[1], cellSize, cellSize))
        elif color == 2:
            pygame.draw.rect(window, SELECTED[self.theme], ((
                pos[0] * cellSize) + gridPos[0], (pos[1] * cellSize) + gridPos[1], cellSize, cellSize))
        elif color == 1:
            pygame.draw.rect(window, HOVERED[self.theme], ((
                pos[0] * cellSize) + gridPos[0], (pos[1] * cellSize) + gridPos[1], cellSize, cellSize))
        
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
        dt = self.clock.tick(30) / 1000
        if self.mistakeCellsIndex < 2:
            for cell in self.mistakeCells:
                pygame.draw.rect(window, MISTAKES[self.theme], ((
                    cell[1] * cellSize) + gridPos[0], (cell[0] * cellSize) + gridPos[1], cellSize, cellSize))
        else:
            for cell in self.mistakeCells:
                pygame.draw.rect(window, BG[self.theme], ((
                        cell[1] * cellSize) + gridPos[0], (cell[0] * cellSize) + gridPos[1], cellSize, cellSize))
            self.mistakeCells = []
            self.mistakeCellsIndex = 0
        self.mistakeCellsIndex += dt

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

