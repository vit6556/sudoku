import os, itertools
from random import shuffle, randint
from copy import deepcopy

sudoku_banner = " ____            _       _\n/ ___| _   _  __| | ___ | | ___   _\n\___ \| | | |/ _` |/ _ \| |/ / | | |\n ___) | |_| | (_| | (_) |   <| |_| |\n|____/ \__,_|\__,_|\___/|_|\_\\\__,_|\n"

class SudokuBoard:
    def __init__(self, amount_of_filled_cells):
        self.__board = [[0] * 9 for _ in range(9)]
        self.__number_list = [i for i in range(1, 10)]
        self.__message_to_show = ""        
        self.__fill_board(deepcopy(self.__board))
        self.__delete_numbers(amount_of_filled_cells)
        self.__start_board = deepcopy(self.__board)
        self.__players_steps = []
    
    def return_to_start_board(self):
        self.__board = deepcopy(self.__start_board)
        self.__players_steps = []

    def next_solution_step(self):
        step = self.__solution[0]
        del self.__solution[0]
        return step

    def __clear(self):
        os.system('cls' if os.name=='nt' else 'clear')

    def add_message_to_show(self, message):
        self.__message_to_show = message

    def show(self):
        self.__clear()
        print(sudoku_banner)
        for i in range(len(self.__board)):
            if i % 3 == 0:
                if i == 0:
                    print(" ----------------------- ")
                else:
                    print("|-------+-------+-------|")

            for j in range(len(self.__board[i])):
                if j % 3 == 0: 
                    print("| ", end="")

                if self.__board[i][j] != 0:
                    print(self.__board[i][j], end="")
                else:
                    print(".", end="")

                if j == 8: 
                    print(" |\n", end="")
                else: 
                    print(" ", end="")

            if i == 8:
                print(" ----------------------- ")
        
        if self.__message_to_show != "":
            print(self.__message_to_show)
            self.__message_to_show = ""

    def put_value(self, x, y, val):
        if (x < 0 or x > 8 or y < 0 or y > 8 or val < 1 or val > 9): 
            self.__message_to_show = "Все числа должны находиться в диапазоне от 1 до 9"
        elif self.__board[x][y] != 0:
            self.__message_to_show = "В этой клетке уже есть число, выберите другую"
        else:
            self.__board[x][y] = val
            self.__players_steps.append((x, y))

    def delete_last_player_step(self):
        if len(self.__players_steps) == 0:
            return False
        else:
            row, col = self.__players_steps[-1][0], self.__players_steps[-1][1]
            self.__board[row][col] = 0
            del self.__players_steps[-1]
            self.show()
            return True


    def board_full(self):
        for line in self.__board:
            if 0 in line:
                return False
        return True

    def check_cell_empty(self, row, col):
        return self.__board[row][col] == 0

    def __valid(self, board, value, row, col):
        for i in range(len(board[0])):
            if board[row][i] == value and col != i:
                return False

        for j in range(9):
            if board[j][col] == value:
                return False

        square_x = col // 3
        square_y = row // 3

        for i in range(square_y * 3, square_y * 3 + 3):
            for j in range(square_x * 3, square_x * 3 + 3):
                if board[i][j] == value and (i, j) != (row, col):
                    return False

        return True

    def __find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)

        return None

    def __fill_board(self, board, solution=[], find_solution=False):
        pos = self.__find_empty(board)
        if not pos:
            self.__board = deepcopy(board)
            self.__solution = deepcopy(solution)
            shuffle(self.__solution)
            return True
        else:
            row, col = pos

        if board[row][col] == 0:
            shuffle(self.__number_list)    
            for value in self.__number_list:
                if self.__valid(board, value, row, col):
                    board[row][col] = value
                    solution.append((row, col, value))

                    if self.__fill_board(board, solution, find_solution):
                        return True

                    del solution[-1]
                    board[row][col] = 0
        
        return False

    def check_board_valid(self):
        for row in self.__board:
            if len(row) != len(set(row)):
                return False

        for i in range(9):
            col = [row[i] for row in self.__board]
            if len(col) != len(set(col)):
                return False

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                square = []
                for row in self.__board[i:i+3]:
                    square += row[j:j+3]
                if len(square) != len(set(tuple(square))):
                    return False
        
        return True

    def __delete_numbers(self, amount_of_filled_cells):
        amount_of_deleted = 0
        while 81 - amount_of_deleted > amount_of_filled_cells:
            row = randint(0,8)
            col = randint(0,8)
            while self.__board[row][col] == 0:
                row = randint(0,8)
                col = randint(0,8)

            self.__board[row][col] = 0
            amount_of_deleted += 1
