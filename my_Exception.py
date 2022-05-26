class BoardException(Exception):
    def __init__(self, *args):
        self.message = args


class BoardOutException(BoardException):
    """Класс исключения, который  используется чтобы отлавливать ошибки, когда игрок пытается выстрелить в клетку за пределами игрового поля.
    """

    def __str__(self):
        return f"Точка с координатами ({self.message[0]},{self.message[1]}) находится за пределами  игрового поля."


class BoardOccupiedCage(BoardException):
    def __str__(self):
        return f"Точка с координатами ({self.message[0]},{self.message[1]}) занята."

class BoardShotUsedCage(BoardException):
    def __str__(self):
        return f"В точка с координатами ({self.message[0]},{self.message[1]}) уже был сделан выстрел."

class DortCordsException(Exception):
    """ """

    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        return f"Ошибка: '{self.message}' координата должна быть число от 0 до 5."


class ShipParamException(Exception):
    def __init__(self, *args):
        self.message = args[0] if args else None


class ShipLengthException(ShipParamException):
    """ """

    def __str__(self):
        return f"Ошибка: длина коробля не может принимать значение '{self.message}'."


class ShipLivesException(ShipParamException):
    """ """

    def __str__(self):
        return f"Ошибка: Число жизней '{self.message}' должно принимать значение от 0 до 3."


class ShipDirectionException(ShipParamException):
    """ """

    def __str__(self):
        return f"Ошибка: Введенное положение корабля '{self.message}' должно принимать значение 'v'/'h'."
