"""Модуль, содержащий кастомные ошибки"""


class MyCustomExceptions:
    """Класс, аккумулирующий производные классы ошибок"""

    class InvalidCountInputArgs(Exception):
        """Класс ошибки неверного количества входных параметров"""

    class InvalidTypesInputArgs(Exception):
        """Класс ошибки невалидных типов входных параметров"""

    class InvalidRangeInputArgs(Exception):
        """Класс ошибки невалидного диапазона входных аргументов"""

    class InvalidGameCell(Exception):
        """Класс ошибки невалидной (уже занятой) клетки игрового поля"""
