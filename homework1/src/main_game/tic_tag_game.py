"""
Реализация классического варианта игры (поле 3x3) крестики-нолики в ООП-стиле.
Используемый линтер - Pylint.
Зависимости собраны в requirements.txt.
Установить зависимости: pip install -r requirements.txt
"""

import random

from src.exceptions.custom_exceptions import MyCustomExceptions
from src.utils.check_str_is_number import is_number


class TicTacGame:
    """Класс, реализующий логику игры крестики-нолики в ООП стиле"""

    def __init__(self):
        self.human_symbol = 'X'
        self.computer_symbol = 'O'
        self.count_rounds_start = 0
        self.count_rounds_end = 9
        self.game_pole = [['-' for i in range(3)] for j in range(3)]

    def show_board(self) -> None:
        """Метод, отображающий игровое поле. Подразумевается вызов на каждой игровой итерации"""

        print("Игровое поле на текущий ход:")
        print(' ', 1, 2, 3)
        for i in range(1, 4):
            print(i, end=' ')
            print(*self.game_pole[i - 1])

    def validate_input(self, params_as_string: str) -> tuple:
        """Метод, реализующий валидацию пользовательского ввода"""

        if len(params_as_string.split()) != 2:
            raise MyCustomExceptions.InvalidCountInputArgs

        str_idx, col_idx = params_as_string.split()

        if not (is_number(str_idx) and is_number(col_idx)):
            raise MyCustomExceptions.InvalidTypesInputArgs

        str_idx, col_idx = int(str_idx), int(col_idx)

        if not (1 <= str_idx <= 3 and 1 <= col_idx <= 3):
            raise MyCustomExceptions.InvalidRangeInputArgs
        if self.game_pole[str_idx - 1][col_idx - 1] != '-':
            raise MyCustomExceptions.InvalidGameCell

        return str_idx - 1, col_idx - 1

    def make_computer_turn(self) -> None:
        """Метод, реализующий ход компьютера"""

        while 1:
            str_idx = random.choice([0, 1, 2])
            col_idx = random.choice([0, 1, 2])
            if self.game_pole[str_idx][col_idx] == '-':
                self.game_pole[str_idx][col_idx] = self.computer_symbol
                self.count_rounds_start += 1
                break

    def make_human_turn(self) -> None:
        """Метод, реализующий ход человека"""

        str_idx, col_idx = self.validate_input(input())

        self.game_pole[str_idx][col_idx] = self.human_symbol
        self.count_rounds_start += 1

    def start_game(self) -> None:
        """Метод, реализующий основную логику игры"""

        print("Первый ход предоставляется человеку; пожалуйста, введите через пробел два числа (номер строки/номер столбца) в "
              "диапазоне 1 - 3")
        self.show_board()
        while not self.check_winner():
            print('==============')
            print("Ход человека")
            print('==============')
            print("Ожидание ввода двух чисел...")
            try:
                self.make_human_turn()
            except MyCustomExceptions.InvalidCountInputArgs:
                print("Неверное кол-во ожидаемых параметров! Попробуйте снова!")
                continue
            except MyCustomExceptions.InvalidTypesInputArgs:
                print("Неверные типы входных параметров - должны быть целые числа! Попробуйте снова!")
                continue
            except MyCustomExceptions.InvalidRangeInputArgs:
                print("Неверные значения входных параметров! Числа должны быть числа в границах 1 - 3! Попробуйте "
                      "вновь!")
                continue
            except MyCustomExceptions.InvalidGameCell:
                print("Выбранная игровая клетка уже занята! Попробуйте выбрать не занятую клетку!")
                continue

            self.show_board()
            if self.check_winner():
                break
            print('==============')
            print("Ход компьютера")
            print('==============')
            self.make_computer_turn()
            self.show_board()

        print("Игра окончена")
        result = self.check_winner()

        if result == self.human_symbol:
            print("Победил человек")
        elif result == self.computer_symbol:
            print("Победил компьютер")
        else:
            print("Ничья!")

    def check_winner(self):
        """Метод, реализующий проверку наличия выигрышной ситуации после очередного хода каждого из игроков"""

        for i in range(3):
            if all(elem == self.human_symbol for elem in self.game_pole[i][:]):
                return self.human_symbol
            if all(elem == self.computer_symbol for elem in self.game_pole[i][:]):
                return self.computer_symbol
            column_line = [self.game_pole[j][i] for j in range(3)]
            if all(elem == self.human_symbol for elem in column_line):
                return self.human_symbol
            if all(elem == self.computer_symbol for elem in column_line):
                return self.computer_symbol
        if all(self.game_pole[i][i] == self.human_symbol for i in range(len(self.game_pole[:]))):
            return self.human_symbol
        if all(self.game_pole[i][i] == self.computer_symbol for i in range(len(self.game_pole[:]))):
            return self.computer_symbol

        side_diagonal = ((0, 2), (1, 1), (2, 0))
        if all(self.game_pole[i][j] == self.human_symbol for i, j in side_diagonal):
            return self.human_symbol
        if all(self.game_pole[i][j] == self.computer_symbol for i, j in side_diagonal):
            return self.computer_symbol

        if self.count_rounds_start == self.count_rounds_end:
            return 'Drawn game'

        return 0


if __name__ == '__main__':
    game = TicTacGame()
    game.start_game()
