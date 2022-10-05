"""
Реализация классического варианта игры (поле 3x3) крестики-нолики в ООП-стиле.
Используемый линтер - Pylint.
Зависимости собраны в requirements.txt.
Установить зависимости: pip install -r requirements.txt
"""

import random

from homework1.src.exceptions import InvalidCountInputArgs, \
    InvalidTypesInputArgs, InvalidRangeInputArgs, \
    InvalidGameCell, InvalidDimensionRange, InvalidGameType


class TicTacGame:
    """Класс, реализующий логику игры крестики-нолики в ООП стиле"""
    first_player_symbol = 'X'
    second_player_symbol = 'O'

    def __init__(self, test_fl=False):
        if test_fl:
            self.dimension = 3
            self.game_type = 'computer'
        else:
            self.dimension = self.define_dimension()
            self.game_type = self.define_game_type()
        self.count_rounds_start = 0
        self.count_rounds_end = self.dimension ** 2
        self.side_diag = self.define_side_diag()
        self.game_pole = [['-' for i in range(self.dimension)] for j in range(self.dimension)]

    def define_dimension(self) -> int:
        """Метод, определяющий и валидирующий введенную пользователем размерность поля"""

        print("Введите желаемую размерность поля - одно число в диапазоне 3-30")
        while 1:
            try:
                dimension = self.validate_input(input(), validate_type='dimension')
                return dimension
            except (InvalidCountInputArgs, InvalidTypesInputArgs, InvalidDimensionRange) as error:
                print(error)
                continue

    def define_game_type(self) -> str:
        """Метод, определяющий и валидирующий введенный пользователем тип игры"""

        print("""Выберите какой тип игры вы желаете - человек-человек/человек-компьютер\n
              Введите human - если хотите играть в формате человек-человек\n
              Введите computer - если хотите играть в формате человек-компьютер""")
        while 1:
            try:
                game_type = self.validate_input(input(), validate_type='game_type')
                return game_type
            except InvalidGameType as error:
                print(error)
                continue

    def validate_input(self, params_as_string: str, validate_type='cell'):
        """Метод, реализующий валидацию пользовательского ввода"""

        if validate_type == 'dimension':
            params_as_string = params_as_string.strip()
            if len(params_as_string.split()) != 1:
                raise InvalidCountInputArgs
            if not params_as_string.isdigit():
                raise InvalidTypesInputArgs
            dimension = int(params_as_string)
            if not 3 <= dimension <= 30:
                raise InvalidDimensionRange

            return dimension

        if validate_type == 'game_type':
            params_as_string = params_as_string.strip().lower()
            if params_as_string not in ['human', 'computer']:
                raise InvalidGameType
            game_type = params_as_string

            return game_type

        params_as_string = params_as_string.strip()
        if len(params_as_string.split()) != 2:
            raise InvalidCountInputArgs

        str_idx, col_idx = params_as_string.split()

        if not (str_idx.isdigit() and col_idx.isdigit()):
            raise InvalidTypesInputArgs

        str_idx, col_idx = int(str_idx), int(col_idx)

        if not (1 <= str_idx <= self.dimension and 1 <= col_idx <= self.dimension):
            raise InvalidRangeInputArgs(self.dimension)
        if self.game_pole[str_idx - 1][col_idx - 1] != '-':
            raise InvalidGameCell

        return str_idx - 1, col_idx - 1

    def show_board(self) -> None:
        """Метод, отображающий игровое поле. Подразумевается вызов на каждой игровой итерации"""

        print("Игровое поле на текущий ход:")
        print(' ', *range(1, self.dimension + 1))
        for i in range(1, self.dimension + 1):
            print(i, end=' ')
            print(*self.game_pole[i - 1])

    def show_information(self, *, fl='first_pl_turn') -> None:
        """Метод, отображающий информацию, необходимую на текущей игровой итерации"""

        if fl == "start_msg":
            print(
                "Первый ход предоставляется человеку; пожалуйста, введите через пробел "
                f"два числа (номер строки/номер столбца) в диапазоне 1 - {self.dimension}")
        elif fl == 'first_pl_turn':
            print("==============")
            print("Ход первого игрока")
            print("==============")
            print("Ожидание ввода двух чисел...""")
        elif fl == 'sec_pl_turn':
            print("==============")
            print("Ход второго игрока")
            print("==============")
        elif fl == 'game_end':
            print("Игра закончена")
            if self.count_rounds_start == self.count_rounds_end:
                print("Ничья!")
                return

            cur_sumb = [self.first_player_symbol, self.second_player_symbol] \
                [(self.count_rounds_start - 1) % 2]
            if cur_sumb == self.first_player_symbol:
                print("Победил первый игрок")
            else:
                print("Победил второй игрок")

    def define_side_diag(self):
        """Метод, определяющий координаты побочной диагонали матрицы"""

        lst_coord = []
        for i in range(self.dimension - 1, -1, -1):
            lst_coord.append((self.dimension - 1 - i, i))

        return lst_coord

    def second_player_turn(self):
        """Метод, определяющий конкретный сценарий игры (человек/компьютер) второго игрока"""

        if self.game_type == 'human':
            self.make_human_turn(self.second_player_symbol)
        else:
            self.make_computer_turn()

    def make_computer_turn(self) -> None:
        """Метод, реализующий ход компьютера"""

        while 1:
            str_idx = random.choice([*range(self.dimension)])
            print(str_idx)
            col_idx = random.choice([*range(self.dimension)])
            if self.game_pole[str_idx][col_idx] == '-':
                self.game_pole[str_idx][col_idx] = self.second_player_symbol
                break
        self.count_rounds_start += 1

    def make_human_turn(self, game_sumb) -> None:
        """Метод, реализующий ход человека"""

        str_idx, col_idx = self.validate_input(input())

        self.game_pole[str_idx][col_idx] = game_sumb
        self.count_rounds_start += 1

    def start_game(self) -> None:
        """Метод, реализующий основную логику игры"""

        self.show_information(fl='start_msg')
        self.show_board()
        while not self.check_winner():
            self.show_information()
            try:
                self.make_human_turn(self.first_player_symbol)
            except (InvalidCountInputArgs, InvalidTypesInputArgs, InvalidRangeInputArgs,
                    InvalidGameCell, InvalidDimensionRange) as error:
                print(error)
                continue

            self.show_board()
            if self.check_winner():
                break
            self.show_information(fl='sec_pl_turn')
            self.second_player_turn()
            self.show_board()

        self.show_information(fl='game_end')

    def check_winner(self):
        """Метод, реализующий проверку наличия выигрышной ситуации
           после очередного хода каждого из игроков"""

        cur_sumb = [self.first_player_symbol, self.second_player_symbol] \
            [(self.count_rounds_start - 1) % 2]
        for i in range(self.dimension):
            if all(elem == cur_sumb for elem in self.game_pole[i][:]):
                return True
            column_line = [self.game_pole[j][i] for j in range(self.dimension)]
            if all(elem == cur_sumb for elem in column_line):
                return True
        if all(cur_sumb == self.game_pole[i][i] for i in range(len(self.game_pole[:]))):
            return True

        if all(cur_sumb == self.game_pole[i][j] for i, j in self.side_diag):
            return True

        if self.count_rounds_start == self.count_rounds_end:
            return 'Drawn game'

        return False


if __name__ == '__main__':
    game = TicTacGame()
    game.start_game()
