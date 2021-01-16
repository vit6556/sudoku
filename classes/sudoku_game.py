import time, pickle, sys, os
from hashlib import md5
from pathlib import Path

sys.path.append("classes/")
from sudoku_board import SudokuBoard, sudoku_banner

class SudokuGame:
    def __init__(self):
        self.self = self

    def setup(self):
        while not self.self.__get_all_params(): pass

    def __get_all_params(self):
        if self.self.__get_new_or_load() == 1:
            self.self.__game_type = self.self.__get_game_type()
            amount_of_filled_cells = self.self.__get_amount_of_filled_cells()
            self.self.__board = SudokuBoard(amount_of_filled_cells)
            return True
        else:
            val, saves = self.self.__get_save_name()

            if val == 0: return False

            with open(f'{saves[val - 1]}', 'rb') as f:
                self.self = pickle.load(f)

            return True

    def __clear(self):
        os.system('cls' if os.name=='nt' else 'clear')
        print(sudoku_banner)

    def __get_game_type(self):
        self.self.__clear()
        game_type = input("Режим игры:\n(1) Для пользователя\n(2) Для компьютера\n\nВаш выбор: ")
        while type(game_type) != int:
            try:
                game_type = int(game_type)
                assert game_type in [1, 2]
            except:
                self.self.__clear() 
                game_type = input("Режим игры:\n(1) Для пользователя\n(2) Для компьютера\n\nРежим игры должен соответствовать одному из представленных вариантов\n\nВаш выбор: ")

        return game_type - 1

    def __get_amount_of_filled_cells(self):
        self.self.__clear()
        amount_of_filled_cells = input("Количество заполненных клеток: ")
        while type(amount_of_filled_cells) != int:
            try:
                amount_of_filled_cells = int(amount_of_filled_cells)
                assert amount_of_filled_cells >= 0 and amount_of_filled_cells <= 80
            except:
                self.self.__clear() 
                amount_of_filled_cells = input("Значение должно быть в диапазоне от 0 до 80\n\nКоличество заполненных клеток: ")

        return amount_of_filled_cells


    def __get_input_for_save_name(self, without_warning=True):
        self.self.__clear()
        saves = []
        print("Сохранения:\n(0) Выход")
        for f in os.listdir():
            if f.endswith(".pkl"):
                print(f"({len(saves) + 1}) {f.replace('.pkl', '')}")
                saves.append(f)

        if not without_warning:
            print("\nНомер сохранения должен соответствовать одному из представленных вариантов")
        val = input("\nВаш выбор: ")
        return val, saves

    def __get_save_name(self):
        val, saves = self.self.__get_input_for_save_name()
        while type(val) != int:
            try:
                val = int(val)
                assert val >= 0 and val <= len(saves)
            except:
                self.self.__clear() 
                val, saves = self.self.__get_input_for_save_name(False)
        
        return val, saves

    def __check_input_types(self, users_input):
        input_values = users_input.split()
        if len(input_values) != 3:
            self.self.__board.add_message_to_show("Нужно ввести три числа через пробел: две координаты клетки и число, которое нужно записать в эту клетку")
            return
        try:
            x = int(input_values[0]) - 1
            y = int(input_values[1]) - 1
            val = int(input_values[2])
            return (x, y, val)
        except:
            self.self.__board.add_message_to_show("Вводимые значения должны быть целыми числами")
            return

    def __get_new_or_load(self):
        self.self.__clear()
        val = input("Тип игры:\n(1) Новая игра\n(2) Загрузить сохранение из файла\n\nВаш выбор: ")
        while type(val) != int:
            try:
                val = int(val)
                assert val in [1, 2]
            except:
                self.self.__clear() 
                val = input("Тип игры:\n(1) Новая игра\n(2) Загрузить сохранение из файла\n\nТип игры должен соответствовать одному из представленных вариантов\n\nВаш выбор: ")

        return val
        
    def play(self):
        self.self.__board.show()
        if self.self.__game_type == 0:
            while not self.self.__board.board_full():
                self.self.__board.show()
                not_prepared_input = input("Введите координаты клетки и число через пробелы:\n")
                if len(not_prepared_input) == 0: continue
                if not_prepared_input.split()[0] == "save":
                    self.self.__clear()
                    name = input("Название сохранения: ").split()[0]
                    with open(f'{name}.pkl', 'wb') as f:
                        pickle.dump(self.self, f)
                    self.self.__board.show()
                elif not_prepared_input.split()[0] == "load":
                    name, saves = self.self.__get_save_name()
                    if name == 0: continue
                    
                    with open(f'{saves[name - 1]}', 'rb') as f:
                        self.self = pickle.load(f)
                    self.self.__board.show()
                elif not_prepared_input.split()[0] == "del":
                    if not self.self.__board.delete_last_player_step():
                        self.self.__board.add_message_to_show("Нет ходов, которые можно удалить")
                        self.self.__board.show()
                elif not_prepared_input.split()[0] == "exit":
                    print("До свидания!")
                    return
                else:
                    users_input = self.self.__check_input_types(not_prepared_input)
                    if users_input != None:
                        self.self.__board.put_value(users_input[0], users_input[1], users_input[2])
            self.self.__board.show()
            if self.self.__board.check_board_valid():
                print(f"Поздравляем! Вы верно решили судоку")
            else:
                self.self.__board.return_to_start_board()
                name = f"game_{md5(str(self).encode()).hexdigest()[:6]}"
                with open(f'{name}.pkl', 'wb') as f:
                    pickle.dump(self.self, f)
                print(f"Судоку решено неверно\nНачальное состояние сохранено в файл {name}, можете попробовать решить судоку еще раз")

        else:
            while not self.self.__board.board_full():
                step = self.self.__board.next_solution_step()
                if self.self.__board.check_cell_empty(step[0], step[1]):
                    time.sleep(1)
                    self.self.__board.put_value(step[0], step[1], step[2])
                    self.self.__board.add_message_to_show(f"Ход компьютера: {step[0] + 1} {step[1] + 1} {step[2]}")
                    self.self.__board.show()
            self.self.__board.show()
            if self.self.__board.check_board_valid:
                print("Компьютер решили судоку")
            else:
                print("Компьютер неправильно решил судоку... Скорее всего это судоку не имеет решений")
