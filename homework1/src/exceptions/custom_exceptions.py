"""Модуль, содержащий кастомные ошибки"""


class InvalidCountInputArgs(Exception):
    """Класс ошибки неверного количества входных параметров"""

    def __str__(self):
        return "Неверное количество входных параметров! Попробуйте снова!"


class InvalidTypesInputArgs(Exception):
    """Класс ошибки невалидных типов входных параметров"""

    def __str__(self):
        return "Неверный тип входных параметров - должно быть целые число! Попробуйте снова!"


class InvalidRangeInputArgs(Exception):
    """Класс ошибки невалидного диапазона входных аргументов"""

    def __str__(self):
        return "Неверные значения входных параметров! Числа должны быть " \
               f"в границах 1 - {self.args[0]}! Попробуйте вновь!"


class InvalidGameCell(Exception):
    """Класс ошибки невалидной (уже занятой) клетки игрового поля"""

    def __str__(self):
        return "Выбранная игровая клетка уже занята! Попробуйте выбрать не занятую клетку!"


class InvalidDimensionRange(Exception):
    """Класс ошибки невалидного размера игрового поля"""

    def __str__(self):
        return "Диапазон игрового поля должен быть в диапазоне [3;30]! Попробуйте снова!"


class InvalidGameType(Exception):
    """Класс неверного типа игры"""

    def __str__(self):
        return "Тип игры должен задаваться словом 'human' или 'computer'! Попробуйте снова!"
