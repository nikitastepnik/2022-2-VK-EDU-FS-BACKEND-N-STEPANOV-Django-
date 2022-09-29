import random
import unittest

from src.exceptions.custom_exceptions import InvalidCountInputArgs, InvalidTypesInputArgs, \
    InvalidRangeInputArgs, InvalidGameCell
from src.main_game.tic_tag_game import TicTacGame


class TestTicTagGame(unittest.TestCase):
    """Класс с юнит-тестами"""

    def setUp(self) -> None:
        self.test_game_obj = TicTacGame(skip_fl=True)

    def test_validate_input_invalid_count_input_args(self):
        params = ['1 2 3 4', 'a b c d e', 'а б в г д']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(InvalidCountInputArgs, lambda: self.test_game_obj.validate_input(elem))

    def test_validate_input_invalid_types_input_args(self):
        params = ['1fsf 1', 'ab b', '. /', 'а б']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(InvalidTypesInputArgs, lambda: self.test_game_obj.validate_input(elem))

    def test_validate_input_range_input_args(self):
        params = ['10 1', '10 10', '1 4', '0 1', '3 4']
        for elem in params:
            with self.subTest(elem=elem):
                self.assertRaises(InvalidRangeInputArgs, lambda: self.test_game_obj.validate_input(elem))

    def test_validate_input_invalid_game_cell(self):
        for i in range(5):
            rand_str_idx = random.randint(1, 3)
            rand_col_idx = random.randint(1, 3)
            self.test_game_obj.game_pole[rand_str_idx - 1][rand_col_idx - 1] = random.choice(
                [self.test_game_obj.first_player_symbol,
                 self.test_game_obj.second_player_symbol])
            elem = ' '.join([str(rand_str_idx), str(rand_col_idx)])

            with self.subTest(elem=elem):
                self.assertRaises(InvalidGameCell, lambda: self.test_game_obj.validate_input(elem))

    def test_check_winner_str_scenario(self):
        str_idx = random.choice(range(self.test_game_obj.dimension))
        for i in range(self.test_game_obj.dimension):
            self.test_game_obj.game_pole[str_idx][i] = self.test_game_obj.first_player_symbol

        self.test_game_obj.count_rounds_start += 1
        res = self.test_game_obj.check_winner()

        self.assertEqual(res, True)

    def test_check_winner_col_scenario(self):
        col_idx = random.choice(range(self.test_game_obj.dimension))
        for i in range(self.test_game_obj.dimension):
            self.test_game_obj.game_pole[i][col_idx] = self.test_game_obj.first_player_symbol

        self.test_game_obj.count_rounds_start += 1
        res = self.test_game_obj.check_winner()

        self.assertEqual(res, True)

    def test_check_winner_main_diag_scenario(self):
        for i in range(self.test_game_obj.dimension):
            self.test_game_obj.game_pole[i][i] = self.test_game_obj.second_player_symbol

        res = self.test_game_obj.check_winner()

        self.assertEqual(res, True)

    def test_check_winner_side_diag_scenario(self):
        for i, j in self.test_game_obj.side_diag:
            self.test_game_obj.game_pole[i][j] = self.test_game_obj.second_player_symbol

        res = self.test_game_obj.check_winner()

        self.assertEqual(res, True)

    def test_check_winner_drawn_game_scenario(self):
        self.test_game_obj.game_pole = [['-' for i in range(self.test_game_obj.dimension)]
                                        for j in range(self.test_game_obj.dimension)]
        self.test_game_obj.count_rounds_start = self.test_game_obj.dimension ** 2
        res = self.test_game_obj.check_winner()
        self.assertEqual(res, 'Drawn game')

        self.test_game_obj.count_rounds_start = 0

    def test_check_winner_not_win_situation(self):
        game_symbols = [self.test_game_obj.first_player_symbol, self.test_game_obj.second_player_symbol]
        k = 0
        for i in range(self.test_game_obj.dimension):
            for j in range(self.test_game_obj.dimension):
                self.test_game_obj.game_pole[i][j] = game_symbols[k % 2]
                k += 1
        self.test_game_obj.game_pole[1][1] = '-'
        res = self.test_game_obj.check_winner()

        self.assertEqual(res, False)

    def tearDown(self) -> None:
        self.test_game_obj.count_rounds_start = 0
        self.test_game_obj.game_pole = [['-' for i in range(self.test_game_obj.dimension)]
                                        for j in range(self.test_game_obj.dimension)]
