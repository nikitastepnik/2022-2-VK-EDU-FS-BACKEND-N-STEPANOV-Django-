import random
import unittest

from src.exceptions.custom_exceptions import MyCustomExceptions
from src.main_game.tic_tag_game import TicTacGame


class TestTicTagGame(unittest.TestCase):
    """Класс с юнит-тестами"""

    def setUp(self) -> None:
        self.test_game_obj = TicTacGame()

    def tearDown(self) -> None:
        self.test_game_obj.count_rounds_start = 0
        self.test_game_obj.game_pole = [['-' for i in range(3)] for j in range(3)]

    def test_validate_input_invalid_count_input_args(self):
        params = ['1 2 3 4', 'a b c d e', 'а б в г д']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(MyCustomExceptions.InvalidCountInputArgs, lambda: self.test_game_obj.validate_input(elem))

    def test_validate_input_invalid_types_input_args(self):
        params = ['1fsf 1', 'ab b', '. /', 'а б']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(MyCustomExceptions.InvalidTypesInputArgs, lambda: self.test_game_obj.validate_input(elem))

    def test_validate_input_range_input_args(self):
        params = ['10 1', '-1 0', '10 10', '1 4', '0 1', '3 4']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(MyCustomExceptions.InvalidRangeInputArgs, lambda: self.test_game_obj.validate_input(elem))

    def test_validate_input_invalid_game_cell(self):
        for i in range(5):
            rand_str_idx = random.randint(1, 3)
            rand_col_idx = random.randint(1, 3)
            self.test_game_obj.game_pole[rand_str_idx - 1][rand_col_idx - 1] = random.choice([self.test_game_obj.human_symbol,
                                                                                              self.test_game_obj.computer_symbol])
            elem = ' '.join([str(rand_str_idx), str(rand_col_idx)])

            with self.subTest(elem=elem):
                self.assertRaises(MyCustomExceptions.InvalidGameCell, lambda: self.test_game_obj.validate_input(elem))

    def test_check_winner_str_scenario(self):
        game_symbol = random.choice([self.test_game_obj.human_symbol, self.test_game_obj.computer_symbol])
        str_idx = random.choice([0, 1, 2])
        for i in range(3):
            self.test_game_obj.game_pole[str_idx][i] = game_symbol

        res = self.test_game_obj.check_winner()

        self.assertEqual(res, game_symbol)

    def test_check_winner_col_scenario(self):
        game_symbol = random.choice([self.test_game_obj.human_symbol, self.test_game_obj.computer_symbol])
        col_idx = random.choice([0, 1, 2])
        for i in range(3):
            self.test_game_obj.game_pole[i][col_idx] = game_symbol

        res = self.test_game_obj.check_winner()

        self.assertEqual(res, game_symbol)

    def test_check_winner_main_diag_scenario(self):
        game_symbol = random.choice([self.test_game_obj.human_symbol, self.test_game_obj.computer_symbol])
        for i in range(3):
            self.test_game_obj.game_pole[i][i] = game_symbol

        res = self.test_game_obj.check_winner()

        self.assertEqual(res, game_symbol)

    def test_check_winner_side_diag_scenario(self):
        game_symbol = random.choice([self.test_game_obj.human_symbol, self.test_game_obj.computer_symbol])
        side_diagonal = ((0, 2), (1, 1), (2, 0))
        for i, j in side_diagonal:
            self.test_game_obj.game_pole[i][j] = game_symbol

        res = self.test_game_obj.check_winner()

        self.assertEqual(res, game_symbol)

    def test_check_winner_drawn_game_scenario(self):
        self.test_game_obj.game_pole = [['-' for i in range(3)] for j in range(3)]
        self.test_game_obj.count_rounds_start = 9
        res = self.test_game_obj.check_winner()
        self.assertEqual(res, 'Drawn game')

        self.test_game_obj.count_rounds_start = 0

    def test_check_winner_not_win_situation(self):
        game_symbols = [self.test_game_obj.human_symbol, self.test_game_obj.computer_symbol]
        k = 0
        for i in range(3):
            for j in range(3):
                self.test_game_obj.game_pole[i][j] = game_symbols[k % 2]
                k += 1
        self.test_game_obj.game_pole[1][1] = '-'
        res = self.test_game_obj.check_winner()
        self.assertEqual(res, 0)
