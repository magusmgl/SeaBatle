class BoardOutException(Exception):
    """
    Класс исключения, который  используется чтобы отлавливать ошибки,
     когда игрок пытается выстрелить в клетку за пределами игрового поля.
    """

    def __init__(self, dot):
        self.dot = dot

    def __str__(self):
        return f"Точка с координатами ({self.dot[0]},{self.dot[1]})\
         находится за пределами  игрового поля."


class ShipParamException(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None


class ShipLengthException(ShipParamException):
    """
    """

    def __str__(self):
        return f"Ошибка: длина коробля не может принимать значение '{self.message}'."


class ShipLivesException(ShipParamException):
    """
    """

    def __str__(self):
        return f"Ошибка: Число жизней '{self.message}' должно принимать значение от 0 до 3."


class ShipDirectionException(ShipParamException):
    """
    """

    def __str__(self):
        return f"Ошибка: Введенное положение корабля '{self.message}' должно принимать значение 'r'/'h'."
