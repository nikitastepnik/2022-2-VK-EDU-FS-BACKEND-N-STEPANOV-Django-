def is_number(string):
    """Метод проверки строки на возможность конвертации в числовой тип. Расширенный аналог is_digit()"""
    try:
        float(string)
        return True
    except ValueError:
        return False
