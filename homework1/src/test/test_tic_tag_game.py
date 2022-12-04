"""Модуль с юнит-тестами"""

import random
import unittest

from homework1.src.exceptions import InvalidCountInputArgs, InvalidTypesInputArgs, \
    InvalidRangeInputArgs, InvalidGameCell, InvalidDimensionRange, InvalidGameType
from homework1.src.main_game.tic_tag_game import TicTacGame


class TestTicTagGame(unittest.TestCase):
    """Класс с юнит-тестами"""

    def setUp(self) -> None:
        """Подготовка тестов (setup)"""
        self.test_game_obj = TicTacGame(test_fl=True)

    def test_validate_input_invalid_count_input_args(self):
        """Тест валидации количества входных аргументов"""
        params = ['1 2 3 4', 'a b c d e', 'а б в г д']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(InvalidCountInputArgs,
                                  lambda: self.test_game_obj.validate_input(elem))

    def test_validate_input_invalid_types_input_args(self):
        """Тест валидации типа входных аргументов"""
        params = ['1fsf 1', 'ab b', '. /', 'а б']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(InvalidTypesInputArgs,
                                  lambda: self.test_game_obj.validate_input(elem))

    def test_validate_input_range_input_args(self):
        """Тест валидации диапазона значений входных элементов"""
        params = ['10 1', '10 10', '1 4', '0 1', '3 4']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(InvalidRangeInputArgs,
                                  lambda: self.test_game_obj.validate_input(elem))

    def test_validate_input_invalid_game_cell(self):
        """Тест валидации невалидной игровой ячейки (ранее занятой)"""
        for _ in range(5):
            rand_str_idx = random.randint(1, 3)
            rand_col_idx = random.randint(1, 3)
            self.test_game_obj.game_pole[rand_str_idx - 1][rand_col_idx - 1] = random.choice(
                [self.test_game_obj.first_player_symbol,
                 self.test_game_obj.second_player_symbol])
            elem = ' '.join([str(rand_str_idx), str(rand_col_idx)])

            with self.subTest(elem=elem):
                self.assertRaises(InvalidGameCell,
                                  lambda: self.test_game_obj.validate_input(elem))

    def test_validate_invalid_count_input_args_dimension(self):
        """Тест валидации невалидного числа входных аргументов"""
        params = ['10 1', '10 10', '1 4', '0 1', '3 4']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(InvalidCountInputArgs,
                                  lambda: self.test_game_obj.validate_input(elem, validate_type='dimension'))

    def test_validate_input_not_digit_input_args_dimension(self):
        """Тест валидации нечисловых типов входных аргументов"""
        params = ['10в', '.', 'ak']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(InvalidTypesInputArgs,
                                  lambda: self.test_game_obj.validate_input(elem, validate_type='dimension'))

    def test_validate_invalid_range_input_args_dimension(self):
        """Тест валидации невалидных значений размерности игрового поля"""
        params = ['100', '2', '31']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(InvalidDimensionRange,
                                  lambda: self.test_game_obj.validate_input(elem, validate_type='dimension'))

    def test_validate_invalid_game_type_input_args(self):
        """Тест невалидного типа игры"""
        params = ['h', 'хуман', 'CoМputer']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(InvalidGameType,
                                  lambda: self.test_game_obj.validate_input(elem, validate_type='game_type'))

    def test_check_winner_str_scenario(self):
        """Тест выигрышного сценария - строка"""
        str_idx = random.choice(range(self.test_game_obj.dimension))
        for i in range(self.test_game_obj.dimension):
            self.test_game_obj.game_pole[str_idx][i] = self.test_game_obj.first_player_symbol

        self.test_game_obj.count_rounds_start += 1
        res = self.test_game_obj.check_winner()

        self.assertEqual(res, True)

    def test_check_winner_col_scenario(self):
        """Тест выигрышного сценария - колонка"""
        col_idx = random.choice(range(self.test_game_obj.dimension))
        for i in range(self.test_game_obj.dimension):
            self.test_game_obj.game_pole[i][col_idx] = self.test_game_obj.first_player_symbol

        self.test_game_obj.count_rounds_start += 1
        res = self.test_game_obj.check_winner()

        self.assertEqual(res, True)

    def test_check_winner_main_diag_scenario(self):
        """Тест выигрышного сценария - основная диагональ"""
        for i in range(self.test_game_obj.dimension):
            self.test_game_obj.game_pole[i][i] = self.test_game_obj.second_player_symbol

        res = self.test_game_obj.check_winner()

        self.assertEqual(res, True)

    def test_check_winner_side_diag_scenario(self):
        """Тест выигрышного сценария - побочная диагональ"""
        for i, j in self.test_game_obj.side_diag:
            self.test_game_obj.game_pole[i][j] = self.test_game_obj.second_player_symbol

        res = self.test_game_obj.check_winner()

        self.assertEqual(res, True)

    def test_check_winner_drawn_game_scenario(self):
        """Тест выигрышного сценария - ничья"""
        self.test_game_obj.game_pole = [['-' for _ in range(self.test_game_obj.dimension)]
                                        for _ in range(self.test_game_obj.dimension)]
        self.test_game_obj.count_rounds_start = self.test_game_obj.dimension ** 2
        res = self.test_game_obj.check_winner()
        self.assertEqual(res, 'Drawn game')

        self.test_game_obj.count_rounds_start = 0

    def test_check_winner_not_win_situation(self):
        """Тест НЕвыигрышного сценария - победитель не определен"""
        game_symbols = [self.test_game_obj.first_player_symbol,
                        self.test_game_obj.second_player_symbol]
        k = 0
        for i in range(self.test_game_obj.dimension):
            for j in range(self.test_game_obj.dimension):
                self.test_game_obj.game_pole[i][j] = game_symbols[k % 2]
                k += 1
        self.test_game_obj.game_pole[1][1] = '-'
        res = self.test_game_obj.check_winner()

        self.assertEqual(res, False)

    def tearDown(self) -> None:
        """Очистка тестового стенда - Teardown"""
        self.test_game_obj.count_rounds_start = 0
        self.test_game_obj.game_pole = [['-' for _ in range(self.test_game_obj.dimension)]
                                        for _ in range(self.test_game_obj.dimension)]
