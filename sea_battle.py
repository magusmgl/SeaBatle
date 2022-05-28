# Внутренняя логика игры — корабли, игровая доска и вся логика связанная с ней
from SeaBatle.my_Exception import *


class CheckCoordDort:
    # data descriptor для класса Dot
    @classmethod
    def validate_coord(cls, value):
        if not isinstance(value, int):
            raise DortCordsException(value)

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        self.validate_coord(value)
        setattr(instance, self.name, value)


class Dot:
    """Класс точек на поле"""
    x = CheckCoordDort()
    y = CheckCoordDort()

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:
    """Корабль на игровом поле"""
    MAX_NUM_SHIP_CELLS = 3
    MIN_NUM_SHIP_CELLS = 1
    MAX_NUM_SHIP_LIVES = 3

    def __init__(self, length: int, start_dot: object, direction: int, number_of_lives: int):
        self.validate_length_ship(length)
        self.validate_num_lives(number_of_lives)
        self.validate_direction_ship(direction)

        self.length = length
        self.start_dot = start_dot
        self.direction = direction
        self.number_of_lives = number_of_lives

    @classmethod
    def validate_length_ship(cls, value: int) -> None:
        """Проверяет значение длины корaбля (число от min до max)"""
        if not isinstance(value, int) or not cls.MIN_NUM_SHIP_CELLS <= value <= cls.MAX_NUM_SHIP_CELLS:
            raise ShipLengthException(value)

    @classmethod
    def validate_num_lives(cls, value: int) -> None:
        """Проверяет значение жизней коробля (число от 0 до max)"""
        if not isinstance(value, int) or not 0 <= value <= cls.MAX_NUM_SHIP_LIVES:
            raise ShipLivesException(value)

    @classmethod
    def validate_direction_ship(cls, value: str) -> None:
        """Проверяет значение направление корабля ('1' и '0')"""
        if value != 1 and value != 0:
            raise ShipDirectionException(value)

    @property
    def dots(self) -> list:
        """Возвращает список всех точек коробля"""
        list_of_dots = []
        for i in range(self.length):
            if self.direction:
                list_of_dots.append(Dot(self.start_dot.x + i, self.start_dot.y))
            else:
                list_of_dots.append(Dot(self.start_dot.x, self.start_dot.y + i))
        return list_of_dots

    @property
    def name(self):
        if self.length == 3:
            self.name = "Линкор"
        if self.length == 2:
            self.name = "Крейсер"
        if self.length == 1:
            self.name = "Подводная лодка"


class Board(Dot):
    """Игровая доска"""
    _hid = None
    BOARD_SIZE = 6

    def __init__(self, list_of_ships: list, number_of_live_ships: int, hid=False):
        self.board = [[" O "] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.list_of_ships = list_of_ships
        self.number_of_live_ships = number_of_live_ships
        self.hid = hid

    @property
    def hid(self):
        return self._hid

    @hid.setter
    def hid(self, value):
        if isinstance(value, bool):
            self._hid = value

    def add_ship(self, ship: object) -> None:
        """Ставит корабль на доску (если ставить не получается, выбрасывает исключения)"""
        for dot in ship.dots:
            if not self.out(dot):
                raise BoardOutException(dot.x, dot.y)
            if self.board[dot.x][dot.y] != " O ":
                raise BoardOccupiedCage(dot.x, dot.y)
            self.board[dot.x][dot.y] = " ■ "
            self.contour(ship)

    def contour(self, ship: object) -> None:
        """Обводит корабль по контуру"""
        x_0 = ship.start_dot.x - 1
        y_0 = ship.start_dot.y - 1

        if ship.length == 1:
            k, m = 3, 3
        else:
            k, m = (ship.length + 2, 3) if ship.direction == 1 else (3, ship.length + 2)

        for i in range(k):
            for j in range(m):
                curr_dot = Dot(i + x_0, j + y_0)
                if self.out(curr_dot) and curr_dot not in ship.dots:
                    self.board[x_0 + i][y_0 + j] = " - "

    def display_board(self) -> None:
        """ Выводит доску в консоль в зависимости от параметра hid"""
        print(" | 0 | 1 | 2 | 3 | 4 | 5 |")
        print("-" * 25)
        if self.hid:
            for i, row in enumerate(self.board):
                print(f"{i}| {'|'.join([' O '] * 6)}|")
                print("-" * 25)
        else:
            for i, row in enumerate(self.board):
                print(f"{i}|{'|'.join(row)}|")
                print("-" * 25)

    def out(self, dot: object) -> bool:
        """Для точки (объекта класса Dot) возвращает True,
        если точка выходит за пределы поля, и False, если не выходит."""
        return all([0 <= dot.x < len(self.board), \
                    0 <= dot.y < len(self.board[0])])

    def shot(self, dot: object) -> str:
        """ Делает выстрел по доске (если есть попытка выстрелить за пределы
         и в использованную точку, нужно выбрасывать исключения).
        """
        if not self.out(dot):
            raise BoardOutException(dot.x, dot.y)
        if self.board[dot.x][dot.y] == " T " or self.board[dot.x][dot.y] == " X ":
            raise BoardShotUsedCage(dot.x, dot.y)
        if self.board[dot.x][dot.y] == " - " or self.board[dot.x][dot.y] == " O ":
            self.board[dot.x][dot.y] = " T "
            res = "miss"
        if self.board[dot.x][dot.y] == " ■ ":
            self.board[dot.x][dot.y] = " X "
            res = "hit"
        return res
