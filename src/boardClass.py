import random
import copy

class Board:
    def __init__(self, code=None):
        self.__resetBoard()

        if code:
            self.code = code
            for row in range(9):
                for col in range(9):
                    self.board[row][col] = int(code[0])
                    code = code [1:]
        else:
            self.code = None
    
    def __resetBoard(self):
        self.board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        return self.board
    
    def boardToCode(self, input_board = None):
        if input_board:
            _code = ''.join([str(i) for j in input_board for i in j])
            return _code
        else:
            self.code = ''.join([str(i) for j in self.board for i in j])
            return self.code
        
    def findSpaces(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if self.board[row][col] == 0:
                    return(row, col)
        return False
    
    # check if number can be fitted into position
    def checkSpace(self, num, space):
        # if space is a number already
        if not self.board[space[0]][space[1]] == 0:
            return False
        
        # if number already in row
        for col in self.board[space[0]]:
            if col == num:
                return False
        
        # if number already in column
        for row in range(len(self.board)):
            if self.board[row][space[1]] == num:
                return False

        _internalBoxRow = space[0] // 3
        _internalBoxCol = space[1] // 3
        
        # if number already in small box
        for i in range(3):
            for j in range(3):
                if self.board[i + (_internalBoxRow * 3)][j + (_internalBoxCol * 3)] == num:
                    return False
        
        return True
    
    def solve(self):
        _spacesAvailable = self.findSpaces()
        
        if not _spacesAvailable:
            return True
        else:
            row, col = _spacesAvailable
            
        for n in range(1, 10):
            if self.checkSpace(n, (row, col)):
                self.board[row][col] = n
                
                if self.solve():
                    return self.board
                
                self.board[row][col] = 0
                
        return False

    def solveForCode(self):
        return self.boardToCode(self.solve())
    
    def __generateRandomCompleteBoard(self):
        self.__resetBoard()
        
        _l = list(range(1, 10))
        for row in range(3):
            for col in range(3):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)
                
        _l = list(range(1, 10))
        for row in range(6, 9):
            for col in range(6, 9):
                _num = random.choice(_l)
                self.board[row][col] = _num
                _l.remove(_num)
        
        return self.__generateCont()
    
    def __generateCont(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    _num = random.randint(1, 9)
                    
                    if self.checkSpace(_num, (row, col)):
                        self.board[row][col] = _num
                        
                        if self.solve():
                            self.__generateCont()
                            return self.board
                        
                        self.board[row][col] = 0
                        
        return False
    
    def __solveToFindNumberOfSolutions(self, row, col):
        for n in range(1, 10):
            if self.checkSpace(n, (row, col)):
                self.board[row][col] = n
                
                if self.solve():
                    return self.board
                
                self.board[row][col] = 0
                
        return False
    
    def __findSpacesToFindNumberOfSolutions(self, board, h):
        _k = 1
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    if _k == h:
                        return (row, col)
                    
                    _k += 1
        return False
    
    def findNumberOfSolutions(self):
        _z = 0
        _list_of_solutions = []
        
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 0:
                    _z += 1
                    
        for i in range(1, _z+1):
            _board_copy = copy.deepcopy(self)
            
            _row, _col = self.__findSpacesToFindNumberOfSolutions(_board_copy.board, i)
            _board_copy_solution = _board_copy.__solveToFindNumberOfSolutions(_row, _col)
            
            _list_of_solutions.append(self.boardToCode(input_board=_board_copy_solution))
            
        return list(set(_list_of_solutions))
    
    def generateQuestionBoard(self, fullBoard, difficulty):
        self.board = copy.deepcopy(fullBoard)
        
        if difficulty == 0:
            _squares_to_remove = 26
        elif difficulty == 1:
            _squares_to_remove = 36
        elif difficulty == 2:
            _squares_to_remove = 46
        else:
            return
        
        _counter = 0
        while _counter < 4:
            _rRow = random.randint(0, 2)
            _rCol = random.randint(0, 2)
            if self.board[_rRow][_rCol] != 0:
                self.board[_rRow][_rCol] = 0
                _counter += 1
                
        _counter = 0
        while _counter < 4:
            _rRow = random.randint(3, 5)
            _rCol = random.randint(3, 5)
            if self.board[_rRow][_rCol] != 0:
                self.board[_rRow][_rCol] = 0
                _counter += 1
                
        _counter = 0
        while _counter < 4:
            _rRow = random.randint(6, 8)
            _rCol = random.randint(6, 8)
            if self.board[_rRow][_rCol] != 0:
                self.board[_rRow][_rCol] = 0
                _counter += 1
                
        _squares_to_remove -= 12
        _counter = 0
        while _counter < _squares_to_remove:
            _row = random.randint(0, 8)
            _col = random.randint(0, 8)
            
            if self.board[_row][_col] != 0:
                n = self.board[_row][_col]
                self.board[_row][_col] = 0
                
                if len(self.findNumberOfSolutions()) != 1:
                    self.board[_row][_col] = n
                    continue
                    
                _counter += 1
                
        return self.board, fullBoard
    
    def generateQuestionBoardCode(self, difficulty):
        self.board, _solution_board = self.generateQuestionBoard(self.__generateRandomCompleteBoard(), difficulty)
        return self.board, _solution_board